# Contributing

This is the **PlutoSky R2**'s devkit, a young port that one board has run.
Contributions are welcome, and so are reports: saying what works and what does
not on a second R2 is a contribution. This page covers where the source lives,
how to add a patch, what to check before a pull request (PR), and what CI does.

Credit for ideas as well as commits lives in [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Two repositories

The PlutoSky R1 / 7020-SDR has its own:
[fishball7020-fpga-devkit](https://github.com/matsvandamme/fishball7020-fpga-devkit).
This one started as a copy of it and still carries the R1's patch series and
device tree, because the R2's are layered on them.

| The change is about | It belongs |
|---|---|
| an R2 pin, the R2's block design, Ethernet through the FPGA, the reference PLL | here, in `firmware/revs/r2/patches/` |
| the R2's device tree or kernel option | here: `firmware-modern/dts/zynq-pluto-sdr-fishball-r2.dts`, `firmware-modern/config/r2.config` |
| a driver, the Debian root, a host tool, anything both boards share | in the R1 repository first, then carried over here. Keep the shared files identical: `firmware/patches/`, `firmware-modern/patches/`, `firmware-modern/dts/zynq-pluto-sdr-fishball.dts`, `fishball_defconfig` |

The two share history up to 2026-11-21, so `git cherry-pick` between them works:
`git remote add r1 https://github.com/matsvandamme/fishball7020-fpga-devkit.git`.

## Where the code lives

**The HDL, kernel and U-Boot source is not in this repo.** It is fetched fresh
and patched:

| half | fetched by | source | patches | CI |
|---|---|---|---|---|
| `firmware/`, the FPGA design | `./devkit setup --target factory` | `hdl/` of the vendor monorepo | the `hdl/` hunks of `firmware/patches/`, with `firmware/revs/r2/patches/` replacing or adding | `verify-patches.yml` |
| `firmware-modern/`, **Linux 6.12 LTS**, U-Boot and the boot loader | `./devkit setup` | the kernel from ADI at a pinned SHA; U-Boot, embeddedsw and bootgen | `firmware-modern/patches/`, and the `u-boot-xlnx/` hunks of `firmware/patches/` | `verify-modern.yml` |

A change is a patch file:

```bash
# run from: firmware/src, with the tree patched and your edit made
git diff -- path/to/file > ../revs/r2/patches/0023-what-it-does.patch
```

A patch in `firmware/revs/r2/patches/` with the **same file name** as one in
`firmware/patches/` replaces it; any other is added
([`rev.sh`](firmware/scripts/rev.sh)). Number a new one after the highest in
`firmware/patches/` and `firmware-modern/patches/`, which share one numbering
space with the R1 repository: the highest there is currently `0022`. Rules:

- **Patches stack.** 0004, 0005 and 0007 all edit `cf_axi_dds.c`. A plain
  `git diff` of such a file includes the earlier patches' changes too. Generate
  yours against a reconstructed pre-change copy (see commit `4468327` for how),
  and check the whole series still applies in order on a fresh `setup`.
- **`setup` stamps the tree** with a digest of the patch set, and the build
  refuses to run without a matching stamp - so after adding a patch, re-run
  `./devkit setup --target factory` before building. `firmware-modern/setup.sh`
  stamps the same way and also recognises a tree patched some other way: if the
  last patch reverses cleanly, the series is on, in order.
- **Do not put a safety-relevant field in `ad9361_rf_phy_state`.**
  `ad9361_clear_state()` `memset`s it, and the debugfs `initialize` calls
  `clear_state` - so anything kept there can be cleared by the surface it exists
  to defend against. Three fields have been moved out for this reason
  (`0016`'s latch, `0018`'s temperature limit, `0019`'s attenuation cache; a
  zeroed attenuation cache means full transmit power). Use
  `struct ad9361_rf_phy`, and seed it so that zero is not the dangerous value.

## Before opening a PR

1. `./devkit doctor` - the machine can build.
2. `./devkit sim --mutate` if you touched HDL - and **add a testbench** for any
   new module, next to `firmware/sim/tb_*.v`, plus at least one mutant in
   `run_sim.sh` that proves it can fail.
3. `./devkit build --target factory` for an FPGA change, then
   `./devkit build --xsa firmware/src/hdl/projects/pluto/system_top.xsa`; boot
   it on an R2, and say so in the PR, with the timing summary for an FPGA
   change. CI cannot run Vivado; "I booted it on an R2 and it works" is the bar.
4. **Add a CI assertion** that your patch landed - a `grep` for something it
   introduces - in `verify-patches.yml` or `verify-modern.yml` depending on which
   target it is for. Every existing patch has one; it is what catches a patch that
   silently stops applying against upstream. If the thing your patch guarantees can
   be checked in a *built artefact* rather than in the source, prefer that:
   `verify-modern.yml` compiles the device tree and audits the `.dtb`
   (`firmware-modern/verify_dtb.py`), because device-tree mistakes can be
   invisible in the `.dts` and still boot.
5. Measured numbers in the docs come from real builds and a real board. If your
   change moves them (LUTs, WNS), update them from your own build, in
   `docs/plutosky-r2.md`. **If you test something that page lists as
   untested, change its row**, with the date and what you saw: that table is
   the most useful thing in this repository to keep true.
6. If you changed anything under `docs/`, check it the way CI does. The pages are
   GitHub Markdown first and are also published as a site with MkDocs Material:

   ```bash
   # run from: the repo root
   python3 docs/check_links.py                   # links, anchors, "run from" lines
   pip install -r docs-site/requirements.txt
   mkdocs build --strict                         # the site, with no warnings
   mkdocs serve                                  # preview at http://127.0.0.1:8000
   ```

   A new page also needs a line in `mkdocs.yml`'s `nav` and in `docs/README.md`.
   For a callout use GitHub's alert syntax (`> [!WARNING]`, `> [!CAUTION]`,
   `> [!NOTE]`, `> [!TIP]`); it renders as a box on GitHub and on the site. Indent
   a code block or paragraph inside a list item by four spaces, not two: GitHub
   accepts two, the site's Markdown parser does not.

## Changing the Debian rootfs

`firmware-modern/debian/` does not work like the rest of the repo, and step 4
above does not apply to it. CI (`verify-rootfs.yml`) builds the root from
scratch when this directory changes and runs `check-rootfs.sh` on it, but
nothing in CI boots it. Run the same check on your own build:

```bash
# run from: the repo root
./devkit build --target modern --rootfs-only
./firmware-modern/debian/check-rootfs.sh
```

- **Packages go in [`packages.txt`](firmware-modern/debian/packages.txt)**, not in
  the `Containerfile`. One per line, with a comment saying what *breaks* without
  it. If you considered something and left it out, put it in the
  "deliberately NOT installed" block at the bottom. That file is also the manifest
  shipped on the board at `/usr/share/fishball/packages.txt`, so a name with no
  reason attached is a name nobody can later remove safely.
- **Anything that must run at boot is a systemd unit** in
  `overlay/etc/systemd/system/`, committed: a file you made on a running board
  is not on the next card. `/mnt/jffs2/autorun.sh` is **not** run
  on this rootfs.
- **Run `systemd-analyze verify` on a new unit.** An ordering cycle makes systemd
  *delete* a unit rather than fail it, so `systemctl status` then reports it does
  not exist, which looks exactly like a typo in the filename.
- **Nothing board-specific may be baked into the image.** It is a release asset,
  so whatever is in it is on every board anyone flashes. Read "No identity in
  the image" in [`docs/debian-root-reference.md`](docs/debian-root-reference.md#no-identity-in-the-image)
  before adding anything that looks like a key, an ID or an address.
- **The base image and the packages are pinned** in the `Containerfile` (`BASE`
  and `DEBIAN_SNAPSHOT`). Change both together, on purpose, and test the result
  on a board.
- **Say in the PR that you wrote a card and booted it**, and paste
  `./devkit selftest --ssh`. Booting it is the only test of the rootfs that
  CI cannot run.

## What CI does and does not do

- `verify-patches.yml`: a fresh clone, `setup_fpga.sh`, and assertions that
  the tree is the R2's design with this repo's FPGA changes in it.
- `verify-modern.yml`: an assertion per kernel patch, plus two things a kernel
  allows that Vivado does not - it **builds the device tree and audits the
  `.dtb`** (16 checks, including that the transmit-attenuation default is still
  89750 mdB; and the R2's tree may differ from the R1's only where the board
  does), and it **cross-builds `uImage`** and fails on a warning in any file
  this repo patches.
- `host-tools.yml`: the Python tools compile and import on 3.8 and 3.12, the
  selftest's measurement maths is asserted against known signals, and the HDL
  simulation with mutation testing runs (triggered by changes under
  `firmware/sim/`, `firmware/patches/` and `tools/`).
- `verify-rootfs.yml`: builds the Debian root from scratch under ARM emulation
  and runs `firmware-modern/debian/check-rootfs.sh` on it (triggered by changes
  under `firmware-modern/debian/`, and weekly).
- `hardware.yml`: for a self-hosted runner wired to a real board. Inert here:
  no runner is registered for this repository, and its checks were written
  against an R1.
- The hosted workflows do **not** build the FPGA design or touch hardware.
- There is no release workflow. Release v0.1 was made by hand: tagged, built at the tag, the Debian root taken from a `verify-rootfs.yml` run on the tag, booted on an R2, then published.

## Style

Scripts over documentation-only workarounds: fix the build in
the script or the relevant `.tcl` rather than telling the next person how
to work around it. Write for someone who has not built an FPGA design before -
define a term where it first appears, and say *why*, not only *what*.

Bug reports: use the issue templates (build failure vs. hardware mismatch);
they ask for the stage, tool versions and logs that speed things up.
