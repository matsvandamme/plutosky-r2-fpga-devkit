---
icon: material/sd
description: Download release v0.1 and write it to a microSD card with the devkit's card writer.
---

# Put the firmware on a card

Download **every file** of release [v0.1](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.1) into one folder. The card needs
**two partitions** (boot files, then Debian), so copying files onto it is not
enough: use the writer.

![The two partitions of the card: a 128 MB FAT boot partition holding BOOT.bin, uImage, devicetree.dtb and uEnv.txt, and a Debian root partition on the rest of the card, which Windows cannot create by itself.](../img/start-card-light.svg#only-light)
![The two partitions of the card: a 128 MB FAT boot partition holding BOOT.bin, uImage, devicetree.dtb and uEnv.txt, and a Debian root partition on the rest of the card, which Windows cannot create by itself.](../img/start-card-dark.svg#only-dark)

=== "Linux"

    With the release files in `~/Downloads`, in a clone of
    [the repository](https://github.com/matsvandamme/plutosky-r2-fpga-devkit):

    ```bash
    # run from: the repo root. DESTROYS everything on the card
    gunzip -c ~/Downloads/debian-rootfs.tar.gz > firmware-modern/debian/rootfs.tar
    ./devkit write-card --dry-run --from ~/Downloads /dev/sdX   # checks the device, writes nothing
    sudo ./devkit write-card --from ~/Downloads /dev/sdX
    ```

    It checks the boot files against the release's `SHA256SUMS` first and
    refuses non-removable disks, but **check the device name yourself**.

    The release card itself was written with the same command into an image
    file (`--image`) and copied to the card; that card booted. Writing
    straight to a card reader has not been done for an R2 yet.

=== "Windows"

    Put `write-card.cmd` from the release in the folder with the other files
    and double-click it. Nothing to install. It is the R1 devkit's writer,
    unchanged; it has **not** been used to make an R2 card yet.
    [How it works, step by step, on the R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/start/write-the-card-windows/):
    use this repository's release, not the one that page links.

**You should see:** the writer end with `Done. The card boots the Debian root by default.`

The release is a **pre-release**: one R2 has booted it, and it has
transmitted at low power only.
[What is tested](../plutosky-r2.md#what-is-tested-and-what-is-not).

The R2's factory firmware is in its QSPI flash. A card does not overwrite it,
and the `BOOT` switch [goes back to it](../plutosky-r2.md#going-back-to-the-factory-firmware).

!!! warning "Never update this board with DFU"
    DFU has bricked units of the R1, and this firmware never uses it. Changing
    firmware means rewriting the card, or `./devkit flash` on a running
    board
    ([put it on the board](../build/flash-your-build.md)).

Rather build it? [Build it yourself](../build/build-from-source.md): no Vivado
needed unless you change the FPGA.

**Next:** [connect and find the board](connect.md).
