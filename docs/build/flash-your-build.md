---
icon: material/upload-network-outline
description: A card from a card reader, which is how the test board was updated, or ./devkit flash over the network, which has not been run on an R2.
---

# Put it on the board

Two ways: a card from a card reader, or over the network to a board that is
already running this firmware.

!!! warning "Over the network is untested on the R2"
    `./devkit flash` is the R1 repository's tool, unchanged, and has not been
    run against an R2. The test board's files were replaced from a card
    reader. It also does not check **which** board answers: pointed at an R1
    it writes R2 files onto it.

## From a card reader

A whole new card, with the Debian root: `sudo ./devkit write-card /dev/sdX`
([build it yourself](build-from-source.md#3-the-card)).

To replace only the boot files on a card that already has this layout, copy
`BOOT.bin`, `uImage`, `devicetree.dtb` and `uEnv.txt` from
`firmware-modern/output/` onto its first (FAT) partition, keeping a copy of
the ones you replace. That is how the test board was updated.

## Over the network

```bash
# run from: the repo root
./devkit flash              # BOOT.bin + uImage
./devkit flash --boot-only  # BOOT.bin only: an FPGA design change
./devkit flash --kernel-only
./devkit flash --dtb-only
```

It backs up the current files, checks the md5 of each new file on the board
before swapping it in, unmounts cleanly and reboots. The previous files stay
on the card as `*.prev` and on your disk in `firmware/.flash-backups/<stamp>/`.
After it, `./devkit verify --board` compares the card with your build.

![Four rows, each from what you changed, to the file that changes, to how it reaches the board. The FPGA (HDL, block design): BOOT.bin, flash --boot-only or copy it onto the card. The kernel (a driver, the config): uImage, flash --kernel-only or copy it onto the card. The device tree: devicetree.dtb, flash --dtb-only or copy it onto the card. The Debian root (the overlay, packages): rootfs.tar, write-card, a new card.](../img/build-change-map-light.svg#only-light)
![Four rows, each from what you changed, to the file that changes, to how it reaches the board. The FPGA (HDL, block design): BOOT.bin, flash --boot-only or copy it onto the card. The kernel (a driver, the config): uImage, flash --kernel-only or copy it onto the card. The device tree: devicetree.dtb, flash --dtb-only or copy it onto the card. The Debian root (the overlay, packages): rootfs.tar, write-card, a new card.](../img/build-change-map-dark.svg#only-dark)

The Debian root cannot be flashed over the network: write a new card
([rebuild the Debian root](rebuild-the-debian-root.md)).

!!! danger "Never flash with DFU"
    DFU has bricked units of the R1, and it cannot replace `BOOT.bin` at all.

??? question "The new files do not boot?"
    Put the previous files back from a card reader, and watch the serial
    console on `DEBUG` (115200 baud) to see how far it gets. The factory
    firmware in the QSPI flash is untouched by all of this:
    [going back to it](../plutosky-r2.md#going-back-to-the-factory-firmware).
