# initramfs

This role performs the following functions:

- Function

## Requirements

This role is tested on [Arch Linux][0], but should work on any machine as long
as the following requirements are met.

- [`pacman`][1]
- [`mkinitcpio`][2]

## Dependencies

None

## Role variables

```
---
initramfs:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean

  # The name of the preset to build from /etc/mkinitcpio.d
  # Default: linux
  preset: string

  # List of supplementary packages to install, e.g. lvm2 if using LVM
  # Default: []
  packages: string[]

  # The hooks to set in mkinitcpio.conf
  # Default:
  #   - base
  #   - udev
  #   - autodetect
  #   - modconf
  #   - block
  #   - filesystems
  #   - keyboard
  #   - fsck
  hooks: string[]
```

## Playbook example

```
---
- name: Playbook for initramfs
  hosts: all
  roles:
    - { role: initramfs, tags: ['initramfs'] }
```

## License

MIT

[0]: https://www.archlinux.org "Arch Linux"
[1]: https://www.archlinux.org/packages/core/x86_64/pacman/ "core/pacman"
[2]: https://www.archlinux.org/packages/core/any/mkinitcpio/ "core/mkinitcpio"
