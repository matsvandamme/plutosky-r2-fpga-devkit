#!/usr/bin/env python3
"""Generate the GitHub cover images for the PlutoSky R2 repository.

    python3 docs/img/covers/generate-covers.py

writes, next to this file:

    devkit-stack-dark.png          2560x1280   README cover, dark theme
    devkit-stack-light.png         2560x1280   README cover, light theme
    devkit-stack-dark-social.png   1280x640    GitHub social preview
    devkit-stack-light-social.png  1280x640

in the VMAT brand: #4069FF, the four-quadrant mark, Bitter for display type
and IBM Plex Mono for the small print.

Each cover is an HTML page, built here and screenshotted with headless Chrome:

    "$CHROME" --headless=new --screenshot=OUT.png --window-size=2560,1280 \
        --hide-scrollbars --force-device-scale-factor=1 \
        --virtual-time-budget=15000 file:///.../cover.html

The -social files are the same page at --force-device-scale-factor=0.5. The
HTML is written to a temporary directory and not kept.

Needs Google Chrome (set CHROME to its binary if it is not in the macOS
default place) and a network connection: the two typefaces come from Google
Fonts. A render where they did not load is refused, not written in a fallback
serif. The logos are read from docs/img/vmat-logo-dark.png (white wordmark,
for the dark cover) and docs/img/vmat-logo.png (dark wordmark, for the light).
"""
import base64, os, pathlib, re, struct, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
IMG = HERE.parent
BLUE = "#4069FF"
W, H = 2560, 1280
CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
FONTS = ['800 124px Bitter', '700 46px Bitter', '600 38px Bitter',
         '400 28px "IBM Plex Mono"']

THEME = {
    "dark":  dict(bg="#0A0E14", bg2="#111823", ink="#F2F6FA", ink2="#93A3B5",
                  rule="#1E2936", logo="vmat-logo-dark.png"),
    "light": dict(bg="#FFFFFF", bg2="#F2F5F9", ink="#0B1220", ink2="#54677E",
                  rule="#DCE3EB", logo="vmat-logo.png"),
}


def _logo_img(t, size=100):
    b64 = base64.b64encode((IMG / t["logo"]).read_bytes()).decode()
    return (f'<img src="data:image/png;base64,{b64}" '
            f'style="height:{size}px;width:auto;display:block">')


def devkit_stack(t):
    """The layers, which is the thing nobody else gives you."""
    layers = [("bitstream", "Vivado 2022.2 &rarr; system_top.bit"),
              ("FSBL", "AMD embeddedsw + gcc-arm-none-eabi"),
              ("U-Boot", "distro cross-compiler"),
              ("kernel", "Linux 6.12, ADI drivers"),
              ("root filesystem", "Debian 13 armhf")]
    rows = ""
    for i, (name, sub) in enumerate(layers):
        y = 330 + i * 152
        rows += f"""
<div style="position:absolute;left:1180px;top:{y}px;width:1240px;height:120px;
     background:{t['bg2']};border:3px solid {t['rule']};border-left:14px solid {BLUE};
     border-radius:14px;display:flex;align-items:center;padding:0 46px;gap:34px">
  <div style="font-weight:700;font-size:46px;min-width:430px">{name}</div>
  <div class="mono" style="font-size:27px;color:{t['ink2']}">{sub}</div>
</div>"""
    return f"""
<div style="position:absolute;left:150px;top:190px;width:900px">
  <div class="mono" style="font-size:29px;letter-spacing:.30em;text-transform:uppercase;color:{BLUE};margin-bottom:34px;white-space:nowrap">
    PlutoSky&nbsp;R2 &middot; XC7Z020&#8209;CLG484
  </div>
  <div style="font-weight:800;font-size:124px;line-height:1.02;letter-spacing:-.022em">
    Every<br>layer,<br>from<br>source.
  </div>
  <div style="font-size:38px;line-height:1.5;color:{t['ink2']};margin-top:40px">
    The FPGA design, the boot loader, Linux&nbsp;6.12 and Debian, built for the&nbsp;R2.
  </div>
</div>
{rows}
<div style="position:absolute;left:150px;bottom:92px;display:flex;align-items:center;gap:40px">
  {_logo_img(t, 100)}
  <div class="mono" style="font-size:28px;color:{t['ink2']}">Zynq&nbsp;XC7Z020&#8209;CLG484 &middot; AD9361</div>
</div>"""


def page(theme):
    t = THEME[theme]
    checks = ",".join(f"document.fonts.check('{f}')" for f in FONTS)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{t['bg']};color:{t['ink']};
  font-family:Bitter,Georgia,serif;-webkit-font-smoothing:antialiased}}
.mono{{font-family:"IBM Plex Mono",monospace}}
.wrap{{position:relative;width:{W}px;height:{H}px}}
</style></head><body><div class="wrap">{devkit_stack(t)}</div>
<script>
const names = new Set([...document.fonts].map(f => f.family.replace(/"/g, '')));
Promise.all({FONTS!r}.map(f => document.fonts.load(f))).then(() => {{
  const ok = [{checks}].every(Boolean) && names.has('Bitter') && names.has('IBM Plex Mono');
  document.body.setAttribute('data-fonts', ok ? 'ok' : 'missing');
}});
</script>
</body></html>"""


def chrome(profile, *args):
    cmd = [CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu",
           "--no-first-run", f"--user-data-dir={profile}",
           f"--window-size={W},{H}", "--virtual-time-budget=15000", *args]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def png_size(path):
    head = path.read_bytes()[:24]
    return struct.unpack(">II", head[16:24])


def render():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME} (set CHROME=/path/to/chrome)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for theme in THEME:
            html = tmp / f"devkit-stack-{theme}.html"
            html.write_text(page(theme))
            url = html.as_uri()
            dom = chrome(tmp / "profile", "--dump-dom", url)
            if not re.search(r'data-fonts="ok"', dom):
                sys.exit(f"{theme}: Bitter / IBM Plex Mono did not load "
                         "(no network?) - nothing written")
            for suffix, scale in (("", 1), ("-social", 0.5)):
                out = HERE / f"devkit-stack-{theme}{suffix}.png"
                chrome(tmp / "profile", f"--screenshot={out}",
                       f"--force-device-scale-factor={scale}", url)
                want = (int(W * scale), int(H * scale))
                got = png_size(out)
                if got != want:
                    sys.exit(f"{out.name}: {got[0]}x{got[1]}, expected {want[0]}x{want[1]}")
                print(f"  wrote {out.name}  {got[0]}x{got[1]}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    render()
