"""Diana Rafael 'Black & White' magazine emails, 16.11.2026. PREVIEW ONLY: nothing here is pushed to Klaviyo.

The 5 emails of the live Black Ice checkout flow XW6UqR, redesigned as one magazine issue: one masthead, one
type system (Champie lettering as images + Cormorant/Manrope stacks), one palette (ink #0F1418 / sand #CFB288 /
bone), but a different editorial layout in every email, so no two consecutive emails share a hero structure:

  1  RGSj5h  Cover story      ink ground, Champie cover line, the piece full-bleed, cover lines under it
  2  U3FYQZ  Split spread     black | bone diptych: a giant 5% on ink beside the piece on bone
  3  TDAQrS  Pull quote       sand ground, 'Still waiting.' set huge, the piece as a captioned still life
  4  Re9UiL  The index        ink contents page: every line item + the 5%, Affirm and gifts as entries
  5  UNZFjJ  Editor's letter  bone letter from Daniel with drop cap and signature, the piece as a postcard

Copy, codes, links and the event variables are carried over from live-fix-2026-11-15/build_live.py (15.11).
Images: the customer's own piece from the event, the real studs photos already in Klaviyo, Champie lettering
rendered by lettering.py into assets/ (referenced as ../assets/ for the preview; swap ASSET_BASE for the
hosted URLs before any rollout).
Usage: python lettering.py && python build.py   -> out/<n>-<template_id>.html
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
ASSET_BASE = os.environ.get("ASSET_BASE", "../assets/")

# ---------------------------------------------------------------- palette + type (DUALITY)
INK, INK2 = "#0F1418", "#1A2127"          # ground + one tone step for surfaces on ink
SAND, SAND_TXT = "#CFB288", "#7A5D2E"     # sand field / sand used as small text on light grounds (AA)
BONE, PAPER, CREAM = "#F4EFE6", "#ECE5D8", "#F2EDE4"
MUTE_D, MUTE_L = "#A9A296", "#564F46"     # secondary text on ink / on light
SERIF = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "'Manrope','Helvetica Neue',Helvetica,Arial,sans-serif"

LOGO_W = "https://cdn.klaviyomail.com/company/UEHusj/images/245032aa-4e6c-4465-8342-06b38204a0d3.png"
LOGO_D = "https://cdn.klaviyomail.com/company/UEHusj/images/e5b28035-6172-4da3-aa10-3e6c4c63e266.png"
STUDS_BLACK = "https://cdn.klaviyomail.com/company/UEHusj/images/d40d6d65-4a9c-4977-ad32-43b1fcbc87b2.jpeg"
STUDS_WHITE = "https://cdn.klaviyomail.com/company/UEHusj/images/66a849f8-e6f6-4cd4-8415-36c8f1ef8dd1.jpeg"

WA = "https://wa.me/97235755066"
BOOK = "https://dianarafael.com/pages/new-website-book-online-appointment"
REVIEWS = "https://dianarafael.com/pages/our-customers-reviews"
CARE = "https://dianarafael.com/pages/new-website-jewelry-care-program"
ADDRESS = ("23 Tuval St., Suite 10-01, Diamond Trading Center, Ramat-Gan, Israel 5252238<br/>"
           "9454 Wilshire Blvd M3, Beverly Hills, CA 90212")

# ---------------------------------------------------------------- Klaviyo variables (exactly as live, 15.11)
CHK = "{{ event.extra.responsive_checkout_url|default:'https://dianarafael.com/cart' }}"
VALUE = "event|lookup:'$value'"
ITEM_IMG = ("{% if item.product.variant.images.0.src %}{{ item.product.variant.images.0.src }}"
            "{% else %}{{ item.product.images.0.src }}{% endif %}")
ITEM_URL = "https://dianarafael.com/products/{{ item.product.handle }}"
FIRST = "{% for item in event.extra.line_items %}{% if forloop.first %}"
FIRST_END = "{% endif %}{% endfor %}"
HAS_IMG = "{% if item.product.variant.images.0.src or item.product.images.0.src %}"
HI = "{% if first_name %}Hi {{ first_name }}, {% else %}Hi, {% endif %}"


def nm(after, alone):
    """'Katherine, <after>' when we know her name, otherwise <alone>."""
    return "{% if first_name %}{{ first_name }}, " + after + "{% else %}" + alone + "{% endif %}"


def apply_url(code):
    # Shopify shareable discount link: sets the code, then returns her to her own saved checkout (live format)
    return ("https://dianarafael.com/discount/" + code + "?redirect="
            "{% if event.extra.responsive_checkout_url %}{{ event.extra.responsive_checkout_url|slice:'23:'|urlencode }}{% else %}%2Fcart{% endif %}")


def wa(text):
    return WA + "?text=" + text.replace(" ", "%20").replace(",", "%2C").replace("'", "%27").replace("?", "%3F")


ASK = wa("Hi Daniel, I have a question about my order.")
QUALIFIES = "{% if " + VALUE + " >= 2000 %}Your order already qualifies.{% else %}With orders from $2,000.{% endif %}"

# ---------------------------------------------------------------- frame
def head(ground, pre):
    return f"""<!DOCTYPE html>
