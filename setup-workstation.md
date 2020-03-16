Here is the software I used to provision and interact with the Nordic nRF52840 SoCs.

Note, I am running Debian 9.0 on an Acer Cloudbook
```
$ uname -a
Linux REMOVED 4.9.0-12-amd64 #1 SMP Debian 4.9.210-1 (2020-01-20) x86_64 GNU/Linux
```


# Software Packages

## APT Packages
Packages that can be installed by aptitude:
- GCC
- libgconf

```bash
sudo apt install -y gcc libgconf-2-4
```


## GNU ARM Embedded Toolchain
[Download Page](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
1. Download package
2. Unzip using `tar -xjvf`
3. Add binaries to the PATH variable. I added this line to my zshrc file.
  ```bash
  export PATH=$PATH:<INSTALL_DIR>/gcc-arm-none-eabi-*/bin
  ```
4. Test installation with the command `arm-none-eabi-gcc`

### Notes
In the Linux download instructions are stored in `share/doc/gcc-arm-none-eabi/readme.txt`


## nRF Command Line tools _and_ JLink
1. [Download](https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download#infotabs)
2. unzip (`tar -xzvf`)
3. Install JLink
  ```
  sudo dpkg -i --force-overwrite JLink_Linux_V660e_x86_64.deb
  ```
4. Install nRFTools
  ```
  sudo dpkg -i --force-overwrite nRF-Command-Line-Tools_10_6_0_Linux-amd64.deb
  ```


### Configuring SEGGER J-Link software on Linux
(Copied from the [Nordic infocenter](https://infocenter.nordicsemi.com/topic/sdk_tz_v4.0.0/thread_zigbee__intro.html))

To either disable the MSD (Mass Storage Device) or force the HWFC (Hardware Flow Control):

**Note**, the documentation says this is for Windows and Linux, but might only work for one.

1. Connect the NRF52810_XXAA, NRF52833_XXAA, or NRF52840_XXAA board to your machine with a USB cable.
2. Run JLinkExe to connect to the target. For example, for NRF52810_XXAA:
    ```
    JLinkExe -device NRF52810_XXAA -if SWD -speed 4000 -autoconnect 1 -SelectEmuBySN [SEGGER_ID]
    ```
3. Run the following commands:
    - To disable the MSD:
    `MSDDisable`
    - To force the HWFC:
    `SetHWFC Force`
4. Power cycle the board using the on/off Power switch.

To enable the MSD, you can repeat the first four steps above and then run the following command: MSDEnable.


## nRF5 SDK for Thread
1. Download the SDK for *Thread and Zigbee* [Download Page](https://www.nordicsemi.com/Software-and-Tools/Software/nRF5-SDK-for-Thread-and-Zigbee/Download#infotabs)
2. unzip using `unzip`
3. set values in `components/toolchain/gcc/Makefile.posix`. My file looks like:
```bash
GNU_INSTALL_ROOT = /home/ender/thread/gcc-arm-none-eabi-9-2019-q4-major/bin/  # Where GNU ARM Embedded Toolchain was installed
GNU_VERSION = 9.2.1   # get from running arm-none-eabi-gcc --version
GNU_PREFIX = arm-none-eabi
```

### Notes
- [Documentation](https://infocenter.nordicsemi.com/topic/struct_sdk/struct/sdk_thread_zigbee_latest.html)



# User Permissions
Make sure your user has permission to access serial port
```bash
sudo adduser <USER> dialout
```


# Things I read about that haven't been used (yet)

## Segger Embeded Studio
[Download Page](https://www.segger.com/downloads/embedded-studio)


## Segger J-Link
[Download Page](https://www.segger.com/downloads/jlink)
Required for Nordic Topology Monitor



## nRF Sniffer for 802.15.4
For learning and debugging 802.15.4 protocols.
Used to troubleshoot connections in the network.
[Download]()
