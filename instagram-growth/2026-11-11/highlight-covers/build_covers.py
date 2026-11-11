"""Instagram Story Highlight covers — Diana Rafael (DUALITY identity).

Direction A: thin-line custom SVG icons, alternating sand / ink covers.
Direction B: typographic — Champie (Light + Bold duality) with the real brand star.

Renders 1080x1920 PNGs via Playwright (Chromium) and a contact-sheet board.png.
Brand sources:
  star  = Dropbox/שיווק Marketing/DUALITY REBRANDING 2025/Logos/Group (2).svg  (copied to brand-star.svg)
  fonts = DUALITY REBRANDING 2025/FOBTS פונטים/CHAMPIETRIAL-*.TTF            (copied to fonts/)
  sand  = #D6B98C (fill in the logo SVG + palette.txt "Light Stone"), ink = #0F1418 (DUALITY letterhead)
Run:  python build_covers.py
"""
import base64
import math
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SAND = "#D6B98C"
INK = "#0F1418"

# order = profile order (after the 11.11 renames) + 3 new highlights
TOPICS = [
    ("reviews", "Reviews"),
    ("ready-to-ship", "Ready to Ship"),
    ("black-diamonds", "Black Diamonds"),
    ("ring-care", "Ring Care"),
    ("shop", "Shop"),
    ("rings", "Rings"),
    ("diamonds", "Diamonds"),
    ("jewelry", "Jewelry"),
    ("in-the-making", "In The Making"),
    ("our-clients", "Our Clients"),
    ("sale", "Sale"),
    ("remnant", "REMNANT"),
    ("made-to-order", "Made to Order"),
]


def is_light(i):
    return i % 2 == 0  # DUALITY: alternate sand / ink along the row


# ---------- Direction A: icons (viewBox 0 0 120 120, stroke = currentColor) ----------
def sparkle(cx, cy, r, k=0.22):
    """Concave 4-point star echoing the brand mark (long vertical, shorter horizontal)."""
    h = r * 0.62
    q = r * k
    return (f"M{cx} {cy-r} Q{cx+q} {cy-q} {cx+h} {cy} Q{cx+q} {cy+q} {cx} {cy+r} "
            f"Q{cx-q} {cy+q} {cx-h} {cy} Q{cx-q} {cy-q} {cx} {cy-r} Z")


DIAMOND = "M42 34 H78 L90 46 L60 92 L30 46 Z"
DIAMOND_FACETS = "M30 46 H90 M42 34 L50 46 L60 34 L70 46 L78 34 M50 46 L60 92 L70 46"


def shards():
    polys = [
        ([(42, 34), (58, 34), (54, 48), (64, 62), (60, 92), (30, 46)], (-5, 1)),
        ([(58, 34), (78, 34), (90, 46), (72, 50), (54, 48)], (5, -5)),
        ([(54, 48), (72, 50), (90, 46), (60, 92), (64, 62)], (6, 5)),
    ]
    out = []
    for pts, (dx, dy) in polys:
        d = "M" + " L".join(f"{x+dx} {y+dy}" for x, y in pts) + " Z"
        out.append(f'<path d="{d}"/>')
    return "".join(out)


def pencil():
    body = ('<g transform="rotate(45 60 60) translate(0 -6)">'
            '<path d="M53 18 H67 V76 L60 94 L53 76 Z"/>'
            '<path d="M53 28 H67 M53 76 H67"/></g>')
    return body + f'<path d="{sparkle(30, 92, 11)}" fill="currentColor" stroke="none"/>'


