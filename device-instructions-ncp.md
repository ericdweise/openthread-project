Instructions to configure devices and set up the Network CoProcessor (NCP).



# Device Setup
## Compile
Based on the OpenThread implementation.
```bash
cd ~/repositories/openthread
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 BORDER_AGENT=1 BORDER_ROUTER=1 COMMISSIONER=1 UDP_FORWARD=1 USB=1
# make -f examples/Makefile-nrf52840 JOINER=1 USB=1
```


## Convert Binary to .hex
```bash
arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-ncp-ftd output/nrf52840/bin/ot-ncp-ftd.hex
```


## Flash Development Kit
1. Plug the Dev. Kit into workstation using microusb cable. Use the USB port on the **short end** of the Dev. Kit
1. Switch the poser supply to "VDD" on the Dev. Kit (SW9)
1. Switch the Dev Kit "ON"
1. Find the Device Serial Number on the top of the Dev Kit.
    It is the 9 digit number printed on the MCU.
1. Flash the compiled .hex file using nrfjprog.
```bash
nrfjprog -f nrf52 --chiperase --program  output/nrf52840/bin/ot-ncp-ftd.hex --reset
```


# NCP Joiner Network
1. Switch the Power Supply to "USB"
1. Plug the node into a workstation using the microUSB port on the long side of the board
1. Turn the board on. No LEDs will light up.
1. Make sure that:
```bash
ls -l /dev/ttyACM0
```
returns:
```
crw-rw----  1 root  dialout 166,     0 Mar 19 16:34 ttyACM0
```
1. Start wpantund
```bash
sudo /usr/local/sbin/wpantund \
    -o Config:NCP:SocketPath /dev/ttyACM0 \
    -o Config:TUN:InterfaceName wpan0 \
    -o Daemon:SyslogMask " -info"
```
Leave this terminal open.
1. Open a new terminal
1. Check that the NCP is on the wpan0 network:
```bash
sudo wpanctl status
```
should return something like
```
wpan0 => [
	"NCP:State" => "offline"
	"Daemon:Enabled" => true
	"NCP:Version" => "OPENTHREAD/20191113-00443-g133ec09b; NRF52840; Mar 27 2020 19:47:01"
	"Daemon:Version" => "0.07.01 (0.07.01-2-g6993264-dirty; Mar 27 2020 17:56:13)"
	"Config:NCP:DriverName" => "spinel"
	"NCP:HardwareAddress" => [F4CE36F64AF8185C]
]
```
1.
```bash
sudo wpanctl -I wpan0
```
1. Join network
```
scan
setprop Network:Key 00000000000000000000000000000000
join 1
```
