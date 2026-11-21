#!/usr/bin/env python3
"""Draw the Getting started figures for the PlutoSky R2, each in a light and a
dark variant.

    # run from: the repo root
    python3 docs/img/make_start_figures.py        # stdlib only

Writes into docs/img/:

    start-r1-or-r2-{light,dark}.svg     what tells an R2 from an R1
    start-card-{light,dark}.svg         the two partitions of the card
    start-connect-{light,dark}.svg      which socket goes where, on the R2
    start-boot-switch-{light,dark}.svg  the BOOT switch set to SD
    start-attenuator-{light,dark}.svg   TX -> attenuator -> RX, with no power figure:
                                        the R2's output power is not measured
    start-loopback-{light,dark}.svg     the same loop with the R1's levels, for the
                                        pages that came with the R1's devkit
    start-network-{light,dark}.svg      the R1's two network interfaces (same pages)
    start-bootchain-{light,dark}.svg    BootROM to root filesystem
    start-buildstages-{light,dark}.svg  the build's seven stages
    start-netconfig-{light,dark}.svg    where the R1's Buildroot address settings live

The R1's repository also draws labelled photographs of its board and its login
message from this script. Their sources are not in this repository, so main()
skips them here: an R1 photograph is not a picture of the R2.

Pages show a diagram as `![alt](img/x-light.svg#only-light)` plus the
`-dark.svg#only-dark` twin, so it follows the site's colour-scheme switch.
Every number and name drawn here comes from the pages that show the figure,
and for the R2 from docs/plutosky-r2.md.
"""
import base64
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent

THEMES = {
    "light": dict(ink="#141415", body="#3c3c43", muted="#6e6e73", surface="#f8f8f8", line="#c9c9cf",
                  accent="#4069FF", accent_soft="#e9eeff", danger="#d6293e", danger_soft="#fdecee",
                  ok="#1a9e5c", ok_soft="#e6f6ee"),
    "dark": dict(ink="#f4f4f6", body="#cfcfd6", muted="#9a9aa3", surface="#1f1f23", line="#4a4a54",
                 accent="#8aa2ff", accent_soft="#232a47", danger="#ff7a8a", danger_soft="#3a1d22",
                 ok="#5fd39a", ok_soft="#17302a"),
}
FONT = "Inter, system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, 'DejaVu Sans Mono', Menlo, Consolas, monospace"


class Fig:
    def __init__(self, w, h, t):
        self.w, self.h, self.t, self.out = w, h, t, []

    def text(self, x, y, s, size=14, fill="body", weight=400, anchor="middle", mono=False):
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        self.out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{self.t[fill]}" '
                        f'text-anchor="{anchor}" font-family="{MONO if mono else FONT}">{s}</text>')

    def box(self, x, y, w, h, title, sub=(), fill="surface", stroke="line", title_fill="ink", r=8, mono_sub=False):
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{self.t[fill]}" '
                        f'stroke="{self.t[stroke]}" stroke-width="1.5"/>')
        sub = [sub] if isinstance(sub, str) else list(sub)
        top = y + h / 2 - (len(sub) * 17) / 2 + 5
        self.text(x + w / 2, top, title, 14, title_fill, 600)
        for i, s in enumerate(sub):
            self.text(x + w / 2, top + 19 + i * 17, s, 12, "muted", mono=mono_sub)

    def arrow(self, x1, y1, x2, y2, label=None, colour="muted", dash=False, label_dy=-8):
        c = self.t[colour]
        d = ' stroke-dasharray="5 4"' if dash else ""
        self.out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.6"{d} '
                        f'marker-end="url(#a-{colour})"/>')
        if label:
            self.text((x1 + x2) / 2, (y1 + y2) / 2 + label_dy, label, 12, colour)

    def line(self, x1, y1, x2, y2, colour="line", width=1.5):
        self.out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.t[colour]}" stroke-width="{width}"/>')

    def raw(self, s):
        self.out.append(s)

    def svg(self, title):
        markers = "".join(
            f'<marker id="a-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{self.t[k]}"/></marker>'
            for k in ("muted", "accent", "danger", "ok", "ink"))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" role="img"><title>{title}</title><defs>{markers}</defs>'
                + "".join(self.out) + "</svg>\n")


