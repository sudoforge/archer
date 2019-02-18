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
#
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


class User(object):
    """
    A user on the machine
    """
    def __init__(self, name):
        try:
            uid = pwd.getpwnam(name).pw_uid
            self.name = name
            self.id = uid
        except KeyError:
            raise Exception("User '%s' not found" % name)


class SRCINFO(object):
    """
    Represents a .SRCINFO file
    """
    def __init__(self, module, path):
        self.store = defaultdict(list)
        _allowed_keys = [
            'arch',
            'epoch',
            'pkgdesc',
            'pkgname',
            'pkgrel',
            'pkgver',
        ]
        with open(path, 'r') as lines:
            for line in lines:
                # ignore commented and empty lines
                if line.startswith('#') or line == "\n": # ignore comments and empty lines
                    continue
                # remove newlines and tabs
                line = line.replace('\n', '').replace('\t', '')
                array = line.split(' = ')
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

        self.store['version'] = '%s-%s' % (self.store['pkgver'], self.store['pkgrel'])
        if self.store['epoch']:
            self.store['version'] = '%s:%s' % (self.store['epoch'], self.store['version'])

        rc, arch, stderr = module.run_command('uname -m', check_rc=False)
        arch = arch.replace('\n', '')
        if rc != 0:
            module.fail_json(msg='Unable to determine machine architecture')

        if self.store['arch'] == 'any':
            arch = 'any'
        elif arch not in self.store['arch']: 
            errmsg = "Machine architecture '%s' not a valid target in list: %s"
            module.fail_json(msg=errmsg % (arch, self.store['arch']))

        self.store['targets'] = []
        if type(self.store['pkgname']) is 'list':
            for name in self.store['pkgname']:
                self.store['targets'].append('%s-%s-%s.pkg.tar.xz' % (name, self.store['version'], arch))
        else:
            self.store['targets'].append('%s-%s-%s.pkg.tar.xz' % (self.store['pkgname'], self.store['version'], arch))


class Package(object):
    """
    Represents an AUR package
    """
    def __init__(self, name, pkgver = None, pkgrel = None, epoch = None, skip_pgp_check = False):
        self.name = name
        self.url = 'https://aur.archlinux.org/cgit/aur.git/snapshot/%s.tar.gz' % name
        self.skip_pgp_check = skip_pgp_check
        self.__version(pkgver, pkgrel, epoch)

    def __get_filename(header):
        """
        Gets the filename from the Content-Disposition header
        """
        if not header:
            return None
        filename = re.findall('filename=(.+)', header)
        if len(filename) == 0:
            return None
        return filename[0]

    def download(self, module, user: User):
        """
        Attempt to download package
        """
        with requests.get(self.url, stream=True) as r:
            header = 'content-disposition'
            value = r.headers.get(header)
            if value:
                matches = re.findall('filename=(.+)', value)
                if len(matches) == 1:
                    filename = matches[0]
                else:
                    raise Exception("More than one filename match found")
            else:
                raise Exception("Header '%s' not found or empty" % header)
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
                self.tarfile = os.path.join(os.getcwd(), filename)

        if not os.path.exists(self.tarfile):
            raise Exception("Tarfile '%s' not found" % self.tarfile)
        else:
            with tarfile.open(self.tarfile, 'r') as f:
                f.extractall()
                self.root = os.path.join(os.getcwd(), self.name)
                os.chown(self.root, user.id, -1)
                srcinfo = SRCINFO(module, os.path.join(self.root, '.SRCINFO'))
                self.__version(srcinfo.store['pkgver'], srcinfo.store['pkgrel'], srcinfo.store['epoch'])
                self.targets = srcinfo.store['targets']


    def __version(self, pkgver, pkgrel, epoch = None):
        self.pkgrel = pkgrel
        self.pkgver = pkgver
        self.epoch = epoch
        self.version = '%s-%s' % (pkgver, pkgrel)
        if epoch:
            self.version = '%s:%s' % (epoch, self.version)


