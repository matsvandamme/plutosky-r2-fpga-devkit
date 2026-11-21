# AGENTS.md — plutosky-r2-fpga-devkit

Editable, rebuildable firmware for the **PlutoSky R2** (Zynq **XC7Z020-CLG484** + **AD9361**) two-channel SDR: FPGA design + bootloader + kernel + Debian root, patch-based. Public, **GPL-2.0**. `README.md` and `CONTRIBUTING.md` are the source of truth.

**This repository is the R2's only.** The PlutoSky R1 / 7020-SDR lives in `matsvandamme/fishball7020-fpga-devkit`, which this one was copied from on 2026-11-21 (shared history; `git cherry-pick` works between them). An image for one board does not work on the other.

## The build driver: `./devkit`
- `./devkit setup --target factory` then `./devkit build --target factory` — the **FPGA design only** (Vivado 2022.2) → `firmware/src/hdl/projects/pluto/system_top.xsa`. There is no 5.15 kernel or Buildroot build here.
- `./devkit doctor`, `./devkit setup`, `./devkit build --xsa firmware/src/hdl/projects/pluto/system_top.xsa` — boot loader, Linux 6.12 and device tree around that design → `firmware-modern/output/`. `--all` adds the Debian root.
- `sudo ./devkit write-card /dev/sdX` — a whole card. `./devkit flash` — boot files onto a running board (does **not** check which board answers).
- `./devkit sim --mutate` — HDL simulation; run it if you touch HDL and **add a testbench**.
- Release **v0.2** (a pre-release, booted on one R2) ships the card files and `system_top.xsa`, which is v0.1's design unchanged; `firmware-modern/fetch-pinned-xsa.sh` fetches that XSA from v0.1 (the pin), so only an FPGA change needs Vivado. A release is made by hand: tag, build at the tag, take `debian-rootfs.tar.gz` from a `verify-rootfs.yml` run on the tag (never from a docker export), boot it on an R2, then publish.

## What is the R1's and still here
`firmware/patches/` (the R1 series), `firmware-modern/dts/zynq-pluto-sdr-fishball.dts` and `config/fishball_defconfig` are the R2's **inputs**: `firmware/revs/r2/patches/` replaces two FPGA patches and adds one, the R2 device tree `#include`s the R1's, and `config/r2.config` is merged over the R1's kernel configuration. Keep those shared files identical to the R1 repository's; put R2 differences in the R2 files. Every board-dependent name is in `firmware/scripts/rev.sh` (`--rev r2` is still accepted; `--rev r1` is refused with a pointer).

## Honesty about state
One R2 has booted this (2026-11-20): boot, receive, Ethernet and USB enumeration work. Transmit works on both channels at low power through attenuators (selftest loopback, mute cases), but **transmit power is unmeasured, and the JP5 outputs (1.8 V, pin 1 = 5 V), and the 10 MHz input are untested on an R2.** `./devkit flash` was run on one R2, from a Mac, with the files already on the card. The Mac work (2026-11-21) came from the R1 repository: the host tools, the USB `ncm` switch with DHCP and zc-stream at 20 MS/s were tested on an R2; release v0.2 was booted on the R2 from a card written on a Mac with `./devkit write-card`, its boot files built with `./devkit container` on an Apple Silicon Mac around v0.1's XSA (the R2's FPGA design and Debian root were not built that way), and `fishball-usb-mode ncm` was run on it. Still untested on an R2: the Windows card writer, NCM or ECM with a Windows PC, `ecm` mode, the `uEnv.txt` line, and the `nofail` path on a board with a missing flash. `docs/plutosky-r2.md` has the table; update it when you test something. Most pages under `docs/radio/` were written and measured on an R1 and say so. Never present an R1 measurement as the R2's.

## Conventions
- **Everything is a patch.** Change a file, then `git diff -- path > firmware/revs/r2/patches/00NN-what-it-does.patch` (or `firmware-modern/patches/`), and re-run the matching `setup`. Don't commit materialised sources.
- R2 pins come from the vendor schematic (`OpenSourceSDRLab/PlutoSky-R2`, `hardware/PlutoSky-R2_Schematic.pdf`), never from R1 material.
- CI (`verify-patches.yml`, `verify-modern.yml`) checks patches apply and audits the built device tree — **it cannot run Vivado**. The bar for hardware changes is "I booted it on an R2 and it works," stated in the PR.
- Keep GPL-2.0 headers; respect `NOTICE`/`LICENSE`.
- Docs are MkDocs (`mkdocs.yml`): `python3 docs/check_links.py`, `python3 docs-site/style_check.py docs/`, `mkdocs build --strict`.
- Don't commit large captures/binaries (`*.sigmf-data`, build outputs).
