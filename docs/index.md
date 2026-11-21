---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# What do you want to do?

Firmware and guides for the **PlutoSky R2**: a Zynq XC7Z020-CLG484 and an
AD9361 radio, with the FPGA design, the boot loader, Linux 6.12 and a Debian
root all built from source. The PlutoSky R1 / 7020-SDR is a different board:
[its site is here](https://matsvandamme.github.io/fishball7020-fpga-devkit/).

<label class="hero-search" for="__search">:material-magnify: Search: build, write the card, Ethernet, SDR++, header pins…</label>

</div>

<p class="banner" markdown>Release [v0.1](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.1) is out, booted on one R2. [What is tested and what is not](plutosky-r2.md#what-is-tested-and-what-is-not).</p>

<div class="grid cards" markdown>

-   :material-flag-checkered:{ .lg }

    **[Getting started](start/index.md)**

    Check the board is an R2, download the release, write the card, connect.

    <span class="count">6 steps</span>

-   :material-chip:{ .lg }

    **[The PlutoSky R2](plutosky-r2.md)**

    What differs from the R1, the 1.8 V header, and the state of every part of
    this port.

    <span class="count">Reference</span>

-   :material-hammer-wrench:{ .lg }

    **[Build your own firmware](build/index.md)**

    Kernel, drivers and Debian with no Vivado; the FPGA design with it.

    <span class="count">9 articles</span>

-   :material-radio-tower:{ .lg }

    **[Use the radio](radio/index.md)**

    Capture IQ, SDR++, aircraft, MATLAB, your own code. Written on the R1; the
    software is the same.

    <span class="count">20 articles</span>

-   :material-alert-octagon-outline:{ .lg }

    **[Transmit safely](start/before-you-transmit.md)**

    Transmit is not tested on the R2 yet. The rules to start from.

    <span class="count">4 rules</span>

-   :material-wrench-outline:{ .lg }

    **[Troubleshooting](troubleshooting.md)**

    Known problems by symptom, each with its cause and fix.

    <span class="count">By symptom</span>

</div>

## From the release to a card

Download every file of [v0.1](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.1) into one folder, then, in a clone of the
repository on Linux:

```bash
# run from: the repo root
gunzip -c ~/Downloads/debian-rootfs.tar.gz > firmware-modern/debian/rootfs.tar
sudo ./devkit write-card --from ~/Downloads /dev/sdX    # DESTROYS the card
```

- To build it yourself instead, no Vivado needed:
  `./devkit build --all --xsa "$(./firmware-modern/fetch-pinned-xsa.sh)"`.
  Only [changing the FPGA](build/add-fpga-logic.md) needs Vivado 2022.2.
- After the first card, `./devkit flash` puts a changed kernel or boot file on
  the running board over the network. It does not check which board answers.
- `./devkit ssh-key` first saves typing the published root password.
- The `JP5` header is **1.8 V** and its pin 1 is **5 V**. An R1 cable does not
  carry over: [the header on the R2](plutosky-r2.md#the-sample-locked-gpio-pins-on-the-r2).

## What one board showed

| | |
|---|---|
| Boot to a running system | about 21 s, no failed services |
| Radio | found, receives samples |
| Ethernet | 1 Gbit/s, DHCP, answers at `fishball.local` |
| FPGA, default build | 12,717 LUTs, timing met, WNS +0.100 ns |
| Transmit, header pins, 10 MHz input | not tested |

One unit, on 2026-11-20 and 2026-11-21. Every measured radio figure elsewhere on this site
(power, image rejection, throughput) was taken on a PlutoSky **R1** and is
labelled as such where it matters.

## Two sites, two boards

| | This site | [The R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/) |
|---|---|---|
| Board | PlutoSky R2, XC7Z020-CLG484 | PlutoSky R1 / 7020-SDR / Fishball7020, XC7Z020-CLG400 |
| Release to download | [v0.1](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.1), a pre-release | yes |
| Hardware pages (ports, header, schematic) | [one page](plutosky-r2.md), from the vendor's schematic | measured on the board |
| Course | no | Fabric School, 54 lessons |

The [repository](https://github.com/matsvandamme/plutosky-r2-fpga-devkit) has
the code; its [README](../README.md) is the short version of this page.
