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
  hwclock: string
  zoneinfo: string
```

| Variable            | Description                                    |
| ------------------- | ---------------------------------------------- |
| `timezone.hwclock`  | If set to `UTC`, generates `/etc/adjtime`      |
| `timezone.zoneinfo` | The zoneinfo value, e.g. `America/Los_Angeles` |

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