<html dir="ltr" lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/><meta name="x-apple-disable-message-reformatting"/>
<meta content="light only" name="color-scheme"/><meta content="light only" name="supported-color-schemes"/>
<title>Diana Rafael</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&amp;family=Manrope:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<style>
body{{margin:0;padding:0;background:{ground};-webkit-text-size-adjust:100%;}}
td,div,span{{font-variant-numeric:lining-nums;}}
img{{border:0;outline:none;text-decoration:none;}}
a{{text-decoration:none;}}
.u,.unsubscribe-link{{color:inherit !important;text-decoration:underline;}}
@media only screen and (max-width:540px){{
 .pad{{padding-left:22px !important;padding-right:22px !important;}}
 .col{{display:block !important;width:100% !important;max-width:100% !important;}}
 .colpad{{padding:0 0 14px 0 !important;}}
 .fluid{{width:100% !important;max-width:100% !important;height:auto !important;}}
 .giant{{font-size:118px !important;}}
 .h2{{font-size:28px !important;}}
 .lead{{font-size:17px !important;}}
 .hide-m{{display:none !important;}}
 .tc{{text-align:center !important;}}
 .btn a{{display:block !important;}}
}}
</style></head>
<body style="margin:0;padding:0;background:{ground};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{ground};opacity:0;">{pre}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{ground}" style="background:{ground};">
<tr><td align="center" style="padding:0;">
<table role="presentation" width="600" border="0" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;">
"""


def tail():
    return "</table></td></tr></table></body></html>"


def duality_bar(h=6, dark=False):
    """The issue's signature: half black/white, half sand, at the top of every email and under the footer.
    The first half is always the opposite of the ground, so the bar reads on ink and on bone alike."""
    first = CREAM if dark else INK
    return (f'<tr><td style="padding:0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td width="50%" bgcolor="{first}" style="background:{first};height:{h}px;line-height:{h}px;font-size:1px;">&nbsp;</td>'
            f'<td width="50%" bgcolor="{SAND}" style="background:{SAND};height:{h}px;line-height:{h}px;font-size:1px;">&nbsp;</td>'
            f'</tr></table></td></tr>')


def masthead(bg, dark):
    """One masthead for the whole issue: logo left, the issue's name right, on the email's own ground."""
    logo = LOGO_W if dark else ASSET_BASE + ("logo-on-sand.png" if bg == SAND else "logo-on-bone.png")
    ink = MUTE_D if dark else MUTE_L
    return (duality_bar(dark=dark) +
            f'<tr><td bgcolor="{bg}" style="background:{bg};padding:22px 32px 20px;" class="pad">'
            f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td valign="middle" align="left"><a href="https://dianarafael.com/" target="_blank">'
            f'<img src="{logo}" width="190" alt="Diana Rafael" style="display:block;width:190px;height:auto;"/></a></td>'
            f'<td valign="middle" align="right" style="font-family:{SERIF};font-style:italic;font-size:16px;line-height:1.2;color:{ink};">'
            f'The Black &amp; White<br/>Issue</td></tr></table></td></tr>')


def lettering(name, alt, w, bg, pad="0 32px", align="left"):
    return (f'<tr><td bgcolor="{bg}" align="{align}" class="pad" style="background:{bg};padding:{pad};">'
            f'<img src="{ASSET_BASE}{name}.png" width="{w}" alt="{alt}" class="fluid" '
            f'style="display:block;width:{w}px;max-width:100%;height:auto;{"margin:0 auto;" if align == "center" else ""}'
            f'font-family:{SERIF};font-size:40px;color:{CREAM if bg == INK else INK};"/></td></tr>')


def btn(label, href, bg, fg, outline=None):
    if outline:
        return (f'<td class="btn" align="center" style="border:1px solid {outline};">'
                f'<a href="{href}" target="_blank" style="display:inline-block;padding:15px 22px;font-family:{SANS};font-size:13px;'
                f'font-weight:700;letter-spacing:.08em;color:{fg};text-decoration:none;">{label}</a></td>')
    return (f'<td class="btn" align="center" bgcolor="{bg}" style="background:{bg};">'
            f'<a href="{href}" target="_blank" style="display:inline-block;padding:16px 26px;font-family:{SANS};font-size:13px;'
            f'font-weight:700;letter-spacing:.08em;color:{fg};text-decoration:none;">{label}</a></td>')


def buttons(items, bg, pad="20px 32px 8px", align="left"):
    """items: [cell_html, ...] side by side on desktop, full-width stacked on a phone."""
    cells = "".join(f'<td class="col colpad" style="padding:0 12px 0 0;"><table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%"><tr>{c}</tr></table></td>' for c in items)
    return (f'<tr><td bgcolor="{bg}" align="{align}" class="pad" style="background:{bg};padding:{pad};">'
            f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" {"align=\"center\"" if align == "center" else ""}><tr>{cells}</tr></table></td></tr>')


def text(html, bg, color, pad="0 32px", size=17, serif=False, align="left", italic=False, lh=1.55):
    fam = SERIF if serif else SANS
    return (f'<tr><td bgcolor="{bg}" align="{align}" class="pad lead" style="background:{bg};padding:{pad};font-family:{fam};font-size:{size}px;'
            f'line-height:{lh};color:{color};{"font-style:italic;" if italic else ""}">{html}</td></tr>')


def space(h, bg):
    return f'<tr><td bgcolor="{bg}" style="background:{bg};height:{h}px;line-height:{h}px;font-size:1px;">&nbsp;</td></tr>'


def code_field(code, pct, line, field, ink, mute, pad="0 32px"):
    """The code set as type on a flat field (no dashed coupon box): label, the code large, one line."""
    return (f'<tr><td class="pad" style="padding:{pad};"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">'
            f'<tr><td bgcolor="{field}" style="background:{field};padding:22px 24px 20px;">'
            f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td class="col tc" valign="middle" style="font-family:{SANS};font-size:14px;line-height:1.5;color:{mute};">'
            f'<span style="font-family:{SERIF};font-size:22px;color:{ink};">An extra {pct}% off, just for you.</span><br/>{line}</td>'
            f'<td class="col tc" valign="middle" align="right" style="font-family:{SERIF};font-size:44px;line-height:1;letter-spacing:.1em;'
            f'font-weight:600;color:{ink};white-space:nowrap;padding-left:16px;">{code}</td></tr></table></td></tr></table></td></tr>')


def gifts_diptych(bg, ink, mute, pad_top=44):
    """Gifts shown big: black studs on ink | white studs on bone. Tap = tell Daniel on WhatsApp. From $2,000."""
    def half(img, label, field, fg, msg):
        return (f'<td class="col" width="50%" valign="top" bgcolor="{field}" style="width:50%;background:{field};padding:18px 14px 20px;" align="center">'
                f'<a href="{wa(msg)}" target="_blank" style="text-decoration:none;">'
                f'<img src="{img}" width="272" alt="Free natural {label.lower()} diamond studs in 14K gold" class="fluid" '
                f'style="display:block;width:100%;max-width:272px;height:auto;margin:0 auto;"/>'
                f'<div style="margin-top:14px;font-family:{SERIF};font-size:24px;line-height:1.1;color:{fg};">{label}</div>'
                f'<div style="margin-top:6px;font-family:{SANS};font-size:13px;font-weight:700;letter-spacing:.06em;color:{fg};text-decoration:underline;">'
                f'I&#39;d choose {label.lower()}</div></a></td>')

    return (space(pad_top, bg) +
            f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:0 32px 16px;">'
            f'<div class="h2" style="font-family:{SERIF};font-size:32px;line-height:1.12;font-weight:500;color:{ink};">Two gifts with your order: diamond studs and an engraving.</div>'
            f'<div style="margin-top:10px;font-family:{SANS};font-size:15px;line-height:1.55;color:{mute};">{QUALIFIES} Natural diamond studs in 14K gold, '
            f'and a date, initials or a word engraved inside your ring. Black or white, which would you choose?</div></td></tr>'
            f'<tr><td bgcolor="{bg}" style="background:{bg};padding:0 32px;" class="pad"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            + half(STUDS_BLACK, "Black", INK, CREAM, "Hi Daniel, I'd choose the black studs.")
            + half(STUDS_WHITE, "White", BONE, INK, "Hi Daniel, I'd choose the white studs.")
            + '</tr></table></td></tr>')


def gifts_fullbleed(bg, ink, mute, intro=None):
    """Gifts at their biggest: each pair of studs full-bleed, one under the other, with a black / white label band."""
    def band(img, label, field, fg, msg):
        return (f'<tr><td style="padding:0;"><a href="{wa(msg)}" target="_blank" style="text-decoration:none;">'
                f'<img src="{img}" width="600" alt="Free natural {label.lower()} diamond studs in 14K gold" class="fluid" '
                f'style="display:block;width:100%;max-width:600px;height:auto;"/></a></td></tr>'
                f'<tr><td bgcolor="{field}" class="pad" style="background:{field};padding:14px 32px;">'
                f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                f'<td style="font-family:{SERIF};font-size:26px;color:{fg};">{label}</td>'
                f'<td align="right"><a href="{wa(msg)}" target="_blank" style="font-family:{SANS};font-size:13px;font-weight:700;letter-spacing:.06em;'
                f'color:{fg};text-decoration:underline;">I&#39;d choose {label.lower()}</a></td></tr></table></td></tr>')
    intro = intro or (f'<div class="h2" style="font-family:{SERIF};font-size:32px;line-height:1.12;font-weight:500;color:{ink};">'
                      f'Two gifts with your order: diamond studs and an engraving.</div>')
    return (space(44, bg) +
            f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:0 32px 20px;">{intro}'
            f'<div style="margin-top:10px;font-family:{SANS};font-size:15px;line-height:1.55;color:{mute};">{QUALIFIES} Natural diamond studs in 14K gold, '
            f'and a date, initials or a word engraved inside your ring. Which pair would you choose?</div></td></tr>'
            + band(STUDS_BLACK, "Black", INK, CREAM, "Hi Daniel, I'd choose the black studs.")
            + band(STUDS_WHITE, "White", CREAM, INK, "Hi Daniel, I'd choose the white studs."))


def gifts_question(bg, ink, mute):
    """Gifts as one question set huge: 'Black or white?', the two pairs side by side on the page's own ground."""
    def pair(img, label, msg):
        return (f'<td class="col colpad" width="50%" valign="top" align="center" style="width:50%;padding:0 6px;">'
                f'<a href="{wa(msg)}" target="_blank" style="text-decoration:none;color:{ink};">'
                f'<img src="{img}" width="262" alt="Free natural {label.lower()} diamond studs in 14K gold" class="fluid" '
                f'style="display:block;width:100%;max-width:262px;height:auto;margin:0 auto;"/>'
                f'<div style="margin-top:12px;font-family:{SANS};font-size:13px;font-weight:700;letter-spacing:.06em;color:{ink};text-decoration:underline;">'
                f'I&#39;d choose {label.lower()}</div></a></td>')
    return (space(52, bg) +
            f'<tr><td bgcolor="{bg}" align="center" class="pad" style="background:{bg};padding:0 32px 6px;">'
            f'<div style="font-family:{SERIF};font-size:56px;line-height:1;font-weight:500;letter-spacing:-.01em;color:{ink};">Black or white?</div>'
            f'<div style="margin-top:14px;font-family:{SANS};font-size:15px;line-height:1.55;color:{mute};">Two gifts with your order: natural diamond studs in 14K gold, '
            f'and a date, initials or a word engraved inside your ring. {QUALIFIES}</div></td></tr>'
            f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:22px 26px 0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            + pair(STUDS_BLACK, "Black", "Hi Daniel, I'd choose the black studs.")
            + pair(STUDS_WHITE, "White", "Hi Daniel, I'd choose the white studs.")
            + '</tr></table></td></tr>')


