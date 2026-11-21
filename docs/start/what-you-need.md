---
icon: material/toolbox-outline
description: A card, a card reader, two USB-C cables, Ethernet, a Linux PC that can build, and an attenuator before anything transmits.
---

# Gather what you need

| | Why |
|---|---|
| **A microSD card, 4 GB or more** | the firmware lives on it. Use a new card and keep any card that came with the board as it is |
| **A card reader** | to write the card |
| **Two USB-C cables** | the vendor's manual says a board that is not detected may be short of power, and to connect **both** sockets. The test board froze once and restarted once with only `DEBUG` connected, and not since |
| **An Ethernet cable to your router** | the network route that is tested. The USB network is RNDIS, which Linux and Windows have a driver for and macOS does not |
| **A Linux PC** | the devkit's build and its card writer are Linux tools. Vivado 2022.2 for the FPGA half runs on Ubuntu 18.04 to 22.04, or in [the container](../build/build-in-a-container.md) on any Linux |
| **About 60 GB of disk** | Vivado with only the Zynq-7000 family is about 30 GB installed, and its installer downloads as much again |
| **A 20 dB attenuator**, before any transmit port is cabled to a receive port | an AD9361 receive input survives about +2.5 dBm; a transmitter with a power amplifier puts out far more |

The `DEBUG` socket is also the serial console: 115200 baud, the second of the
two serial ports it presents. It works before the network does, which makes it
the way to see why a board does not boot.

!!! danger "Before anything transmits"
    Read [before you transmit](before-you-transmit.md). Transmit has not been
    tested on the R2.

**Next:** [build the firmware and write the card](write-the-card.md).
