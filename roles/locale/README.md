# locale

This role performs the following functions:

- Generate locales for the system
- Apply a template to `/etc/locale.conf`

## Requirements

None

## Dependencies

None

## Role variables

```
---
locale:
  # Whether or not this role should be enabled
  # Default: false
  enabled: boolean

  # Determines the LANG variable
  # Default: en_US.UTF-8
  lang: string

  # Determines the LC_TIME variable
  # Default: en_DK.UTF-8
  lc_time: string

  # Determines the LC_COLLATE variable
  # Default: C
  lc_collate: string

  # Determines which locales to generate. The value of the 'lang' variable is
  # included implicitly, and does not need to be defined in this list.
  #
  # Default: []
  locales: string[]
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
