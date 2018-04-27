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
    device: string
```

| Variable               | Description                                   |
| ---------------------- | --------------------------------------------- |
| `systemd.boot.enabled` | Whether or not to run the tasks in this role  |
| `systemd.boot.device`  | The `LABEL` or `PARTUUID` for the root device |

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
