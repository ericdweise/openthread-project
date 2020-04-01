# Setting Up Devices
## Dev Kit
This device will be the Commissioner.
```bash
cd ~/repositories/openthread/
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 USB=1 COMMISSIONER=1
arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd WEISENET-DK-commissioner.hex
nrfjprog -f nrf52 --chiperase --program  WEISENET-DK-commissioner.hex --reset
```

## Dongles
These devices will be the NCP and the Joiners.

1. Make sure that the Dongles bootloader is not overwritten.
  ```bash
  sed -i '/FLASH (rx) : ORIGIN/c\  FLASH (rx) : ORIGIN = 0x1000, LENGTH = 0xdb000' examples/platforms/nrf528xx/nrf52840/nrf52840.ld
  sed -i '/RAM (rwx) :  ORIGIN/c\  RAM (rwx) :  ORIGIN = 0x20000008, LENGTH = 0x3fff8' examples/platforms/nrf528xx/nrf52840/nrf52840.ld
  ```
1. Compile
  ```bash
  cd ~/repositories/openthread/
  make -f examples/Makefile-nrf52840 clean
  make -f examples/Makefile-nrf52840 USB=1 BOOTLOADER=USB JOINER=1
  arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-ncp-ftd WEISENET-Dongle-NCP.hex
  arm-none-eabi-objcopy -O ihex output/nrf52840/bin/ot-cli-ftd WEISENET-Dongle-joiner.hex
  ```
1. Flash the Dongles using NRF Connect
  Make sure to label the NCP dongle when it is flashed.

# Setting up the Network



# Running the Experiments
