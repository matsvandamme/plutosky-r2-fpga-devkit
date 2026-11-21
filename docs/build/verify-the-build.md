---
icon: material/clipboard-check-outline
description: ./devkit verify checks a build before you flash it; --board checks the board runs it.
---

# Check the build

```bash
# run from: the repo root
./devkit verify            # is the build sane?
./devkit verify --board    # ...and is the board running it?
```

| It checks | Why |
|---|---|
| the four boot files are present | |
| `BOOT.bin` holds exactly three partitions: the boot loader, the bitstream, U-Boot | a missing or extra partition does not boot |
| the bitstream in `BOOT.bin` is byte-identical to the one in the `.xsa` you passed | the FPGA on the board is then the design you built, not a stale one |
| `--board`: the files on the card against `output/` | a card holding a different build of the same size looks entirely normal |

**You should see**, as from the build of 2026-11-21:

```text
=== files ===
  ok    BOOT.bin           2709004 B
  ok    uImage             5617896 B
  ok    devicetree.dtb       22720 B
  ok    uEnv.txt              8252 B
=== BOOT.bin ===
  BOOT.bin: 2709004 bytes, 3 partitions
    fsbl.elf         offset      5888  length     98316  sha256 654196a543f70084
    system_top.bit   offset    104256  length   2189888  sha256 4d1d372595280900
    u-boot.elf       offset   2294144  length    414860  sha256 d7336653f55afa46
  PASS  exactly the three partitions this board boots from
  PASS  bitstream partition is byte-identical to the XSA's (2189888 bytes, sha256 4d1d372595280900)
```

Two things it does not check, and how to:

**The device tree.** Device-tree mistakes usually build and boot. Audit the
built file, 16 checks; the R2's tree passes all of them:

```bash
# run from: the repo root
python3 firmware-modern/verify_dtb.py firmware-modern/output/devicetree.dtb   # stdlib only
```

**Timing.** It is the FPGA build's result, printed at the end of
`./devkit build --target factory` and kept in
`firmware/src/hdl/projects/pluto/timing.rpt`:

```text
WNS(ns)      TNS(ns)  TNS Failing Endpoints
  0.100        0.000                      0
```

That is the default design. A negative `WNS` is a design that does not meet
timing, and it still produces a bitstream.

!!! warning "`--board` has not been run against an R2"
    It is the R1 repository's check, unchanged.

**Next:** [put it on the board](flash-your-build.md).
