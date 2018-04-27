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
  primary: string
  extra: string[]
```

| Variable         | Description                           |
| ---------------- | ------------------------------------- |
| `locale.primary` | The default locale. Determines `LANG` |
| `locale.extra`   | Additional locales to generate        |

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
