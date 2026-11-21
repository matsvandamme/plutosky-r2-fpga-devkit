---
icon: material/stethoscope
description: ./devkit doctor checks the compilers, host packages, disk and sources in about a second.
---

# Check your machine can build

```bash
# run from: the repo root
./devkit doctor                     # the boot files, kernel and Debian root
./devkit doctor --target factory    # the FPGA design: Vivado, the source tree and its patch stamp
```

It checks the compilers, host packages, disk and the sources, in about a
second. Every check is a failure that once cost somebody an hour: run it before
the build, not during.

**You should see** every line say `ok`, as on a machine that can build
everything but the FPGA design:

```
=== preflight ===
  ok     kernel source
  ok     U-Boot source
  ok     get_default_envs.sh
  ok     embeddedsw
  ok     bootgen source
  ok     bare-metal cross (FSBL)
  ok     ARM Linux cross (U-Boot, kernel): arm-linux-gnueabihf-gcc
  ok     make
  ok     flex (U-Boot, kernel)
  ok     bison (U-Boot, kernel)
  ok     mkimage (uImage)
  ok     bc (kernel)
  ok     unzip
  ARM Linux compiler: arm-linux-gnueabihf-gcc
=== preflight passed; nothing built (--preflight-only) ===
```

| Missing | What to install |
|---|---|
| `arm-none-eabi-gcc`, or one without the hard-float multilib (*"uses VFP register arguments"*) | `gcc-arm-none-eabi` + `libnewlib-arm-none-eabi` |
| an ARM Linux cross-compiler | `gcc-arm-linux-gnueabi` (or `arm-linux-gnueabihf-gcc`) |
| `gmp.h` | `libgmp-dev`, `libmpc-dev`, `libmpfr-dev` |
| Vivado 2022.2 | needed for the FPGA design: [install it](install-vivado.md), or use [the container](build-in-a-container.md) |

On Ubuntu 22.04, one line installs the lot:

```bash
# run from: anywhere, on your host
sudo apt update
sudo apt install -y git build-essential bison flex libssl-dev \
    device-tree-compiler u-boot-tools screen python3 \
    libgmp-dev libmpc-dev libmpfr-dev sshpass iverilog libiio-utils \
    gcc-arm-none-eabi libnewlib-arm-none-eabi gcc-arm-linux-gnueabi
```

??? question "On Arch, or another distribution?"
    Arch has no ARM Linux cross-compiler in its official repositories: use Arm's
    prebuilt toolchain ([how, on the R1's site](https://matsvandamme.github.io/fishball7020-fpga-devkit/building/#an-arm-cross-compiler-on-arch)).
    For an FPGA build on anything but Ubuntu 18.04 to 22.04, use
    [the container](build-in-a-container.md).

**Next:** [build it yourself](build-from-source.md).
