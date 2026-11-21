---
icon: material/chip
description: What differs between the PlutoSky R2 and the R1, how this firmware is put together for the R2, and what has and has not been tested.
---

# The PlutoSky R2

The PlutoSky R2 is a different board from the PlutoSky R1 / 7020-SDR, and this
repository builds for the R2 only. **An R1 image does not work on it**: the
board boots Linux and has no radio, no Ethernet and no USB. The R1 has
[its own repository](https://github.com/matsvandamme/fishball7020-fpga-devkit);
the two were one, with a `--rev` switch, until 2026-11-21.

!!! note "Release v0.1, booted on one R2 on 2026-11-21"
    [v0.1](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.1), a pre-release, is built with Vivado 2022.2 (timing met, WNS
    +0.100 ns) and was booted from a card on one PlutoSky R2: the radio is found
    and receives, both transmitters come up muted, Ethernet gets a DHCP address
    at 1 Gbit/s, and USB enumerates. Transmit works on both channels at low
    power through attenuators; its output power is not measured. The `JP5` outputs and the 10 MHz
    input are not tested yet.

## Which board do you have

| | PlutoSky R1 / 7020-SDR | PlutoSky R2 |
|---|---|---|
| Zynq package | XC7Z020-**CLG400** | XC7Z020-**CLG484** |
| Vendor v0.38 firmware version | `v0.38-4-g95aad` | `v0.38-5-g76414` |
| QSPI flash | 16 MB (W25Q128) | 32 MB (W25Q256) |
| Extra socket | none | `10M_IN`, a 10 MHz reference input |
| Repository | [fishball7020-fpga-devkit](https://github.com/matsvandamme/fishball7020-fpga-devkit) | this one |

`iio_attr -C -u ip:192.168.2.1 fw_version` prints the version on the vendor's
firmware. The package is printed on the Zynq itself.

## What differs

Measured on one R2 on 2026-11-18, by reading the processor's pin-mux, clock and
GPIO registers and the device tree under its factory firmware and under an R1
v2.3 image, and checked against the vendor's
[schematic and source](https://github.com/OpenSourceSDRLab/PlutoSky-R2).

| | R1 | R2 |
|---|---|---|
| FPGA pins | CLG400 balls | CLG484 balls: every constraint differs |
| Ethernet PHY | on processor pins MIO 16–27, MDIO on MIO 52/53, address 0 | on FPGA pins, behind a GMII-to-RGMII core; PHY at address 1, core at address 8 |
| MIO bank 501 (MIO 16–53) | 1.8 V | 3.3 V |
| USB PHY reset | MIO 52 | MIO 46 |
| LED | MIO 0 | MIO 7 |
| `JP5` header | 2×10, `3V3_IO1`–`4` at **3.3 V** | 2×12, `EXT_IO` pairs at **1.8 V**, pin 1 is **5 V** |
| Reference | free-running 40 MHz | 40 MHz locked to `10M_IN` by an ADF4001 the FPGA programs |

With an R1 image on an R2 the kernel log shows all three failures:

```text
ad9361 spi0.0: ad9361_spi_check : Unsupported PRODUCT_ID 0xFF
mdio_bus e000b000.ethernet-ffffffff: MDIO device at address 0 is missing.
macb e000b000.ethernet eth0: Could not attach PHY (-19)
```

## Build for the R2

```bash
# run from: the repo root

# 1. The FPGA design (Vivado 2022.2, 10 minutes to over an hour). Fetches hdl/ only, ~0.2 GB.
./devkit setup --target factory
./devkit build --target factory

# 2. The boot files and the kernel, around that design.
#    Skipped step 1? --xsa "$(./firmware-modern/fetch-pinned-xsa.sh)" uses release v0.1's.
./devkit setup
./devkit build --xsa firmware/src/hdl/projects/pluto/system_top.xsa

# 3. A card, with the Debian root.
./devkit build --rootfs-only
sudo ./devkit write-card /dev/sdX
```

| Step | Writes |
|---|---|
| 1 | `firmware/src/hdl/projects/pluto/system_top.xsa` |
| 2 | `firmware-modern/output/`: `BOOT.bin`, `uImage`, `devicetree.dtb`, `uEnv.txt` |
| 3 | `firmware-modern/debian/rootfs.tar`, then the card |

An XSA for the R1's part is refused, so an R1 design cannot be packaged for an
R2 by passing the wrong file. Step by step:
[build it yourself](build/build-from-source.md).

!!! danger "`./devkit flash` does not check which board answers"
    It copies `firmware-modern/output/` to whatever board it finds. Pointed at
    an R1 it writes R2 files onto it, and that board then boots without a
    network. The way back is a card reader.

## Where each part comes from

| Part | R2 source |
|---|---|
| FPGA design | [`firmware/revs/r2/patches/`](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/tree/main/firmware/revs/r2/patches): the vendor's R2 design, then this repo's FPGA patches with R2 pin constraints |
| First-stage boot loader | generated from the R2 XSA, which sets the pin-mux and the 3.3 V bank |
| U-Boot | the R1's source, unchanged |
| Kernel | the R1's, plus `CONFIG_XILINX_GMII2RGMII` ([`config/r2.config`](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/blob/main/firmware-modern/config/r2.config)) |
| Device tree | [`zynq-pluto-sdr-fishball-r2.dts`](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/blob/main/firmware-modern/dts/zynq-pluto-sdr-fishball-r2.dts): includes the R1's and overrides Ethernet, the USB reset pin, the LED pin and the model |
| Debian root | the same |

The factory target builds **only** the FPGA design here. There is no R2 build
of the vendor's 5.15 kernel or of a Buildroot root: the R1 repository has
both, for the R1. The R1's patch series and device tree are still in this
repository because the R2's are layered on them.

## The sample-locked GPIO pins on the R2

The four [sample-locked outputs](https://matsvandamme.github.io/fishball7020-fpga-devkit/tx-gpio-bitmap/)
(the R1's page explains the feature) keep their `JP5` pin
numbers, 7, 9, 11 and 13, so the same cable fits. **The level does not carry
over: 1.8 V on the R2, 3.3 V on the R1.**

| Signal | `JP5` pin | R2 net | R2 ball |
|---|---|---|---|
| `sample_gpio0` | 7 | `EXT_IO3_P` | M19 |
| `sample_gpio1` | 9 | `EXT_IO3_N` | M20 |
| `sample_gpio2` | 11 | `EXT_IO5_P` | M21 |
| `sample_gpio3` | 13 | `EXT_IO5_N` | M22 |

![The PlutoSky R2's JP5 header as two rows of twelve pins, odd numbers in one row and even in the other. Pin 1 is 5 V. Pins 2, 22 and 24 are ground. Pins 7, 9, 11 and 13 are sample_gpio0 to 3, outputs at 1.8 V. The numbering is the vendor's schematic's; nothing has been probed, and pin 1 must be found on the board before connecting anything.](img/hw-jp5-light.svg#only-light)
![The PlutoSky R2's JP5 header as two rows of twelve pins, odd numbers in one row and even in the other. Pin 1 is 5 V. Pins 2, 22 and 24 are ground. Pins 7, 9, 11 and 13 are sample_gpio0 to 3, outputs at 1.8 V. The numbering is the vendor's schematic's; nothing has been probed, and pin 1 must be found on the board before connecting anything.](img/hw-jp5-dark.svg#only-dark)

Pin 1 of the R2's `JP5` is `VCC5V`, and pins 2, 22 and 24 are ground. Do not
plug an R1 wiring harness in without checking it against the R2 schematic.

## What is tested and what is not

| | State |
|---|---|
| A Vivado build of the R2 design | run on 2026-11-19 and again on 2026-11-21, from this repository after it was split from the R1's: the same bitstream both times (sha256 `4d1d372595280900…`), timing met, WNS +0.100 ns, 12,717 LUTs. Two warnings come with the vendor's design: a pin constraint for a `gpio_sync` port that does not exist, and the reference PLL's slow SPI clock, which has no timing constraint |
| The boot loader's generated headers (`firmware/fsbl/generated/`) | made from an R1 design; the build's check accepts them for the R2 XSA, and the pin and memory setup is taken from the XSA itself |
| Booting the result on an R2 | done on one board. Release v0.1, 2026-11-21: 20.7 s to a running system, no failed units, radio probed and receiving, both transmitters at 89.75 dB of attenuation, Ethernet and `fishball.local`, ssh and iiod reachable, `usb0` up. `/boot` read back and matched the release's `SHA256SUMS` |
| Ethernet on Linux 6.12 through the converter core | works at 1 Gbit/s. The device tree says `rgmii-id`, not the vendor tree's `rgmii-rxid`: with the vendor's value the board receives and cannot send |
| Transmit, both channels, at low power through attenuators | tested on one board, 2026-11-21, with `./devkit selftest --loopback` (TX1 to RX1 through 30 dB, TX2 to RX2 through 20 dB) and the stream-end cases of `tools/tx-idle-cases/cases123.sh`. Both transmitters produce a clean tone at 900 MHz (harmonics below -71 dBc, image rejection 52 to 58 dBc after calibration), the attenuator is linear (1.00 dB per dB), and the path is smooth from 100 MHz to 5 GHz. Each transmitter mutes on a clean stop, within 0.1 s of its client being killed, and after 250 ms without data; the transmit gate refuses without an affirmation. The self-test passed in 13 of 14 runs; one run reported a failure that did not repeat and was not identified |
| Transmit power | **not measured.** Never taken above 30 dB of attenuation (the self-test's own floor is 35 dB), and no power meter was used. With the attenuators at their marked values, the loop has about 7.5 dB more gain than the self-test's R1 model expects, the same on both channels, so the R2's transmitter or receiver has more gain than the R1's. Do not assume the R1's +19 dBm |
| The FPGA decimators, both receive channels | checked on one board with the AD9361's built-in test tone and the ÷8 decimator engaged: a 960 kHz tone arrives intact on both channels, and a 3.84 MHz tone, outside the decimated band, is removed on both. The alias measurement of [both receive channels](both-receive-channels.md) has not been redone on an R2 |
| The sample-locked `JP5` outputs | not tested on the R2 |
| `./devkit write-card` | `--from` a release into an image file (`--image`), copied to the card: that card booted. Writing straight to a card reader on Linux has not been done for an R2 |
| `./devkit flash` | run on one board, 2026-11-21: `--dtb-only --no-reboot`, then the default (`BOOT.bin` and `uImage`) with its reboot. Backup, checksum before the swap, `*.prev` copies and the check after the reboot all worked, and the board came back with no failed units, the radio found and both transmitters muted. The files sent were release v0.1's, the ones already on the card, so this shows the mechanism and not a changed file taking effect. It leaves `/boot` mounted read-only until the next reboot. The host was a Mac without `sshpass`, so the login used a key in place of the password |
| `./devkit selftest` | run on one board, 2026-11-21: 24 of 24 checks pass without a cable, including the internal digital loopback. Its baselines and its power model are the R1's |
| `./devkit tx-guard` | works: affirm, status, refusal and revoke, over ssh with a key |
| `verify --board`, `gpio-check`, `clock` | not run on an R2 |
| The USER LED | its pin (MIO 7) is in the device tree; not looked at on the board |
| A release, and a pinned R2 XSA | v0.1; `fetch-pinned-xsa.sh` downloads its `system_top.xsa`, so only an FPGA change needs Vivado |
| The Windows card writer, `write-card.cmd` | in the release, unchanged from the R1's; not used for an R2 card |
| A second R2, an AD9363 unit, a unit with a power amplifier | none tried: one board has run this |
| The 10 MHz reference input | the FPGA programs the PLL as the vendor's design does; nothing here reads its lock state |

## Power, USB and the vendor's manual

The vendor's [PlutoSky R2 user manual](https://blog.opensourcesdrlab.com/archives/plutosky-R2)
says a board that is not detected may be short of power, and to connect both
USB-C sockets. On the test board, one freeze and one restart were seen with
only `DEBUG` connected and none after `USB2.0` was connected as well; that
fits the manual, and is not proven to be the cause.

The USB network is RNDIS, as on the R1. macOS has no driver for it, so from a
Mac use Ethernet or the serial console on `DEBUG` (115200 baud, the second of
the two serial ports the socket presents). Do not send that console a serial
BREAK: on the test board it flooded the console with NUL bytes.

On link-up the kernel prints `unable to generate target frequency: 125000000
Hz`. On the test board the link worked at 1 Gbit/s regardless; the message has
not been looked into.

## Going back to the factory firmware

The R2's factory firmware is in its QSPI flash and a card does not overwrite
it. Power off, set the `BOOT` switch to QSPI (`1 0`), power on.
