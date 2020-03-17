Notes about flashing the nRF52480 Dev Kit and Dongle

Before anything here is done you must set up your workstation. See `setup-workstation.md` for instructions.

# Compiling Examples Provided in the SDK
Try to compile one of the examples to make sure I've set everything up right.
To do this follow these steps:
1. Change directory to one of the examples
  ```bash
  cd examples/thread/cli/ftd/usb/pca10056/blank/armgcc/
  ```
2.  Compile the code using `make`
  ```bash
  make  # yeah, that's all
  ```
3. Connect the **Dev. Kit** to your computer using a microusb cable connected to the port on the short side of the board, next to the coin battery. Make sure the power source switch is set to "VDD" and then switch the device to "on"
4. Copy the compiled HEX file to the device:
  ```bash
  nrfjprog -f NRF52 --chiperase --program _build/nrf52840_xxaa.hex --reset
  ```

### Did it work?
How do you tell?
