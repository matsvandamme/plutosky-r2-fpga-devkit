# firmware-modern: everything around the FPGA design

Linux 6.12 LTS from Analog Devices, the boot loader and a Debian 13 root
filesystem, for the **PlutoSky R2**. It builds around an FPGA design it does
not make: an `.xsa` file from [`firmware/`](../firmware/README.md).

| | |
|---|---|
| kernel | **6.12**, Analog Devices `main`, the R1's configuration plus [`config/r2.config`](config/r2.config) |
| device tree | [`dts/zynq-pluto-sdr-fishball-r2.dts`](dts/zynq-pluto-sdr-fishball-r2.dts), which includes the R1's tree and overrides what the R2 changes |
| userspace | **Debian 13 armhf with systemd**, on the SD card ([`debian/`](debian/README.md)); the same root as the R1's |
| FPGA | always taken from an XSA; an R1 one is refused by its part number |

The `./devkit` commands act on this target by default; `--target modern` below
only says so explicitly.

## Quick start

You need an **XSA**: the FPGA design in one file, the bitstream plus a
description of the hardware around it. This target never runs Vivado, so it
cannot make one, and no release carries an R2 design yet. Build it first:
`./devkit setup --target factory && ./devkit build --target factory`.

```bash
# run from: the repo root
XSA=firmware/src/hdl/projects/pluto/system_top.xsa
./devkit setup --target modern                  # fetch the sources, apply the patches (~0.6 GB)
./devkit build --target modern --xsa "$XSA"     # BOOT.bin, uImage, devicetree.dtb, uEnv.txt
./devkit verify --target modern                 # read the parts back out of BOOT.bin and check them
```

The build needs an ARM Linux cross-compiler (a compiler that runs on your PC and
produces code for the board's ARM cores). Either `gcc-arm-linux-gnueabi` or
`gcc-arm-linux-gnueabihf` works. With neither installed, put `container` in
front and the build runs in a container that has one:
`./devkit container build --target modern --xsa "$XSA"`.

Then put it on the board. **Over the network**, onto a board that is already
running this firmware, with a backup and an md5 check before anything is
swapped. Not run against an R2 yet, and it does not check which board answers:

```bash
# run from: the repo root
./devkit flash --target modern --boot-only      # BOOT.bin
./devkit flash --target modern --kernel-only    # uImage
./devkit flash --target modern --dtb-only       # devicetree.dtb
```

**A whole new card**, from a card reader, including the Debian root:

```bash
# run from: the repo root
./devkit build --target modern --rootfs-only              # debian/rootfs.tar, ~10 min
./devkit write-card --target modern --dry-run /dev/sdX    # checks the device, writes nothing
sudo ./devkit write-card --target modern /dev/sdX         # refuses any non-removable disk
```

`./devkit build --target modern --all --xsa "$XSA"` builds the boot files and
the root in one go. The root is built in its own container, so run that on your
PC rather than inside `./devkit container`.

## What is in this directory

| | |
|---|---|
| `setup.sh`, `build_all.sh`, `verify_output.sh` | what `./devkit setup`, `build` and `verify` run for this target |
| [`patches/`](patches/README.md) | the ten driver patches, most of them transmitter safety |
| `dts/zynq-pluto-sdr-fishball-r2.dts` | the R2's device tree: it includes the next one and overrides Ethernet, two pins and the model |
| `dts/zynq-pluto-sdr-fishball.dts` | the R1's device tree, an overlay on ADI's. The R2's input; change it in the R1 repository too |
| `config/fishball_defconfig`, `config/r2.config` | the R1's kernel configuration, and the one option the R2 adds; `config/fishball.config` explains each option |
| [`debian/`](debian/README.md) | the Debian root filesystem, and `write-card.sh` |
| `verify_dtb.py` | checks a built device tree; CI runs it |
| `dump_context.py` | lists every IIO attribute, to compare two kernels with `diff` |
| `write_card.sh` | puts a kernel on a card from a card reader (see below) |
| `factory-xsa.pin`, `fetch-pinned-xsa.sh` | the slot for a released R2 design. The pin still names the R1's, so the script says there is none and stops |
| `baseline/` | self-test results from an **R1**; nothing has been recorded on an R2 |

## Building the kernel by hand

`build_all.sh` does this for you. By hand:

```bash
# run from: firmware-modern/src/linux
CROSS=arm-linux-gnueabihf-      # or arm-linux-gnueabi-
make ARCH=arm CROSS_COMPILE=$CROSS fishball_defconfig
./scripts/kconfig/merge_config.sh -m .config ../../config/r2.config
make ARCH=arm CROSS_COMPILE=$CROSS olddefconfig
make ARCH=arm CROSS_COMPILE=$CROSS uImage LOADADDR=0x8000 -j$(nproc)
make ARCH=arm CROSS_COMPILE=$CROSS DTC_FLAGS=-@ xilinx/zynq-pluto-sdr-fishball-r2.dtb
```

Use `fishball_defconfig` **with `r2.config` merged over it**. Without the
fragment the kernel is the R1's and the R2 has no Ethernet. **Never
`zynq_pluto_defconfig` on its own**: that is ADI's configuration for an
ADALM-Pluto, which has no Ethernet and no SD card, and a kernel built from it
boots without either. U-Boot, built by hand with a
hard-float compiler, needs `CC="${CROSS}gcc -mfloat-abi=soft"`;
[`docs/troubleshooting.md`](../docs/troubleshooting.md) explains why.

## Rules for changing the kernel

- **Keep the serial console open** (`DEBUG`, 115200 baud). It is the way back
  in when Ethernet does not come up. The USB network at `192.168.2.1` is
  another, from a PC with an RNDIS driver (not a Mac).
- **Ethernet's `phy-mode` is `rgmii-id`.** The vendor's `rgmii-rxid` gives a
  board that receives and cannot send on this kernel; the `.dts` says why.
- **Never ship a kernel without the SD card driver.** Flashing over the network
  works by mounting the SD card on the running board; without it, the only
  fix is a card reader. `verify_dtb.py` checks for it.
- **Check the built `.dtb`**, not just the build log. Device-tree mistakes
  usually build cleanly and boot:
  `python3 firmware-modern/verify_dtb.py firmware-modern/src/linux/arch/arm/boot/dts/xilinx/zynq-pluto-sdr-fishball-r2.dtb`
- **Rebuild `debian/rootfs.tar` after changing `debian/overlay/`.** `write-card`
  refuses a tarball older than the overlay.

## When a kernel does not boot

A kernel that does not boot cannot be replaced over the network, because
flashing needs the board's own kernel running. Take the card out, let your
desktop mount it, and use `write_card.sh`:

```bash
# run from: the repo root, card in a reader
./firmware-modern/write_card.sh             # put the new uImage and devicetree.dtb on the card
./firmware-modern/write_card.sh --restore   # put the *.prev copies back
```

It keeps the first copy of each file it replaces as `*.prev` and never
overwrites it, so the file kept is the last one known to boot.

## Further reading

- [`docs/modern-kernel.md`](../docs/modern-kernel.md): why ADI 6.12 and not
  mainline, the device tree, the IIO comparison with 5.15, throughput and
  reproducible builds.
- [`patches/README.md`](patches/README.md): each driver patch.
- [`debian/README.md`](debian/README.md) and
  [`docs/debian-rootfs.md`](../docs/debian-rootfs.md): the root filesystem.
- [The PlutoSky R2](../docs/plutosky-r2.md): what differs from the R1, and what is tested.
