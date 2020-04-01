Instructions to set up the OpenThread Border Router using the Raspberry Pi 3B.


# Install Raspbian
1. Plug SD card into computer.
Find the device file.
This guide assumes it's `/dev/mmcblk0`
1. Download Raspbian
```bash
cd ~/Downloads
wget -O 2019-04-08-raspbian-stretch-lite.zip -c http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-04-09/2019-04-08-raspbian-stretch-lite.zip
unzip 2019-04-08-raspbian-stretch-lite.zip
```
1. Flash the SD card
```bash
sudo dd \
    if=2019-04-08-raspbian-stretch-lite.img \
    of=/dev/mmcblk0 \
    bs=4M \
    status=progress \
    conv=fsync
```
1. `touch` a file named `ssh` in the root of the boot partition on the sd card.
1. Plug the SD Card into the Raspberry Pi and turn it on

# Log in and configure Pi
Log into the Pi.
I prefer to do this over SSH.
The starting credentials are:
```
user: pi
pass: raspberry
```
Change default Password
```bash
passwd
```


# Install OTBR-posix
1. Install dependencies
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git vim tmux libreadline-dev
```
1. Start a new tmux session
```bash
tmux new
```
1.  Build OTBR
```bash
git clone https://github.com/openthread/ot-br-posix
cd ot-br-posix
git checkout thread-br-certified-20180819
./script/bootstrap
sed -i '/NETWORK_MANAGER/c\NETWORK_MANAGER=0' examples/platforms/raspbian/default
NETWORK_MANAGER=0 ./script/setup
```


#  Configure NAT
Maybe do this?

https://openthread.io/guides/border-router/access-point#configure-nat


# Attach NCP
1. Plug the NCP device into the Pi using the microUSB port on the long side of the Dev Kit
1. Find the serial port the NCP attaches to.
The next step assumes it is `/dev/ttyACM0`
1. Edit wpantund.conf: `sudo vi /etc/wpantund.conf`
  - Change
    ```
    Config:NCP:SocketPath "/dev/ttyUSB0"
    ```
    to
    ```
    Config:NCP:SocketPath "/dev/ttyACM0"
    ```
  - Add line:
    ```
    Config:TUN:NetworkName wpan0
    ```
1. Restart services
  ```bash
  sudo systemctl restart avahi-daemon
  sudo systemctl restart otbr-agent
  sudo systemctl restart otbr-web
  sudo systemctl restart wpantund
  ```
1. Restart
  ```bash
  sudo reboot
  ```
1. Verify the NCP is connected
  ```bash
  sudo wpanctl status
  ```
  should return
  ```
  wpan0 => [
  	"NCP:State" => "offline"
  	"Daemon:Enabled" => true
  	"NCP:Version" => "OPENTHREAD/20191113-00443-g133ec09b; NRF52840; Mar 27 2020 20:31:41"
  	"Daemon:Version" => "0.08.00d (/b161410; Mar 29 2020 04:06:01)"
  	"Config:NCP:DriverName" => "spinel"
  	"NCP:HardwareAddress" => [F4CE36F64AF8185C]
  ]
  ```
  Make sure that `NCP:State` is **not** `uninitialized`


# Join Network
This section assumes that the thread network has already been started on one of the FTD devices.
1. Run wpanctl in interactive mode
```bash
sudo wpanctl -I wpan0
```
1. Scan for the Thread network
```
scan
```
1. Join the network
```
join --type router --panid 0x1234 --xpanid 0123456789012345 --channel 17 --name weisenet
joiner start M0untWH!tn3y
```


# Form Thread Network
For the record, I can't get this to work.
1. Set the Network Parameters through the NCP
```bash
sudo wpanctl setprop Network:PANID 0x1234
sudo wpanctl setprop Network:XPANID 9988776655443322
sudo wpanctl setprop Network:Key 11112222333344445555666677778888
sudo wpanctl config-gateway -d "fd11:22::"
```
1. Generate PreShared key
```bash
cd ~/ot-br-posix/tools
# ./pskc <PASSPHRASE> <EXTPANID> <NETWORK_NAME>
./pskc 123456 9988776655443322 weisenet | xargs sudo wpanctl setprop Network:PSKc --data
```
1. Start Network
```bash
sudo wpanctl form "weisenet"
```
1. Confirm the network configuration
```bash
sudo wpanctl status
sudo wpanctl getprop Thread:OnMeshPrefixes
sudo wpanctl getprop Network:PSKc
```
