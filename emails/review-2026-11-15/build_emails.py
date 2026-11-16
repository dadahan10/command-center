"""Two campaign emails for 17.11 and 19.11.2026 (Daniel 15.11: 2-3 emails a week, promotions everywhere).

Art: made for each email from our own catalog renders (cut out, graded, set on purpose-made grounds) and the
studs render; no AI jewelry. Prices = live Shopify price + compare-at (checked 15.11). Offers = only what is
live: 15% sale price, free 1 ct black diamond studs over $2,000, VIP list. No Archive, no BF %, no deadlines.

  python build_emails.py          -> art/*.jpg + e1-gift.html + e2-zodiac.html (+ preview PNGs via Playwright later)
Images are served from diana-rafael-remnant (GitHub Pages) at BASE, then copied into Klaviyo's CDN.
"""
import importlib.util, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WEEK = os.path.join(HERE, "..", "..", "social", "2026-11-16-week")
spec = importlib.util.spec_from_file_location("RW", os.path.join(WEEK, "render_week.py"))
RW = importlib.util.module_from_spec(spec); spec.loader.exec_module(RW)
R = RW.R
ART = os.path.join(HERE, "art"); os.makedirs(ART, exist_ok=True)
BASE = "https://dadahan10.github.io/diana-rafael-remnant/assets/email/2026-11-17/"
INK, SAND, CREAM = RW.INK, RW.SAND, RW.CREAM

# ------------------------------------------------------------------ art
def ground(w, h, color, glow, cy=.5, amt=.2, rad=.5):
    y, x = np.ogrid[:h, :w]
    r = np.sqrt(((x - w / 2) / w) ** 2 + ((y - h * cy) / w) ** 2) / rad
    g = np.clip(1 - r, 0, 1) ** 2 * amt
    a = np.array(color, float)[None, None] * (1 - g[..., None]) + np.array(glow, float)[None, None] * g[..., None]
    return Image.fromarray(a.astype(np.uint8)).convert("RGBA")


def place(base, cutname, cx, cy, maxw, maxh, shadow=.5):
    c = RW.cut(cutname)
    g = R.grade(c.convert("RGB"), warm=1.02, sat=1.04, con=1.08, bri=1.03).convert("RGBA"); g.putalpha(c.split()[3])
    s = min(maxw / g.width, maxh / g.height)
    g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0)); tmp.paste(g, (int(cx - g.width / 2), int(cy - g.height / 2)), g)
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh.putalpha(tmp.split()[3].filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * shadow)))
    base.alpha_composite(sh, (0, 16)); base.alpha_composite(tmp)
    return base


def words(img, lines):
    d = ImageDraw.Draw(img)
    W = img.width
    for (txt, wgt, size, col, y, track) in lines:
        f = R.font(wgt, size); fd = RW.dfont(wgt, size)
        fs = [fd if ch.isdigit() else f for ch in txt]
        ws = [d.textlength(ch, font=ff) for ch, ff in zip(txt, fs)]
        x = (W - sum(ws) - track * (len(txt) - 1)) / 2
        for ch, cw, ff in zip(txt, ws, fs):
            d.text((x, y - (size * .1 if ff is fd else 0)), ch, font=ff, fill=col)
            x += cw + track
    return img


def save(img, name):
    img.convert("RGB").save(os.path.join(ART, name), quality=88, optimize=True, progressive=True)


