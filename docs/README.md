# Documentation map

Every page in `docs/`, grouped by what you want to do. This is the PlutoSky
**R2**'s documentation; the [top-level README](../README.md) says where the port
stands. The PlutoSky R1 / 7020-SDR has
[its own](https://matsvandamme.github.io/fishball7020-fpga-devkit/).

## The board, and getting it running

| Page | Read it when you want to |
|---|---|
| [The PlutoSky R2](plutosky-r2.md) | know what differs from the R1, where each part of the build comes from, and what is and is not tested |
| [Start here](start/index.md) | go from a board in its box to one running this firmware, in six steps |
| [Hardware and I/O](hw/index.md) | know the header voltage, the pins this firmware drives, and where the schematic is |
| [How it works](how-it-works.md) | understand what a build produces and why, assuming nothing (written for the R1) |
| [Transmitter safety](transmitter-safety.md) | transmit anything at all. Transmit is untested on the R2; the R1's measurements and rules |
| [Reaching the board and changing its IP address](networking.md) | log in, fix the address (mostly the R1's Buildroot firmware; the Debian parts apply) |
| [Flashing the board](flashing.md) | the R1's flashing reference, with what differs on the R2 at the top |
| [Troubleshooting](troubleshooting.md) | fix a build or a board that misbehaves |

## Building and changing the firmware

| Page | Read it when you want to |
|---|---|
| [Build your own firmware](build/index.md) | build the FPGA design and the firmware around it, then change one part |
| [Building in a container](building-in-a-container.md) | build with Vivado on a host newer than Ubuntu 22.04 |
| [The modern kernel](modern-kernel.md) | know why Linux 6.12 from Analog Devices, and what is patched |
| [Why the modern target runs Debian](debian-rootfs.md) | know why the root is Debian, and what it had to keep |
| [The Debian root reference](debian-root-reference.md) | know what each boot unit and overlay setting on the board does |

## Using the radio

Written on the R1. The software is the same on the R2; the measured numbers
are not the R2's, and transmit is untested there.

| Page | Read it when you want to |
|---|---|
| [Use the radio](radio/index.md) | pick a short task page |
| [Using this board in your own project](your-own-project.md) | choose where your code lives: your PC, the board, the kernel or the FPGA |
| [Capturing IQ](capturing-iq.md) | record samples with metadata and a dropped-sample check |
| [Using SDR++ with this board](sdrpp.md) | listen and watch a band in SDR++ |
| [Aircraft overhead: ADS-B](adsb.md) | `./devkit adsb`: aircraft decoded live from 1090 MHz; receive only |
| [Other SDR tools](other-sdr-tools.md) | use SDR++, inspectrum, URH, Maia SDR or pyadi-iio instead of GNU Radio |
| [MATLAB](matlab.md) | use MATLAB or Simulink |
| [Both receive channels](both-receive-channels.md) | use RX1 and RX2 with the FPGA decimator on |
| [Cyclic buffers and triggers](cyclic-buffers.md) | replay a waveform from the board's memory, or play it once per trigger |
| [Watching a sweep live: chirp-view](chirp-view.md) | sweep TX1 and watch RX1 receive it |
| [The automation server](automation.md) | script repeatable bench measurements against a server on the board |
| [The board in a Claude Code pane](claude-code-pane.md) | watch the board from Claude Code (`./devkit claude-pane start`); reads only |
| [Claude and the radio: the MCP server](mcp-server.md) | let Claude tune, scan and capture through the sibling Fishball7020-mcp server |

## Not here: the R1's pages

These describe the R1's hardware or report measurements taken on it, and live
on [the R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/):
what is on the board, GPIO, the sample-locked outputs, the USER LED, the vendor
schematic, measured performance, the modulation gallery, throughput, the stock
block design, the FM channelizer, the factory (5.15, Buildroot) build,
building from a released FPGA design, provenance, and the Fabric School course.

## Elsewhere in the repository

- [`firmware/revs/r2/`](../firmware/revs/r2/README.md): the R2's FPGA patches.
- [`firmware-modern/`](../firmware-modern/README.md) and [`firmware/`](../firmware/README.md): the two halves of the build.
- [`examples/`](../examples/README.md): GNU Radio and MATLAB examples, written on the R1.
- [`tools/selftest/`](../tools/selftest/README.md): what the self-test checks. Its baselines are the R1's.

These pages are also published, searchable, at
<https://matsvandamme.github.io/plutosky-r2-fpga-devkit/> (built by
[`mkdocs.yml`](../mkdocs.yml)). CI checks every link with
`python3 docs/check_links.py` and builds the site with `mkdocs build --strict`.