def signoff(bg, ink, accent, line="Talk soon,", pad="36px 32px 8px"):
    return (f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:{pad};">'
            f'<div style="font-family:{SERIF};font-style:italic;font-size:24px;line-height:1.3;color:{ink};">{line}</div>'
            f'<div style="margin-top:4px;font-family:{SANS};font-size:14px;color:{accent};">Daniel, Diana Rafael</div></td></tr>')


def colophon(bg, ink, mute, link):
    """Trust messages as a magazine colophon: reviews, payment, a person, care, natural diamonds."""
    a = f'style="color:{link};text-decoration:underline;"'
    items = [f'<a {a} href="{REVIEWS}" target="_blank">550+ reviews</a>',
             'Pay over time with Affirm',
             f'<a {a} href="{BOOK}" target="_blank">15 minutes with Daniel</a> or <a {a} href="{WA}" target="_blank">WhatsApp</a>',
             f'Insured express shipping, paid by us · <a {a} href="{CARE}" target="_blank">Lifetime care</a>']
    return (f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:34px 32px 10px;font-family:{SANS};font-size:14px;line-height:1.9;color:{ink};">'
            + "<br/>".join(items) +
            f'<div style="margin-top:14px;font-size:12px;line-height:1.6;color:{mute};">Every diamond we set is natural, never lab-grown, moissanite or a simulant. '
            f'Your piece ships with a certificate for its diamonds and solid gold.</div></td></tr>')


