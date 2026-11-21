#!/bin/bash
# Which hardware revision is this repository for? Source it; do not run it.
#
#     DEVKIT_REV=r2   PlutoSky R2   XC7Z020-CLG484   (the only one here)
#
# THIS REPOSITORY BUILDS FOR THE PLUTOSKY R2 AND NOTHING ELSE. The PlutoSky R1 /
# 7020-SDR (XC7Z020-CLG400) has its own:
#     https://github.com/matsvandamme/fishball7020-fpga-devkit
# The two were one repository with a --rev switch until 2026-11-21; the names
# below are what is left of it. Every revision-dependent name still lives HERE,
# once, so the scripts that source this cannot disagree.
#
# WHY THE R2 IS NOT THE R1 WITH A DIFFERENT LABEL. It is another package
# (CLG484), so every FPGA ball is different; its Ethernet PHY is on FPGA pins
# behind a GMII-to-RGMII core where the R1's is on PS MIO 16-27; and its MIO
# bank 501 runs at 3.3 V where the R1's runs at 1.8 V. An R1 boot image on an R2
# boots Linux with no radio, no Ethernet and no USB (measured 2026-11-18: AD9361
# PRODUCT_ID 0xFF, "Could not attach PHY (-19)", no usb0). So an XSA for the R1
# must be refused here (import_xsa.sh does, by REV_PART).
#
# WHAT IS STILL THE R1's IN THIS TREE, and must stay: firmware/patches/ is the
# R1 series the R2's is layered on (devkit_patch_series below), and the R2's
# device tree includes the R1's. They are the R2's inputs, not a second board.
DEVKIT_REV="${DEVKIT_REV:-r2}"
case "$DEVKIT_REV" in
    r2)
        # No suffix: output/, src/ and boot/hdl/ are the R2's, there being no
        # other revision in this repository to keep them apart from.
        REV_SUFFIX=""
        REV_NAME="PlutoSky R2"
        REV_PART="xc7z020clg484-2"
        REV_DTB="zynq-pluto-sdr-fishball-r2"
        ;;
    r1)
        echo "ERROR: this repository builds for the PlutoSky R2 only. The PlutoSky R1 / 7020-SDR is at" >&2
        echo "           https://github.com/matsvandamme/fishball7020-fpga-devkit" >&2
        exit 1 ;;
    *)
        echo "ERROR: unknown hardware revision '$DEVKIT_REV'. This repository builds for r2, the PlutoSky R2." >&2
        exit 1 ;;
esac
export DEVKIT_REV
# Nothing to add to the commands messages print: r2 is the default and the only one.
REV_FLAG=""

# The factory patch series for this revision, one path per line, in apply order.
#
#   firmware/patches/*.patch              the series, written for the R1
#   firmware/revs/<rev>/patches/*.patch   this revision's own
#
# A revision patch with the SAME FILE NAME as a series patch REPLACES it; any
# other is added. The merged list is ordered by file name, so 0000-... goes on
# first.
devkit_patch_series() {   # <firmware dir>
    local fw="$1" revdir="$1/revs/$DEVKIT_REV/patches" p
    {
        for p in "$fw"/patches/*.patch; do
            [ -f "$revdir/$(basename "$p")" ] || echo "$p"
        done
        if [ -d "$revdir" ]; then
            for p in "$revdir"/*.patch; do [ -f "$p" ] && echo "$p"; done
        fi
    } | awk -F/ '{ print $NF "\t" $0 }' | sort | cut -f2-
}
