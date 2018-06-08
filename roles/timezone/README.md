# timezone

This role performs the following functions:

- Set the system timezone via symlink
- Set the hardware clock from the system clock
    - This will only run if `/etc/adjtime` is not present

## Requirements

None

## Dependencies

None

## Role variables

```
---
timezone:
  # required variables
  enabled: boolean
  hwclock: string
  zoneinfo: string
```

| Variable   | Default | Description                                    |
| ---------- | ------- | ---------------------------------------------- |
| `enabled`  | `false` | Whether or not this role is enabled            |
| `hwclock`  | `UTC`   | If set to `UTC`, generates `/etc/adjtime`      |
| `zoneinfo` | `UTC`   | The zoneinfo value, e.g. `America/Los_Angeles` |

## Playbook example

```
---
- name: Playbook for timezone
  hosts: all
  roles:
    - { role: timezone, tags: ['timezone'] }
```

## License

MIT