def both(name, title, draw):
    for theme, t in THEMES.items():
        f = draw(t)
        (HERE / f"{name}-{theme}.svg").write_text(f.svg(title))


# --- R1 or R2 ----------------------------------------------------------------

def r1_or_r2(t):
    f = Fig(760, 262, t)
    f.box(20, 14, 240, 232, "", ())
    f.box(500, 14, 240, 232, "", (), fill="accent_soft", stroke="accent")
    f.text(140, 42, "PlutoSky R1 / 7020-SDR", 14, "ink", 600)
    f.text(140, 61, "the other repository", 12, "muted")
    f.text(620, 42, "PlutoSky R2", 14, "ink", 600)
    f.text(620, 61, "this firmware", 12, "accent")
    rows = (
        ("printed on the Zynq", "XC7Z020-CLG400", "XC7Z020-CLG484", True),
        ("socket on the case", "no 10M_IN", "10M_IN", False),
        ("JP5 header", "2 × 10 pins", "2 × 12 pins", False),
        ("vendor firmware says", "v0.38-4-g95aad", "v0.38-5-g76414", True),
    )
    for i, (what, r1, r2, mono) in enumerate(rows):
        y = 98 + i * 40
        f.text(380, y, what, 12.5, "muted")
        f.line(268, y - 4, 300, y - 4, "line")
        f.line(460, y - 4, 492, y - 4, "line")
        f.text(140, y, r1, 13, "body", mono=mono)
        f.text(620, y, r2, 13, "ink", 600, mono=mono)
    return f


# --- which socket goes where, on the R2 ---------------------------------------

def connect(t):
    f = Fig(760, 300, t)
    f.box(280, 30, 200, 240, "", ())
    f.text(380, 58, "The PlutoSky R2", 14, "ink", 600)
    f.text(380, 77, "BOOT switch: SD", 12, "muted")
    for i, (name, sub) in enumerate((("ETH", "RJ45"), ("DEBUG", "USB-C"), ("USB2.0", "USB-C"))):
        y = 100 + i * 56
        f.box(300, y, 160, 42, name, sub, fill="accent_soft", stroke="accent")
    f.box(20, 94, 180, 54, "Your router", "hands out the address")
    f.arrow(300, 121, 202, 121, colour="accent")
    f.text(250, 112, "network", 12, "accent")
    f.text(110, 176, "then, from your PC:", 12, "muted")
    f.text(110, 195, "ssh root@fishball.local", 12.5, "accent", mono=True)
    f.box(560, 150, 180, 54, "USB power", "and the serial console")
    f.arrow(558, 177, 462, 177, "power")
    f.box(560, 212, 180, 54, "USB power", "the second socket")
    f.arrow(558, 233, 462, 233, "power")
    f.text(650, 100, "Connect both: one alone", 12, "muted")
    f.text(650, 117, "can be short of power", 12, "muted")
    return f


# --- the BOOT switch ----------------------------------------------------------

def boot_switch(t):
    f = Fig(760, 150, t)
    f.box(20, 20, 170, 110, "", ())
    f.text(105, 44, "ON", 13, "ink", 600)
    for i in range(2):
        x = 58 + i * 58
        f.raw(f'<rect x="{x}" y="56" width="36" height="60" rx="5" fill="{t["surface"]}" '
              f'stroke="{t["line"]}" stroke-width="1.5"/>')
        f.raw(f'<rect x="{x + 4}" y="86" width="28" height="26" rx="4" fill="{t["accent"]}"/>')
    f.text(220, 52, "SD card: both sliders away from ON", 14, "ink", 600, "start")
    f.text(220, 76, "What this firmware boots from. Set it with the board off.", 12.5, "body", anchor="start")
    f.text(220, 100, "A wrong position is silent: nothing appears,", 12.5, "muted", anchor="start")
    f.text(220, 118, "not even on the serial console.", 12.5, "muted", anchor="start")
    return f


