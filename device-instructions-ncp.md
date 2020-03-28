Instructions to configure devices and set up the Network CoProcessor (NCP).
This will also act as the Commissioner for the network.


# Device Setup
## Compile
Based on the OpenThread implementation.
```bash
cd ~/repositories/openthread
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 COMMISSIONER=1 USB=1 BOOTLOADER=USB
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


# Start OpenThread Network
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
1. Open a screen instance to connect to the board:
```bash
screen /dev/ttyACM0
```
1. 
