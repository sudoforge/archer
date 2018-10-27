# desktop

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
desktop:
  # Whether or not this role is enabled
  # Default: false
  enabled: boolean


  # lightdm configuration
  lightdm:

    # Whether or not to enable the lightdm tasks
    # Default: false
    enabled: boolean

    # Whether or not the systemd service should be enabled
    # Default: false
    service: boolean

    # lightdm-gtk-greeter configuration
    greeter:
      
      # Whether or not to enable the lightdm-gtk-greeter tasks
      # Default: false
      enabled: boolean

      # The name of the GTK theme to use
      # Default: "Adwaita:dark"
      gtk_theme: string

      # The name of the background image to use from the backgrounds dir
      # Default: red-mountains.png
      background: string

      # Whether or not to hide the user image
      # Default: true
      hide_user_image: boolean
```

## Playbook example

```
---
- name: Playbook for desktop
  hosts: all
  roles:
    - { role: desktop, tags: ['desktop'] }
```

## License

MIT

[0]: https://www.archlinux.org "Arch Linux"