def footer():
    return (f'<tr><td bgcolor="{INK}" align="left" class="pad" style="background:{INK};padding:30px 32px 30px;font-family:{SANS};">'
            f'<img src="{LOGO_W}" width="150" alt="Diana Rafael" style="display:block;width:150px;height:auto;"/>'
            f'<div style="font-size:12px;line-height:1.6;color:{MUTE_D};margin-top:14px;">{ADDRESS}</div>'
            f'<div style="font-size:12px;color:{MUTE_D};margin-top:10px;">No longer want to receive these emails? {{% unsubscribe \'Unsubscribe\' %}}</div>'
            f'</td></tr>' + duality_bar(8, dark=True))


def piece_caption(color, mute, size=26):
    return (f'<a href="{ITEM_URL}" target="_blank" style="text-decoration:none;font-family:{SERIF};font-size:{size}px;line-height:1.15;color:{color};">'
            f'{{{{ item.product.title }}}}</a><br/><span style="font-family:{SANS};font-size:13px;letter-spacing:.04em;color:{mute};">{{{{ item.variant_title }}}}</span>')


def more_items(bg, color, pad="10px 32px 0"):
    """Other line items, one line each (the first one is the star of the page)."""
    return ("{% for item in event.extra.line_items %}{% if not forloop.first %}"
            f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:{pad};font-family:{SANS};font-size:14px;color:{color};">'
            f'+ <a href="{ITEM_URL}" target="_blank" style="color:{color};text-decoration:underline;">{{{{ item.product.title }}}}</a></td></tr>'
            "{% endif %}{% endfor %}")


