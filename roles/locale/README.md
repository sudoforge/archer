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
  system: value
  list: []
```

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
