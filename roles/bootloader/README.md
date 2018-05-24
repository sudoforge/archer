# systemd-boot

This role performs the following functions:

- Configure a bootloader. Currently supported bootloaders include:
    - `systemd-boot`
- Conditionally install and configure `intel-ucode` (for microcode updates)

## Requirements

None

## Dependencies

None

## Role variables

```
---
bootloader:
  systemd:
    # required variables
    enabled: boolean
    options: string[]
```

| Variable          | Description                               |
| ----------------- | ----------------------------------------- |
| `systemd.enabled` | Whether or not to configure systemd-boot  |
| `systemd.options` | Kernel parameter options for systemd-boot |

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