ICONS = {
    "reviews": (
        '<path d="M30 32 H90 A6 6 0 0 1 96 38 V72 A6 6 0 0 1 90 78 H56 L40 92 V78 H30 A6 6 0 0 1 24 72 V38 A6 6 0 0 1 30 32 Z"/>'
        f'<path d="{sparkle(60, 55, 14)}" fill="currentColor" stroke="none"/>'),
    "ready-to-ship": (
        '<rect x="32" y="52" width="56" height="42"/><rect x="27" y="40" width="66" height="12"/>'
        '<path d="M60 40 V94"/>'
        '<path d="M60 40 C52 26 38 28 42 37 C44 41 54 41 60 40 C66 41 76 41 78 37 C82 28 68 26 60 40 Z"/>'),
    "black-diamonds": (
        f'<path d="{DIAMOND}" fill="currentColor"/>'
        f'<path d="{DIAMOND_FACETS}" stroke="BGCOLOR" stroke-width="2.4"/>'),
    "ring-care": (
        '<path d="M58 28 C58 28 34 58 34 74 A24 24 0 0 0 82 74 C82 58 58 28 58 28 Z"/>'
        '<path d="M46 76 A12 12 0 0 0 58 88"/>'
        f'<path d="{sparkle(88, 34, 13)}" fill="currentColor" stroke="none"/>'),
    "shop": (
        '<path d="M32 46 H88 L84 94 H36 Z"/><path d="M47 46 V40 A13 13 0 0 1 73 40 V46"/>'),
    "rings": (
        '<circle cx="60" cy="76" r="24"/>'
        '<path d="M49 41 L54 33 H66 L71 41 L60 52 Z M49 41 H71"/>'),
    "diamonds": f'<path d="{DIAMOND}"/><path d="{DIAMOND_FACETS}" stroke-width="2.6"/>',
    "jewelry": (
        '<path d="M28 26 C32 56 46 68 60 70 C74 68 88 56 92 26"/><path d="M60 70 V76"/>'
        f'<path d="{sparkle(60, 90, 14)}" fill="currentColor" stroke="none"/>'),
    "in-the-making": (
        '<circle cx="60" cy="28" r="5"/><path d="M57 33 L40 92 M63 33 L80 92"/>'
        '<path d="M44 78 Q60 86 76 78"/>'),
    "our-clients": '<circle cx="48" cy="62" r="22"/><circle cx="72" cy="62" r="22"/>',
    "sale": (
        '<path d="M26 60 L47 37 H92 V83 H47 Z"/><circle cx="46" cy="60" r="4.5"/>'),
    "remnant": shards(),
    "made-to-order": pencil(),
}


def icon_svg(key, fg, bg, size=680, sw=4.2):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="{size}" height="{size}" '
            f'style="color:{fg};--bg:{bg}" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[key].replace("BGCOLOR", bg)}</svg>')


# ---------- Direction B: typography ----------
WORDS = {  # (light part, bold part) — DUALITY: one Light, one Bold
    "reviews": ("", "Reviews"),
    "ready-to-ship": ("Ready", "to ship"),
    "black-diamonds": ("Black", "diamonds"),
    "ring-care": ("Ring", "care"),
    "shop": ("", "Shop"),
    "rings": ("", "Rings"),
    "diamonds": ("", "Diamonds"),
    "jewelry": ("", "Jewelry"),
    "in-the-making": ("In the", "making"),
    "our-clients": ("Our", "clients"),
    "sale": ("", "Sale"),
    "remnant": ("", "REMNANT"),
    "made-to-order": ("Made", "to order"),
}


def font_face():
    css = []
    for name, w in (("CHAMPIE-LIGHT.ttf", 300), ("CHAMPIE-MEDIUM.ttf", 500), ("CHAMPIE-BOLD.ttf", 700)):
        b = base64.b64encode((HERE / "fonts" / name).read_bytes()).decode()
        css.append(f"@font-face{{font-family:Champie;font-weight:{w};src:url(data:font/ttf;base64,{b})}}")
    return "".join(css)


STAR_SRC = (HERE / "brand-star.svg").read_text(encoding="utf-8")


def brand_star(color, width):
    s = STAR_SRC.replace("#D6B98C", color)
    return re.sub(r'width="299" height="283"', f'width="{width}" height="{round(width*283/299)}"', s, count=1)


