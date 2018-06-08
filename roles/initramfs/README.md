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
  enabled: boolean
  packages: string[]
  hooks: string[]
  preset: string
```

| Variable   | Default   | Description                                              |
| ---------- | --------- | -------------------------------------------------------- |
| `enabled`  | `false`   | Whether or not this role is enabled                      |
| `packages` | `[]`      | List of supplementary packages (e.g. `lvm2`)             |
| `hooks`    | see below | The hooks to set in `mkinitcpio.conf`                    |
| `preset`   | `linux`   | The name of the preset to build from `/etc/mkinitcpio.d` |

`hooks` default items:

- `base`
- `udev`
- `autodetect`
- `modconf`
- `block`
- `filesystems`
- `keyboard`
- `fsck`

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
