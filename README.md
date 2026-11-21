# PlutoSky R2 Devkit

**Editable, rebuildable firmware for the PlutoSky R2: the FPGA design, the boot loader, Linux 6.12 and a Debian root, from source.**

<p align="center">
  <a href="https://matsvandamme.github.io/plutosky-r2-fpga-devkit/"><img src="https://img.shields.io/badge/docs-matsvandamme.github.io-4069FF" alt="The documentation site"></a>
  <img src="https://img.shields.io/badge/board-PlutoSky%20R2%20%C2%B7%20XC7Z020--CLG484%20%2B%20AD9361-blue" alt="Board: PlutoSky R2, Zynq XC7Z020-CLG484 + AD9361">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--2.0-lightgrey" alt="License: GPL-2.0"></a>
  <a href="../../actions/workflows/verify-patches.yml"><img src="https://github.com/matsvandamme/plutosky-r2-fpga-devkit/actions/workflows/verify-patches.yml/badge.svg" alt="Verify patches CI status"></a>
  <a href="../../actions/workflows/verify-modern.yml"><img src="https://github.com/matsvandamme/plutosky-r2-fpga-devkit/actions/workflows/verify-modern.yml/badge.svg" alt="Verify the modern firmware CI status"></a>
</p>

> **This repository is for the PlutoSky R2 only.** The PlutoSky R1 / 7020-SDR / Fishball7020 is a different board with its own repository: **[fishball7020-fpga-devkit](https://github.com/matsvandamme/fishball7020-fpga-devkit)**. An image for one does not work on the other: an R1 image on an R2 boots with no radio, no Ethernet and no USB.

## Where this stands

Booted on **one** PlutoSky R2, on 2026-11-20. This is a young port: read the table before you rely on it.

| | State on the R2 |
|---|---|
| FPGA design builds with Vivado 2022.2, timing met (WNS +0.100 ns) | **done** |
| boots to Debian 13 / Linux 6.12 from the SD card, about 23 s to a login | **works** |
| radio found, receives samples | **works** |
| Ethernet: 1 Gbit/s, DHCP, `fishball.local` | **works** |
| USB: the board enumerates on a PC | **works** (the host was a Mac, which has no driver for its network function) |
| transmit | **not tested** |
| the four sample-locked header pins, the 10 MHz reference input | **not tested** |
| `./devkit write-card`, `./devkit flash`, `./devkit selftest` on an R2 | **not run** on an R2 |
| a release to download | **none yet**: you build it, and the FPGA half needs Vivado |

The full list, with how each item was checked: [what is tested and what is not](docs/plutosky-r2.md#what-is-tested-and-what-is-not).

## Is this your board?

| | PlutoSky R2 (this repository) | PlutoSky R1 / 7020-SDR ([the other one](https://github.com/matsvandamme/fishball7020-fpga-devkit)) |
|---|---|---|
| Zynq package, printed on the chip | XC7Z020-**CLG484** | XC7Z020-**CLG400** |
| Extra socket on the case | `10M_IN`, a 10 MHz reference input | none |
| Vendor v0.38 firmware version | `v0.38-5-g76414` | `v0.38-4-g95aad` |
| QSPI flash | 32 MB (W25Q256) | 16 MB (W25Q128) |

More ways to tell, and what differs inside: [the PlutoSky R2](docs/plutosky-r2.md).

> **Not the official Analog Devices / OpenSourceSDRLab repository.** This is an independent port. The vendor's own schematic and source are at [OpenSourceSDRLab/PlutoSky-R2](https://github.com/OpenSourceSDRLab/PlutoSky-R2).

## Build it

There is no release, so the first step is the FPGA design, which needs **Vivado 2022.2** (on Ubuntu 18.04 to 22.04, or in the container `./devkit container` builds for you). Everything after it needs only an ARM cross-compiler.

```bash
# run from: wherever you want the devkit to live (e.g. ~)
git clone https://github.com/matsvandamme/plutosky-r2-fpga-devkit.git
cd plutosky-r2-fpga-devkit

# 1. The FPGA design. Fetches hdl/ only (~0.2 GB); Vivado runs 10 minutes to over an hour.
./devkit setup --target factory
./devkit build --target factory          # -> firmware/src/hdl/projects/pluto/system_top.xsa

# 2. The boot files, the kernel and the Debian root, around that design (~0.6 GB of source).
./devkit doctor                          # can this machine build?
./devkit setup
./devkit build --all --xsa firmware/src/hdl/projects/pluto/system_top.xsa

# 3. A whole card, from a card reader. DESTROYS the card.
sudo ./devkit write-card /dev/sdX
```

Read the timing summary step 1 prints: a design that misses timing still produces a bitstream.

Then put the card in, set the **`BOOT`** switch to SD (both sliders away from `ON`), connect **both** USB-C sockets for power, and plug in Ethernet. Step by step: **[start here](docs/start/index.md)**.

```bash
# run from: the repo root
ssh root@fishball.local    # password: analog
./devkit ssh-key           # never type the password again: then just `ssh fishball`
./devkit status            # what is built, what the board is running
```

After the first card, `./devkit flash --kernel-only` puts a changed kernel on the running board over the network. It does not check which board answers: do not point it at an R1.

> [!CAUTION]
> ### Before you ever transmit
> Transmit has **not been tested on the R2** with this firmware, and nothing here has measured its transmitter. The rules written for the R1 are the ones to start from: the receive port of an AD9361 board survives about **+2.5 dBm**, a board with a power amplifier puts out far more than that, so **never loop TX back to RX without at least 20 dB of attenuation**, and never transmit at power into an open port. The devkit's transmitting tools refuse to run until you record `./devkit tx-guard affirm`. Read [transmitter safety](docs/transmitter-safety.md) first.

## The header is 1.8 V

The R2's `JP5` header is 2×12 pins at **1.8 V**, and **pin 1 is 5 V**. The R1's is 2×10 at 3.3 V. A cable or a circuit made for an R1 does not carry over: check it against the [vendor schematic](https://github.com/OpenSourceSDRLab/PlutoSky-R2) first. [The pins this firmware drives](docs/plutosky-r2.md#the-sample-locked-gpio-pins-on-the-r2).

## 📚 Documentation

**[matsvandamme.github.io/plutosky-r2-fpga-devkit](https://matsvandamme.github.io/plutosky-r2-fpga-devkit/)**

| I want to… | Start at |
|---|---|
| get a board running | **[Start here](docs/start/index.md)** |
| know what differs from the R1, and what is tested | **[The PlutoSky R2](docs/plutosky-r2.md)** |
| change the kernel, a driver, the device tree or the FPGA | **[Build your own firmware](docs/build/index.md)** |
| receive, use SDR++ or Python | **[Use the radio](docs/radio/index.md)** |
| fix a problem | **[Troubleshooting](docs/troubleshooting.md)** |

The guides under *Use the radio* were written and measured on the **R1**. The software is the same on both boards, so the commands apply; the measured numbers, the photographs and anything about transmit power are the R1's until someone measures an R2. The R1's hardware pages (its ports, its header, its schematic) are not copied here; they are on the [R1's documentation site](https://matsvandamme.github.io/fishball7020-fpga-devkit/hw/), as is the [Fabric School course](https://matsvandamme.github.io/fishball7020-fpga-devkit/course/).

## How it relates to the R1 repository

This repository started as a copy of [fishball7020-fpga-devkit](https://github.com/matsvandamme/fishball7020-fpga-devkit) and shares its history up to 2026-11-21. What the R2 changes sits on top of the R1's files, which are still here because they are its inputs:

| Part | Where the R2's comes from |
|---|---|
| FPGA design | [`firmware/patches/`](firmware/patches/) (the R1 series) with [`firmware/revs/r2/patches/`](firmware/revs/r2/README.md) replacing three of them: the vendor's R2 design, then this devkit's FPGA changes on R2 pins |
| First-stage boot loader | generated from the R2 design's `.xsa`, which sets the pin-mux and the 3.3 V bank |
| U-Boot | the R1's source, unchanged |
| Kernel | the R1's configuration plus [`config/r2.config`](firmware-modern/config/r2.config) |
| Device tree | [`zynq-pluto-sdr-fishball-r2.dts`](firmware-modern/dts/zynq-pluto-sdr-fishball-r2.dts), which includes the R1's and overrides Ethernet, two pins and the model |
| Debian root | the same |

`./devkit help` lists every command and `./devkit help <command>` explains one; `./devkit completion install` adds tab completion.

## 💭 Feedback and contributing

Something not working on your R2? [Open an issue](../../issues/new/choose) and say what you see: one board has run this, so a second report is worth a lot. Contributions are welcome: [CONTRIBUTING.md](CONTRIBUTING.md). People who shaped the firmware this builds on are in [CONTRIBUTORS.md](CONTRIBUTORS.md).

The repository's own scripts, patches and documentation are GPL-2.0; downloaded upstream sources keep their licenses, and Vivado and AMD IP are proprietary ([LICENSE](LICENSE)). [`.claude/skills/goal-creator/`](.claude/skills/goal-creator/VENDORED.md) is a vendored third-party skill under MIT.
