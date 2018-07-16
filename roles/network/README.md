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

  # The types of connections to configure
  # Default:
  #  - ethernet
  #  - wireless
  profiles: string[]

  # systemd-boot variables
  systemd:
    # Whether or not to install and configure systemd-boot
    # Default: false
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