def art():
    # E1 hero: the studs, big, on ink, with the line in Champie
    h = ground(1200, 1300, INK, SAND, .55, .12)
    s = R.grade(Image.open(RW.STUDS).convert("RGB"), warm=1.02, con=1.08, bri=.96).resize((1200, 857), Image.LANCZOS)
    fy = np.clip(np.minimum(np.arange(857), 856 - np.arange(857)) / (857 * .16), 0, 1)[:, None]
    h.paste(s, (0, 300), Image.fromarray((np.ones((857, 1200)) * fy * 255).astype(np.uint8)))
    words(h, [("THE STUDS ARE ON US.", "BOLD", 86, SAND, 120, 5),
              ("1 ct natural black diamond studs, free over $2,000", "LIGHT", 44, CREAM, 1190, 1)])
    save(h, "e1-hero.jpg")
    for k in ["centauri-y", "selkie-y", "algol-r34", "spindle-y", "noireclipse", "hyades-r34"]:
        b = ground(600, 600, (20, 17, 16), SAND, .5, .16)
        place(b, k, 300, 300, 470, 470 if k != "noireclipse" else 540)
        save(b, f"e1-{k}.jpg")
    # E2: cream world, one tinted ground per element
    h = ground(1200, 1300, (243, 238, 230), (214, 185, 140), .5, .25, .6)
    pos = [(310, 470, "corcaroli-r34", "FIRE"), (890, 470, "pleiades-y", "EARTH"),
           (310, 980, "polaris-y", "AIR"), (890, 980, "selkie-w", "WATER")]
    for x, y, k, el in pos:
        place(h, k, x, y, 420, 330, .35)
    words(h, [("EVERY SIGN HAS A RING.", "BOLD", 74, INK, 70, 5)])
    d = ImageDraw.Draw(h)
    for x, y, k, el in pos:
        f = R.font("MEDIUM", 36); tw = d.textlength(el, font=f) + 8 * (len(el) - 1)
        xx = x - tw / 2
        for ch in el:
            d.text((xx, y + 200), ch, font=f, fill=(150, 118, 72)); xx += d.textlength(ch, font=f) + 8
    save(h, "e2-hero.jpg")
    tints = {"fire": ((44, 20, 14), (196, 98, 48), "corcaroli-r34"), "earth": ((236, 226, 208), (190, 160, 110), "pleiades-y"),
             "air": ((238, 240, 242), (200, 205, 214), "polaris-y"), "water": ((14, 30, 38), (70, 120, 140), "selkie-w")}
    for el, (c1, c2, k) in tints.items():
        b = ground(600, 600, c1, c2, .5, .35, .55)
        place(b, k, 300, 300, 480, 420, .45)
        save(b, f"e2-{el}.jpg")


# ------------------------------------------------------------------ html
SERIF = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "'Manrope','Helvetica Neue',Arial,sans-serif"
LOGO_W = "https://cdn.klaviyomail.com/company/UEHusj/images/245032aa-4e6c-4465-8342-06b38204a0d3.png"
LOGO_D = "https://cdn.klaviyomail.com/company/UEHusj/images/e5b28035-6172-4da3-aa10-3e6c4c63e266.png"
ICON = {"reviews": "https://cdn.klaviyomail.com/company/UEHusj/images/f219a773-84e2-4ae9-b781-f4afd211578c.png",
        "consult": "https://cdn.klaviyomail.com/company/UEHusj/images/5d386d70-74d1-4daa-ba1a-268e01fd11eb.png",
        "gift": "https://cdn.klaviyomail.com/company/UEHusj/images/b8e27243-6b8d-4da4-8319-184c449e0ed8.png",
        "pay": "https://cdn.klaviyomail.com/company/UEHusj/images/5d7c6a56-376f-4672-b5b5-2d2b1263b903.png",
        "diamond": "https://cdn.klaviyomail.com/company/UEHusj/images/3bf50158-05b4-4295-8e8c-2cf394472457.png"}