def page(ground, pre, rows):
    html = head(ground, pre) + "".join(rows) + tail()
    return html


# ================================================================ 1 / 5  COVER STORY  (RGSj5h, 2h)
def e1():
    g = INK
    rows = [masthead(g, True), space(18, g),
            lettering("h-cover", "Is this the one?", 520, g),
            space(26, g),
            # the piece, full-bleed: the cover photograph
            FIRST + HAS_IMG +
            f'<tr><td bgcolor="{g}" style="background:{g};padding:0;"><a href="{ITEM_URL}" target="_blank">'
            f'<img src="{ITEM_IMG}" width="600" alt="{{{{ item.product.title }}}}" class="fluid" style="display:block;width:100%;max-width:600px;height:auto;"/></a></td></tr>'
            "{% endif %}"
            # cover lines under the photo, two columns like a magazine cover
            f'<tr><td bgcolor="{INK2}" class="pad" style="background:{INK2};padding:22px 32px;">'
            f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td class="col colpad" valign="top" width="58%" style="width:58%;padding-right:20px;">{piece_caption(CREAM, MUTE_D, 24)}</td>'
            f'<td class="col" valign="top" style="font-family:{SERIF};font-style:italic;font-size:19px;line-height:1.35;color:{SAND};">'
            f'Light and dark, held in one piece.</td></tr></table></td></tr>' + FIRST_END,
            more_items(g, MUTE_D, "14px 32px 0"),
            space(30, g),
            text(HI + "I kept your order exactly as you left it: the piece, the size, the gold.", g, CREAM, size=19, serif=False),
            buttons([btn("Return to my order", apply_url("CART5"), SAND, INK), btn("Ask Daniel", ASK, None, CREAM, outline=SAND)], g, pad="24px 32px 30px"),
            code_field("CART5", 5, "Already applied when you tap the button above. One use, on top of today&#39;s prices.", INK2, CREAM, MUTE_D),
            gifts_diptych(g, CREAM, MUTE_D),
            colophon(g, CREAM, MUTE_D, SAND),
            signoff(g, CREAM, SAND, "Talk soon,", pad="22px 32px 40px"),
            footer()]
    return page(g, "Saved exactly as you left it, with an extra 5% and two gifts.", rows)


