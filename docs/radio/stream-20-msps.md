---
icon: material/speedometer
description: The patched SDR++ and zc-stream give a live 20 MHz-wide view over the network.
---

# Stream 20 MS/s to SDR++

!!! note "Written on the PlutoSky R1"
    This page came with the R1's devkit and has not been redone on an R2. The
    software is the same, so the commands apply; the measured numbers and the
    pictures are the R1's, and the R2's transmit power is unmeasured. A command with
    `--target factory` in it is the exception: here that target builds only
    the FPGA design ([build your own firmware](../build/index.md)).
    [What is tested on the R2](../plutosky-r2.md#what-is-tested-and-what-is-not).

libiio carries about **10 MS/s** for one receiver over the network. The
**Fast TCP** transport carries **20 MS/s**, using 8-bit samples from
`zc-stream` on the board. It needs the [patched SDR++](install-patched-sdrpp.md)
and the Debian root (`firmware-modern/`), which has systemd and a compiler.

![Inside the board, the AD9361 feeds zc-stream on ports 5555 (RX1) and 5556 (RX2), which sends 8-bit samples to SDR++ on the PC. SDR++ sends tuning, gain, rate and RX port to iiod on port 30431, which sets the AD9361.](../img/radio-fasttcp-light.svg#only-light)
![Inside the board, the AD9361 feeds zc-stream on ports 5555 (RX1) and 5556 (RX2), which sends 8-bit samples to SDR++ on the PC. SDR++ sends tuning, gain, rate and RX port to iiod on port 30431, which sets the AD9361.](../img/radio-fasttcp-dark.svg#only-dark)

1. Once: build and install `zc-stream` on the board as a service. It then
   starts at every boot and waits, idle, for SDR++.

    ```bash
    # run from: the repo root, on your PC
    scp -r tools/stream-paths/zc-stream root@192.168.2.1:
    ```

    ```bash
    # run from: the board, in ~/zc-stream
    apt install gcc make libiio-dev
    make && make install
    systemctl enable --now zc-stream
    ```

2. In SDR++, stop, set **Transport** to **Fast TCP, 8-bit (zc-stream)**, pick
   a rate up to 20 MHz, and play. Leave **zc-stream port** at 5555: RX1 comes
   from port 5555 and RX2 from 5556.

| What it costs | |
|---|---|
| **dynamic range** | about 48 dB between the strongest and weakest signal you can see at once, instead of 72 dB. Set the gain so the strongest signal is near the top |
| **the network only** | it needs the board's address (an `ip:` device); over USB, use libiio |
| **one program receives at a time** | another program that tries to stream is refused with "Device or resource busy" |
| **up to 20 MS/s** | **pick 19 MS/s when every sample counts** |

**You should see:** a live view up to 20 MHz wide, as here across the FM band:

![SDR++ at 20 MS/s through zc-stream: 88 to 108 MHz live, centred on 98 MHz, with FM stations near 90.4, 95.7, 98.6, 101.5, 102.1 and 104.7 MHz in the spectrum and waterfall.](../img/sdrpp-fast-20msps.jpg)

The costs in full, and the measurements:
[SDR++](../sdrpp.md#faster-the-fast-tcp-transport) ·
[faster streaming](https://matsvandamme.github.io/fishball7020-fpga-devkit/streaming-paths/).
