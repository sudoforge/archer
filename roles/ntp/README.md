# ntp

This role performs the following functions:

- Apply a template for `/etc/systemd/timesyncd.conf`
- Enable and start the `systemd-timesyncd` service

## Requirements

This role is tested on [Arch Linux][0], but should work on any machine as long
as the following requirements are met.

-

## Dependencies

None

## Role variables

```
---
ntp:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean

  # The primary NTP server(s) to use for network time syncing
  # Default:
  #   - 0.arch.pool.ntp.org
  #   - 1.arch.pool.ntp.org
  #   - 2.arch.pool.ntp.org
  #   - 3.arch.pool.ntp.org
  primary: string[]

  # The fallback NTP server(s) to use for network time syncing
  # Default:
  #   - 0.pool.ntp.org
  #   - 1.pool.ntp.org
  #   - 0.us.pool.ntp.org
  fallback: string[]
```

## Playbook example

```
---
- name: Playbook for ntp
  hosts: all
  roles:
    - { role: ntp, tags: ['ntp'] }
```

## License

MIT

[0]: https://www.archlinux.org "Arch Linux"
