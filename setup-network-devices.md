## Base Station
- Docker container running on workstation

### Build
1. step 1

### Run
1. step 1


## NRC
- nRF52840 Development Kit
- Must be attached to workstation using USB during operation

### Compile
```bash
cd ~/repositories/openthread
make -f examples/Makefile-nrf52840 clean
make -f examples/Makefile-nrf52840 JOINER=1 USB=1
```

### Flash Development Kit
Note: The device serial number is a 9 digit number printed at the bottom of the MCU.
```bash
nrfjprog -f nrf52 -s <DEVICE_SERIAL_NUMBER> --chiperase --program  ~/repositories/openthread/output/nrf52840/bin/ot-ncp-ftd --reset
```

### Operation
1. step 1


## Routing Candidate Nodes
- nRF52840 Dongle

### Compile
1. step 1

### Flash
1. step 1

### Operation
1. step 1
