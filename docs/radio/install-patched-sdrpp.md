---
icon: material/package-variant-closed
description: The SDR++ build that knows this board's second receiver, its FPGA decimator and the Fast TCP transport.
---

# Install the patched SDR++

!!! note "Written on the PlutoSky R1"
    This page came with the R1's devkit and has not been redone on an R2. The
    software is the same, so the commands apply; the measured numbers and the
    pictures are the R1's, and transmit is untested on the R2. A command with
    `--target factory` in it is the exception: here that target builds only
    the FPGA design ([build your own firmware](../build/index.md)).
    [What is tested on the R2](../plutosky-r2.md#what-is-tested-and-what-is-not).

Stock SDR++ does not know this board's second receiver or its FPGA.
[`tools/sdrpp/`](../../tools/sdrpp/README.md) builds SDR++ with a patch that
adds them to the PlutoSDR source panel.

![The patched PlutoSDR source panel: RX Port, FPGA /8 decimator, Bandwidth, Gain Mode, Gain, Quadrature tracking, RF DC tracking, Baseband DC tracking, Freq. corr. (ppm), and the status lines Board, Firmware and Temp.](../img/sdrpp-source-panel.png){ width="340" }

=== "Arch"

    ```bash
    # run from: tools/sdrpp/
    makepkg -f
    sudo pacman -U sdrpp-git-*-x86_64.pkg.tar.zst
    ```

=== "Another Linux"

    Build SDR++ from source at the same commit with the patch applied:

    ```bash
    # run from: wherever you build software
    git clone https://github.com/AlexandreRouma/SDRPlusPlus.git && cd SDRPlusPlus
    git checkout 8c9f5ee8fe405775bfcd62c8c8f8c0fc928a64af
    patch -p1 < /path/to/plutosky-r2-fpga-devkit/tools/sdrpp/plutosdr-fishball.patch
    cmake -B build -DCMAKE_BUILD_TYPE=Release && make -C build -j"$(nproc)"
    sudo make -C build install
    ```

    Its dependencies are SDR++'s own (`fftw`, `glfw`, `glew`, `volk`, `libiio`,
    `libad9361`, an audio library); its
    [build instructions](https://github.com/AlexandreRouma/SDRPlusPlus#building-on-linux--bsd)
    list them per distribution.

**You should see:** the PlutoSDR source panel with **RX Port**, **FPGA /8
decimator** and **Transport**, as in the picture.

What each control does: [SDR++](../sdrpp.md#this-boards-controls-the-patched-sdr).

**Next:** [stream 20 MS/s to SDR++](stream-20-msps.md) or
[listen to DAB+ radio](listen-to-dab.md).