# ================================================================ 2 / 5  SPLIT SPREAD  (U3FYQZ, ~2d 20h)
def e2():
    g = BONE
    left = (f'<td class="col" width="50%" valign="middle" bgcolor="{INK}" style="width:50%;background:{INK};padding:36px 28px 34px;">'
            f'<div style="font-family:{SERIF};font-style:italic;font-size:22px;line-height:1.2;color:{SAND};">{nm("an extra", "An extra")}</div>'
            f'<div class="giant" style="font-family:{SERIF};font-size:132px;line-height:.95;font-weight:500;letter-spacing:-.03em;color:{CREAM};">5%</div>'
            f'<div style="font-family:{SERIF};font-style:italic;font-size:22px;line-height:1.2;color:{SAND};">is yours.</div></td>')
    right = (f'<td class="col" width="50%" valign="middle" bgcolor="{PAPER}" style="width:50%;background:{PAPER};padding:0;">'
             + FIRST + f'<a href="{ITEM_URL}" target="_blank"><img src="{ITEM_IMG}" width="300" alt="{{{{ item.product.title }}}}" class="fluid" '
             f'style="display:block;width:100%;max-width:300px;height:auto;"/></a>' + FIRST_END + '</td>')
    rows = [masthead(g, False),
            f'<tr><td style="padding:0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>{left}{right}</tr></table></td></tr>',
            # caption strip under the spread
            FIRST + f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:18px 32px 0;">{piece_caption(INK, MUTE_L, 22)}</td></tr>' + FIRST_END,
            more_items(g, MUTE_L),
            space(26, g),
            text("Use it on the piece you chose. It is applied for you when you tap the button.", g, INK, size=19, serif=False),
            buttons([btn("Apply 5% and check out", apply_url("CART5"), INK, CREAM), btn("Ask Daniel", ASK, None, INK, outline=INK)], g, pad="22px 32px 30px"),
            code_field("CART5", 5, "Or enter it at checkout. One use, on top of today&#39;s prices.", PAPER, INK, MUTE_L),
            gifts_fullbleed(g, INK, MUTE_L),
            colophon(g, INK, MUTE_L, SAND_TXT),
            signoff(g, INK, SAND_TXT, "Talk soon,", pad="22px 32px 40px"),
            footer()]
    return page(g, "Your code CART5 is inside, plus two gifts with your order.", rows)


