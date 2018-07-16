# timezone

This role performs the following functions:

- Set the system timezone via symlink
- Conditionally set the hardware clock from the system clock
    - This will only run if `/etc/adjtime` is not present

## Requirements

None

## Dependencies

None

## Role variables

```
---
timezone:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean

  # If set to "UTC", conditionally generates /etc/adjtime
  # Default: UTC
  hwclock: string

  # The /usr/share/zoneinfo property to use, e.g. "America/Los_Angeles". You
  # generally want this set to the primary region you reside in.
  #
  # Default: UTC
  zoneinfo: string
```
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