WA = "https://wa.me/97235755066"
BOOK = "https://dianarafael.com/pages/new-website-book-online-appointment"
REVIEWS = "https://dianarafael.com/pages/our-customers-reviews"
P = {"centauri": ("Centauri", "centauri-oval-natural-black-diamond-engagement-ring-side-stones", "Black oval, two side stones", 2600, 2210),
     "selkie": ("Selkie", "selkie-bypass-oval-natural-black-diamond-engagement-ring", "Black oval on a bypass", 2500, 2125),
     "algol": ("Algol", "algol-east-west-oval-natural-black-diamond-bezel-ring", "East-west oval in a bezel", 3600, 3060),
     "spindle": ("Spindle", "spindle-1-5-carat-cone-natural-black-diamond-lever-back-earrings", "1.5 ct pavé cone earrings", 3000, 2550),
     "noireclipse": ("Noir Eclipse", "noir-eclipse-natural-black-diamond-halo-pendant-with-necklace", "Halo pendant on its chain", 1400, 1190),
     "hyades": ("Hyades", "hyades-chevron-natural-black-diamond-contour-wedding-band", "Chevron band of black diamonds", 1800, 1530),
     "corcaroli": ("Cor Caroli", "cor-caroli-heart-natural-black-diamond-bezel-ring", "Black heart in a bezel", 2500, 2125),
     "pleiades": ("Pleiades", "pleiades-graduated-baguette-natural-black-diamond-ring", "Graduated black baguettes", 2000, 1700),
     "polaris": ("Polaris", "polaris-compass-natural-black-diamond-ring-baguettes", "A compass of black baguettes", 2000, 1700)}


def u(path, camp, content, extra=""):
    sep = "&amp;" if "?" in path else "?"
    return f"https://dianarafael.com{path}{sep}{extra}utm_source=klaviyo&amp;utm_medium=email&amp;utm_campaign={camp}&amp;utm_content={content}"


def money(v):
    return f"${v:,}"


T = {"dark": dict(bg="#0b0a09", card="#141110", text="#f4efe9", muted="#bdb3a7", accent="#c9a84c", rule="#2a2421",
                  btn_bg="#c9a84c", btn_fg="#1a1416", band="#1a1416", logo=LOGO_W),
     "light": dict(bg="#e9e3d9", card="#f6f2ec", text="#1f1b16", muted="#5d5449", accent="#9a7a3c", rule="#ddd3c4",
                   btn_bg="#1f1b16", btn_fg="#f6f2ec", band="#1f1b16", logo=LOGO_D)}


def btn(t, label, href, primary=True):
    th = T[t]
    if primary:
        return (f'<td align="center" bgcolor="{th["btn_bg"]}" style="background:{th["btn_bg"]};border-radius:2px;"><a href="{href}" target="_blank" '
                f'style="display:inline-block;padding:15px 26px;font-family:{SANS};font-size:12px;font-weight:700;letter-spacing:.14em;'
                f'text-transform:uppercase;color:{th["btn_fg"]};text-decoration:none;">{label}</a></td>')
    return (f'<td align="center" style="border:1px solid {th["accent"]};border-radius:2px;"><a href="{href}" target="_blank" '
            f'style="display:inline-block;padding:14px 24px;font-family:{SANS};font-size:12px;font-weight:700;letter-spacing:.14em;'
            f'text-transform:uppercase;color:{th["text"]};text-decoration:none;">{label}</a></td>')


def cbtn(t, label, href, primary=False):
    """Compact button that fits inside a 282px product card."""
    th = T[t]
    if primary:
        return (f'<td align="center" bgcolor="{th["btn_bg"]}" style="background:{th["btn_bg"]};border-radius:2px;"><a href="{href}" target="_blank" '
                f'style="display:inline-block;padding:11px 16px;font-family:{SANS};font-size:11px;font-weight:700;letter-spacing:.12em;'
                f'text-transform:uppercase;color:{th["btn_fg"]};text-decoration:none;">{label}</a></td>')
    return (f'<td align="center" style="border:1px solid {th["accent"]};border-radius:2px;"><a href="{href}" target="_blank" '
            f'style="display:inline-block;padding:10px 15px;font-family:{SANS};font-size:11px;font-weight:700;letter-spacing:.12em;'
            f'text-transform:uppercase;color:{th["text"]};text-decoration:none;">{label}</a></td>')


