# hostapd

This role performs the following functions:

- Install `hostapd`
- Apply a teamplate to `/etc/hostapd/hostapd.conf`

## Requirements

None

## Dependencies

None

## Role variables

```
---
hostapd:
  # required variables
  enabled: boolean
  ssid: string
  passphrase: string
  interface: string
  bridge: string
  driver: string
  channel: integer
  pairwise: string
```

## Playbook example

```
---
- name: Playbook for hostapd
  hosts: all
  roles:
    - { role: hostapd, tags: ['hostapd'] }
```

| Variable     | Default       | Description                                 |
| ------------ | ------------- | ------------------------------------------- |
| `enabled`    | `false`       | Whether or not to configure `hostapd`       |
| `ssid`       | `archer-wifi` | The name of the wireless network            |
| `passphrase` | `archerwifi`  | The passphrase for the wireless network     |
| `interface`  | `wlan0`       | The name of the interface to broadcast from |
| `bridge`     | `br0`         | The name of the bridge                      |
| `driver`     | `nl80211`     | The name of the driver                      |
| `channel`    | `7`           | The channel to broadcast on                 |
| `pairwise`   | `CCMP`        | WPA2's data encryption                      |

## License

MIT