# ================================================================ 3 / 5  PULL QUOTE + STILL LIFE  (TDAQrS, ~3d 20h)
def e3():
    g = SAND
    rows = [masthead(g, False), space(34, g),
            lettering("h-still", "Still waiting.", 520, g, align="center"),
            space(14, g),
            text(nm("your extra 5% is still on it, and your two gifts too.", "Your extra 5% is still on it, and your two gifts too.")
                 + " If something is holding you back, tell me and I&#39;ll fix it.", g, INK, pad="0 56px", size=19, align="center"),
            buttons([btn("Apply 5% and check out", apply_url("CART5"), INK, CREAM), btn("Talk to Daniel", BOOK, None, INK, outline=INK)], g,
                    pad="24px 32px 40px", align="center"),
            # still life: the piece on bone, caption column beside it
            f'<tr><td bgcolor="{BONE}" class="pad" style="background:{BONE};padding:32px;">'
            f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            + FIRST +
            f'<td class="col colpad" width="62%" valign="top" style="width:62%;padding-right:22px;"><a href="{ITEM_URL}" target="_blank">'
            f'<img src="{ITEM_IMG}" width="330" alt="{{{{ item.product.title }}}}" class="fluid" style="display:block;width:100%;max-width:330px;height:auto;"/></a></td>'
            f'<td class="col" valign="bottom" style="padding-bottom:4px;">{piece_caption(INK, MUTE_L, 22)}'
            f'<div style="margin-top:16px;font-family:{SERIF};font-style:italic;font-size:19px;line-height:1.35;color:{SAND_TXT};">'
            f'Saved, untouched, exactly as you left it.</div></td>'
            + FIRST_END +
            '</tr></table></td></tr>',
            more_items(BONE, MUTE_L, "0 32px 24px"),
            space(28, g),
            code_field("CART5", 5, "Applied for you with the button above. One use.", BONE, INK, MUTE_L),
            gifts_question(g, INK, "#3B342B"),
            colophon(g, INK, "#3B342B", INK),
            signoff(g, INK, INK, "Talk soon,", pad="22px 32px 40px"),
            footer()]
    return page(g, "Your extra 5% (CART5) is still here, and so are your gifts.", rows)


# ================================================================ 4 / 5  THE INDEX  (Re9UiL, ~5d 20h)
def e4():
    g = INK

    def entry(left_html, right_html, href=None):
        r = (f'<td valign="top" style="padding:16px 0;font-family:{SERIF};font-size:22px;line-height:1.2;color:{CREAM};">{left_html}</td>'
             f'<td valign="top" align="right" style="padding:16px 0 16px 16px;font-family:{SANS};font-size:14px;line-height:1.45;color:{MUTE_D};">{right_html}</td>')
        return f'<tr>{r}</tr>'

    items = ("{% for item in event.extra.line_items %}"
             f'<tr><td colspan="2" style="padding:0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
             f'<td width="112" valign="top" style="width:112px;padding:14px 18px 14px 0;"><a href="{ITEM_URL}" target="_blank">'
             f'<img src="{ITEM_IMG}" width="112" alt="{{{{ item.product.title }}}}" style="display:block;width:112px;height:auto;"/></a></td>'
             f'<td valign="middle" style="padding:14px 0;">{piece_caption(CREAM, MUTE_D, 21)}</td></tr></table></td></tr>'
             "{% endfor %}")
    index = (f'<tr><td bgcolor="{INK2}" class="pad" style="background:{INK2};padding:26px 32px 18px;">'
             f'<div style="font-family:{SERIF};font-style:italic;font-size:20px;color:{SAND};padding-bottom:4px;">In this issue, saved for you</div>'
             f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">'
             + items
             + entry("Your extra 5%", "CART5, applied with the button")
             + entry("Affirm at checkout", "See your monthly plan first")
             + entry("Two gifts", "Diamond studs + an engraving")
             + '</table></td></tr>')
    rows = [masthead(g, True), space(22, g),
            lettering("h-wear", "Wear it now. Pay over time.", 520, g),
            space(18, g),
            text(nm("choose Affirm at checkout and see your monthly plan before you commit.",
                    "Choose Affirm at checkout and see your monthly plan before you commit.")
                 + " Checking won&#39;t affect your credit score. Your extra 5% still applies.", g, CREAM, size=18),
            buttons([btn("See my Affirm options", apply_url("CART5"), SAND, INK),
                     btn("Talk numbers with me", wa("Hi Daniel, can we talk through payment options?"), None, CREAM, outline=SAND)], g, pad="24px 32px 34px"),
            index,
            space(26, g),
            code_field("CART5", 5, "Applied for you with the button above. Works with Affirm.", INK2, CREAM, MUTE_D),
            gifts_diptych(g, CREAM, MUTE_D),
            colophon(g, CREAM, MUTE_D, SAND),
            signoff(g, CREAM, SAND, "Talk soon,", pad="22px 32px 40px"),
            footer()]
    return page(g, "Choose Affirm at checkout, keep your extra 5%, and your gifts.", rows)