STUDS = "1-carats-round-diamond-earrings-1"   # Classic Martini 1 ct natural black diamond studs = the free gift


def buttons(t, items, pad="18px 32px 8px"):
    cells = "".join(f'<td class="col" style="padding:5px;"><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr>'
                    f'{btn(t, l, h, p)}</tr></table></td>' for l, h, p in items)
    return f'<tr><td align="center" style="padding:{pad};"><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr>{cells}</tr></table></td></tr>'


def eyebrow(t, txt, pad="30px 40px 0"):
    return (f'<tr><td align="center" style="padding:{pad};font-family:{SANS};font-size:12px;letter-spacing:.32em;font-weight:600;'
            f'text-transform:uppercase;color:{T[t]["accent"]};">{txt}</td></tr>')


def h1(t, txt, size=40, pad="14px 40px 6px"):
    return (f'<tr><td align="center" style="padding:{pad};"><h1 style="margin:0;font-family:{SERIF};font-size:{size}px;line-height:1.12;'
            f'font-weight:500;color:{T[t]["text"]};">{txt}</h1></td></tr>')


def para(t, html, pad="8px 48px 4px", size=16, color=None, align="center"):
    return (f'<tr><td align="{align}" style="padding:{pad};font-family:{SANS};font-size:{size}px;line-height:1.6;'
            f'color:{color or T[t]["text"]};">{html}</td></tr>')


def img_row(src, alt, href, w=600):
    return (f'<tr><td><a href="{href}" target="_blank"><img src="{src}" width="{w}" alt="{alt}" '
            f'style="display:block;width:100%;max-width:{w}px;height:auto;border:0;"/></a></td></tr>')


def card(t, key, img, camp, note=None, cta=None):
    th = T[t]; name, handle, desc, was, now = P[key]
    href = u(f"/products/{handle}", camp, f"card_{key}")
    n = (f'<div style="font-family:{SANS};font-size:11px;letter-spacing:.2em;font-weight:700;text-transform:uppercase;color:{th["accent"]};margin-top:6px;">{note}</div>'
         if note else "")
    return (f'<td class="col" width="50%" valign="top" style="padding:6px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="background:{th["card"]};"><tr><td><a href="{href}" target="_blank"><img src="{BASE}{img}" width="282" alt="{name}: {desc}" '
            f'style="display:block;width:100%;height:auto;border:0;"/></a></td></tr><tr><td align="center" style="padding:14px 10px 20px;">'
            f'<div style="font-family:{SERIF};font-size:24px;line-height:28px;color:{th["text"]};">{name}</div>'
            f'<div style="font-family:{SANS};font-size:13px;line-height:19px;color:{th["muted"]};margin-top:2px;">{desc}</div>'
            f'<div style="font-family:{SANS};font-size:16px;line-height:24px;color:{th["text"]};margin-top:8px;">'
            f'<span style="text-decoration:line-through;opacity:.55;">{money(was)}</span>&nbsp;&nbsp;<strong style="color:{th["accent"]};font-size:19px;">{money(now)}</strong></div>'
            f'{n}<table role="presentation" align="center" cellpadding="0" cellspacing="0" style="margin-top:14px;"><tr>'
            f'{cbtn(t, cta or "See " + name, u(f"/products/{handle}", camp, f"btn_{key}"))}</tr></table></td></tr></table></td>')


def grid(cells):
    rows = "".join(f'<tr><td style="padding:0 18px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>{"".join(cells[i:i + 2])}</tr></table></td></tr>'
                   for i in range(0, len(cells), 2))
    return rows


