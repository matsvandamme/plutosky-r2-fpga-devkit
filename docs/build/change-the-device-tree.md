---
icon: material/file-tree-outline
description: Build the device tree, audit the built .dtb, and flash it with --dtb-only.
---

# Change the device tree

The R2's tree is `firmware-modern/dts/zynq-pluto-sdr-fishball-r2.dts`. It
`#include`s the R1's, `zynq-pluto-sdr-fishball.dts`, and overrides what the R2
changes: Ethernet, the USB reset pin, the LED pin and the model. The R1's is in
turn an overlay on ADI's `zynq-pluto-sdr.dtsi`. Put an R2 difference in the R2
file; a change to the shared file belongs in the R1 repository too.

![ADI's zynq-pluto-sdr.dtsi, which describes an ADALM-Pluto, and this board's overlay zynq-pluto-sdr-fishball.dts, which states only where this board differs, compile into devicetree.dtb. verify_dtb.py runs 16 checks on the built file, and flash --dtb-only puts it on the running board.](../img/build-devicetree-light.svg#only-light)
![ADI's zynq-pluto-sdr.dtsi, which describes an ADALM-Pluto, and this board's overlay zynq-pluto-sdr-fishball.dts, which states only where this board differs, compile into devicetree.dtb. verify_dtb.py runs 16 checks on the built file, and flash --dtb-only puts it on the running board.](../img/build-devicetree-dark.svg#only-dark)

```bash
# run from: firmware-modern/src/linux
CROSS=arm-linux-gnueabi-      # or arm-linux-gnueabihf-
make ARCH=arm CROSS_COMPILE=$CROSS DTC_FLAGS=-@ xilinx/zynq-pluto-sdr-fishball-r2.dtb
# The rename is yours to do: tools/flash.sh looks for the literal name
# devicetree.dtb and aborts if it is missing.
cp arch/arm/boot/dts/xilinx/zynq-pluto-sdr-fishball-r2.dtb ../../output/devicetree.dtb
```

```bash
# run from: the repo root
python3 firmware-modern/verify_dtb.py firmware-modern/output/devicetree.dtb   # stdlib only
./devkit flash --dtb-only
```

`./devkit setup` copies both `.dts` files into the kernel tree; after editing
one in `firmware-modern/dts/`, run it again or copy the file across yourself.

**Check the built `.dtb`, not the `.dts`.** Most of what lands in it comes from
the dtsi, and two mistakes found here built and booted fine:

| Mistake | Effect |
|---|---|
| a `memory@0` node beside the dtsi's `memory` node | the kernel gets two memory sizes; `dtc` only warns "duplicate unit-address" |
| no `adi,channels` | the DMA driver fails to probe on this board's 2018-era FPGA cores, and nothing streams |

`verify_dtb.py` runs 16 checks, including that every node the factory tree
enables is still enabled, and the R2's tree passes all of them. CI also builds
the R2's tree and fails if it differs from the R1's anywhere but the five
things the board changes. Keep
`adi,tx-attenuation-mdB = 89750` in the AD9361 node: it is the safety setting
that makes the transmitter come up at −89.75 dB.

!!! warning "Ethernet's `phy-mode` is `rgmii-id`, on purpose"
    The vendor's tree says `rgmii-rxid`. With that value on this kernel the
    board receives and cannot send: measured, and explained in the `.dts`.

!!! warning "The device tree must match the bitstream"
    Change what the FPGA contains and the description may need to change too.

More: [the modern kernel](../modern-kernel.md#the-device-tree).
