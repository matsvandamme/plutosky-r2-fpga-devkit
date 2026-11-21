---
name: Build failure
about: ./devkit setup or ./devkit build failed partway through
title: ""
labels: build
---

**Which command failed?** (`./devkit build --target factory`, the FPGA design, or `./devkit build --xsa ...`, everything else; and the last `=== ... ===` banner in the output)

**Host OS + version** (`lsb_release -a`):

**Vivado version** (`vivado -version`):

**Exact error output** (the last ~30 lines before the script exits, or a
link to the full log — `./devkit build ... 2>&1 | tee build.log` captures
everything; for the FPGA design, also `firmware/src/hdl/projects/pluto/build_hdl.log`):

**What you changed, if anything, before this happened** (HDL edit, patch
edit, different upstream commit, etc. — leave blank if you ran the steps
exactly as documented):
