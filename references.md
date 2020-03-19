Some high level resources that I found helpful.

# OpenThread documentation


# OpenThread Docker
Use this as the border router.
[DockerHub](https://hub.docker.com/u/openthread/)


# OpenThread Code Labs
The page with all code labs can be found [here](https://openthread.io/guides).
Below are the labs I found useful.

### [Border Router with Docker](https://openthread.io/guides#border_router_with_docker)


### [Hardware Code Lab](https://openthread.io/guides#hardware_codelab)
Dive right into hardware, where you will learn how to:
- Flash OpenThread on Nordic nRF52840 development boards
- Build a real Thread network
- Authenticate Thread nodes with Commissioning
- Use the OpenThread CLI for Multicast and UDP


# Nordic Documentation

### [nRF CLI Documentation](https://infocenter.nordicsemi.com/pdf/nRF5x_Command_Line_Tools_v1.0.pdf)
- documentation for `nrfjprog`


### [Nordic Infocenter](https://infocenter.nordicsemi.com)
Technical documentation published by Nordic.
- Getting started guide
- SDK Guide
- Exhaustive information


### [nRF52480 Dongle User Guide](https://infocenter.nordicsemi.com/pdf/nRF52840_Dongle_User_Guide_v1.1.pdf)


### [nRF52840 Dev Kit USer Guide](https://infocenter.nordicsemi.com/pdf/nRF52840_DK_User_Guide_v1.4.pdf)


## Nordic nRF5 SDK for Thread and Zigbee
### SDK Documentation
[Home for Documentation](https://infocenter.nordicsemi.com/topic/struct_sdk/struct/sdk_thread_zigbee_latest.html) -- If all other links fail then start here.

[Introduction](https://infocenter.nordicsemi.com/topic/sdk_tz_v4.0.0/index.html)

[Getting Started with Thread and Zigbee](https://infocenter.nordicsemi.com/topic/sdk_tz_v4.0.0/thread_zigbee__intro.html)

[API Reference](https://infocenter.nordicsemi.com/topic/sdk_tz_v4.0.0/index.html)


### [Nordic Topology Monitor](https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Thread-topology-monitor)
Used to monitor the toplogy of thread networks in real time.


## Guides
The project relied heavily on two examples published by Nordic Semiconductor.

The border router was built following these [instructions](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.thread_zigbee.v3.0.0/thread_border_router.html)


The other nodes were built following the [NCP/RCP Example](https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.thread_zigbee.v3.0.0/thread_ncp_rcp_example.html)
