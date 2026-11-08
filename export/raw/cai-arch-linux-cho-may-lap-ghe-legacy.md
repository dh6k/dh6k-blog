# CÀI Arch linux cho máy lap ghẻ legacy

Spec máy mình là: Core i3-2350m, 4gb ram, 500gb hdd, vga onboard (hd 3000).
sau đây là chi tiết cách cài:

-1, tạo usb boot có bộ cài arch mới nhất. cắm vào máy, mở f12 boot menu, chọn usb storage device, sau đó là boot to arch linux dòng đầu tiên.

-2, Kết nối wifi (ethernet ko cần)

```
$ iwctl
$ station wlan0 connect "Tên Wifi"

``` 
+`passphrase`: điền mật khẩu vào

-3, danh sách phân vùng:

```
$ lsblk
``` 
-4, phân vùng ổ đĩa (sda1 chính, sda2 swap)
+đầu tiên hãy thiết lập ổ đĩa
 ```
$ cfdisk /dev/sda

```
+để phân vùng sda1 là `linux`, sda2 là `linux swap/solaris`, sau đó chọn `write` > `yes`, sau đó exit.
+sau đó format:
```
$ mkfs.ext4 /dev/sda1
$ mkswap /dev/sda2 
$ swapon /dev/sda2
```

-5, mount các phân vùng lại:
```
$ mount /dev/sda1 /mnt

```
-6, reflect mirror sang Việt Nam cho nó nhanh (thực ra câu lệnh này là tìm các server mirror nhanh nhất của 1 quốc gia mà máy có thể kết nối được, nhma Việt Nam chỉ có mỗi cái server bizflycloud thôi.)
```
$ reflector --verbose --country 'Vietnam' -l 10 -p http --sort rate --save /etc/pacman.d/mirrorlist

```
-7, bắt đầu cài đặt arch linux (dùng xfce4,lightdm)
```
$ pacstrap /mnt base base-devel linux linux-firmware linux-headers vim sudo nano xfce4 xfce4-goodies xorg xorg-init lightdm lightdm-gtk-greeter git pulseaudio pulseaudio-equalizer 

```
+ đợi khoảng 4-15p 

-8, tạo file `fstab`:
```
$ genfstab -U -p /mnt >> /mnt/etc/fstab
$ cat /mnt/etc/fstab

```
-9, đăng nhập vào arch đã cài trong ổ cứng:
```
$ arch-chroot /mnt

```

-10, thiết lập locale (EN_US.UTF-8)
```
# nano /etc/locale.gen

```

+ trong nano bỏ dấu thăng ở chỗ `en_US.UTF-8`
ctrl + O để lưu, ctrl + X để thoát

```
# locale-gen
# echo LANG=EN_US.UTF-8 > /etc/locale.conf
# export LANG=EN_US.UTF-8
```

-11, chỉnh múi giờ (GMT/UTC + 7):
```
# ln -sf /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime
# hwclock --systohc --utc

```

-12, thiết lập hostname `n5110`, host:
```
# echo n5110 > /etc/hostname
# nano /etc/hosts

```

+ viết cách dòng dưới cùng 1 dòng:

```
127.0.0.1 localhost
::1 localhost
127.0.0.1 n5110.localdomain n5110

```
ctrl + O, ctrl + X

-13, tạo root password
```
# passwd
```

+ nhập password sau đó nhập lại password 1 lần nữa rồi nhấn enter

-14, thêm người dùng và set password:

```
# useradd -mG lp,network,power,storage,wheel,sys,log dldkk
# passwd dldkk
```
+ nhập password và sau đó nhập lại password, tương tự như bước 13.

-15, thêm user vào sudoers:

```
# nano /etc/sudoers

```

+ nhập sau dòng root:

```
dldkk ALL=(ALL) ALL

```

+ uncomment ở chỗ `#wheel`, `#wheel (no pass)` và `#sudo`.
ctrl + O, ctrl + X

-16, Network Manager:

```
# pacman -S networkmanager
# systemctl enable NetworkManager

```

-17, tạo bootloader (cụ thể là `grub` )cho legacy:

```
# mkinitcpio -p linux
# pacman -S grub
# grub-install /dev/sda
# grub-mkconfig -o /boot/grub/grub.cfg

```

-18, thiết lập lightdm do mình đã cài từ trước đó:

```
# nano /etc/lightdm/lightdm.conf
[Seat:*]
....
greeter-session=lightdm-gtk-greeter
....
```

+ ctrl + O, ctrl + X

```
# systemctl enable lightdm.service

```

-19, thoát ra và khởi đông lại máy

```
# exit
$ umount -R /mnt
$ reboot
```

+ Bây giờ có thể rút usb boot ra ngoài.
+ Sau khi khởi động lại thành công

20, kết nối wifi:
```
$ nmcli device wifi list
$ nmcli device wifi connect "Tên wifi" password *mật khẩu wifi*
```
  =>và thế là xong.

phần sau các bạn thích cài gì thì cài.
DE thì khuyên dùng gnome, cài xong bỏ cái gói `gnome-software` đi cho nó nhẹ máy. Máy yếu thì khuyên dùng XFCE, LXDE, hay là wm như Openbox, i3,....
Nhớ cài thêm `yay` nếu bạn muốn dùng AUR, `pamac` và `libpamac` cho nó dễ dùng.

Ngoài ra còn có `chaotic-aur` giúp cài app aur build sẵnvới hướng dẫn chi tiết bằng tiếng Anh tại [đây](https://aur.chaotic.cx/).

