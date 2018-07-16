# systemd-boot

This role performs the following functions:

- Install and configure a bootloader. Supported bootloaders include:
    - `systemd-boot`
- Conditionally install and configure `intel-ucode` (for microcode updates)

## Requirements

This role is tested on [Arch Linux][0] specifically, but should work on any
machine as long as the following requirements are met.

- [`pacman`][1]

## Dependencies

None

## Role variables

```
---
bootloader:
  systemd:
    # Whether or not this role is enabled
    # Default: false
    enabled: boolean

    # Kernel parameter options for systemd-boot
    # Default: []
    options: string[]
```

## Playbook example

```
---
- name: Playbook for bootloader
  hosts: all
  roles:
    - { role: bootloader, tags: ['bootloader'] }
```

## License

MIT

[0]: https://www.archlinux.org "Arch Linux"
[1]: https://www.archlinux.org/packages/core/x86_64/pacman/ "core/pacman"
