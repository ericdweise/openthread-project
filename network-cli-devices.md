# Setting Up Devices
## Dev Kit
This device will be the Commissioner.
This is the simplest way, right now, to compile and flash the comissioner.
```bash
cd ~/repositories/openthread/
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 USB=1 COMMISSIONER=1
arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd WEISENET-DK-commissioner.hex
nrfjprog -f nrf52 --chiperase --program  WEISENET-DK-commissioner.hex --reset
```

## Dongles
These instructions will build the Commissioner, Joiners, and the NCP onto the Dongle
Before any code is compiled make sure that the Bootloader is not overwritten:
```bash
cd ~/repositories/openthread/
sed -i '/FLASH (rx) : ORIGIN/c\  FLASH (rx) : ORIGIN = 0x1000, LENGTH = 0xdb000' examples/platforms/nrf528xx/nrf52840/nrf52840.ld
sed -i '/RAM (rwx) :  ORIGIN/c\  RAM (rwx) :  ORIGIN = 0x20000008, LENGTH = 0x3fff8' examples/platforms/nrf528xx/nrf52840/nrf52840.ld
```

### Commissioner and Joiner Devices
For the sake of simplicity these devices will be identical.

1. Compile
  ```bash
  make -f examples/Makefile-nrf52840 clean
  make -f examples/Makefile-nrf52840 USB=1 BOOTLOADER=USB COMMISSIONER=1 JOINER=1
  arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd WEISENET-Dongle-FTD.hex
  ```
1. Flash the Dongles using nRF Connect.
  It is possible to use nrfutil but that involves some steps that I don't fully understand yet.
  Maybe in the future I will work that out.

### Network Co-Processor (NCP)
This device has special compilation parameters.
1. Compile
  ```bash
  make -f examples/Makefile-nrf52840 clean
  make -f examples/Makefile-nrf52840 USB=1 BOOTLOADER=USB BORDER_AGENT=1 BORDER_ROUTER=1 COMMISSIONER=1 UDP_FORWARD=1
  arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-ncp-ftd WEISENET-Dongle-NCP.hex
  ```
1. Flash the Dongle using nRF Connect.
1. Physically label this Dongle to distinguish it from the CLI devices.



# Setting up the Network
## Starting the Network
Use these commands from any of the devices set ups as a Commissioner.
1. Attach to the OpenThread CLI using `screen`.
  Note, the serial port `/dev/ttyACM0` might be different on different computers.
  ```bash
  screen /dev/ttyACM0
  ```
1. Bring up networking
  ```bash
  ifconfig up
  ```
1. Set OpenThread network parameters
  ```
  dataset init new
  dataset networkname weisenet
  dataset panid 0xE41C
  dataset channel 17
  dataset commit active
  ```
1. Start the OpenThread network and wait for a few seconds
  ```
  thread start
  ```
1. Start commissioner and wait until active
  ```
  commissioner start
  ```
1. Allow any device with a Pre-Shared Key to join the network
  ```
  commissioner joiner add * MTWH1TN3Y
  ```

## Joining the network
Complete these steps on *all* devices that are not the NCP.
1. Attach to the OpenThread CLI using `screen`.
  Note, the serial port `/dev/ttyACM0` might be different on different computers.
  ```bash
  screen /dev/ttyACM0
  ```
1. Bring up networking
  ```bash
  ifconfig up
  ```
1. Set the PAN ID
  ```
  panid 0xE41C
  ```
1. Discover the network using `scan`.
  Wait until weisenet appears in the output.
  Make sure there is a `1` in the `J` column for weisenet.
  ```
  scan
  ```
1. Join the network.
  Wait until the output returns `Join success`.
  ```
  joiner start MTWH1TN3Y
  ```
1. Start thread
  ```
  thread start
  ```
1. Make `state` returns `router`
  ```
  state
  ```


# Running the Experiments