# --- TX -> attenuator -> RX, without the R1's power figures --------------------

def attenuator(t):
    f = Fig(760, 250, t)
    f.text(20, 28, "With the attenuator", 14, "ink", 600, "start")
    f.box(20, 44, 150, 64, "TX1", "power not measured")
    f.arrow(170, 76, 300, 76)
    f.box(300, 44, 160, 64, "Attenuator", "20 dB, better 30", fill="accent_soft", stroke="accent")
    f.arrow(460, 76, 590, 76, "20 dB less or more")
    f.box(590, 44, 150, 64, "RX1", "limit: about +2.5 dBm")
    f.text(20, 158, "Without it", 14, "ink", 600, "start")
    f.box(20, 174, 150, 56, "TX1", "power not measured")
    f.arrow(170, 202, 590, 202, "everything the transmitter puts out", "danger")
    f.box(590, 174, 150, 56, "RX1", "can be destroyed", fill="danger_soft", stroke="danger")
    return f


# --- TX -> attenuator -> RX, with the R1's levels ------------------------------

def loopback(t):
    f = Fig(760, 250, t)
    f.text(20, 28, "With the attenuator", 14, "ink", 600, "start")
    f.box(20, 44, 150, 64, "TX1A", "about +19 dBm out")
    f.arrow(170, 76, 300, 76, "+19 dBm")
    f.box(300, 44, 160, 64, "20 dB attenuator", "at least 20 dB", fill="accent_soft", stroke="accent")
    f.arrow(460, 76, 590, 76, "about −1 dBm", "ok")
    f.box(590, 44, 150, 64, "RX1A", "survives +2.5 dBm", fill="ok_soft", stroke="ok")
    f.text(20, 158, "Without it", 14, "ink", 600, "start")
    f.box(20, 174, 150, 56, "TX1A", "about +19 dBm out")
    f.arrow(170, 202, 590, 202, "+19 dBm, about 16 dB over the limit", "danger")
    f.box(590, 174, 150, 56, "RX1A", "destroyed", fill="danger_soft", stroke="danger")
    return f


# --- the card ----------------------------------------------------------------

def card(t):
    f = Fig(760, 210, t)
    f.text(20, 26, "One microSD card, two partitions", 14, "ink", 600, "start")
    f.box(20, 42, 250, 150, "", (), fill="accent_soft", stroke="accent")
    f.text(145, 68, "1 · Boot partition", 14, "ink", 600)
    f.text(145, 87, "FAT, 128 MB: the board boots from it", 12, "muted")
    for i, name in enumerate(("BOOT.bin", "uImage", "devicetree.dtb", "uEnv.txt")):
        f.text(145, 112 + i * 19, name, 12.5, "body", mono=True)
    f.box(290, 42, 450, 150, "", ())
    f.text(515, 68, "2 · Debian root", 14, "ink", 600)
    f.text(515, 87, "ext4 (ext3 when written on Windows): Debian 13, with systemd", 12, "muted")
    f.text(515, 122, "the rest of the card", 12.5, "body")
    f.text(515, 144, "unpacked from debian-rootfs.tar.gz", 12.5, "body")
    f.text(515, 172, "Windows cannot create this one: use the card writer", 12, "muted")
    return f


# --- the two interfaces ------------------------------------------------------

def network(t):
    f = Fig(760, 250, t)
    f.box(290, 24, 180, 202, "", ())
    f.text(380, 52, "The board", 14, "ink", 600)
    f.text(380, 71, "fishball.local", 12.5, "accent", mono=True)
    f.box(306, 88, 148, 54, "USB cable", "192.168.2.1", fill="ok_soft", stroke="ok", mono_sub=True)
    f.box(306, 156, 148, 54, "Ethernet", "DHCP, or static", fill="accent_soft", stroke="accent")
    f.box(20, 88, 190, 54, "Your PC", "ssh root@192.168.2.1", mono_sub=True)
    f.arrow(306, 115, 212, 115, colour="ok")
    f.text(259, 106, "fixed", 12, "ok")
    f.box(550, 156, 190, 54, "Your router", "hands out the address")
    f.arrow(454, 183, 548, 183, colour="accent")
    f.text(115, 172, "never changes with", 12, "muted")
    f.text(115, 189, "devkit net: the way back in", 12, "muted")
    f.text(645, 106, "devkit net static / dhcp", 12, "muted")
    f.text(645, 123, "change this side only", 12, "muted")
    return f