def trust(t):
    th = T[t]
    items = [("reviews", "550+ reviews", REVIEWS), ("consult", "Talk to Daniel", BOOK), ("gift", "Free studs over $2,000", None),
             ("pay", "Pay over time", None), ("diamond", "Natural diamonds", None)]
    cells = []
    for k, label, href in items:
        inner = (f'<img src="{ICON[k]}" width="40" height="40" alt="" style="display:block;margin:0 auto;width:40px;height:40px;border:0;"/>'
                 f'<div style="margin-top:8px;font-family:{SANS};font-size:11px;line-height:1.3;color:{th["text"]};">{label}</div>')
        if href:
            inner = f'<a href="{href}" target="_blank" style="text-decoration:none;">{inner}</a>'
        cells.append(f'<td align="center" valign="top" width="20%" style="width:20%;padding:0 4px;">{inner}</td>')
    return (f'<tr><td style="padding:26px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-top:1px solid {th["rule"]};border-bottom:1px solid {th["rule"]};"><tr><td style="padding:18px 0;">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>{"".join(cells)}</tr></table></td></tr></table></td></tr>')


def vip(t, camp):
    th = T[t]
    return (f'<tr><td style="padding:6px 32px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {th["accent"]};">'
            f'<tr><td align="center" style="padding:22px 24px;"><div style="font-family:{SANS};font-size:11px;letter-spacing:.3em;font-weight:700;'
            f'text-transform:uppercase;color:{th["accent"]};">The VIP list</div><div style="font-family:{SERIF};font-size:24px;line-height:1.25;color:{th["text"]};margin:8px 0 14px;">'
            f'Black Friday is coming. VIPs hear about every offer first.</div><table role="presentation" align="center" cellpadding="0" cellspacing="0"><tr>'
            f'{btn(t, "Join the VIP list", u("/", camp, "vip_join", "vip=join&amp;"), False)}</tr></table></td></tr></table></td></tr>')


def page(t, title, preheader, band, body, camp):
    th = T[t]
    return f"""<!DOCTYPE html>
<html dir="ltr" lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{title}</title>
<style>@media only screen and (max-width:620px){{.col{{display:block !important;width:100% !important}} h1{{font-size:32px !important}}}}</style></head>
<body style="margin:0;padding:0;background:{th["bg"]};">
<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{preheader}</div>
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="background:{th["bg"]};"><tr><td align="center" style="padding:24px 10px;">
<table role="presentation" width="600" border="0" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:{th["card"]};">
<tr><td align="center" style="background:{th["band"]};padding:10px 16px;font-family:{SANS};font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#c9a84c;">{band}</td></tr>
<tr><td align="center" style="padding:28px 40px 22px;"><a href="{u('/', camp, 'logo')}" target="_blank"><img src="{th["logo"]}" width="300" alt="Diana Rafael" style="display:block;width:300px;height:auto;border:0;"/></a></td></tr>
{body}
{trust(t)}
<tr><td style="padding:0 48px 30px;font-family:{SANS};font-size:13px;line-height:1.65;color:{th["muted"]};" align="center">
Every piece is made to order in our studio, in solid gold with natural diamonds, and ships within 10 business days, insured, with FedEx.<br/>
Questions? Reply to this email or <a href="{WA}" style="color:{th["accent"]};">WhatsApp us</a>. A real person answers, never an AI.</td></tr>
<tr><td align="center" style="padding:24px 40px 30px;background:{th["bg"]};font-family:{SANS};font-size:11px;color:{th["muted"]};line-height:1.6;">
23 Tuval St., Suite 10-01, Diamond Trading Center, Ramat-Gan, Israel 5252238<br/>9454 Wilshire Blvd M3, Beverly Hills, CA 90212<br/><br/>
No longer want to receive these emails? {{% unsubscribe %}}<br/>{{{{ organization.name }}}} {{{{ organization.full_address }}}}</td></tr>
<tr><td style="height:6px;line-height:6px;font-size:6px;background:#c9a84c;">&nbsp;</td></tr>
</table></td></tr></table></body></html>"""


