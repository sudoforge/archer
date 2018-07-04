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
  enabled: true
  profiles: string[]
  systemd:
    enabled: bool
```    

## Playbook example

```
---
- name: Playbook for network
  hosts: all
  roles:
    - { role: network, tags: ['network'] }
```

| Variable          | Default                | Description                              |
| ----------------- | ---------------------- | ---------------------------------------- |
| `enabled`         | `false`                | Whether or not this role is enabled      |
| `profiles`        | `[ethernet, wireless]` | The types of connections to set up       |
| `systemd.enabled` | `false`                | Whether or not to use `systemd-networkd` |

## License

MIT