# --- rows of stages ----------------------------------------------------------

def row(title, stages, width=760, box_w=None, h=110):
    def draw(t):
        n = len(stages)
        gap = 22
        bw = box_w or (width - 40 - gap * (n - 1)) / n
        f = Fig(width, h, t)
        if title:
            f.text(20, 24, title, 14, "ink", 600, "start")
        y = 38 if title else 14
        for i, (name, sub) in enumerate(stages):
            x = 20 + i * (bw + gap)
            f.box(x, y, bw, 58, name, sub)
            if i < n - 1:
                f.arrow(x + bw + 2, y + 29, x + bw + gap - 2, y + 29, colour="accent")
        return f
    return draw


def netconfig(t):
    f = Fig(760, 220, t)
    f.box(20, 70, 210, 80, "U-Boot environment", ("128 KB in QSPI flash", "/dev/mtd1"), fill="accent_soft", stroke="accent")
    f.arrow(230, 110, 318, 110, colour="accent")
    f.text(274, 100, "every boot", 12, "muted")
    f.box(320, 76, 170, 68, "S40network", "reads it with fw_printenv")
    for i, name in enumerate(("/etc/network/interfaces", "/etc/udhcpd.conf", "/opt/config.txt")):
        y = 22 + i * 66
        f.arrow(490, 110, 548, y + 22, colour="muted")
        f.box(550, y, 190, 44, name, (), title_fill="body")
    f.text(645, 214, "generated: edits here are lost at reboot", 12, "muted")
    return f


# --- labelled photographs ----------------------------------------------------

def photo_figure(name, title, src, crop, size, labels, t=THEMES["light"]):
    """crop: WxH+X+Y of the source photo; size: the photo's drawn (w, h).
    labels: (text, sub, side, y, (px, py)) with the point in drawn-photo pixels."""
    jpg = subprocess.run(["magick", str(HERE / src), "-crop", crop, "+repage", "-resize", f"{size[0]}x{size[1]}!",
                          "-quality", "82", "jpg:-"], check=True, capture_output=True).stdout
    pw, ph = size
    margin = 215
    f = Fig(pw + 2 * margin, ph + 20, t)
    f.raw(f'<rect width="{f.w}" height="{f.h}" rx="10" fill="#ffffff" stroke="#e3e3e6"/>')
    f.raw(f'<image x="{margin}" y="10" width="{pw}" height="{ph}" '
          f'href="data:image/jpeg;base64,{base64.b64encode(jpg).decode()}"/>')
    for text, sub, side, y, (px, py) in labels:
        px, py = px + margin, py + 10
        lx = margin - 14 if side == "left" else pw + margin + 14
        f.raw(f'<line x1="{lx}" y1="{y - 4}" x2="{px}" y2="{py}" stroke="#4069FF" stroke-width="1.6"/>')
        f.raw(f'<circle cx="{px}" cy="{py}" r="5" fill="#ffffff" stroke="#4069FF" stroke-width="2"/>')
        anchor = "end" if side == "left" else "start"
        tx = lx - 6 if side == "left" else lx + 6
        f.text(tx, y, text, 14, "ink", 600, anchor)
        if sub:
            f.text(tx, y + 17, sub, 12, "muted", 400, anchor)
    (HERE / f"{name}.svg").write_text(f.svg(title))


