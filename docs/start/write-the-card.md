---
icon: material/sd
description: Download release v0.2 and write it to a microSD card with the devkit's card writer, on Linux or macOS.
---

# Put the firmware on a card

Download **every file** of release [v0.2](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.2) into one folder. The card needs
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

    Release v0.1's card was written with the same command into an image
    file (`--image`) and copied to the card; that card booted. Writing
    straight to a card reader on Linux has not been done for an R2 yet.

=== "macOS"

    With the release files in `~/Downloads`:

    ```bash
    # run from: the repo root. DESTROYS everything on the card
    diskutil list external physical                              # names the card: /dev/diskN
    ./devkit write-card --from ~/Downloads --dry-run /dev/diskN  # checks the disk and the release, writes nothing
    sudo ./devkit write-card --from ~/Downloads /dev/diskN
    ```

    No `gunzip` line here: the Mac writer takes `debian-rootfs.tar.gz` from
    the folder as it is. It needs only the Python that macOS's developer tools
    bring (`xcode-select --install`). It checks every file against the
    release's `SHA256SUMS` first and refuses internal, non-removable and boot
    disks, but **check the disk name yourself**. The root partition is ext3,
    as from the Windows writer.

    Release v0.2's card was written this way and booted in the R2 on
    2026-11-21: the one R2 card the Mac writer has made. Before that, a 32 GB
    card with the R1's release v2.3, written on a Mac, booted in an R1.
    More: [use the devkit on a Mac](use-a-mac.md#write-a-card).

=== "Windows"

    Put `write-card.cmd` from the release in the folder with the other files
    and double-click it. Nothing to install. It is the R1 devkit's writer,
    unchanged; it has **not** been used to make an R2 card yet.
    [How it works, step by step, on the R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/start/write-the-card-windows/):
    use this repository's release, not the one that page links.

**You should see:** the Linux writer end with `Done. The card boots the Debian root by default.`
The macOS and Windows writers end with their own check passing,
`OK: all ... read back identical`.

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
