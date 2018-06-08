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
  enabled: boolean
  primary: string
  extra: string[]
```

| Variable  | Default       | Description                           |
| --------- | ------------- | ------------------------------------- |
| `enabled` | `false`       | Whether or not enable this role       |
| `primary` | `en_US.UTF-8` | The default locale. Determines `LANG` |
| `extra`   | `[]`          | Additional locales to generate        |

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
