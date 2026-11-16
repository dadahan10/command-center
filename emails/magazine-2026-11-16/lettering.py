"""Brand headline lettering (Champie, DUALITY: one line Light, one line Bold) rendered to PNG at 2x.

Email clients do not load Champie, so every display headline is an image with the same words as alt text.
Champie is a TRIAL font: its digits render as watermark boxes, so a line containing a digit is refused here
(digits/prices are set in the HTML serif instead).
Each image is drawn on the exact ground colour of the band it sits in (not transparent), so a client that
inverts colours in dark mode still shows the lettering on its own ground.
Usage: python lettering.py  -> assets/h-*.png
"""
import os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONTS = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Microsoft", "Windows", "Fonts")  # per-user install (office PC)
LIGHT = os.path.join(FONTS, "CHAMPIETRIAL-LIGHT.TTF")
BOLD = os.path.join(FONTS, "CHAMPIETRIAL-BOLD.TTF")

SCALE = 2  # retina


def letter(name, lines, bg, width=520, size=78, leading=0.98, align="left", pad_top=4, pad_bottom=10):
    """lines: [(text, 'light'|'bold', hex colour)] -> assets/<name>.png, displayed at `width` css px."""
    for text, _, _ in lines:
        if re.search(r"\d", text):
            raise ValueError(f"Champie trial has no digits: {text!r}")
    W = width * SCALE
    fonts = {w: ImageFont.truetype(LIGHT if w == "light" else BOLD, size * SCALE) for w in ("light", "bold")}
    # shrink until the widest line fits
    while True:
        widths = [fonts[w].getlength(t) for t, w, _ in lines]
        if max(widths) <= W:
            break
        size -= 2
        fonts = {w: ImageFont.truetype(LIGHT if w == "light" else BOLD, size * SCALE) for w in ("light", "bold")}
    lh = int(size * SCALE * leading)
    asc, desc = fonts["bold"].getmetrics()
    H = pad_top * SCALE + lh * (len(lines) - 1) + asc + desc + pad_bottom * SCALE
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    y = pad_top * SCALE
    for (t, w, col), wd in zip(lines, widths):
        x = 0 if align == "left" else (W - wd) / 2 if align == "center" else W - wd
        d.text((x, y), t, font=fonts[w], fill=col)
        y += lh
    os.makedirs(ASSETS, exist_ok=True)
    im.save(os.path.join(ASSETS, name + ".png"), optimize=True)
    return name + ".png", width, H // SCALE


INK, SAND, BONE, PAPER, CREAM = "#0F1418", "#CFB288", "#F4EFE6", "#ECE5D8", "#F2EDE4"

SPECS = {
    # cover: on ink, sand light + cream bold
    "h-cover": dict(lines=[("Is this", "light", SAND), ("the one?", "bold", CREAM)], bg=INK, width=520, size=96),
    # still waiting: on sand, ink light + ink bold, centred
    "h-still": dict(lines=[("Still", "light", INK), ("waiting.", "bold", INK)], bg=SAND, width=520, size=120, align="center", leading=0.92),
    # affirm index: on ink
    "h-wear": dict(lines=[("Wear it now.", "light", CREAM), ("Pay over time.", "bold", SAND)], bg=INK, width=520, size=70),
    # letter: on bone
    "h-letter": dict(lines=[("My best", "light", INK), ("offer.", "bold", INK)], bg=BONE, width=300, size=64, pad_bottom=6),
}

def flat_logo():
    """The dark DUALITY logo flattened onto each light ground (bone, sand): a transparent dark logo vanishes when a
    mail app inverts a light email into dark mode; on its own ground it stays readable as a small light plate."""
    import io, urllib.request
    src = "https://cdn.klaviyomail.com/company/UEHusj/images/e5b28035-6172-4da3-aa10-3e6c4c63e266.png"
    logo = Image.open(io.BytesIO(urllib.request.urlopen(src).read())).convert("RGBA")
    for name, bg in (("logo-on-bone", BONE), ("logo-on-sand", SAND)):
        im = Image.new("RGBA", logo.size, bg)
        im.alpha_composite(logo)
        im.convert("RGB").save(os.path.join(ASSETS, name + ".png"), optimize=True)
        print(name, logo.size)


if __name__ == "__main__":
    for n, s in SPECS.items():
        print(letter(n, **s))
    flat_logo()
