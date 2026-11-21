---
icon: material/apple
description: What works from macOS with a PlutoSky R2, what needs the next release's firmware, and what was tested only on the R1 or not at all.
---

# Use the devkit on a Mac

The host tools, the card writer, the container build and the patched SDR++ run
on macOS. The USB network needs one setting on the board, and firmware from the
next release.

This work was done in the R1's repository and carried over. Everything on this
page was tested on 2026-11-21 on one Apple Silicon Mac, with the `/bin/bash`
3.2 that macOS ships and no `sshpass` installed, but **not all of it on an
R2**: each row says which board. Intel Macs were not tested.

| Task | On a Mac | Tested on |
|---|---|---|
| Log in, `status`, `net`, `selftest --ssh`, `flash` | the same commands as on Linux | a PlutoSky R2 |
| Reach the board over the USB cable | switch the board to `ncm` | a PlutoSky R2; needs firmware from the next release |
| Fast TCP (`zc-stream`) at 20 MS/s | a script on the Mac | a PlutoSky R2 |
| Write a card | `./devkit write-card` with `/dev/diskN` | an **R1**, with the R1's release: that card booted. No R2 card was written this way |
| Build the firmware | `./devkit container`, with Docker through Colima | the **R1 repository's** targets. `./devkit container` has not built the R2 from this repository; nothing built this way was booted |
| SDR++ with the patch | `tools/sdrpp/build-macos.sh` | no board: it builds and starts; receiving in the window was not checked |

## Set up the host tools

Flashing and checking a board need `ssh`, `python3` and a way to log in.
macOS has `ssh`; `python3` comes with `xcode-select --install`.

```bash
# run from: the repo root, on the Mac
./devkit doctor --host      # ssh, python3 and a login, nothing about building
./devkit ssh-key            # makes ~/.ssh/fishball; asks for the board's password once (analog)
./devkit status             # what the board runs
```

- **No `sshpass` needed.** `flash`, `net`, `selftest --ssh` and `gpio-check`
  try the key `./devkit ssh-key` makes first, and use `sshpass` only where it
  is installed. Without a key and without `sshpass` they stop and name both
  fixes.
- **Tested from the Mac on a PlutoSky R2:** `ssh-key`, `net`, `net find`,
  `status`, `selftest --ssh`, `flash --kernel-only --no-reboot`, and `flash`
  with the reboot. The files flashed were the release's own, so this shows
  the tool and not a changed file taking effect.
- **`./devkit flash` does not check which board answers.** Pointed at an R1
  it writes R2 files onto it.
- **A macOS job in CI** runs the host tests under bash 3.2.

Tab completion, in zsh or bash:

```bash
# run from: the repo root, on the Mac
eval "$(./devkit completion)"          # this shell
./devkit completion install --rc       # every new shell: adds one line to ~/.zshrc
```

Without `--rc` it prints the line and edits nothing. `--shell bash` writes for
bash, whose startup file on a Mac is `~/.bash_profile`.

## Write a card

!!! warning "Not yet done for an R2"
    The Mac writer has written the R1's release to a card, and that card booted
    in an R1. It has not written a card that an R2 then booted. The R2's
    release card was made with the Linux writer, through an image file
    ([put the firmware on a card](write-the-card.md)).

