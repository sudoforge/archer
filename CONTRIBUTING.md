# Contributing to Archer

Thank you for considering contributing to Archer.

## Requirements

* [`git`][pkg-git]
* [`docker`][pkg-docker]
* [`make`][pkg-make]
* [`python-pipenv`][pkg-pipenv]

To install all of the requirements at once:

```
pacman -S git docker make python-pipenv
```

## Testing

Roles in Archer are tested using [`molecule`][molecule-docs]. To test a role,
first change to the project directory and then activate the virtual
environment:

```
$ cd path/to/archer
$ pipenv shell
```

Next, navigate to the directory of the role you wish to test...

```
cd roles/timezone
```

...and run the test(s):

```
molecule test
```

To test all of the roles at once from the project root:

```
make test
```

## Creating a new role

New roles should be generated with `molecule`, and from a template included in
the `roles/templates` directory. Because `molecule` will generate the role in
your current directory, you should make sure you are in the `roles` directory to
begin with.

Generating a new role from an included template will create the new role
directory, and set up the basic file structure for testing with `molecule`.

```
$ pipenv shell
$ cd roles
$ molecule init template --url templates/NAME
```

Replace `NAME` with the name of the template you wish to use. Template names
map to the driver molecule will use when creating the virtual environment for
the role's tests. Archer currently supports the following template names:

* docker

You will be prompted for a few values:

| Parameter     | Description                                       |
| ------------- | ------------------------------------------------- |
| `role_name`   | The name of the new role                          |
| `description` | A description of the role for Ansible Galaxy      |
| `tags`        | A space-separated list of tags for Ansible Galaxy |

You now have a new directory in `roles/` with boilerplate code for a new task,
including a basic test scenario and a pre-populated metadata file for Ansible
Galaxy.

## Adding tasks

Tasks should be added to `roles/your_role/tasks/main.yml`. If you are new to
Ansible, we suggest reading the [Getting Started][adocs-intro] guide to learn
about Ansible.

## Using tags

Because of Archer's design goals, both roles and tasks should be tagged.

### Tagging roles

Any given role should be tagged with a name equal or similar to the name of the
role. the tag should be added to the role when the role is added to
`local.yml`.

For example:

```
roles:
  - { role: timezone, tags: ['timezone'] }
```

Tagging entire roles makes it easy to exclusively skip or run roles.

### Tagging tasks

Tasks inherit their role's tag, so there is no need to tag tasks with the
role's name. Instead, tasks should be tagged only if they meet any of the
special cases defined below.

| Tag name | Use case                                 |
| ---------|----------------------------------------- |
| `chroot` | The task can be run in a chroot jail     |
| `aur`    | The task relates to an AUR package       |
| `notest` | This task should be skipped during tests |

#### The `chroot` tag

In a chroot jail, such as when you are first installing Arch Linux on
a machine, certain tasks will fail, such as those attempting to access files
that are outside of the chroot environment.

Every task in Archer should run successfully in a live, working environment. By
providing the `chroot` tag to tasks, we can enable users to run Archer while in
a chroot jail, thus providing inital machine configuration during installation,
such as creating users, configuring the boot loader, installing a desktop
environment, and more.

See the [Change root][awiki-chroot] entry on the Arch Wiki to learn more.

#### The `aur` tag

If a task relates to the AUR in any way, such as installing a package from the
AUR, it should be tagged with `aur`. This is to enable users to easily skip all
AUR packages if they wish to.

#### The `notest` tag

Archer's role templates configure the test instance provisioner (Ansible) to
skip tasks that have the `notest` tag. Ideally, we would not need to use this,
however, there are certain things (like setting the hardware clock) that simply
do not work in virtual environments.

[adocs-intro]: http://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html
[awiki-chroot]: https://wiki.archlinux.org/index.php/Change_root
[pkg-git]: https://www.archlinux.org/packages/extra/x86_64/git
[pkg-make]: https://www.archlinux.org/packages/core/x86_64/make
[pkg-pipenv]: https://www.archlinux.org/packages/community/any/python-pipenv
[pkg-docker]: https://www.archlinux.org/packages/community/x86_64/docker
