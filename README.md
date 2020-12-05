# Archer [![Build Status][trunk-workflow-badge]][trunk-workflow-url]

**Archer** provides [Ansible][ansible-web] roles for use in provisioning a
machine running [Arch Linux][al-web]. It can be used directly after the [Chroot
step][awiki-chroot] of the [Installation Guide][awiki-install] or at any other
point in time during the machine's life cycle.

## Usage

Archer aims to automate various steps of administering an Arch Linux
installation: initial machine configuration during the chroot step, and
post-installation configuration both during the initial setup and ongoing
maintenance. Due to its flexibility and easy per-host customisation, you might
consider Archer a framework of sorts.

To take advantage of the suite of roles contained in this project, see
[**Customizing the build**](#customizing-the-build).

To report a bug or request a new feature, please [search the issues][issues]
and create a new issue if one does not already exist.

### Requirements

* [Arch Linux][al-web] or [Arch Linux ARM][alarm-web]
* [`ansible`][pkg-ansible]

To install the requirements:

```
pacman -S git ansible
```

### Customizing the build

Archer tries to subscribe to an *opt-in* philosophy, which in reality means that
_most_ roles in this repository **will not run by default**. You will instead
need to enable them by configuring the host variables on your machine(s).

To do this, download `host_vars/localhost.example` from this repository:

```
curl --create-dirs -o /etc/ansible/host_vars/localhost \
    https://raw.githubusercontent.com/sudoforge/archer/trunk/localhost.example.yml
```

Open the file with an editor. Look through the file and change the `enabled`
property from `false` to `true` for roles which you want to enable. You can
remove sections that relate to roles you do not want to install. Once you have
configured the file as you wish, it is recommended to save this in your own
version-controlled repository.

> **IMPORTANT**
> Note that **there are roles which will take action by default**. It would be
> best to thoroughly review the roles declared in `local.yml`, or optionally,
> omit roles which you do not want to run from that file entirely.

### Running Archer

The recommended way to execute Archer is with `ansible-pull`. By default, this
will clone the project repository to `$HOME/.ansible/pull`. There are different
options you will want to use based on your current context.

_Please read the following section carefully!_


#### Standard execution

```
ansible-pull -U https://github.com/sudoforge/archer.git [OPTIONS]
```

#### Significant options

Pass any relevant options to the command displayed above.

| Option      | Use case                                      |
| ----------- | --------------------------------------------- |
| `-t <tag>`  | Only run tasks which have the given `<tag>`   |
| `-K`        | Running Archer as a non-root user             |
| `-o`        | Only run if the repository has been updated   |
| `-C`        | Use a specific tree, such as a feature branch |

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
[trunk-workflow-badge]: https://github.com/sudoforge/archer/workflows/trunk/badge.svg
[trunk-workflow-url]: https://github.com/sudoforge/archer/actions?query=workflow%3Atrunk