# ================================================================ 5 / 5  EDITOR'S LETTER  (UNZFjJ, ~6d 20h)
def e5():
    g = BONE
    dear = "{% if first_name %}Dear {{ first_name }},{% else %}Hello,{% endif %}"
    letter_body = (
        f'<div style="font-family:{SERIF};font-style:italic;font-size:24px;line-height:1.3;color:{INK};margin-bottom:18px;">{dear}</div>'
        f'<p style="margin:0 0 16px;font-family:{SERIF};font-size:21px;line-height:1.5;color:{INK};">'
        f'<span style="float:left;font-family:{SERIF};font-size:66px;line-height:.82;padding:6px 6px 0 0;color:{INK};">T</span>'
        f'his is my last email about this piece, so here is my best offer: an extra 10%, on top of today&#39;s prices. '
        f'Pay in full or over time with Affirm.</p>'
        f'<p style="margin:0 0 16px;font-family:{SERIF};font-size:21px;line-height:1.5;color:{INK};">'
        f'Some pieces finish a story. If this one is yours, it is ready when you are. And if you have a question, '
        f'you&#39;ll always get a real person, never an AI. That&#39;s a promise.</p>')
    postcard = (FIRST + HAS_IMG +
                f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:6px 32px 0;">'
                f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                f'<td bgcolor="{PAPER}" style="background:{PAPER};padding:16px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                f'<td class="col colpad" width="230" valign="middle" style="width:230px;padding-right:20px;"><a href="{ITEM_URL}" target="_blank">'
                f'<img src="{ITEM_IMG}" width="230" alt="{{{{ item.product.title }}}}" class="fluid" style="display:block;width:100%;max-width:230px;height:auto;"/></a></td>'
                f'<td class="col" valign="middle">{piece_caption(INK, MUTE_L, 22)}</td>'
                f'</tr></table></td></tr></table></td></tr>'
                "{% endif %}" + FIRST_END)
    rows = [masthead(g, False), space(30, g),
            # letter head: lettering left, the date-less dateline right
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 32px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td class="col" valign="bottom" width="300" style="width:300px;"><img src="{ASSET_BASE}h-letter.png" width="300" alt="My best offer." '
            f'style="display:block;width:300px;max-width:100%;height:auto;font-family:{SERIF};font-size:40px;color:{INK};"/></td>'
            f'<td class="col hide-m" valign="bottom" align="right" style="font-family:{SERIF};font-style:italic;font-size:17px;line-height:1.4;color:{SAND_TXT};padding-bottom:12px;">'
            f'A letter from Daniel,<br/>Ramat Gan</td></tr></table></td></tr>',
            space(26, g),
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 64px 0 32px;">{letter_body}</td></tr>',
            signoff(g, INK, SAND_TXT, "With gratitude,", pad="4px 32px 6px"),
            buttons([btn("Apply 10% and check out", apply_url("CART10"), INK, CREAM), btn("Talk to Daniel", BOOK, None, INK, outline=INK)], g, pad="26px 32px 30px"),
            code_field("CART10", 10, "Applied for you with the button above. One use, on top of today&#39;s prices.", INK, CREAM, MUTE_D),
            space(30, g),
            postcard,
            more_items(g, MUTE_L),
            gifts_fullbleed(g, INK, MUTE_L, intro=f'<div class="h2" style="font-family:{SERIF};font-style:italic;font-size:30px;line-height:1.15;color:{INK};">P.S. Your two gifts are still yours: diamond studs and an engraving.</div>'),
            colophon(g, INK, MUTE_L, SAND_TXT),
            space(30, g),
            footer()]
    return page(g, "Your code CART10 is inside: an extra 10% off, plus your gifts.", rows)


EMAILS = [("1-RGSj5h-cover", e1), ("2-U3FYQZ-split", e2), ("3-TDAQrS-pullquote", e3), ("4-Re9UiL-index", e4), ("5-UNZFjJ-letter", e5)]

if __name__ == "__main__":
    for name, f in EMAILS:
        html = f()
        open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(html)
        print(name, f"{len(html.encode('utf-8'))/1024:.1f} KB")
