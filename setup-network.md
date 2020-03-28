How to configure devices and set up the network



# Routing Candidate Nodes
- Use the nRF52840 Dongle
- Every node will be put programmed as a Full Thread Device (FTD)
- Here I use the 'cli' example provided by OpenThread

## References
- [Programming the nRF52840 Dongle](https://infocenter.nordicsemi.com/topic/ug_nrf52840_dongle/UG/nrf52840_Dongle/programming.html)
- [nRF52840 Dongle User Guide](https://infocenter.nordicsemi.com/pdf/nRF52840_Dongle_User_Guide_v1.1.pdf)
- [Nordic Tutorial on Programming Dongle](https://devzone.nordicsemi.com/nordic/short-range-guides/b/getting-started/posts/nrf52840-dongle-programming-tutorial)

## Compile
1. Change to the OpenThread Repository
```bash
cd ~/repositories/openthread/
```
1. Compile a USB, Joiner node
```bash
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 JOINER=1 USB=1 BOOTLOADER=USB
```

## Convert Binary to .hex
```bash
arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd output/nrf52840/bin/ot-cli-ftd.hex
```

## Flash with nRF Connect
Flashing has to be done using the
1. Plug the dongle into your workstation.
Make sure that no other devices are plugged in.
Otherwise you will need to determine which tty shell is connected to the Dongle.
1. Press the Reset Button.
The Red LED should start pulsing slowly.
The following steps assume it is `/dev/ttyACM0`
1. Open the nRF Connect "Programmer" App.
1. "Select Device" (upper left of the window).
It can take a few minutes for the Programmer to read the device memory.
Let it sit until the
1. "Add HEX file" (menu on the right)

## Operation
1. plug into usb power and wait...?


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

1. Plug the Dev. Kit into workstation using microusb cable. Use the USB port on the **short end** of the Dev. Kit
1. Switch the poser supply to "VDD" on the Dev. Kit (SW9)
1. Switch the Dev Kit "ON"
1. Find the Device Serial Number on the top of the Dev Kit.
    It is the 9 digit number printed on the MCU.
1. Flash the compiled .hex file using nrfjprog.
```bash
nrfjprog -f nrf52 -s <DEVICE_SERIAL_NUMBER> --chiperase --program  output/nrf52840/bin/ot-ncp-ftd.hex --reset
```

## Unplug the Dev Kit
You will need to plug it back in **using the other microusb port** later.


# Border Router
- Docker container running on workstation
- Instructions and overview can be found [here](https://openthread.io/guides/border-router/docker)
- Instructions on running Docker and NCP as full Base Station found [here]()

## References
- [OpenThread Border Router Guide](https://openthread.io/guides/border-router/docker).
    Use the Physical NCP instructions
- [Running the Docker Container](https://openthread.io/guides/border-router/docker/run)

## Steps
1. Pull Container
```bash
sudo docker pull openthread/otbr:latest
```

1. Attach Dev Kit
Plug the microusb cable into the **long side** of the Dev Kit.
Make sure that the serial port attaches correctly:
```bash
ls -l /dev/tty* | grep ACM
```
should return
```
crw-rw----  1 root  dialout 166,     0 Mar 19 16:34 ttyACM0
```
If there is no output then the board isn't connecting over USB.
If it is a directory you need to unplug the device and delete `/dev/ttyACM0`.
NOTE: On other platforms the serial shell might not be `ttyACM[0-9]`

1. Run
To connect the NCP you mount the correct shell to the Docker container as a shared volume.
The shell should be something like `/dev/ttyACM[0-9]`, but might be different on different distros.
For example, on my Debian 9.0 computer the shell is `/dev/ttyS[0-9]`.
```bash
sudo docker run --sysctl "net.ipv6.conf.all.disable_ipv6=0 \
    net.ipv4.conf.all.forwarding=1 \
    net.ipv6.conf.all.forwarding=1" \
    -p 8080:80 --dns=127.0.0.1 -it --rm \
    --volume /dev/ttyACM0:/dev/ttyACM0 \
    --privileged openthread/otbr \
    --ncp-path /dev/ttyACM0
```

1. Did It Work?
If you see the following printed to STDOUT:
```
otbr-agent[221]: Border router agent started.
```
Then it worked!
Do not close the terminal or stop the Docker instance.
