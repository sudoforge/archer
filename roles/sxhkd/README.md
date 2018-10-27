# sxhkd

This role performs the following functions:

- Function

## Requirements

This role is tested on [Arch Linux][0], but should work on any machine as long
as the following requirements are met.

-

## Dependencies

None

## Role variables

```
---
sxhkd:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean

  # Whether or not the systemd service should be enabled
  # Default: false
  service: boolean
```

## Playbook example

```
---
- name: Playbook for sxhkd
  hosts: all
  roles:
    - { role: sxhkd, tags: ['sxhkd'] }
```

## License

MIT

[0]: https://www.archlinux.org "Arch Linux"
