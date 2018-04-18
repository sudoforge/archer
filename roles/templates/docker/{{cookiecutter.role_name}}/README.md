# {{ cookiecutter.role_name }}

This role performs the following functions:

- Function

## Requirements

None

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
    - { role: {{ cookiecutter.role_name }}, tags: ['{{ cookiecutter.role_name }}'] i}
```

## License

MIT
