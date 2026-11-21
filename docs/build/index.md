---
icon: material/hammer-wrench
description: Build the R2's FPGA design and the firmware around it, check it, put it on the board, then change the kernel, the device tree, the FPGA or the Debian root.
---

# Build your own firmware

Every file on the SD card builds from source, in two halves:

| Half | Command | Needs | Writes |
|---|---|---|---|
| The FPGA design | `build --target factory` | Vivado 2022.2 | `system_top.xsa` |
| The boot loader, kernel, device tree and Debian root, around that design | `build --all --xsa FILE` | an ARM cross-compiler | the four boot files and `rootfs.tar` |

Both are `./devkit` commands; [build it yourself](build-from-source.md) has the
full paths. The second half never runs Vivado. Once you have an `.xsa`, a kernel, driver or
device-tree change needs only the second command. Release v0.1 ships an
`.xsa` (v0.2 carries the same one), which `./firmware-modern/fetch-pinned-xsa.sh` downloads and checks, so
Vivado is needed only to change the FPGA design.

## The path

![The build path as five boxes joined by arrows: doctor (can this machine build?), setup (fetch the sources, apply the patches), build (the boot files and the Debian root), verify (is the build sane?) and write-card (a whole card, from a card reader). Each is one ./devkit command, run from the repo root.](../img/build-path-light.svg#only-light)
![The build path as five boxes joined by arrows: doctor (can this machine build?), setup (fetch the sources, apply the patches), build (the boot files and the Debian root), verify (is the build sane?) and write-card (a whole card, from a card reader). Each is one ./devkit command, run from the repo root.](../img/build-path-dark.svg#only-dark)

<div class="grid cards steps" markdown>

-   :material-numeric-1-circle:{ .lg } **[Check your machine can build](check-your-machine.md)**


    `./devkit doctor` answers in about a second.

-   :material-numeric-2-circle:{ .lg } **[Build it yourself](build-from-source.md)**


    Around the released FPGA design, or your own; then a card.

-   :material-numeric-3-circle:{ .lg } **[Check the build](verify-the-build.md)**


    `./devkit verify` before it goes on the board.

-   :material-numeric-4-circle:{ .lg } **[Put it on the board](flash-your-build.md)**


    A card from a card reader, or `./devkit flash` over the network.

</div>

## Change something

<div class="grid cards" markdown>

-   :material-chip:{ .lg .middle } **[Change a kernel driver](change-a-driver.md)**


    Build `uImage` alone, replace it alone.

-   :material-file-tree-outline:{ .lg .middle } **[Change the device tree](change-the-device-tree.md)**


    Build it, audit the built `.dtb`, replace it alone.

-   :material-memory:{ .lg .middle } **[Add your own logic to the FPGA](add-fpga-logic.md)**


    Simulate first, delete the Vivado project, rebuild the design.

-   :material-docker:{ .lg .middle } **[Build with Vivado in a container](build-in-a-container.md)**


    For a Linux newer than Ubuntu 22.04.

-   :material-download-box-outline:{ .lg .middle } **[Install Vivado 2022.2](install-vivado.md)**


    Through the container, or on an Ubuntu host.

-   :material-debian:{ .lg .middle } **[Rebuild the Debian root](rebuild-the-debian-root.md)**


    After a change to the root's overlay, then a new card.

</div>

## Reference

[The PlutoSky R2](../plutosky-r2.md#where-each-part-comes-from): where each
part of the build comes from ·
[building in a container](../building-in-a-container.md) ·
[the modern kernel](../modern-kernel.md) ·
[why Debian](../debian-rootfs.md) ·
[the Debian root reference](../debian-root-reference.md).

The R1 repository documents things this one does not build: the vendor's 5.15
kernel and Buildroot root, and a comparison with the factory firmware. They
are on
[the R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/build/).
