---
icon: material/source-branch
description: Build the boot files, kernel and Debian root around the released FPGA design with no Vivado, or build the FPGA design too.
---

# Build it yourself

Three steps: an FPGA design, everything around it, the card. The first is a
download unless you want to change the FPGA.

## 1. The FPGA design

**Without Vivado:** use the design release v0.1 ships. Nothing to do in this
step; step 2 fetches it and checks its hash:

```bash
# run from: the repo root
./firmware-modern/fetch-pinned-xsa.sh    # prints where it put system_top.xsa
```

**With Vivado 2022.2**, to build the design yourself or change it:
[install it](install-vivado.md), or use [the container](build-in-a-container.md)
on a Linux newer than Ubuntu 22.04.

```bash
# run from: the repo root
./devkit setup --target factory     # fetches hdl/ only, ~0.2 GB, and applies the R2 patch series
./devkit build --target factory     # synthesis, implementation, bitstream
```

**You should see** a timing summary with no negative slack, then:

```text
=== Done: .../firmware/src/hdl/projects/pluto/system_top.xsa ===
```

On the machine this port was made on, an Apple Silicon Mac running Vivado
under x86-64 emulation, the build took about 9 minutes and met timing with
+0.100 ns to spare. A design that misses timing still produces a bitstream:
read the summary.

## 2. The boot files, the kernel and the Debian root

```bash
# run from: the repo root
./devkit doctor      # can this machine build? answers in a second
./devkit setup       # the kernel and boot-loader source, ~0.6 GB
./devkit build --all --xsa "$(./firmware-modern/fetch-pinned-xsa.sh)"
# or, with your own design from step 1:
#   ./devkit build --all --xsa firmware/src/hdl/projects/pluto/system_top.xsa
```

`--all` builds the Debian root as well, which needs podman or docker and takes
about ten minutes. It writes:

| File | Where |
|---|---|
| `BOOT.bin`, `uImage`, `devicetree.dtb`, `uEnv.txt` | `firmware-modern/output/` |
| `rootfs.tar` | `firmware-modern/debian/` |

An `.xsa` for the R1's part is refused, so an R1 design cannot be packaged for
an R2 by passing the wrong file.

## 3. The card

![The two partitions of the card: a 128 MB FAT boot partition holding BOOT.bin, uImage, devicetree.dtb and uEnv.txt, and a Debian root partition on the rest of the card, which Windows cannot create by itself.](../img/start-card-light.svg#only-light)
![The two partitions of the card: a 128 MB FAT boot partition holding BOOT.bin, uImage, devicetree.dtb and uEnv.txt, and a Debian root partition on the rest of the card, which Windows cannot create by itself.](../img/start-card-dark.svg#only-dark)

```bash
# run from: the repo root. DESTROYS everything on the card
./devkit write-card --dry-run /dev/sdX        # checks the device, writes nothing
sudo ./devkit write-card /dev/sdX
```

It refuses non-removable disks, but **check the device name yourself**.

!!! note "How far the writer is tested for the R2"
    The release card was made with `write-card --from` into an image file
    (`--image`), which was then copied onto the card, because the build
    machine was a Mac and the writer is a Linux tool. That card booted.
    Writing straight to a card reader on Linux uses the same code and has not
    been done for an R2.

The R2's factory firmware is in its QSPI flash. A card does not overwrite it,
and the `BOOT` switch [goes back to it](../plutosky-r2.md#going-back-to-the-factory-firmware).

!!! warning "Never update this board with DFU"
    DFU has bricked units of the R1, and this firmware never uses it. Changing
    firmware means rewriting the card, or `./devkit flash` on a running board
    ([put it on the board](flash-your-build.md)).

**Next:** [check the build](verify-the-build.md), then [connect and find the board](../start/connect.md).
