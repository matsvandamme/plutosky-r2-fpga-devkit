---
icon: material/clipboard-check-outline
description: ./devkit verify checks a build before you flash it; --board checks the board runs it.
---

# Check the build

```bash
# run from: the repo root
./devkit verify                  # is the build sane?
./devkit verify --board          # ...and is the board running it?
./devkit verify --require-board  # the same, but FAIL if the board is stale or unreadable
```

| It checks | Why |
|---|---|
| the four boot files are present and not trivially small | |
| `firmware-modern/verify_dtb.py` audits the built device tree, 16 checks | device-tree mistakes usually build and boot. The R2's tree passes all 16 |
| `--board`: every file on the card against `output/`, by checksum | a card holding a different build of the same size looks entirely normal |

Timing is not one of them. It is the FPGA build's result, printed at the end of
`./devkit build --target factory` and kept in
`firmware/src/hdl/projects/pluto/timing.rpt`:

```text
WNS(ns)      TNS(ns)  TNS Failing Endpoints
  0.100        0.000                      0
```

That is the default design, built on 2026-11-19. A negative `WNS` is a design
that does not meet timing, and it still produces a bitstream.

!!! warning "`--board` has not been run against an R2"
    It is the R1 repository's check, unchanged.

!!! note "`--board` reports, it does not fail"
    It reports without changing the exit status. Use `--require-board` in a
    script that must fail on a stale card.

**Next:** [put it on the board](flash-your-build.md).
