# hostname

This role performs the following functions:

- Set the system hostname for the current session
    - _If it differs from the current hostname_
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
  # required variables
  enabled: boolean
  name: string

  # optional variables
  aliases: string[]
```

| Variable  | Default  | Description                              |
| --------- | -------- | ---------------------------------------- |
| `enabled` | `false`  | Whether or not this role is enabled      |
| `name`    | `archer` | The hostname to set for the machine      |
| `aliases` | `[]`     | Any aliases to also point to `127.0.0.1` |

## Playbook example

```
---
- name: My Playbook
  hosts: all
  roles:
    - { role: hostname, tags: ['hostname'] }
```

## License

MIT
