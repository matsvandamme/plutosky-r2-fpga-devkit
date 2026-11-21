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

<p class="banner" markdown>Booted on one R2 so far. [What is tested and what is not](plutosky-r2.md#what-is-tested-and-what-is-not).</p>

<div class="grid cards" markdown>

-   :material-flag-checkered:{ .lg }

    **[Getting started](start/index.md)**

    Check the board is an R2, build the firmware, write the card, connect.

    <span class="count">6 steps</span>

-   :material-chip:{ .lg }

    **[The PlutoSky R2](plutosky-r2.md)**

    What differs from the R1, the 1.8 V header, and the state of every part of
    this port.

    <span class="count">Reference</span>

-   :material-hammer-wrench:{ .lg }

    **[Build your own firmware](build/index.md)**

    The FPGA design with Vivado; the kernel, drivers and Debian around it.

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

## From nothing to a card

```bash
# run from: the repo root
./devkit setup --target factory && ./devkit build --target factory   # the FPGA design: Vivado 2022.2
./devkit doctor && ./devkit setup                                    # the rest: an ARM cross-compiler
./devkit build --all --xsa firmware/src/hdl/projects/pluto/system_top.xsa
sudo ./devkit write-card /dev/sdX                                    # DESTROYS the card
```

- There is **no release to download yet**. The FPGA half needs Vivado 2022.2;
  [the container](build/build-in-a-container.md) runs it on any Linux.
- After the first card, `./devkit flash` puts a changed kernel or boot file on
  the running board over the network. It does not check which board answers.
- `./devkit ssh-key` first saves typing the published root password.
- The `JP5` header is **1.8 V** and its pin 1 is **5 V**. An R1 cable does not
  carry over: [the header on the R2](plutosky-r2.md#the-sample-locked-gpio-pins-on-the-r2).

## What one board showed

| | |
|---|---|
| Boot to a login prompt | about 23 s, no failed services |
| Radio | found, receives samples |
| Ethernet | 1 Gbit/s, DHCP, answers at `fishball.local` |
| FPGA, default build | 12,717 LUTs, timing met, WNS +0.100 ns |
| Transmit, header pins, 10 MHz input | not tested |

One unit, on 2026-11-20. Every measured radio figure elsewhere on this site
(power, image rejection, throughput) was taken on a PlutoSky **R1** and is
labelled as such where it matters.

## Two sites, two boards

| | This site | [The R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/) |
|---|---|---|
| Board | PlutoSky R2, XC7Z020-CLG484 | PlutoSky R1 / 7020-SDR / Fishball7020, XC7Z020-CLG400 |
| Release to download | none yet | yes |
| Hardware pages (ports, header, schematic) | [one page](plutosky-r2.md), from the vendor's schematic | measured on the board |
| Course | no | Fabric School, 54 lessons |

The [repository](https://github.com/matsvandamme/plutosky-r2-fpga-devkit) has
the code; its [README](../README.md) is the short version of this page.
