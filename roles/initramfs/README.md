# initramfs

This role performs the following functions:

- Function

## Requirements

None

## Dependencies

None

## Role variables

```
---
initramfs:
  # required variables
  packages: string[]
  hooks: string[]
```

| Variable             | Description                                  |
| -------------------- | -------------------------------------------- |
| `initramfs.packages` | List of supplementary packages (e.g. `lvm2`) |
| `initramfs.hooks`    | The hooks to set in `mkinitcpio.conf`        |

## Playbook example

```
---
- name: Playbook for initramfs
  hosts: all
  roles:
    - { role: initramfs, tags: ['initramfs'] }
```

## License

MIT