class Repository(object):
    def __init__(self, module, path, user: User, packages: [Package] = []):
        self.module = module
        self.path = path
        self.root = os.path.dirname(path)
        self.name = os.path.basename(path)[:os.path.basename(path).index('.')]
        self.user = user
        self.packages = packages
        self.existing_packages = []

        if os.path.exists(self.path):
            # Get packages from existing repository
            cmd = subprocess.Popen(
                'pacman -Sl %s | sed -e "s/^%s //"' % (self.name, self.name),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)

            for line in cmd.stdout.readlines():
                line = line.decode()
                line = line.replace('\n', '').replace('\t', '').replace(' [installed]', '')
                array = line.split(' ')
                pkgname = array[0]
                vstring = array[1]

                epoch = None
                match = re.match('^(\d+):', vstring)
                if match:
                    epoch = match.groups()[0]
                    vstring = vstring.replace('%s:' % epoch, '') # remove epoch

                pkgver =  vstring.split('-')[0]
                pkgrel = vstring.split('-')[1]
                self.existing_packages.append(Package(pkgname, pkgver, pkgrel, epoch))
        else:
            self.__create()

    def __create(self):
        """
        Create repository root and initalize database
        """
        os.mkdir(self.root)
        os.chown(self.root, self.user.id, -1)
        self.packages = []
        try:
            subprocess.Popen('sudo -u %s repo-add %s' % (self.user.name, self.path), shell=True)
        except:
            raise Exception('Failed to create repository')
            
    def sync(self, module):
        """
        Sync repository database
        """
        rc, stdout, stderr = module.run_command('sudo pacsync %s' % self.name, check_rc=False)
        if rc != 0:
            module.fail_json(msg='failed to sync repository: %s' % stderr)

    def build(self, module, package: Package, skip_pgp_check = False):
        """
        Attempt to build an AUR package
        """
        makepkg_args = '--force --noconfirm --needed --noprogressbar'
        if module.params['install'] is True:
            makepkg_args += ' --install'
        if skip_pgp_check is True:
            makepkg_args += ' --skippgpcheck'
        if platform.machine().startswith('arm'):
            makepkg_args += ' -Acsr'
        else:
            makepkg_args += ' -csr'
        cmd = 'sudo -u %s PKGDEST="%s" makepkg %s' % (self.user.name, self.root, makepkg_args)
        rc, stdout, stderr = module.run_command(cmd, check_rc=False)
        if rc != 0:
            module.fail_json(msg='failed to build package: %s' % stderr)

    def add(self, module, package: Package):
        cmd = 'sudo -u %s repo-add %s %s'
        for target in package.targets:
            pkgfile = os.path.join(self.root, target)
            rc, stdout, stderr = module.run_command(cmd % (self.user.name, self.path, pkgfile), check_rc=False)
            if rc != 0:
                module.fail_json(msg='failed to add package to repository: %s' % stderr)

    def has_package(self, package: Package):
        return any(rp.name == package.name and rp.version == package.version for rp in self.existing_packages)



def pacman_in_path(module):
    """
    Determine if pacman is available
    """
    rc, stdout, stderr = module.run_command('which pacman', check_rc=False)
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
        module.exit_json(changed=True, msg='%s package(s) would be installed' % (len(would_be_changed)))
    else:
        module.exit_json(changed=False, msg='all packages are already installed')


def build_packages(module, repo: Repository, packages: [Package]):
    """
    Install the specified packages to the specified repository
    """
    num_success = 0

    for package in packages:
        # Attempt to download the package
        package.download(module, repo.user)
        # If the package is already installed, skip the install
        if repo.has_package(package):
            continue
        # Change into the package directory
        with cd(package.root):
            # Attempt to build the package
            repo.build(module, package)
            # Attempt to add the package to the repository database
            repo.add(module, package)
            # Increment success count
            num_success += 1

    repo.sync(module)

    # Exit with the number of packages succesfully installed
    if num_success > 0:
        module.exit_json(changed=True, msg='added %s package(s) to the repository' % num_success)
    else:
        module.exit_json(changed=False, msg='all packages were already installed')


def main():
    module = AnsibleModule(
        argument_spec = dict(
            user = dict(required=True),
            name = dict(required=True),
            dbpath = dict(required=True),
            install = dict(default=False, type='bool'),
            skip_pgp = dict(default=False, type='bool'),
        ),
        supports_check_mode = True
    )

    # Fail if pacman is not available
    if not pacman_in_path(module):
        module.fail_json(msg="could not locate pacman executable")

    # Create user
    user = User(module.params['user'])

    # Create package objects
    packages = []
    for pkgname in module.params['name'].split(','):
        packages.append(Package(pkgname))

    # Create repository
    repo = Repository(module, module.params['dbpath'], user, packages)

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chown(tmpdir, user.id, -1)
        os.chdir(tmpdir)

        if module.check_mode:
            check_packages(module, repo)

        build_packages(module, repo, packages)


main()
