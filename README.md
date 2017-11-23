# Archer

**Archer** is a collection of [Ansible][0] playbooks meant to provision
machines running [Arch Linux][1]. It is forked from the excellent
[`pigmonkey/spark`][2], with various improvements for my own environment and
workflows.

These playbooks have been made with the following goals in mind:

* Keep it simple
* Make it easy to use
* Don't make assumptions

If you find that someething is not working for you, or that one or more of the
above goals is not being met, please [open an issue][3].

## ARCHER IS IN PROGRESS

Please avoid forking, or using the playbook(s) within this repository until
this message is removed.

## Use cases

The playbooks included in this repository utilize different roles to configure
machines for different purposes. Below is a quick overview of some of use cases
for each supported playbook.

| Playbook          | Use cases |
| ----------------- | --------- |
| `init.yml`        | Set up a basic environment with root shell access. **Run this first.** |
| `workstation.yml` | General purpose machine used for anything from programming to watching videos. |
| `thin-client.yml` | A machine primarily used to access the workstation remotely. |

[0]: https://www.ansible.com "Ansible"
[1]: https://www.archlinux.org "Arch Linux"
[2]: https://github.com/pigmonkey/spark "Spark"
[3]: https://github.com/bddenhartog/archer/issues "view or create issues"
