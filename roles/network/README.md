# network

This role performs the following functions:

- 

## Requirements

None

## Dependencies

None

## Role variables

```
---
network:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean

  # The types of connections to set up
  # Default:
  #   - ethernet
  #   - wireless
  profiles: ENUM[ethernet, wireless]

  # Whether or not to use systemd-networkd
  # Default: false
  systemd:
    enabled: boolean
```    

## Playbook example

```
---
- name: Playbook for network
  hosts: all
  roles:
    - { role: network, tags: ['network'] }
```

## License

MIT