With every file of release
[v0.1](https://github.com/matsvandamme/plutosky-r2-fpga-devkit/releases/tag/v0.1)
in `~/Downloads`:

```bash
# run from: the repo root, on the Mac. DESTROYS everything on the card
diskutil list external physical                              # names the card: /dev/diskN
./devkit write-card --from ~/Downloads --dry-run /dev/diskN  # every check and the plan; writes nothing
sudo ./devkit write-card --from ~/Downloads /dev/diskN
```

`--from` names the directory holding a downloaded release: `BOOT.bin`,
`uImage`, `devicetree.dtb`, `uEnv.txt` and `debian-rootfs.tar.gz`, and
`SHA256SUMS` if you downloaded it, against which each file is then checked.
Unlike on Linux there is no `gunzip` step: the root is taken from
`debian-rootfs.tar.gz` as it is. The writer is two Python files with no
dependencies (`tools/write_card_mac.py`, `tools/card_image.py`): no Linux
tools and no container.

- **It refuses** internal disks (except a card in the Mac's own SD slot), the
  disk macOS runs from, disks that are not removable, disk images, partitions,
  and anything over 280 GB (`ALLOW_LARGE=1` lifts that one).
- **It checks the whole release before it erases anything**, shows what it
  will erase, and makes you type the disk's name.
- **It reads back everything it wrote** and compares, then reads the four boot
  files out of the FAT partition and compares their SHA-256.
- **`--image FILE`** writes the same layout into a new file, 2048 MB unless
  `--size MB` says otherwise. It needs no `sudo`.

The card differs from one the Linux writer makes in one way: the root
partition is **ext3**, as from the Windows writer, where Linux makes ext4. The
kernel mounts it with its ext4 driver. As on Linux, the root fills the rest of
the card.

**Tested, on the R1:** a 32 GB card in a USB reader, with the R1's release
v2.3: 926 MB written in 81 s and read back identical. That card booted in an
R1 on 2026-11-21.

**Tested, for the R2, without a board:** release v0.1 laid out into an image
file with `--from` and `--image`, every file matching its `SHA256SUMS` and the
image read back identical. That image was not written to a card or booted.

## Reach the board over the USB cable

The board's USB network (the `USB2.0` socket) is RNDIS by default, and macOS
has no RNDIS driver: a Mac sees no network port, and `192.168.2.1` does not
answer. Three things still work in that state:

- **Ethernet:** `ssh root@fishball.local`.
- **The serial console on `DEBUG`:** 115200 baud, the second of the two serial
  ports that socket presents.
- **libiio over USB:** the `usb:` transport needs no network. A scan from the
  Mac listed the boards over USB in either mode.

!!! warning "Needs firmware from the next release"
    The switch below is not in release v0.1. On v0.1 a Mac reaches the board
    over Ethernet.

Switch the board to NCM, which macOS drives:

```bash
# run on: the board (over Ethernet, or the serial console)
fishball-usb-mode ncm       # stores it in the U-Boot environment and applies it now
fishball-usb-mode           # shows what is set and what runs
fishball-usb-mode rndis     # back to the default
```

Everything on the USB cable drops for a few seconds while it switches: the
network, the console on that cable and USB libiio. Ethernet is not touched.

**You should see** a network port named `PlutoSDR (ADALM-PLUTO)` in System
Settings on the Mac. The board hands the Mac `192.168.2.10`, and
`ssh root@192.168.2.1` works.

**Tested** on a PlutoSky R2 with the Mac: with `ncm` set in
`/etc/default/fishball-usb-gadget` the port appeared, the Mac got
`192.168.2.10` from the board's DHCP server, and ping, ssh and
`./devkit selftest` worked over `192.168.2.1`. The setting survived a reboot,
and switching back to `rndis` worked. Not tested on a board: `ecm`, the
`uEnv.txt` line below, and `fishball-usb-mode` writing the U-Boot environment.

| Mode | Windows | Linux | macOS |
|---|---|---|---|
| `rndis` (the default) | yes | yes | no driver |
| `ncm` | Windows 11; Windows 10 has no in-box driver | yes | yes |
| `ecm` | no driver | yes | yes |

With no Ethernet and no console, the mode can be set on the card instead. Put
the card in the Mac's reader and add one line to `uEnv.txt` on its `FISHBOOT`
partition (not tested on a board):

```bash
# run from: anywhere, on the Mac, with the card in a reader
printf '\nusb_ethernet_mode=ncm\n' >> /Volumes/FISHBOOT/uEnv.txt
diskutil eject /Volumes/FISHBOOT
```

A rewritten card loses that line; the U-Boot variable `fishball-usb-mode` sets
does not. All three places the mode is read from, and their order:
[networking](../networking.md#the-usb-network-rndis-ncm-or-ecm).

## Build the firmware

!!! warning "Not yet run for the R2 from this repository"
    `./devkit container` on a Mac built the R1 repository's targets: its boot
    files, its Debian root and its factory firmware with Vivado. The R2's FPGA
    design was built on the same Mac earlier, by hand in the same container
    image: 9 minutes, timing met
    ([how](../build/build-in-a-container.md)). The commands below are what
    this repository's `./devkit container` should do for the R2, and have not
    been run. Nothing built on the Mac was booted on a board.

macOS cannot build the firmware natively, and `./devkit build` says so. The
build runs in a Linux container, with Docker through Colima:

```bash
# run from: anywhere, on the Mac, once
brew install colima docker docker-buildx
colima start --vm-type vz --vz-rosetta --mount-type virtiofs --cpu 8 --memory 16 --disk 120
```

Everything around the FPGA design, with no Vivado:

```bash
# run from: the repo root, on the Mac
./devkit container build-image                    # once: a native arm64 image
./devkit container doctor
./devkit container setup                          # the kernel and boot-loader source
./devkit container build --xsa "$(./firmware-modern/fetch-pinned-xsa.sh)"
./devkit container verify                         # checks the output; not ./devkit verify
./devkit build --rootfs-only                      # the Debian root, on the Mac itself
```

- **The sources live in Docker volumes**, not on the Mac's disk. The boot
  files land on the Mac's disk, in `firmware-modern/output/`.
- **`--rootfs-only` is the one build that runs on the Mac itself.** It drives
  `docker buildx`.
- **Keep the checkout under your home directory:** Colima shares only that
  with its VM.

The FPGA design, with Vivado in an x86-64 image under Rosetta:

```bash
# run from: the repo root, on the Mac
./devkit container build-image --target factory   # once: the x86-64 image
./devkit container doctor --target factory
./devkit container setup --target factory
./devkit container build --target factory         # Vivado -> system_top.xsa
./devkit container build --boot-only --xsa firmware/src/hdl/projects/pluto/system_top.xsa
```

On a Mac `firmware/src/` is one of the Docker volumes, so `system_top.xsa` is
written inside it and is not a file on the Mac's disk. The last command finds
it because the container mounts the same volume at the same path. Installing
Vivado, the times measured for the R1's targets, and what was not proven:
[building in a container](../building-in-a-container.md#macos-on-apple-silicon).

## SDR++ with the patch

```bash
# run from: the repo root, on the Mac
tools/sdrpp/build-macos.sh --install-deps    # without the flag it names the missing Homebrew formulae and stops
~/.cache/fishball-sdrpp/sdrpp                # the launcher it writes
```

It builds SDR++ at the pinned commit with the patch and the DAB+ decoder into
one directory, with no `sudo`. Pick the board from the device menu under the
**PlutoSDR** source: there is no address field, the menu lists what libiio's
scan finds.

**Tested:** it builds, starts, and loads the PlutoSDR source, the audio sink
and the DAB+ decoder. Receiving in the window was not checked, on either
board. Fast TCP (`zc-stream`) was measured from the Mac with a script on a
PlutoSky R2: 20 MS/s arrived in full on both receive ports.

Details: [install the patched SDR++](../radio/install-patched-sdrpp.md).

## Not tested

- An R2 card written by the Mac writer, and booted.
- `./devkit container` building the R2's boot files, Debian root or FPGA
  design from this repository.
- Booting anything built in the container on the Mac.
- `./devkit container install` with AMD's real installer. Vivado came from an
  existing Docker volume.
- Intel Macs, and podman on macOS.
- `./devkit ssh-key` on a Buildroot root (for an R2, the vendor's firmware in
  the QSPI flash), where it saves the key in `/mnt/jffs2` so that it survives
  a reboot.
- `./devkit verify --board` and `gpio-check` from a Mac: neither has been run
  on an R2 from any host.
- Receiving in the SDR++ window.
