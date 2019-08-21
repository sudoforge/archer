# hostname

This role performs the following functions:

- Set the desired hostname in `/etc/hostname`
- Edit `/etc/hosts`, and ensure the following values are the only values
  assigned to `127.0.0.1`:
    - `{{ hostname.name }}`
    - `{{ hostname.name }}.localdomain`
    - Any values in `{{ hostname.aliases }}`

## Requirements

None

## Dependencies

None

## Role variables

```
---
hostname:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean

  # Detremine the hostname for the machine
  # Default: archer
  name: string

  # Additional hostname entries in /etc/hosts
  # Default: []
  aliases: string[]
```

## Playbook example

```
---
- name: Playbook for hostname
  hosts: all
  roles:
    - { role: hostname, tags: ['hostname'] }
```

## License

MIT
