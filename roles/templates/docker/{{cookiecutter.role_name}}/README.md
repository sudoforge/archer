# {{ cookiecutter.role_name }}

This role performs the following functions:

- Function

## Requirements

This role is tested on [Arch Linux][0], but should work on any machine as long
as the following requirements are met.

-

## Dependencies

None

## Role variables

```
---
{{ cookiecutter.role_name }}:
  # required variables
  foo: bar

  # optional variables
  baz: qux
```

## Playbook example

```
---
- name: Playbook for {{ cookiecutter.role_name }}
  hosts: all
  roles:
    - { role: {{ cookiecutter.role_name }}, tags: ['{{ cookiecutter.role_name }}'] }
```

| Variable | Default | Description |
| -------- | ------- | ----------- |
| | | |

## License

MIT

[0]: https://www.archlinux.org "Arch Linux"
