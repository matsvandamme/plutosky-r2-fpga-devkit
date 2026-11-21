#!/usr/bin/env python3
"""Draw the Hardware and I/O figure for the PlutoSky R2, in the same style as
the Getting started ones (the helpers come from make_start_figures.py).

    # run from: the repo root
    python3 docs/img/make_hw_figures.py        # stdlib only

Writes into docs/img/:

    hw-jp5-{light,dark}.svg    the R2's 2x12 JP5 header: 5 V, ground, and the four
                               pins this firmware drives

Pin numbers, the 5 V pin, the grounds and the 1.8 V level are from the vendor's
schematic by way of docs/plutosky-r2.md and
firmware/revs/r2/patches/0006-tx-sample-nibble-to-gpio.patch. Nothing on the
header has been probed on a board, and where pin 1 sits physically has not
been looked up, so the drawing says to find it instead of guessing.

refclock(), pin_owner() and user_led() draw the R1's hardware (its R107/R109
links, its 3.3 V pins, its LED on MIO 0) for pages only the R1's repository
has; main() does not draw them here.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_start_figures import Fig, both  # noqa: E402


# --- the reference clock: three configurations ---------------------------------

def refclock(t):
    f = Fig(860, 430, t)
    rows = (
        ("As shipped: R107 fitted, R109 empty", True, False,
         "the radio runs from Y3; EXT_CLK is connected to nothing", "muted"),
        ("Reference in: R107 empty, R109 fitted", False, True,
         "the radio runs from whatever is on EXT_CLK: at most 1.3 V p-p, AC-coupled", "ok"),
        ("Both fitted: reference out only", True, True,
         "Y3's 40 MHz appears on EXT_CLK. Never connect a source here", "danger"),
    )
    for i, (title, r107, r109, verdict, colour) in enumerate(rows):
        y = 14 + i * 142
        f.text(20, y + 14, title, 14, "ink", 600, "start")
        by = y + 30
        f.box(20, by, 130, 56, "Y3", "40 MHz oscillator")
        f.box(365, by, 130, 56, "AD9361", "XTALN, ball M12", fill="accent_soft", stroke="accent")
        f.box(710, by, 130, 56, "EXT_CLK", "RF1, U.FL")
        for x1, x2, name, fitted in ((150, 365, "R107", r107), (495, 710, "R109", r109)):
            mid = (x1 + x2) / 2
            if fitted:
                f.line(x1, by + 28, mid - 44, by + 28, "ink", 1.8)
                f.line(mid + 44, by + 28, x2, by + 28, "ink", 1.8)
                f.raw(f'<rect x="{mid - 44}" y="{by + 16}" width="88" height="24" rx="4" '
                      f'fill="{t["surface"]}" stroke="{t["ink"]}" stroke-width="1.8"/>')
                f.text(mid, by + 33, f"{name} 33 Ω", 12, "ink", 600)
            else:
                f.line(x1, by + 28, mid - 44, by + 28, "line", 1.8)
                f.line(mid + 44, by + 28, x2, by + 28, "line", 1.8)
                f.raw(f'<rect x="{mid - 44}" y="{by + 16}" width="88" height="24" rx="4" fill="none" '
                      f'stroke="{t["muted"]}" stroke-width="1.5" stroke-dasharray="4 3"/>')
                f.text(mid, by + 33, f"{name} empty", 12, "muted")
        f.text(20, by + 78, verdict, 12.5, colour, 500, "start")
    return f


# --- who drives the four free pins ---------------------------------------------

def pin_owner(t):
    f = Fig(860, 230, t)
    f.box(20, 14, 240, 74, "Linux", ("EMIO GPIO 18–21", "gpiochip0 lines 72–75"))
    f.box(20, 148, 240, 62, "The transmit samples", ("low four bits of channel 0's I",))
    f.box(350, 78, 200, 74, "tx_sample_gpio_en", ("0: Linux drives the pins", "1: the samples do"),
          fill="accent_soft", stroke="accent")
    f.arrow(260, 51, 348, 96, colour="muted")
    f.arrow(260, 179, 348, 134, colour="muted")
    f.text(300, 60, "0", 13, "ink", 600)
    f.text(300, 176, "1", 13, "ink", 600)
    f.arrow(550, 115, 638, 115, colour="accent")
    f.box(640, 78, 200, 74, "JP5 pins 7, 9, 11, 13", ("3.3 V, pulled down", "0 at power-on: Linux"),
          fill="ok_soft", stroke="ok")
    return f


# --- the USER LED --------------------------------------------------------------

def user_led(t):
    f = Fig(860, 210, t)
    f.box(20, 20, 250, 62, "A TX attenuation change", ("ad9361_set_tx_atten()",), mono_sub=True)
    f.arrow(270, 51, 328, 51, colour="accent")
    f.box(330, 14, 200, 74, "tx-active trigger", ("lit: a chain is out of mute", "dark: both at −89.75 dB"),
          fill="accent_soft", stroke="accent")
    f.arrow(530, 51, 618, 51, colour="accent")
    f.box(620, 20, 220, 62, "USER LED", ("led0:green, PS MIO pin 0",), fill="ok_soft", stroke="ok")
    f.box(330, 122, 200, 74, "Your own setting", ("trigger and brightness", "in /sys/class/leds"))
    f.arrow(530, 159, 700, 84, colour="muted")
    f.box(20, 122, 250, 74, "Your HDL", ("cannot drive it: MIO pins are", "not routed into the fabric"),
          fill="danger_soft", stroke="danger")
    return f


# --- the R2's JP5 header --------------------------------------------------------

def jp5(t):
    f = Fig(790, 250, t)
    f.text(20, 26, "JP5 on the PlutoSky R2: 2 × 12 pins, 1.8 V logic", 14, "ink", 600, "start")
    kinds = {1: "danger", 2: "ink", 22: "ink", 24: "ink", 7: "accent", 9: "accent", 11: "accent", 13: "accent"}
    x0, pitch = 62, 60.5
    f.raw(f'<rect x="20" y="62" width="750" height="92" rx="8" fill="{t["surface"]}" stroke="{t["line"]}" '
          f'stroke-width="1.5"/>')
    for col in range(12):
        x = x0 + col * pitch
        for pin, y, ty in ((2 * col + 1, 86, 55), (2 * col + 2, 130, 172)):
            kind = kinds.get(pin)
            fill = t[kind + "_soft"] if kind in ("danger", "accent") else (t["ink"] if kind else "none")
            stroke = t[kind] if kind else t["muted"]
            f.raw(f'<circle cx="{x}" cy="{y}" r="11" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            f.text(x, ty, str(pin), 12, kind if kind in ("danger", "accent") else "muted", 600 if kind else 400)
    legend = (
        (20, "danger", True, "pin 1: 5 V"),
        (150, "ink", False, "pins 2, 22, 24: ground"),
        (350, "accent", True, "pins 7, 9, 11, 13: sample_gpio0 to 3, outputs at 1.8 V"),
    )
    for x, kind, soft, label in legend:
        fill = t[kind + "_soft"] if soft else t[kind]
        f.raw(f'<circle cx="{x + 8}" cy="204" r="7" fill="{fill}" stroke="{t[kind]}" stroke-width="2"/>')
        f.text(x + 24, 209, label, 12.5, "body", anchor="start")
    f.text(20, 236, "Numbered as on the vendor's schematic; nothing here has been probed. "
           "Find pin 1 on the board before you connect anything.", 12, "muted", anchor="start")
    return f


def main():
    both("hw-jp5", "The PlutoSky R2's JP5 header: 5 V on pin 1, ground, and the four pins this firmware drives", jp5)


if __name__ == "__main__":
    main()
