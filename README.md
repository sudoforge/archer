# Archer [![Build Status][travis-build]][travis-url]

**Archer** provides [Ansible][ansible-web] roles for use in provisioning a
machine running [Arch Linux][al-web]. It can be used directly after the [Chroot
step][awiki-chroot] of the [Installation Guide][awiki-install] or at any other
point in time during the machine's life cycle.

## IMPORTANT: ARCHER IS IN PROGRESS

PLEASE AVOID FORKING OR USING THE PLAYBOOK(S) WITHIN THIS REPOSITORY UNTIL THIS
MESSAGE IS REMOVED.

The `develop` branch is effectively a rewrite of the project from the ground
up. It will likely receive force pushes, rebases, and other tomfoolery. It will
eventually be promoted to `master`. When this happens, the git history will be
overwritten. From the beginning. We'll have a new "initial commit".

You have been warned.

## Usage

Archer aims to automate various steps of administering an Arch Linux
installation: initial machine configuration during the chroot step, and
post-installation configuration both during the initial setup and ongoing
maintenance. Due to its flexibility and easy per-host customisation, you might
consider Archer as a framework of sorts.

By default, Archer simply provides a few sane default settings:

* Boot loading with `systemd-boot`
* Network management with `systemd-networkd` and `wpa_supplicant`
* Some system configuration, e.g. timezone and hosts

To take advantage of the suite of roles contained in this project, see
[**Customizing the build**](#customizing-the-build).

To report a bug or request a new feature, please [search the issues][issues]
and create a new issue if one does not already exist.

### Requirements

* [Arch Linux][al-web] or [Arch Linux ARM][alarm-web]
* [`ansible`][pkg-ansible]

To install the requirements:

```
pacman -S ansible
```

### Customizing the build

Archer subscribes to an *opt-in* philosophy. Many of the roles you see in this
repository **will not run by default**. Instead, you need to enable them by
configuring them for your host machine. This is to allow consumers of this
project to selectively choose the software and tools their machine is
configured with, instead of installing an opinionated collection of tools.

To do this, download `host_vars/localhost.example` from this repository:

```
curl --create-dirs -o /etc/ansible/host_vars/localhost \
    https://raw.githubusercontent.com/sudoforge/archer/develop/localhost.example
```

Open the file with an editor. Look through the file and change the `enabled`
property from `false` to `true` for roles which you want to enable. You can
remove sections that relate to roles you do not want to install. Once you have
configured the file as you wish, it is recommended to save this in your own
version-controlled repository.

**IMPORTANT**
Without customizing this file, every task will be skipped.

### Running Archer

The recommended way to execute Archer is with `ansible-pull`. By default, this
will clone the project repository to `$HOME/.ansible/pull`. There are different
options you will want to use based on your current context.

_Please read the following section carefully!_


#### Standard execution

```
ansible-pull -U https://github.com/sudoforge/archer.git -C develop [OPTIONS]
```

#### Significant options

Pass any relevant options to the command displayed above.

| Option      | Use case                                    |
|-------------|---------------------------------------------|
| `-t chroot` | Running Archer in a chroot jail             |
| `-K`        | Running Archer as a non-root user           |
| `-o`        | Only run if the repository has been updated |

#### Running as a cron job

Because Archer is idempotent, you can safely run it on a schedule via `cron`.
The cron task must run as root. See the [Cron article][awiki-cron] on the Arch
Wiki for more information.

Archer recommends the following command when running automatically:

```
/usr/bin/ansible-pull -U https://github.com/sudoforge/archer.git -o
```

### Contributing

Please see [`CONTRIBUTING.md`][contributing].

[ansible-web]: https://www.ansible.com "Ansible"
[al-web]: https://www.archlinux.org "Arch Linux"
[alarm-web]: https://www.archlinuxarm.org "Arch Linux ARM"
[awiki-install]: https://wiki.archlinux.org/index.php/Installation_guide
[awiki-chroot]: https://wiki.archlinux.org/index.php/Installation_guide#Chroot
[pkg-ansible]: https://www.archlinux.org/packages/community/any/ansible
[pkg-git]: https://www.archlinux.org/packages/extra/x86_64/git
[molecule-docs]: https://molecule.readthedocs.io "Molecule Documentation"
[awiki-cron]: https://wiki.archlinux.org/index.php/Cron
[contributing]: CONTRIBUTING.md
[issues]: https://github.com/sudoforge/archer/issues "view or create issues"
[travis-build]: https://travis-ci.org/sudoforge/archer.svg?branch=develop
[travis-url]: https://travis-ci.org/sudoforge/archer