def e1():
    t, camp = "dark", "2026-11-17-gift"
    body = "".join([
        img_row(BASE + "e1-hero.jpg", "Free 1 ct natural black diamond studs in yellow gold, with every order over $2,000", u("/collections/new-arrivals", camp, "hero")),
        buttons(t, [("See the free studs", u(f"/products/{STUDS}", camp, "btn_studs"), False)], "22px 32px 0"),
        h1(t, "The gift that comes<br/>with a gift.", pad="26px 40px 6px"),
        para(t, "Everything on dianarafael.com is already <strong>15% off</strong>, with the old price crossed out next to the new one.<br/>"
                "Spend $2,000 or more and we add a pair of <strong>1&nbsp;ct black diamond studs</strong> to the box, by hand. No code, nothing to remember."),
        buttons(t, [("Shop the gift edit", u("/collections/new-arrivals", camp, "cta_top"), True),
                    ("Ask us anything", WA + "?text=Hi%2C%20I%27m%20looking%20for%20a%20gift", False)]),
        eyebrow(t, "Over $2,000 · studs included", "34px 40px 14px"),
        grid([card(t, "centauri", "e1-centauri-y.jpg", camp, "+ free studs", "See the Centauri ring"),
              card(t, "selkie", "e1-selkie-y.jpg", camp, "+ free studs", "See the Selkie ring"),
              card(t, "algol", "e1-algol-r34.jpg", camp, "+ free studs", "See the Algol ring"),
              card(t, "spindle", "e1-spindle-y.jpg", camp, "+ free studs", "See the earrings")]),
        buttons(t, [("Choose your gift", u("/collections/new-arrivals", camp, "cta_over2000"), True)], "20px 32px 4px"),
        eyebrow(t, "Under $2,000 · still 15% off", "30px 40px 14px"),
        grid([card(t, "noireclipse", "e1-noireclipse.jpg", camp, None, "See the pendant"),
              card(t, "hyades", "e1-hyades-r34.jpg", camp, None, "See the Hyades band")]),
        eyebrow(t, "Quick question", "34px 40px 0"),
        h1(t, "A ring, or something that needs no size?", 28),
        buttons(t, [("A ring", u("/collections/all-engagement-rings", camp, "style_pick-ring", "style_pick=ring&amp;"), False),
                    ("Earrings or a pendant", u("/collections/black-ice-earring-collection", camp, "style_pick-nosize", "style_pick=nosize&amp;"), False)], "10px 32px 20px"),
        vip(t, camp),
        buttons(t, [("Shop the gift edit", u("/collections/new-arrivals", camp, "cta_bottom"), True),
                    ("Talk to Daniel", BOOK + "?utm_source=klaviyo&amp;utm_medium=email&amp;utm_campaign=" + camp + "&amp;utm_content=cta_book", False)],
                "22px 32px 4px"),
    ])
    return page(t, "The gift that comes with a gift",
                "Every piece is already 15% off. Over $2,000, black diamond studs come in the box, free.",
                "15% off every piece · Free black diamond studs over $2,000", body, camp)


