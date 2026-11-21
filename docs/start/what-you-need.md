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
| **A Linux PC** | the devkit's card writer and its build are Linux tools. A Windows PC can write the release card with `write-card.cmd`, which has not been tried for an R2 yet |
| **A 20 dB attenuator**, before any transmit port is cabled to a receive port | an AD9361 receive input survives about +2.5 dBm; a transmitter with a power amplifier puts out far more |

The `DEBUG` socket is also the serial console: 115200 baud, the second of the
two serial ports it presents. It works before the network does, which makes it
the way to see why a board does not boot.

!!! danger "Before anything transmits"
    Read [before you transmit](before-you-transmit.md). Transmit has not been
    tested on the R2.

**Next:** [put the firmware on a card](write-the-card.md).
