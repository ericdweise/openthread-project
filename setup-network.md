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


# Border Router
- Docker container running on workstation
- Instructions and overview can be found [here](https://openthread.io/guides/border-router/docker)
- Instructions on running Docker and NCP as full Base Station found [here]()

## References
- [OpenThread Border Router Guide](https://openthread.io/guides/border-router/docker).
    Use the Physical NCP instructions
- [Running the Docker Container](https://openthread.io/guides/border-router/docker/run)

### Pull Container
```bash
sudo docker pull openthread/otbr:latest
```

### Build container
This is necessary because the wpantund.conf file is incorrect in the

Make sure to run this command from the same directory as this MarkDown file.

```bash
sudo docker build -f DockerfileOtbr -t my-otbr .
```

### Run
To connect the NCP you mount the correct shell to the Docker container as a shared volume.
The shell should be something like `/dev/ttyACM[0-9]`, but might be different on different distros.
For example, on my Debian 9.0 computer the shell is `/dev/ttyS[0-9]`.
To find which device file to use run `ls /dev/tty*` twice, once with the NCP plugged in and once with it removed.

```bash
sudo docker run --sysctl "net.ipv6.conf.all.disable_ipv6=0 \
    net.ipv4.conf.all.forwarding=1 \
    net.ipv6.conf.all.forwarding=1" \
    -p 8080:80 --dns=127.0.0.1 -it --rm \
    --volume /dev/ttyACM0:/dev/ttyACM0 \
    --privileged openthread/otbr \
    --ncp-path /dev/ttyACM0
```



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
