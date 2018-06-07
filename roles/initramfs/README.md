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
  preset: string
```

| Variable   | Description                                              |
| ---------- | -------------------------------------------------------- |
| `packages` | List of supplementary packages (e.g. `lvm2`)             |
| `hooks`    | The hooks to set in `mkinitcpio.conf`                    |
| `preset`   | The name of the preset to build from `/etc/mkinitcpio.d` |

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
