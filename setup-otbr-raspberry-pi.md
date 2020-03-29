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


# Install OTBR-posix
Log into the Pi.
I prefer to do this over SSH.
The starting credentials are:
```
user: pi
pass: raspberry
```
1. Install dependencies
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git vim
```


# Build OTBR
```bash
git clone https://github.com/openthread/ot-br-posix
cd ot-br-posix
./script/bootstrap
./script/setup
```
Then reboot the Pi `sudo reboot`


# Attach NCP
1. Plug the NCP device into the Pi using the microUSB port on the long side of the Dev Kit
1. Find the serial port the NCP attaches to.
The next step assumes it is `/def/tty`
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


# Configure Pi to Start Network
1. Install Packages:
```bash
sudo apt install -y hostapd dnsmasq tayga
```

## Configure IPv4
1. Block dhcp from using wlan0:
```bash
echo 'denyinterfaces wlan0' | sudo tee -a /etc/dhcpcd.conf
```
1. Configure static IPv4 addresses on the wlan0 interface:
```bash
echo 'allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.1.2
    netmask 255.255.255.0
    network 192.168.1.0
    broadcast 192.168.1.255' | sudo tee /etc/network/interfaces.d/wlan0
```

## Configure hostapd
1. Configure hostapd
  ```bash
  printf '# The Wi-Fi interface configured for static IPv4 addresses
  interface=wlan0\n
  # Use the 802.11 Netlink interface driver
  driver=nl80211\n
  # The user-defined name of the network
  ssid=BorderRouter-AP\n
  # Use the 2.4GHz band
  hw_mode=g\n
  # Use channel 6
  channel=6\n
  # Enable 802.11n
  ieee80211n=1\n
  # Enable WMM
  wmm_enabled=1\n
  # Enable 40MHz channels with 20ns guard interval
  ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]\n
  # Accept all MAC addresses
  macaddr_acl=0\n
  # Use WPA authentication
  auth_algs=1\n
  # Require clients to know the network name
  ignore_broadcast_ssid=0\n
  # Use WPA2
  wpa=2\n
  # Use a pre-shared key
  wpa_key_mgmt=WPA-PSK\n
  # The network passphrase
  wpa_passphrase=12345678\n
  # Use AES, instead of TKIP
  rsn_pairwise=CCMP\n' | sudo tee /etc/hostapd/hostapd.conf
  ```
1. Enable DAEMON_CONF
  ```bash
  echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee -a /etc/default/hostapd
  ```
1. Bootstrap hostapd on reboot:
  ```bash
  sudo systemctl unmask hostapd
  sudo systemctl restart hostapd
  ```
1. Add parameters to hostapd.services
```bash
printf '[Unit]
Description=Hostapd IEEE 802.11 Access Point
After=sys-subsystem-net-devices-wlan0.device
BindsTo=sys-subsystem-net-devices-wlan0.device\n
[Service]
Type=forking
PIDFile=/var/run/hostapd.pid
ExecStart=/usr/sbin/hostapd -B /etc/hostapd/hostapd.conf -P /var/run/hostapd.pid\n
[Install]
WantedBy=multi-user.target\n' | sudo tee /etc/systemd/system/hostapd.service
```
1. Edit rc.local
```bash
sudo sed -i '/exit 0/c\sudo service hostapd start' /etc/rc.local
echo 'exit 0' | sudo tee -a /etc/rc.local
```


## Configure DNSMASQ
1. Backup original configuration file
```bash
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```
1. Make new configuration
```bash
printf '# The Wi-Fi interface configured for static IPv4 addresses
interface=wlan0\n
# Explicitly specify the address to listen on
listen-address=192.168.1.2\n
# Bind to the interface to make sure we arent sending things elsewhere
bind-interfaces\n
# Forward DNS requests to the Google DNS
server=8.8.8.8\n
# Dont forward short names
domain-needed\n
# Never forward addresses in non-routed address spaces
bogus-priv\n
# Assign IP addresses between 192.168.1.50 and 192.168.1.150 with a 12 hour lease time
dhcp-range=192.168.1.50,192.168.1.150,12h\n' | sudo tee /etc/dnsmasq.conf
```
1. Start bind9 after dnsmasq
```bash
sudo sed -i '/After=/c\After=network.target dnsmasq.service' /lib/systemd/system/bind9.service
```


## Configure NAT
1. Edit tayga configuration file
```bash
echo 'prefix 64:ff9b::/96
dynamic-pool 192.168.255.0/24
ipv6-addr 2001:db8:1::1
ipv4-addr 192.168.255.1' | sudo tee -a /etc/tayga.conf
```
1. Enable tayga
```bash
sudo sed -i '/RUN/c\RUN="yes"' /etc/default/tayga
```
1. Enable IPv4 and IPv6 forwarding
```bash
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo sh -c "echo 1 > /proc/sys/net/ipv6/conf/all/forwarding"
```
1. Ensure IPv4 forwarding remains enabled after reboot
```bash
sudo sed -i '/net.ipv4.ip_forward/c\net.ipv4.ip_forward=1' /etc/sysctl.conf
```
1. Configure NAT with iptables
  ```bash
  sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
  sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
  sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

  sudo sed -i '/exit 0/c\iptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local
  echo 'exit 0' | sudo tee -a /etc/rc.local
  ```

## Reboot
```bash
sudo reboot
```

## Join the New Network
The Raspberry Pi should be running a WiFi Access Point called `BorderRouter-AP`.
The Password is `12345678`.
Join this using another computer.
You will no longer be able to ssh into the Raspberry pi.


# Start the Thread Network
1. Find the ipv4 address of the Pi:
  - If the Pi is plugged in to the ethernet use `eth0` inet address.
  - If the Pi is broadcasting using WiFi then use the `wlan0` inet address.
1. On another computer on the same network open a web browser and put the ip address found in previous step into the URL bar.
1. Go to the "Form" Page
1. Configure any


# References
[OpenThread - Raspberry Pi 3B](https://openthread.io/guides/border-router/raspberry-pi-3b)

[OpenThread - Build otbr-posix](https://openthread.io/guides/border-router/build)
