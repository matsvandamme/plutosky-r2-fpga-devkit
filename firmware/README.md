# firmware: the PlutoSky R2's FPGA design

This directory builds **one thing**: the R2's FPGA design, with Vivado 2022.2,
into `src/hdl/projects/pluto/system_top.xsa`. Everything else on the card (the
boot loader, the kernel, the Debian root) is built around that file by
[`firmware-modern/`](../firmware-modern/README.md).

```bash
# run from: the repo root
./devkit setup --target factory     # hdl/ from the vendor monorepo (~0.2 GB) + the R2 patch series
./devkit doctor --target factory    # Vivado, the source tree, the patch stamp
./devkit build --target factory     # synthesis, implementation, bitstream, system_top.xsa
```

Read the timing summary the build prints. A design that misses timing still
produces a bitstream. The default design, built on 2026-11-19: timing met, WNS
+0.100 ns, 12,717 LUTs.

It is called the *factory* target because in the R1 repository, where these
files come from, the same name builds the R1's whole factory firmware: the
vendor's 5.15 kernel and a Buildroot root as well. None of that exists for the
R2 here.

## What is in this directory

| | |
|---|---|
| [`patches/`](patches/README.md) | the R1's patch series, one section per patch. **The R2's input**: its `hdl/` hunks are applied to the R2's design, and its `u-boot-xlnx/` hunks to U-Boot by `firmware-modern/`. The kernel and Buildroot hunks are never applied here |
| [`revs/r2/patches/`](revs/r2/README.md) | the R2's own three patches, which replace or add to the series: the vendor's R2 design, and two of the series' FPGA changes redone on R2 pins |
| `scripts/rev.sh` | the R2's names (part, device tree) and the rule that merges the two patch directories |
| `scripts/setup_fpga.sh`, `build_fpga.sh` | what `./devkit setup` and `build` run with `--target factory` |
| `scripts/build_hdl.tcl`, `*.coe`, `gen_fir_coe.py`, `gen_fir_coe.m` | the Vivado run, and the receive-filter coefficient files |
| `scripts/fetch_common.sh` | the pinned upstream, U-Boot, FSBL and bootgen commits, shared with `firmware-modern/` |
| `scripts/import_xsa.sh`, `boot.bif`, `check_bootbin.py` | used by `firmware-modern/`: reading an `.xsa`, packaging `BOOT.bin`, reading one back apart |
| [`fsbl/`](fsbl/README.md) | builds the first-stage boot loader without Vitis; used by `firmware-modern/` |
| `sim/` | testbenches for the devkit's own HDL; `./devkit sim` runs them |
| `src/` | the FPGA source, cloned and patched by `setup`; not committed |

## Rules that save you an hour

- **Nothing in `src/` is yours.** `setup` clones and patches it, and the surest
  fix for a confused tree is `rm -rf firmware/src && ./devkit setup --target factory`.
  Put your changes in a numbered patch.
- **Never edit a patch that is already applied.** `setup` cannot apply a changed
  patch over its earlier version; add a new, higher-numbered patch instead.
- **Delete the Vivado project before rebuilding after a source change.**
  `build_hdl.tcl` reuses an existing `pluto.xpr`; the build refuses to start
  when it sees sources newer than the project, and prints the `rm`.
- **`source tools/env-vivado.sh`, never Vivado's own `settings64.sh`.** It
  supplies the old libraries Vivado 2022.2 needs.
- **An R2 pin comes from the R2 schematic**
  ([OpenSourceSDRLab/PlutoSky-R2](https://github.com/OpenSourceSDRLab/PlutoSky-R2)),
  never from anything written for the R1. The two packages share no pin-out,
  and the R2's header is 1.8 V.

## Further reading

- [`revs/r2/README.md`](revs/r2/README.md): the R2's patches.
- [`patches/README.md`](patches/README.md): each patch of the R1 series, what it changes and why.
- [The PlutoSky R2](../docs/plutosky-r2.md): what differs from the R1, and what is tested.
- [Add your own logic to the FPGA](../docs/build/add-fpga-logic.md).
