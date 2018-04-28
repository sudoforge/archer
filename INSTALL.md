# Installation guide

These are the steps I personally take when provisioning a new
machine. With this guide, there are a few assumptions:

- The machine has a single disk
- The user wants to fully encrypt the system (LVM on LUKS)
- The user is **not** using the `GRUB` boot loader
    - This means we will not be encrypting the boot partition


```
export DISK="<device path, e.g. /dev/sda2>"

sytemctl start dhcpcd.service && while ! ping -c1 archlinux.org &> /dev/null; do sleep 1; done
timedatectl set-ntp true

dd if=/dev/urandom of="$DISK" bs=4096 status=progress
parted "$DISK" mklabel gpt
parted "$DISK" mkpart primary fat32 1MiB 513MiB
parted "$DISK" set 1 boot on
parted "$DISK" mkpart primary 513MiB 100%

cryptsetup luksFormat --type luks2 "$DISK"
cryptsetup open "$DISK" lvm
pvcreate /dev/mapper/lvm
vgcreate archlinux /dev/mapper/lvm
lvcreate -L 4GiB -n swap archlinux
lvcreate -L 24GiB -n root archlinux
lvcreate -l 100%FREE -n home archlinux

mkfs.vfat -F32 "${DISK}p1"
mkfs.ext4 /dev/mapper/archlinux-root
mkfs.ext4 /dev/mapper/archlinux-home
mkswap /dev/mapper/archlinux-swap
swapon -d /dev/mapper/archlinux-swap

pacstrap /mnt base base-devel wpa_supplicant git ansible vim
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
```

Next, follow the README to configure your system using Archer!
