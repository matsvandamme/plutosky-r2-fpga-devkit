---
icon: material/docker
description: Run the Vivado build in a pinned Ubuntu 22.04 container, so your host distribution does not matter.
---

# Build with Vivado in a container

Vivado 2022.2 runs only on Ubuntu 18.04 to 22.04. `./devkit container` runs the
build in a pinned Ubuntu 22.04 container, so your distribution does not matter.

```bash
# run from: the repo root
./devkit container build-image                       # once, ~3 min
./devkit container doctor --target factory           # the same checks as ./devkit doctor, inside
./devkit container setup --target factory            # hdl/ and the R2 patch series, ~0.2 GB
./devkit container build --target factory            # Vivado -> system_top.xsa
```

!!! note "How the R2's design was actually built"
    In this container image, started by hand under Docker on an Apple Silicon
    Mac, with Vivado running under x86-64 emulation: about 9 minutes, timing
    met. `./devkit container` itself has not been run for an R2 build, on a
    Linux host (where it uses podman) or on a Mac. Two things that mattered
    there: Vivado waits for ever unless its standard input is closed
    (`</dev/null`), which `./devkit build --target factory` now does, and
    `tools/env-vivado.sh`, not Vivado's own `settings64.sh`, supplies the old
    libraries it needs.

**Build in the container; flash from the host:** `flash`, `selftest`,
`gpio-check` and `verify --board` are host commands.

**On an Apple Silicon Mac** `./devkit container` takes the same commands, with
Docker through Colima: an x86-64 image under Rosetta runs Vivado, and the
sources and Vivado live in Docker volumes, so `system_top.xsa` is written into
a volume and not onto the Mac's disk. Start with
`./devkit container build-image --target factory`. This route built the R1
repository's whole factory firmware on one Mac (1 h 04 min, timing met); it has
not built the R2's design from this repository. For the R2 it built release
v0.2's boot files, around v0.1's design, and those booted. Setup and what was
not proven:
[macOS on Apple Silicon](../building-in-a-container.md#macos-on-apple-silicon).

**No Vivado installed yet?** [Install Vivado 2022.2](install-vivado.md) first:
the container runs the installer too. Budget an hour.

What is in the image and other operating systems, written for the R1's build:
[building in a container](../building-in-a-container.md).

**Next:** the second half,
[the boot files, the kernel and the Debian root](build-from-source.md#2-the-boot-files-the-kernel-and-the-debian-root).
