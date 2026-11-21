---
icon: material/toolbox-outline
description: A card, a card reader, two USB-C cables, Ethernet, a Linux PC that can build, and an attenuator before anything transmits.
---

# Gather what you need

Six things. The two USB-C cables and the Ethernet cable are what differ from
most small radios.

| | Why |
|---|---|
| **A microSD card, 4 GB or more** | the firmware lives on it. Use a new card and keep any card that came with the board as it is |
| **A card reader** | to write the card |
| **Two USB-C cables** | the vendor's manual says a board that is not detected may be short of power, and to connect **both** sockets. The test board froze once and restarted once with only `DEBUG` connected, and not since |
| **An Ethernet cable to your router** | the network route that is tested with release v0.1. The USB network is RNDIS, which Linux and Windows have a driver for and macOS does not; from the next release the board can be switched to `ncm`, which macOS drives |
| **A Linux PC or a Mac** | the devkit's card writer and its build are Linux tools. [On a Mac](use-a-mac.md) the host tools run as they are and were run on the R2; the Mac card writer has only written the R1's release, and the container build has not built the R2 from this repository. A Windows PC can write the release card with `write-card.cmd`, which has not been tried for an R2 yet |
| **A 20 dB attenuator**, before any transmit port is cabled to a receive port | an AD9361 receive input survives about +2.5 dBm; a transmitter with a power amplifier puts out far more |

The `DEBUG` socket is also the serial console: 115200 baud, the second of the
two serial ports it presents. It works before the network does, which makes it
the way to see why a board does not boot.

!!! danger "Before anything transmits"
    Read [before you transmit](before-you-transmit.md). The R2 has
    transmitted at low power through attenuators only, and its output power
    is not measured.

**Next:** [put the firmware on a card](write-the-card.md).
