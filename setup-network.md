How to configure devices and set up the network


# Network Co-Processor (NCP) Using the Dev. Kit
- nRF52840 Development Kit
- Must be attached to workstation using USB during operation
- Works as the Commissioner for the Border Router
- Using the NCP provided by the OpenThread Repository

## References
- Follows instructions for the OpenThread [Build and Flash NCP](https://openthread.io/guides/border-router/build#build-and-flash-ncp)
- [Instructions for compiling](https://openthread.io/platforms/co-processor/firmware)

## Compile
Based on the OpenThread implementation.
```bash
cd ~/repositories/openthread
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 BORDER_AGENT=1 BORDER_ROUTER=1 COMMISSIONER=1 UDP_FORWARD=1 USB=1 LINK_RAW=1
```

## Convert Binary to .hex
```bash
arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-ncp-ftd output/nrf52840/bin/ot-ncp-ftd.hex
```

## Flash Development Kit

1. Plug the Dev. Kit into workstation using microusb cable. Use the USB port on the short end of the Dev. Kit
1. Switch the poser supply to "VDD" on the Dev. Kit (SW9)
1. Switch the Dev Kit "ON"
1. Find the Device Serial Number on the top of the Dev Kit.
    It is the 9 digit number printed on the MCU.
1. Flash the compiled .hex file using nrfjprog.
```bash
nrfjprog -f nrf52 -s <DEVICE_SERIAL_NUMBER> --chiperase --program  output/nrf52840/bin/ot-ncp-ftd.hex --reset
```


# Base Station
- Docker container running on workstation

## References
- [OpenThread Border Router Guide](https://openthread.io/guides/border-router/docker/run).
    Use the Physical NCP instructions

## Build
1. step 1

## Attach NCP

## Run
1. step 1



# Routing Candidate Nodes
- nRF52840 Dongle

## Compile
1. step 1
```bash
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 JOINER=1 USB=1 BOOTLOADER=USB
```

## Convert Binary to .hex
```bash
# is right??? arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd output/nrf52840/bin/ot-cli-ftd.hex
```

## Flash
```bash
nrfjprog -f nrf52 --chiperase --program output/nrf52840/bin/ot-cli-ftd.hex --reset
```

## Operation
1. plug into usb power and wait...
