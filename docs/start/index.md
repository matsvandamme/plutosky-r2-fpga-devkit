---
icon: material/flag-checkered
description: The path from a PlutoSky R2 in its box to one running this firmware, in six short steps.
---

# Start here

From a PlutoSky R2 in its box to one running this firmware: six short steps, one page each.

!!! note "There is no release to download yet"
    Step 3 builds the firmware, and its FPGA half needs Vivado 2022.2. Allow
    an afternoon the first time, most of it downloads.

<div class="grid cards steps" markdown>

-   :material-numeric-1-circle:{ .lg } **[Check you have an R2](right-board.md)**


    The package printed on the Zynq, or one command, tells the R2 from the R1.

-   :material-numeric-2-circle:{ .lg } **[Gather what you need](what-you-need.md)**


    A card, a card reader, two USB-C cables, Ethernet, and a Linux PC that can build.

-   :material-numeric-3-circle:{ .lg } **[Build the firmware and write the card](write-the-card.md)**


    The FPGA design, then the boot files, kernel and Debian root, then the card.

-   :material-numeric-4-circle:{ .lg } **[Connect and find the board](connect.md)**


    Both USB-C sockets for power, Ethernet for the network, `fishball.local`.

-   :material-numeric-5-circle:{ .lg } **[Check what it runs](check-the-firmware.md)**


    Confirm the board booted the firmware you built.

-   :material-numeric-6-circle:{ .lg } **[Before you transmit](before-you-transmit.md)**


    Transmit is untested on the R2. The rules to start from.

</div>

## Then

- **Use the radio:** [capture IQ](../capturing-iq.md), [SDR++](../sdrpp.md),
  [aircraft (ADS-B)](../adsb.md).
- **Change the address or name:** [change the IP address](change-the-address.md).
- **Stop typing the password:** [log in with a key](log-in-with-a-key.md).
- **Go back to the factory firmware:** [set the `BOOT` switch to QSPI](../plutosky-r2.md#going-back-to-the-factory-firmware).
- **Something is wrong:** [troubleshooting](../troubleshooting.md).
