#!/usr/bin/env python

# This poorly written jumble of python serves as an Ansible module
# for managing a custom Pacman repository on the local system, and
# adding packages to it from the Arch User Repository.
#
# It is _potentially dangerous_ to install packages from the AUR.
# Automating it in a fashion such as this is not recommended, as
# installing AUR packages without verifying the contents is akin to
# running a random shell script from the internet on your local machine.
#
# That said, the author is super lazy when provisioning new machines, and
# assigns a certain level of trust to certain internet strangers who manage
# PKGBUILDs on the AUR.
#
# Feature requests, bugs, source code, and comments:
# https://github.com/sudoforge/ansible-aur-repository
#
# ##############################################################################
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

from ansible.module_utils.basic import *
from collections import defaultdict
from glob import glob
from os import chdir, chown, getcwd, mkdir
from os.path import abspath, basename, dirname, exists, expanduser, join
from platform import machine
from pprint import pprint
from pwd import getpwnam
from subprocess import Popen
from tempfile import TemporaryDirectory
import re
import requests
import tarfile


class cd:
    """
    Context manager for changing the current working directory
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class SRCINFO(object):
    """
    Represents a .SRCINFO file
    """

    def __init__(self, module, path):
        self.store = defaultdict(list)
        _allowed_keys = ["arch", "epoch", "pkgdesc", "pkgname", "pkgrel", "pkgver"]
        with open(path, "r") as lines:
            for line in lines:
                # ignore commented and empty lines
                if (
                    line.startswith("#") or line == "\n"
                ):  # ignore comments and empty lines
                    continue
                # remove newlines and tabs
                line = line.replace("\n", "").replace("\t", "")
                array = line.split(" = ")
                key = array[0]
                value = array[1]
                if key in _allowed_keys:
                    if not self.store[key]:
                        self.store[key] = value
                    else:
                        if not type(self.store[key]) is list:
                            self.store[key] = [self.store[key], value]
                        else:
                            self.store[key].append(value)

        self.store["version"] = f'{ self.store["pkgver"] }-{ self.store["pkgrel"] }'
        if self.store["epoch"]:
            self.store["version"] = f'{ self.store["epoch"] }:{ self.store["version"] }'

        rc, arch, stderr = module.run_command("uname -m", check_rc=False)
        arch = arch.replace("\n", "")
        if rc != 0:
            module.fail_json(msg="Unable to determine machine architecture")

        if self.store["arch"] == "any":
            arch = "any"
        elif arch not in self.store["arch"]:
            module.fail_json(
                msg=f"Machine architecture '{arch}' not a valid target in list: {self.store['arch']}"
            )

        self.store["targets"] = []
        if isinstance(self.store["pkgname"], list):
            for name in self.store["pkgname"]:
                self.store["targets"].append(
                    f'{name}-{self.store["version"]}-{arch}.pkg.tar.xz'
                )
        else:
            self.store["targets"].append(
                f'{self.store["pkgname"]}-{self.store["version"]}-{arch}.pkg.tar.xz'
            )


class Package(object):
    """
    Represents an AUR package
    """

    def __init__(
        self, name, pkgver=None, pkgrel=None, epoch=None, skip_pgp_check=False
    ):
        self.name = name
        self.url = f"https://aur.archlinux.org/cgit/aur.git/snapshot/{name}.tar.gz"
        self.skip_pgp_check = skip_pgp_check
        self.__version(pkgver, pkgrel, epoch)

    def __get_filename(header):
        """
        Gets the filename from the Content-Disposition header
        """
        if not header:
            return None
        filename = re.findall("filename=(.+)", header)
        if len(filename) == 0:
            return None
        return filename[0]

    def download(self, module):
        """
        Attempt to download package
        """
        with requests.get(self.url, stream=True) as r:
            header = "content-disposition"
            value = r.headers.get(header)
            if value:
                matches = re.findall("filename=(.+)", value)
                if len(matches) == 1:
                    filename = matches[0]
                else:
                    raise Exception("More than one filename match found")
            else:
                raise Exception(f"Header '{header}' not found or empty")
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
                self.tarfile = os.path.join(os.getcwd(), filename)

        if not os.path.exists(self.tarfile):
            raise Exception(f"Tarfile '{self.tarfile}' not found")
        else:
            with tarfile.open(self.tarfile, "r") as f:
                f.extractall()
                self.root = os.path.join(os.getcwd(), self.name)
                srcinfo = SRCINFO(module, os.path.join(self.root, ".SRCINFO"))
                self.__version(
                    srcinfo.store["pkgver"],
                    srcinfo.store["pkgrel"],
                    srcinfo.store["epoch"],
                )
                self.targets = srcinfo.store["targets"]

    def __version(self, pkgver, pkgrel, epoch=None):
        self.pkgrel = pkgrel
        self.pkgver = pkgver
        self.epoch = epoch
        self.version = f"{pkgver}-{pkgrel}"
        if epoch:
            self.version = f"{epoch}:{self.version}"


class Repository(object):
    def __init__(self, module, path, packages: [Package] = []):
        self.module = module
        self.path = path
        self.root = os.path.dirname(path)
        self.name = os.path.basename(path)[: os.path.basename(path).index(".")]
        self.packages = packages
        self.existing_packages = []

        if os.path.exists(self.path):
            # Get packages from existing repository
            cmd = subprocess.Popen(
                f'pacman -Sl {self.name} | sed -e "s/^{self.name} //"',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )

            for line in cmd.stdout.readlines():
                line = line.decode()
                line = (
                    line.replace("\n", "").replace("\t", "").replace(" [installed]", "")
                )
                array = line.split(" ")
                pkgname = array[0]
                vstring = array[1]

                epoch = None
                match = re.match("^(\d+):", vstring)
                if match:
                    epoch = match.groups()[0]
                    vstring = vstring.replace(f"{epoch}:", "")  # remove epoch

                pkgver = vstring.split("-")[0]
                pkgrel = vstring.split("-")[1]
                self.existing_packages.append(Package(pkgname, pkgver, pkgrel, epoch))
        else:
            self.__create()

    def __create(self):
        """
        Create repository root and initalize database
        """
        os.mkdir(self.root)
        self.packages = []
        try:
            subprocess.Popen(f"repo-add {self.path}", shell=True)
        except:
            raise Exception("Failed to create repository")

    def build(self, module, package: Package, skip_pgp_check=False):
        """
        Attempt to build an AUR package
        """
        makepkg_args = "--force --noconfirm --needed --noprogressbar"
        if module.params["install"] is True:
            makepkg_args += " --install"
        if skip_pgp_check is True:
            makepkg_args += " --skippgpcheck"
        if platform.machine().startswith("arm"):
            makepkg_args += " -Acsr"
        else:
            makepkg_args += " -csr"
        cmd = f'makepkg PKGDEST="{self.root}" {makepkg_args}'
        rc, stdout, stderr = module.run_command(cmd, check_rc=False)
        if rc != 0:
            module.fail_json(msg=f"failed to build package: {stderr}")

    def add(self, module, package: Package):
        for target in package.targets:
            pkgfile = os.path.join(self.root, target)
            rc, stdout, stderr = module.run_command(
                f"repo-add {self.path} {pkgfile}", check_rc=False,
            )
            if rc != 0:
                module.fail_json(msg=f"failed to add package to repository: {stderr}")

    def has_package(self, package: Package):
        return any(
            rp.name == package.name and rp.version == package.version
            for rp in self.existing_packages
        )


def pacman_in_path(module):
    """
    Determine if pacman is available
    """
    rc, stdout, stderr = module.run_command("which pacman", check_rc=False)
    return rc == 0


def check_packages(module, repo: Repository, packages: [Package]):
    """
    Inform the user what would change if the module were run
    """
    would_be_changed = []

    for package in packages:
        if repo.has_package(package):
            would_be_changed = package

    if would_be_changed:
        module.exit_json(
            changed=True, msg=f"{len(would_be_changed)} package(s) would be installed"
        )
    else:
        module.exit_json(changed=False, msg="all packages are already installed")


def build_packages(module, repo: Repository, packages: [Package]):
    """
    Install the specified packages to the specified repository
    """
    num_success = 0

    for package in packages:
        # Attempt to download the package
        package.download(module)
        # If the package is already installed, skip the install
        if repo.has_package(package) and module.params["upgrade"] is False:
            continue
        # Change into the package directory
        with cd(package.root):
            # Attempt to build the package
            repo.build(module, package)
            # Attempt to add the package to the repository database
            repo.add(module, package)
            # Increment success count
            num_success += 1

    # Exit with the number of packages succesfully installed
    if num_success > 0:
        module.exit_json(
            changed=True, msg=f"added {num_success} package(s) to the repository"
        )
    else:
        module.exit_json(changed=False, msg="all packages were already installed")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            dbpath=dict(required=True),
            upgrade=dict(default=False, type="bool"),
            install=dict(default=False, type="bool"),
            skip_pgp=dict(default=False, type="bool"),
        ),
        supports_check_mode=True,
    )

    # Fail if pacman is not available
    if not pacman_in_path(module):
        module.fail_json(msg="could not locate pacman executable")

    # Create package objects
    packages = []
    for pkgname in module.params["name"].split(","):
        packages.append(Package(pkgname))

    # Create repository
    repo = Repository(module, module.params["dbpath"], packages)

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)

        if module.check_mode:
            check_packages(module, repo)

        build_packages(module, repo, packages)


main()
