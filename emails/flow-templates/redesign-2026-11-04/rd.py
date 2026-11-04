"""Shared pieces for the 4.11.2026 flow-email redesign (one purpose-made image + layout per email).

Every email is built from these blocks, but each email picks its own theme (noir / ink / bone / paper) and
its own hero treatment, so the 29 emails do not share one look. Copy (body text) is carried over from the
approved 3.11 templates, including the corrected return-policy wording.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = json.load(open(os.path.join(HERE, "images.json"), encoding="utf-8"))

SERIF = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "'Manrope','Helvetica Neue',Arial,sans-serif"
GOLD = "#b08d3c"
GOLD_LT = "#d4b26a"

THEMES = {
    # outer bg, card bg, text, muted, accent, rule, logo
    "noir":  dict(outer="#0b0a09", card="#121110", text="#efe8dc", muted="#a69c8c", accent=GOLD_LT, rule="#2a2622", logo="logo-duality-white", btn_bg=GOLD, btn_fg="#121110"),
    "ink":   dict(outer="#1a1917", card="#22201d", text="#efe8dc", muted="#b3a998", accent=GOLD_LT, rule="#3a352f", logo="logo-duality-white", btn_bg=GOLD_LT, btn_fg="#1a1917"),
    "bone":  dict(outer="#efe9df", card="#fbf8f3", text="#1f1b16", muted="#5c544a", accent="#7a5d1e", rule="#e2d8c6", logo="logo-duality-dark", btn_bg="#1f1b16", btn_fg="#fbf8f3"),
    "paper": dict(outer="#e9e4da", card="#f6f1e7", text="#2a241d", muted="#5c544a", accent="#7a5d1e", rule="#ddd2bf", logo="logo-duality-dark", btn_bg=GOLD, btn_fg="#1f1b16"),
}

ADDRESS = ("23 Tuval St., Suite 10-01, Diamond Trading Center, Ramat-Gan, Israel 5252238<br/>"
           "9454 Wilshire Blvd M3, Beverly Hills, CA 90212")


def head(t, preheader=""):
    th = THEMES[t]
    pre = (f'<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;'
           f'color:{th["outer"]};opacity:0;">{preheader}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>') if preheader else ""
    return f"""<!DOCTYPE html>