def login_message():
    """The captured login message as an SVG: one <text> per line, one <tspan>
    per colour run. Handles the escapes the message uses: reset, bold, dim and
    24-bit foreground colour."""
    import re
    raw = (HERE / "start-login-message.ansi").read_text()
    lines = raw.split("\n")
    last = max(i for i, l in enumerate(lines) if "Health" in l)
    lines = lines[: last + 1]
    cw, lh, pad = 7.83, 17, 16
    width = max(len(re.sub(r"\x1b\[[0-9;]*m", "", l)) for l in lines)
    w, h = int(width * cw + 2 * pad), len(lines) * lh + 2 * pad
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
           f'<title>The board\'s login message</title><rect width="{w}" height="{h}" rx="8" fill="#16161a"/>'
           f'<g font-family="{MONO}" font-size="13" xml:space="preserve" style="white-space:pre">']
    colour, bold, dim = "#e6e6ea", False, False
    for n, line in enumerate(lines):
        x, spans = 0, []
        for part in re.split(r"(\x1b\[[0-9;]*m)", line):
            m = re.fullmatch(r"\x1b\[([0-9;]*)m", part)
            if m:
                codes = [int(c) for c in m.group(1).split(";") if c] or [0]
                if codes[:2] == [38, 2]:
                    colour = "#%02x%02x%02x" % tuple(codes[2:5])
                for c in ([] if codes[:2] == [38, 2] else codes):
                    if c == 0:
                        colour, bold, dim = "#e6e6ea", False, False
                    elif c == 1:
                        bold = True
                    elif c == 2:
                        dim = True
                continue
            if not part:
                continue
            fill = "#8f8f99" if dim else colour
            # one <tspan> per run of non-space characters, each at its own
            # column: SVG collapses runs of spaces, and a fallback font's
            # glyphs are not exactly one column wide
            for run in re.finditer(r"\S+", part):
                text = run.group(0).replace("&", "&amp;").replace("<", "&lt;")
                spans.append(f'<tspan x="{pad + (x + run.start()) * cw:.1f}" '
                             f'textLength="{len(run.group(0)) * cw:.1f}" lengthAdjust="spacingAndGlyphs" '
                             f'fill="{fill}"{" font-weight=\"700\"" if bold else ""}>{text}</tspan>')
            x += len(part)
        out.append(f'<text y="{pad + 12 + n * lh}">{"".join(spans)}</text>')
    out.append("</g></svg>\n")
    (HERE / "start-login-message.svg").write_text("".join(out))


def main():
    both("start-r1-or-r2", "What tells a PlutoSky R2 from a PlutoSky R1", r1_or_r2)
    both("start-card", "The two partitions of the microSD card", card)
    both("start-connect", "Which of the PlutoSky R2's sockets goes where", connect)
    both("start-boot-switch", "The BOOT switch set to SD: both sliders away from ON", boot_switch)
    both("start-attenuator", "A transmit port joined to a receive port through an attenuator", attenuator)
    # For the pages that came with the R1's devkit and say so.
    both("start-loopback", "A transmit port joined to a receive port through a 20 dB attenuator", loopback)
    both("start-network", "The board's USB and Ethernet interfaces and their addresses", network)
    both("start-bootchain", "The boot chain, from BootROM to the root filesystem",
         row("", (("BootROM", "in silicon"), ("FSBL", "on-chip RAM"), ("bitstream", "into the FPGA"),
                  ("U-Boot", "in DDR"), ("kernel + DTB", "in DDR"), ("root filesystem", "RAM or ext4")), width=900, h=86))
    both("start-buildstages", "The seven build stages, in dependency order",
         row("", (("HDL", ""), ("bitstream", ""), ("FSBL", "needs the bitstream"), ("U-Boot", ""), ("kernel", ""),
                  ("root filesystem", ""), ("BOOT.bin", "the package")), width=1080, h=86))
    both("start-netconfig", "On Buildroot the address settings live in the U-Boot environment", netconfig)
    # photo_figure() and login_message() are the R1 repository's: their sources
    # (the R1's photographs, a captured login message) are not in this one.


if __name__ == "__main__":
    main()
