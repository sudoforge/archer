# systemd-boot

This role performs the following functions:

- Configure `systemd-boot`
- Conditionally install and configure `intel-ucode` (microcode updates)

## Requirements

None

## Dependencies

None

## Role variables

```
---
systemd:
  boot:
    # required variables
    enabled: boolean
    options: string[]
```

| Variable               | Description                                  |
| ---------------------- | -------------------------------------------- |
| `systemd.boot.enabled` | Whether or not to run the tasks in this role |
| `systemd.boot.options` | Kernel parameter options                     |

## Playbook example

```
---
- name: Playbook for systemd-boot
  hosts: all
  roles:
    - { role: systemd-boot, tags: ['systemd-boot'] }
```

## License

MIT
