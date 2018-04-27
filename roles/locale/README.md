# locale

This role performs the following functions:

- Generate the system locales
- Apply a template to `/etc/locale.conf`

## Requirements

None

## Dependencies

None

## Role variables

```
---
locale:
  # required variables
  system: string
  list: string[]
```

| Variable        | Description                                    |
| --------------- | ---------------------------------------------- |
| `locale.system` | The default system language. Determines `LANG` |
| `locale.list`   | The list of locales to generate for the system |

## Playbook example

```
---
- name: Playbook for locale
  hosts: all
  roles:
    - { role: locale, tags: ['locale'] }
```

## License

MIT