def e2():
    t, camp = "light", "2026-11-19-zodiac"
    els = [("fire", "Fire", "Aries · Leo · Sagittarius", "She walks in first and laughs the loudest. A black heart, set bold, that doesn't apologise.", "corcaroli", True),
           ("earth", "Earth", "Taurus · Virgo · Capricorn", "Steady, exact, the one everybody calls. Graduated baguettes, lined up like a promise kept.", "pleiades", False),
           ("air", "Air", "Gemini · Libra · Aquarius", "Curious, quick, a little restless. A compass of black baguettes, for someone who always finds her way.", "polaris", False),
           ("water", "Water", "Cancer · Scorpio · Pisces", "Deep, intuitive, impossible to fool. An oval held by a bypass that moves like a tide.", "selkie", True)]
    th = T[t]
    blocks = []
    for k, el, signs, line, key, studs in els:
        name, handle, desc, was, now = P[key]
        href = u(f"/products/{handle}", camp, f"element_{k}")
        extra = (f'<div style="font-family:{SANS};font-size:11px;letter-spacing:.2em;font-weight:700;text-transform:uppercase;color:{th["accent"]};margin-top:8px;">+ free black diamond studs</div>' if studs else "")
        blocks.append(
            f'<tr><td style="padding:10px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#fbf9f5;"><tr>'
            f'<td class="col" width="50%" valign="middle"><a href="{href}" target="_blank"><img src="{BASE}e2-{k}.jpg" width="276" alt="{name}: {desc}" style="display:block;width:100%;height:auto;border:0;"/></a></td>'
            f'<td class="col" width="50%" valign="middle" style="padding:18px 22px;">'
            f'<div style="font-family:{SANS};font-size:11px;letter-spacing:.3em;font-weight:700;text-transform:uppercase;color:{th["accent"]};">{el}</div>'
            f'<div style="font-family:{SANS};font-size:12px;color:{th["muted"]};margin-top:4px;">{signs}</div>'
            f'<div style="font-family:{SERIF};font-size:20px;line-height:1.3;color:{th["text"]};margin-top:10px;">{line}</div>'
            f'<div style="font-family:{SANS};font-size:14px;color:{th["text"]};margin-top:12px;"><strong>{name}</strong> &nbsp;<span style="text-decoration:line-through;opacity:.55;">{money(was)}</span>'
            f'&nbsp; <strong style="color:{th["accent"]};">{money(now)}</strong></div>{extra}'
            f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin-top:14px;"><tr>{btn(t, "See the " + el + " ring", href, True)}</tr></table>'
            f'<div style="margin-top:10px;font-family:{SANS};font-size:12px;"><a href="{u(f"/products/{handle}", camp, f"link_{k}")}" target="_blank" style="color:{th["accent"]};">{name}: choose gold &amp; size &rarr;</a></div></td></tr></table></td></tr>')
    body = "".join([
        img_row(BASE + "e2-hero.jpg", "Four black diamond rings for fire, earth, air and water signs", u("/collections/new-arrivals", camp, "hero")),
        eyebrow(t, "Proposal season", "30px 40px 0"),
        h1(t, "Which ring is her sign?"),
        para(t, "The question we hear most this time of year: <em>which one is her?</em> Start with her element. "
                "Every ring here is already <strong>15% off</strong>, and two of them come with free black diamond studs."),
        buttons(t, [("Find her ring", u("/collections/new-arrivals", camp, "cta_top"), True),
                    ("All engagement rings", u("/collections/all-engagement-rings", camp, "cta_top_rings"), False)]),
        "".join(blocks),
        buttons(t, [("Shop the collection", u("/collections/new-arrivals", camp, "cta_after_elements"), True),
                    ("See the free studs", u(f"/products/{STUDS}", camp, "btn_studs"), False)], "18px 32px 4px"),
        para(t, "Not sure of her sign, or her size? Every ring is made to order in the gold you choose, and we can change the stone, the band or the finish.",
             pad="24px 48px 4px"),
        buttons(t, [("Book 15 minutes with Daniel", BOOK + "?utm_source=klaviyo&amp;utm_medium=email&amp;utm_campaign=" + camp, True),
                    ("WhatsApp us", WA + "?text=Hi%2C%20she%27s%20a%20", False)]),
        vip(t, camp),
        buttons(t, [("Choose her ring", u("/collections/all-engagement-rings", camp, "cta_bottom"), True)], "22px 32px 4px"),
    ])
    return page(t, "Which ring is her sign?",
                "Fire, earth, air or water. Four rings, four characters, all 15% off now.",
                "Proposal season · 15% off every ring · Free studs over $2,000", body, camp)


if __name__ == "__main__":
    if "html" not in sys.argv:
        art()
    open(os.path.join(HERE, "e1-gift.html"), "w", encoding="utf-8").write(e1())
    open(os.path.join(HERE, "e2-zodiac.html"), "w", encoding="utf-8").write(e2())
    print("ok")