<html dir="ltr" lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<meta content="light only" name="color-scheme"/><meta content="light only" name="supported-color-schemes"/><title>Diana Rafael</title>
<style>
body{{margin:0;padding:0;background:{th['outer']};}}
a{{color:{th['accent']};}}
.u,.unsubscribe-link{{color:{th['muted']} !important;text-decoration:underline;}}
@media only screen and (max-width:620px){{
 .pad{{padding-left:24px !important;padding-right:24px !important;}}
 .h1{{font-size:34px !important;line-height:1.1 !important;}}
 .big{{font-size:120px !important;}}
 .col{{display:block !important;width:100% !important;}}
 .colpad{{padding:0 0 18px 0 !important;}}
}}
</style></head>
<body style="margin:0;padding:0;background:{th['outer']};">{pre}
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{th['outer']}" style="background:{th['outer']};">
<tr><td align="center" style="padding:20px 8px;">
<table role="presentation" width="600" border="0" cellpadding="0" cellspacing="0" bgcolor="{th['card']}" style="width:100%;max-width:600px;background:{th['card']};">
"""


def kicker(t, text, align="center", pad="22px 40px 0"):
    th = THEMES[t]
    return (f'<tr><td align="{align}" class="pad" style="padding:{pad};font-family:{SANS};font-size:11px;letter-spacing:.28em;'
            f'text-transform:uppercase;font-weight:700;color:{th["accent"]};">{text}</td></tr>')


def logo(t, pad="22px 40px 22px", width=200, align="center"):
    th = THEMES[t]
    return (f'<tr><td align="{align}" class="pad" style="padding:{pad};"><a href="https://dianarafael.com/" target="_blank">'
            f'<img src="{IMG[th["logo"]]}" width="{width}" alt="Diana Rafael" style="display:block;width:{width}px;height:auto;border:0;"/></a></td></tr>')


def hero(src, alt, href=None, pad="0", radius=0, width=600, bg=None):
    img = (f'<img src="{src}" width="{width}" alt="{alt}" style="display:block;width:100%;max-width:{width}px;height:auto;border:0;'
           f'{"border-radius:%dpx;" % radius if radius else ""}"/>')
    if href:
        img = f'<a href="{href}" target="_blank">{img}</a>'
    bgs = f'background:{bg};' if bg else ''
    return f'<tr><td align="center" style="padding:{pad};{bgs}">{img}</td></tr>'


def h1(t, text, align="center", pad="34px 48px 10px", size=40, italic=False):
    th = THEMES[t]
    return (f'<tr><td align="{align}" class="pad" style="padding:{pad};"><h1 class="h1" style="margin:0;font-family:{SERIF};'
            f'font-size:{size}px;line-height:1.12;font-weight:500;{"font-style:italic;" if italic else ""}color:{th["text"]};">{text}</h1></td></tr>')


def body(t, html, pad="8px 48px 6px", align="left", size=16):
    th = THEMES[t]
    html = html.replace("<p>", f'<p style="margin:0 0 14px;font-family:{SANS};font-size:{size}px;line-height:1.65;color:{th["text"]};">')
    return f'<tr><td class="pad" align="{align}" style="padding:{pad};font-family:{SANS};font-size:{size}px;line-height:1.65;color:{th["text"]};">{html}</td></tr>'


def button(t, label, href, pad="18px 40px 30px", align="center"):
    th = THEMES[t]
    return (f'<tr><td align="{align}" class="pad" style="padding:{pad};"><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td align="center" bgcolor="{th["btn_bg"]}" style="background:{th["btn_bg"]};border-radius:2px;">'
            f'<a href="{href}" target="_blank" style="display:inline-block;padding:15px 34px;font-family:{SANS};font-size:13px;font-weight:700;'
            f'letter-spacing:.16em;text-transform:uppercase;color:{th["btn_fg"]};text-decoration:none;">{label}</a></td></tr></table></td></tr>')


def signoff(t, line="With care,", pad="6px 48px 30px", align="left"):
    th = THEMES[t]
    return (f'<tr><td class="pad" align="{align}" style="padding:{pad};"><p style="margin:0 0 6px;font-family:{SERIF};font-style:italic;font-size:22px;'
            f'line-height:1.4;color:{th["text"]};">{line}</p><p style="margin:0;font-family:{SANS};font-size:14px;letter-spacing:.04em;'
            f'color:{th["accent"]};">Daniel, Diana Rafael</p></td></tr>')


def rule(t, pad="0 48px"):
    th = THEMES[t]
    return f'<tr><td class="pad" style="padding:{pad};"><div style="height:1px;line-height:1px;font-size:1px;background:{th["rule"]};">&nbsp;</div></td></tr>'


def spacer(h):
    return f'<tr><td style="height:{h}px;line-height:{h}px;font-size:1px;">&nbsp;</td></tr>'


def trust(t, pad="20px 40px 6px"):
    th = THEMES[t]
    a = f'style="color:{th["accent"]};text-decoration:underline;"'
    return (f'<tr><td align="center" class="pad" style="padding:{pad};font-family:{SANS};font-size:12px;line-height:1.8;color:{th["muted"]};">'
            f'Insured express shipping, paid by us · <a {a} href="https://dianarafael.com/pages/new-website-jewelry-care-program" target="_blank">Lifetime care</a>'
            f' · Diamond &amp; gold certificate · <a {a} href="https://dianarafael.com/pages/our-customers-reviews" target="_blank">530+ reviews</a></td></tr>'
            f'<tr><td align="center" class="pad" style="padding:2px 40px 24px;font-family:{SANS};font-size:13px;color:{th["text"]};">Questions? '
            f'<a {a} href="https://dianarafael.com/pages/new-website-book-online-appointment" target="_blank">15 minutes with Daniel</a> or '
            f'<a {a} href="https://wa.me/97235755066" target="_blank">WhatsApp</a></td></tr>')


def foot(t):
    th = THEMES[t]
    dark = t in ("noir", "ink")
    fbg = "#0b0a09" if dark else "#e6dfd2"
    return (f'<tr><td align="center" bgcolor="{fbg}" style="background:{fbg};padding:26px 36px 30px;font-family:{SANS};">'
            f'<div style="font-family:{SERIF};font-size:22px;font-weight:600;color:{th["accent"]};">Diana Rafael</div>'
            f'<div style="font-size:12px;line-height:1.6;color:{th["muted"]};margin-top:10px;">{ADDRESS}</div>'
            f'<div style="font-size:12px;color:{th["muted"]};margin-top:10px;">No longer want to receive these emails? {{% unsubscribe \'Unsubscribe\' %}}</div>'
            f'</td></tr><tr><td bgcolor="{GOLD}" style="height:4px;line-height:4px;font-size:4px;background:{GOLD};">&nbsp;</td></tr>'
            f'</table></td></tr></table></body></html>')
