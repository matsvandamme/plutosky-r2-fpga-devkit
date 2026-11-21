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
    Mac, with Vivado running under x86-64 emulation: about 10 minutes, timing
    met. `./devkit container` itself, which uses podman on a Linux host, has
    not been run for an R2 build. Two things that mattered there: Vivado hangs
    at start unless its standard input is closed (`</dev/null`), and
    `tools/env-vivado.sh`, not Vivado's own `settings64.sh`, supplies the old
    libraries it needs.

**Build in the container; flash from the host:** `flash`, `selftest`,
`gpio-check` and `verify --board` are host commands.

**No Vivado installed yet?** [Install Vivado 2022.2](install-vivado.md) first:
the container runs the installer too. Budget an hour.

What is in the image and other operating systems, written for the R1's build:
[building in a container](../building-in-a-container.md).

**Next:** the second half,
[the boot files, the kernel and the Debian root](../start/write-the-card.md#2-the-boot-files-the-kernel-and-the-debian-root).
