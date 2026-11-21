---
icon: material/check-decagram-outline
description: Confirm the board booted the firmware you built, and that it is the R2's.
---

# Check what it runs

Log in and look:

```bash
# run on the board
cat /proc/device-tree/model   # FISH Ball PlutoSDR R2 (Z7020/AD9361)
cat /etc/os-release           # first line: PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
uname -r                      # 6.12.0-...
grep fishball_ /boot/uEnv.txt
```

| You see | It means |
|---|---|
| the model ending `R2 (Z7020/AD9361)` | this firmware's device tree |
| `fishball_rev=r2` and `fishball_fpga=xc7z020clg484-2, Vivado 2022.2` in `uEnv.txt` | boot files built here, for the R2's part |
| Debian 13 and kernel `6.12.0-…` | the firmware on the card, not the one in the flash |
| Buildroot and `fw_version` `v0.38-5-g76414` | the vendor's factory firmware: the `BOOT` switch is on QSPI, or the card did not boot |

An image for the R1 fails on this board with `Unsupported PRODUCT_ID 0xFF` from
the radio and `Could not attach PHY (-19)` from Ethernet. Neither should be in
the kernel log:

```bash
# run on the board
dmesg | grep -E 'PRODUCT_ID|Could not attach PHY'   # prints nothing on a good build
ip -br addr show eth0                                # an address from your router
```

From a clone, `./devkit status` says the same in one line without logging in.
A release card reads `modern` and its release, `v0.1`; a build between
releases reads `modern (Debian)` with its `git describe`.

**Built it yourself and the board is on the network?** Compare the card with
your build:

```bash
# run from: the repo root
./devkit verify --board
```

`verify --board` has not been run against an R2; the checks above are the ones
that were.

**Next:** [before you transmit](before-you-transmit.md).
