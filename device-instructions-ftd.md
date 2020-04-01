Instructions for setting up and running the Commissioner Node.
The network needs one commissioner to configure the network and add other devices.
The network will be started from this device and the other devices will join.
I use the nRF52840 Dongle (PCS10059) for This.



# Device Setup
## Modify Start Address
Necessary to not overwrite the bootloader
```bash
vi ~/repositories/openthread/.....
```


## Compile
Compile a USB, Joiner node
```bash
cd ~/repositories/openthread/
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 COMMISSIONER=1 USB=1 BOOTLOADER=USB
```


## Convert Binary to .hex
```bash
arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd output/nrf52840/bin/ot-cli-ftd.hex
```


## Flash the Dongle
This has to be done using the nRF Connect Programmer.
1. Plug the dongle into your workstation.
Make sure that no other devices are plugged in.
Otherwise you will need to determine which tty shell is connected to the Dongle.
1. Press the Reset Button.
The Red LED should start pulsing slowly.
1. Open the nRF Connect "Programmer" App.
1. "Select Device" (upper left of the window).
1. "Add HEX file" (menu on the top right)
1. "Write" to Dongle (menu on the bottom right)



# Start the Thread Network
[Reference](https://openthread.io/guides/build/commissioning)
1. Start the **COMMISSIONER** device and attach a screen session.
  ```bash
  screen /dev/ttyACM0
  ```
1. Set Thread Network Parameters
  ```
  ifconfig up
  dataset init new
  dataset networkname weisenet
  dataset masterkey 00000000000000000000000000000000
  dataset panid 0x1234
  dataset extpanid 0123456789012345
  dataset channel 17
  dataset
  dataset commit active
  ```
1. Start the Network
  ```
  ifconfig up
  thread start
  ```
1. Start the Commissioner Role
  ```
  commissioner start
  ```
1. Allow any device to join with a passkey:
  ```
  commissioner joiner add * M0untWH!tn3y
  ```



# Joining the Network
Use the **COMMISSIONER** Node to add a **JOINER** device to the weisenet network.
Start by plugging the device into the workstation and accessing the CLI by either:
- `screen /dev/ttyACM0` if this is a regular

Then, follow these steps:
1. Start networking
```
ifconfig up
```
1. scan for the network to see if you can join
```
> scan
__|Joinable | NetworkName        | PAN ID | Ch | XPanID           | HWAddr           | RSSI
__|---------+--------------------+--------+----+------------------+------------------+------
1 |      NO | "weisenet"         | 0x1234 | 17 | 0123456789012345 | 1E7A8FF9ABE8E72A |  -59
```
1. Find EUI of Joiner
```
> eui64
2f57d222545271f1
```
1. From the **COMMISSIONER** device add the new device
```
commissioner joiner add <EUI64> <PSKc>
```
1. From the **JOINER** join the network
```
ifconfig up
joiner start weisenet M0untWH!tn3y
thread start
```
1. Verify that the **JOINER** is part of the network.
From the **JOINER**
```
state   # Should return "child"
rloc16  # Will identify the node in the COMMISSIONER tables
```
From the **COMMISSIONER**
```
router table
child table
```



# References
[Programming the nRF52840 Dongle](https://infocenter.nordicsemi.com/topic/ug_nrf52840_dongle/UG/nrf52840_Dongle/programming.html)

[nRF52840 Dongle User Guide](https://infocenter.nordicsemi.com/pdf/nRF52840_Dongle_User_Guide_v1.1.pdf)

[Nordic Tutorial on Programming Dongle](https://devzone.nordicsemi.com/nordic/short-range-guides/b/getting-started/posts/nrf52840-dongle-programming-tutorial)

[DevZone - replacing stock bootloader](https://devzone.nordicsemi.com/f/nordic-q-a/39185/pca10059-replacing-stock-bootloader-with-adafruit-uf2-using-usb-dfua-signature-i-can-generate-a-zip-file-with-nrfutil-but-what-key-should-i-use-i-tried-to-use-just-a-private-key-and-flash-that-generated-packet-with-nrfutil-bu)

[DevZone - flashing dongle tutorial](https://devzone.nordicsemi.com/nordic/short-range-guides/b/getting-started/posts/nrf52840-dongle-programming-tutorial)

[DevZone - Getting Started with Nordic's Secure DFU Bootloader](https://devzone.nordicsemi.com/nordic/nordic-blog/b/blog/posts/getting-started-with-nordics-secure-dfu-bootloader)

[DevZone - Dongle Programming Tutorial](https://devzone.nordicsemi.com/nordic/short-range-guides/b/getting-started/posts/nrf52840-dongle-programming-tutorial)
