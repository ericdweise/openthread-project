Here is the software I used to provision and interact with the Nordic nRF52840 SoCs.

Note, I am running Ubuntu 18.04 on a Lenovo IdeaPad
```
$ uname -a
Linux ideapad 5.3.0-42-generic #34~18.04.1-Ubuntu SMP Fri Feb 28 13:42:26 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```


# Software Packages

## APT Packages
Packages that can be installed by aptitude:

```bash
sudo apt install -y \
    gcc \
    cmake \
    libgconf-2-4 \
    screen \
    libreadline-dev \
    device-tree-compiler \
    gcc-multilib \
    git \
    wget \
    ninja-build \
    gperf \
    ccache \
    dfu-util \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    xz-utils \
    file \
    make \
    gcc-multilib
```


## Install SEGGER JLink
Download the .deb file from the SEGGER [download page](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack)
```bash
sudo dpkg --force-overwrite -i JLink_Linux_*.deb
```


## GNU ARM Embedded Toolchain
Used to compile binaries.
1. [Download package](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
1. Decompress
  ```bash
  tar -xjvf gcc-arm-none-eabi-*.tar.bz2
  ```
1. Copy binaries to `/opt/gnuarmemb`
  ```bash
  sudo mkdir -p /opt/gnuarmemb/
  sudo cp -r gcc-arm-none-eabi*/ /opt/gnuarmemb
  ```
1. Add binaries to the PATH variable
  ```bash
  # For scripts that define #!/bin/bash
  echo 'PATH="$PATH:/opt/gnuarmemb/bin"' >> ~/.bashrc
  source ~/.bashrc
  ```
1. Test installation: `which arm-none-eabi-gcc`

### Note
In the Linux download instructions are stored in the archive under `share/doc/gcc-arm-none-eabi/readme.txt`.


## nRF Command Line tools
Install `nrfjprog`
1. [Download](https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download#infotabs)
1. decompress
  ```bash
  tar -xzvf nRF-Command-Line-Tools*
  ```
1. Install nRFTools
  ```bash
  sudo dpkg -i --force-overwrite nRF-Command-Line-Tools_*.deb
  ```


## nRF5 SDK for Thread (and Zigbee)
The code that will be flashed to the PCA10059 "Dongle".
1. Download the SDK for *Thread and Zigbee* [Download Page](https://www.nordicsemi.com/Software-and-Tools/Software/nRF5-SDK-for-Thread-and-Zigbee/Download#infotabs)
1. unzip using `unzip`
1. Find your `GNU_VERSION`:
    ```bash
    arm-none-eabi-gcc --version
    ```
1. set values in `components/toolchain/gcc/Makefile.posix`. My file looks like:
```
GNU_INSTALL_ROOT = /home/ender/thread/gcc-arm-none-eabi-9-2019-q4-major/bin/  # Where GNU ARM Embedded Toolchain was installed
GNU_VERSION = 9.2.1
GNU_PREFIX = arm-none-eabi
```

### References
- [SDK Documentation](https://infocenter.nordicsemi.com/topic/struct_sdk/struct/sdk_thread_zigbee_latest.html)


## nRF Connect
Necessary to program the Dongle because the Dongle does not have an onboard debugger.

1. [Download](https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Connect-for-desktop)
1. Make the .AppImage file executable
1. Optional: Copy the file to `/usr/local/bin` to add it to your path. Then you can open it from the program search
1. Open nRF Connect
1. Install the "Getting Started Assistant"
1. Open the "Getting Started Assistant" and follow all the steps therein.
The "variables" on the right hand side should be set to:
  - GnuArmEmb_path: `/opt/gnuamremb`
  - sourcecode_root: `~/repositories`
  - ncs_tag: `v1.2.0` **and** you need to `git checkout v1.2.0` and `west update` in the nrf repo.
1. Install the "Programmer" App (found in the "APPS" tab)


### References
- [User Guide](https://infocenter.nordicsemi.com/pdf/nRF_Connect_Programmer_User_Guide_v1.1.pdf)
- [Nordic InfoCenter](https://infocenter.nordicsemi.com/topic/ug_nc_programmer/UG/nrf_connect_programmer/ncp_introduction.html)


## nrfutil
```bash
pip3 install --upgrade pip
pip3 install nrfutil
python -m pip install nrfutil
```

### Did it work?
```bash
which nrfutil
```


## nrf-udev
Download and install the most recent nrf-udev from [GitHub](https://github.com/nordicsemiconductor/nrf-udev/releases)


## Install Docker
This is required to run the otbr-posix Docker container.
```bash
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

systemctl status docker
sudo docker run hello-world
```



# User Permissions
Make sure your user has permission to access serial port
```bash
sudo adduser $(whoami) dialout
```



# Clone Repositories
```bash
if ! [ -d ~/repositories ]; then
  mkdir ~/repositories/
fi

# Clone openthread
cd ~/repositories
git clone --recursive https://github.com/openthread/openthread.git
cd openthread
./script/bootstrap
./bootstrap

# Clone wpantund
cd ~/repositories
git clone --recursive https://github.com/openthread/wpantund.git
cd wpantund
git checkout full/latest-release

# Read INSTALL.md for up to date instructions
sudo apt install -y dbus libreadline
sudo apt install -y gcc g++ libdbus-1-dev libboost-dev libreadline-dev
sudo apt install -y libtool autoconf autoconf-archive

./bootstrap.sh
./configure --sysconfdir=/etc
make
sudo make install
```
Now reboot your system: `sudo reboot`