def cover_html(direction, key, i):
    light = is_light(i)
    bg, fg = (SAND, INK) if light else (INK, SAND)
    if direction == "A":
        inner = icon_svg(key, fg, bg)
    else:
        lt, bd = WORDS[key]
        size = 300  # shrunk to fit by the script below
        lines = ""
        if lt:
            lines += f'<div style="font-weight:300;font-size:{size}px;line-height:1">{lt}</div>'
            lines += f'<div style="font-weight:700;font-size:{size}px;line-height:1.02">{bd}</div>'
        else:
            lines += f'<div style="font-weight:700;font-size:{size}px;line-height:1">{bd}</div>'
        inner = (f'<div style="display:flex;flex-direction:column;align-items:center;gap:34px">'
                 f'{brand_star(fg, 170)}<div id="t" style="text-align:center;letter-spacing:.01em">{lines}</div></div>'
                 "<script>document.fonts.ready.then(()=>{const t=document.getElementById('t');"
                 "for(const d of t.children){d.style.display='inline-block'}"
                 "let w=Math.max(...[...t.children].map(d=>d.getBoundingClientRect().width));"
                 "const lim=t.children.length>1?700:740;const f=Math.min(1,lim/w)*300;"
                 "for(const d of t.children){d.style.display='block';d.style.fontSize=f+'px'}"
                 "document.body.dataset.ready=1})</script>")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}"
            f"html,body{{margin:0;width:1080px;height:1920px;background:{bg};color:{fg};font-family:Champie}}"
            f"body{{display:flex;align-items:center;justify-content:center}}</style></head>"
            f"<body>{inner}</body></html>")


FONTS = font_face()


def board_html(paths_by_dir):
    def row(direction, theme):
        bgc, txt, ring = (("#FFFFFF", "#000000", "#DBDBDB") if theme == "light" else ("#000000", "#F5F5F5", "#363636"))
        items = "".join(
            f'<div class="hl"><div class="ring" style="border-color:{ring}">'
            f'<div class="c" style="background-image:url(data:image/png;base64,{b64})"></div></div>'
            f'<div class="lb" style="color:{txt}">{label}</div></div>'
            for (label, b64) in paths_by_dir[direction])
        small = "".join(
            f'<div class="c60" style="background-image:url(data:image/png;base64,{b64})"></div>'
            for (_, b64) in paths_by_dir[direction])
        return (f'<section style="background:{bgc}"><h2 style="color:{txt}">Direction {direction} — '
                f'{"thin-line icons" if direction=="A" else "typographic"} · {theme} app</h2>'
                f'<div class="row">{items}</div><div class="row60">{small}<span style="color:{txt}">← 60px check</span></div></section>')

    return (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            "body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}"
            "section{padding:30px 40px 34px}h2{margin:0 0 22px;font-size:20px;font-weight:600}"
            ".row{display:flex;gap:22px}.hl{width:124px;display:flex;flex-direction:column;align-items:center}"
            ".ring{width:118px;height:118px;border:1.5px solid;border-radius:50%;display:flex;align-items:center;justify-content:center;box-sizing:border-box}"
            ".c{width:110px;height:110px;border-radius:50%;background-size:110px auto;background-position:center}"
            ".lb{margin-top:8px;font-size:12px;white-space:nowrap}"
            ".row60{display:flex;gap:14px;align-items:center;margin-top:22px;font-size:12px}"
            ".c60{width:60px;height:60px;border-radius:50%;background-size:60px auto;background-position:center}"
            "</style></head><body>"
            + row("A", "light") + row("A", "dark") + row("B", "light") + row("B", "dark") +
            "</body></html>")


def crop_circle_b64(png_path):
    """Centre 1080x1080 of the 1080x1920 story = what Instagram puts in the highlight circle."""
    from io import BytesIO
    from PIL import Image
    im = Image.open(png_path).crop((0, 420, 1080, 1500)).resize((330, 330), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def main():
    by_dir = {"A": [], "B": []}
    with sync_playwright() as p:
        br = p.chromium.launch()
        page = br.new_page(viewport={"width": 1080, "height": 1920})
        for d in ("A", "B"):
            for i, (key, label) in enumerate(TOPICS):
                out = HERE / d / f"{i+1:02d}-{key}.png"
                page.set_content(cover_html(d, key, i))
                page.evaluate("document.fonts.ready")
                if d == "B":
                    page.wait_for_selector("body[data-ready]")
                page.screenshot(path=str(out))
                by_dir[d].append((label, crop_circle_b64(out)))
                print("wrote", out.relative_to(HERE))
        bp = br.new_page(viewport={"width": len(TOPICS) * 146 + 80, "height": 400})
        bp.set_content(board_html(by_dir))
        bp.evaluate("document.fonts.ready")
        bp.screenshot(path=str(HERE / "board.png"), full_page=True)
        print("wrote board.png")
        br.close()


if __name__ == "__main__":
    main()
