---
icon: material/hammer-wrench
description: Build the R2's FPGA design and the firmware around it, check it, put it on the board, then change the kernel, the device tree, the FPGA or the Debian root.
---

# Build your own firmware

Every file on the SD card builds from source, in two halves:

| Half | Command | Needs | Writes |
|---|---|---|---|
| The FPGA design | `./devkit build --target factory` | Vivado 2022.2 | `firmware/src/hdl/projects/pluto/system_top.xsa` |
| The boot loader, kernel, device tree and Debian root, around that design | `./devkit build --xsa FILE` | an ARM cross-compiler | `firmware-modern/output/`, `firmware-modern/debian/rootfs.tar` |

The second half never runs Vivado. Once you have an `.xsa`, a kernel, driver or
device-tree change needs only the second command. No release carries an R2
design yet, so the first `.xsa` is one you build.

## The path

![The build path as five boxes joined by arrows: doctor (can this machine build?), setup (fetch the sources, apply the patches), build (the SD-card files, into output/), verify (is the build sane? with --board: is it running?) and flash (over the network, md5-verified). Each is one ./devkit command, run from the repo root.](../img/build-path-light.svg#only-light)
![The build path as five boxes joined by arrows: doctor (can this machine build?), setup (fetch the sources, apply the patches), build (the SD-card files, into output/), verify (is the build sane? with --board: is it running?) and flash (over the network, md5-verified). Each is one ./devkit command, run from the repo root.](../img/build-path-dark.svg#only-dark)

<div class="grid cards steps" markdown>

-   :material-numeric-1-circle:{ .lg } **[Check your machine can build](check-your-machine.md)**


    `./devkit doctor` answers in about a second.

-   :material-numeric-2-circle:{ .lg } **[Build the firmware and write the card](../start/write-the-card.md)**


    The FPGA design, the files around it, and a card.

-   :material-numeric-3-circle:{ .lg } **[Check the build](verify-the-build.md)**


    `./devkit verify` before it goes on the board.

-   :material-numeric-4-circle:{ .lg } **[Put it on the board](flash-your-build.md)**


    A card, or `./devkit flash` over the network.

</div>

## Change something

<div class="grid cards" markdown>

-   :material-chip:{ .lg .middle } **[Change a kernel driver](change-a-driver.md)**


    Build `uImage` alone, flash it alone.

-   :material-file-tree-outline:{ .lg .middle } **[Change the device tree](change-the-device-tree.md)**


    Build it, audit the built `.dtb`, flash it with `--dtb-only`.

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
kernel and Buildroot root, a build from a released FPGA design with no Vivado,
and a comparison with the factory firmware. They are on
[the R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/build/).
