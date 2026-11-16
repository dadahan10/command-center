"""The Black & White Issue, rollout 16.11.2026 (Daniel approved the direction + copy 16.11, with "more calls to action").

All four live abandon flows, email actions only (SMS untouched):
  XW6UqR  Checkout, Black Ice      5 emails  A B C D E
  VB4v4q  Checkout, not Black Ice  7 emails  A B H C G D E
  VWbEYm  Abandoned cart           8 emails  A C H F G D B E   (order of 16.11: 2 = natural diamond, 7 = call)
  Y6Zunh  Browse abandonment       5 emails  A G F D B
Families (LAYOUT-MAP.md): A cover story, B split spread, C pull quote + still life, D index, E editor's letter,
F photo essay, G Q&A, H letters page (real reviews from dianarafael.com/pages/our-customers-reviews, quoted verbatim).

CTAs (Daniel 16.11 "more buttons"): a primary button near the top, a button on the product / gift blocks, and a closing
button; 3-4 buttons per email, each with a specific label. Copy, codes, links and event variables are the live
15.11/16.11 ones (live-fix-2026-11-15: build_live.py, build_more.py, build_cart.py).
Images: Champie lettering + flattened logos hosted in the Klaviyo image library (rollout/assets-klaviyo.json, written by
upload_assets.py); no local paths in the HTML.
Usage: python mag.py -> out/<flow>-<n>-<family>.html + plan.json
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import build as M   # the 16.11 sample system: frame, palette, code field, gifts, colophon, footer
from build import (INK, INK2, SAND, SAND_TXT, BONE, PAPER, CREAM, MUTE_D, MUTE_L, SERIF, SANS, LOGO_W, STUDS_BLACK, STUDS_WHITE,
                   BOOK, REVIEWS, CARE, head, tail, duality_bar, text, space, btn, code_field, gifts_diptych, gifts_fullbleed,
                   gifts_question, signoff, colophon, footer, wa)

OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
ASSETS = json.load(open(os.path.join(HERE, "assets-klaviyo.json"), encoding="utf-8"))
IMG = json.load(open(os.path.join(HERE, "..", "..", "flow-templates", "redesign-2026-11-04", "images.json"), encoding="utf-8"))
REFUND = "https://dianarafael.com/policies/refund-policy"
DARKTXT = "#3B342B"


def asset(name):
    """Hosted URL of a lettering/logo PNG (Klaviyo image library). ASSET_BASE of build.py, resolved per file."""
    return ASSETS[name]["url"]


# ---------------------------------------------------------------- the piece, per trigger event
class Src:
    """Where 'her piece' comes from. Checkout: line items. Cart: the Added to Cart event. Browse: the Viewed Product event."""

    def __init__(self, kind):
        self.kind = kind
        if kind == "chk":
            self.open, self.close = M.FIRST, M.FIRST_END
            self.if_img, self.img = M.HAS_IMG, M.ITEM_IMG
            self.url, self.title, self.sub = M.ITEM_URL, "{{ item.product.title }}", "{{ item.variant_title }}"
        elif kind == "cart":
            self.open = self.close = ""
            self.if_img, self.img = "{% if event.ImageURL %}", "{{ event.ImageURL }}"
            self.url = ("{% if 'myshopify.com' in event.URL %}https://dianarafael.com{{ event.URL|slice:'34:' }}"
                        "{% else %}{{ event.URL|default:'https://dianarafael.com/cart' }}{% endif %}")
            self.title = "{{ event|lookup:'Product Name'|default:'Your piece' }}"
            self.sub = "{{ event|lookup:'Variant Name' }}"
        else:  # browse
            self.open = self.close = ""
            self.if_img, self.img = "{% if event.ImageURL %}", "{{ event.ImageURL }}"
            self.url = "{{ event.URL|default:'https://dianarafael.com/collections/black-ice' }}"
            self.title, self.sub = "{{ event.Name }}", ""

    def go(self, code=None):
        """The link that takes her back (with the code applied when the email carries one)."""
        if self.kind == "chk":
            return M.apply_url(code) if code else M.CHK
        if self.kind == "cart":
            if not code:
                return self.url
            return ("https://dianarafael.com/discount/" + code + "?redirect="
                    "{% if 'myshopify.com' in event.URL %}{{ event.URL|slice:'34:'|urlencode }}{% else %}%2Fcart{% endif %}")
        if not code:
            return self.url
        return ("https://dianarafael.com/discount/" + code + "?redirect="
                "{% if event.URL %}{{ event.URL|slice:'23:'|urlencode }}{% else %}%2Fcollections%2Fblack-ice{% endif %}")

    def caption(self, color, mute, size=26):
        sub = (f'<br/><span style="font-family:{SANS};font-size:13px;letter-spacing:.04em;color:{mute};">{self.sub}</span>' if self.sub else "")
        return (f'<a href="{self.url}" target="_blank" style="text-decoration:none;font-family:{SERIF};font-size:{size}px;line-height:1.15;color:{color};">'
                f'{self.title}</a>{sub}')

    def more(self, bg, color, pad="10px 32px 0"):
        return M.more_items(bg, color, pad) if self.kind == "chk" else ""

    def image(self, w, extra_style=""):
        return (f'<a href="{self.url}" target="_blank"><img src="{self.img}" width="{w}" alt="{self.title}" class="fluid" '
                f'style="display:block;width:100%;max-width:{w}px;height:auto;{extra_style}"/></a>')

    def price(self):
        if self.kind == "cart":
            return "{% if event.Price %}$" + '{{ event.Price|floatformat:"0g" }}' + "{% endif %}"
        if self.kind == "browse":
            return "{{ event.Price|default:'' }}"
        return ""


# ---------------------------------------------------------------- shared rows
def masthead(bg, dark):
    logo = LOGO_W if dark else asset({SAND: "logo-on-sand", PAPER: "logo-on-paper"}.get(bg, "logo-on-bone"))
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
            f'<img src="{asset(name)}" width="{w}" alt="{alt}" class="fluid" '
            f'style="display:block;width:{w}px;max-width:100%;height:auto;{"margin:0 auto;" if align == "center" else ""}'
            f'font-family:{SERIF};font-size:40px;color:{CREAM if bg == INK else INK};"/></td></tr>')


def cta(primary, bg, secondary=None, sec_fg=None, outline=None, pad="22px 32px 30px", align="left", fill=SAND, fill_fg=INK, link=None):
    """One primary button (+ an optional outline button, or a plain text link) on one row; stacked on a phone."""
    cells = [btn(primary[0], primary[1], fill, fill_fg)]
    if secondary:
        cells.append(btn(secondary[0], secondary[1], None, sec_fg, outline=outline))
    row = M.buttons(cells, bg, pad=pad, align=align)
    if link:
        ln = (f'<tr><td bgcolor="{bg}" align="{align}" class="pad tc" style="background:{bg};padding:0 32px 30px;font-family:{SANS};font-size:15px;'
              f'line-height:1.5;color:{link[2]};">{link[0]}</td></tr>')
        row = row.replace(f'padding:{pad};', f'padding:{pad.split()[0]} 32px 12px;', 1) + ln
    return row


def tlink(label, href, color):
    return f'<a href="{href}" target="_blank" style="color:{color};text-decoration:underline;font-weight:600;">{label}</a>'


def gifts(style, bg, ink, mute, go_href, label, intro=None, fill=SAND, fill_fg=INK):
    """The gifts block (studs black/white + engraving) and its own button: order with the gifts."""
    if style == "diptych":
        g = gifts_diptych(bg, ink, mute)
    elif style == "fullbleed":
        g = gifts_fullbleed(bg, ink, mute, intro=intro)
    else:
        g = gifts_question(bg, ink, mute)
    return g + cta((label, go_href), bg, pad="24px 32px 6px", align="center" if style == "question" else "left", fill=fill, fill_fg=fill_fg)


def closing(bg, label, href, fill, fg, line=None, line_color=None):
    """The last thing in the email before the footer: one wide button (+ a short line above it)."""
    above = (f'<tr><td bgcolor="{bg}" align="center" class="pad" style="background:{bg};padding:8px 32px 0;font-family:{SERIF};font-style:italic;'
             f'font-size:20px;line-height:1.35;color:{line_color};">{line}</td></tr>') if line else ""
    return (above + f'<tr><td bgcolor="{bg}" align="center" class="pad" style="background:{bg};padding:18px 32px 44px;">'
            f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:420px;"><tr>'
            f'{btn(label, href, fill, fg)}</tr></table></td></tr>')


def piece_block(src, bg, ink, mute, lead, button, fill=INK, fill_fg=CREAM, w=200, field=None):
    """Her piece, small, with its own button: thumbnail | lead, title, button."""
    field = field or bg
    return (src.open +
            f'<tr><td bgcolor="{bg}" class="pad" style="background:{bg};padding:0 32px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">'
            f'<tr><td bgcolor="{field}" style="background:{field};padding:16px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            + src.if_img +
            f'<td class="col colpad" width="{w}" valign="middle" style="width:{w}px;padding-right:20px;">{src.image(w)}</td>'
            "{% endif %}"
            f'<td class="col" valign="middle"><div style="font-family:{SANS};font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:{mute};padding-bottom:6px;">{lead}</div>'
            f'{src.caption(ink, mute, 22)}'
            f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin-top:16px;"><tr>{btn(button[0], button[1], fill, fill_fg)}</tr></table></td>'
            f'</tr></table></td></tr></table></td></tr>' + src.close)


def page(ground, pre, rows):
    return head(ground, pre) + "".join(rows) + tail()


# ================================================================ A  COVER STORY
def fam_A(src, c):
    g = INK
    rows = [masthead(g, True), space(18, g), lettering(c["h"], c["alt"], 520, g), space(26, g),
            src.open + src.if_img +
            f'<tr><td bgcolor="{g}" style="background:{g};padding:0;">{src.image(600)}</td></tr>'
            "{% endif %}"
            f'<tr><td bgcolor="{INK2}" class="pad" style="background:{INK2};padding:22px 32px;">'
            f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td class="col colpad" valign="top" width="58%" style="width:58%;padding-right:20px;">{src.caption(CREAM, MUTE_D, 24)}</td>'
            f'<td class="col" valign="top" style="font-family:{SERIF};font-style:italic;font-size:19px;line-height:1.35;color:{SAND};">'
            f'{c.get("tag", "Light and dark, held in one piece.")}</td></tr></table></td></tr>' + src.close,
            src.more(g, MUTE_D, "14px 32px 0"),
            space(28, g),
            text(c["lead"], g, CREAM, size=19),
            cta(c["primary"], g, c["secondary"], CREAM, SAND, pad="24px 32px 30px")]
    if c.get("code"):
        rows.append(code_field(*c["code"], INK2, CREAM, MUTE_D))
    rows += [gifts("diptych", g, CREAM, MUTE_D, c["gift_href"], c["gift_label"]),
             colophon(g, CREAM, MUTE_D, SAND), signoff(g, CREAM, SAND, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], SAND, INK), footer()]
    return page(g, c["pre"], rows)


# ================================================================ B  SPLIT SPREAD
def fam_B(src, c):
    """Black | bone diptych: a giant figure on ink beside a picture (her piece, or a brand photo) on paper."""
    g = BONE
    left = (f'<td class="col" width="50%" valign="middle" bgcolor="{INK}" style="width:50%;background:{INK};padding:36px 28px 34px;">'
            f'<div style="font-family:{SERIF};font-style:italic;font-size:22px;line-height:1.2;color:{SAND};">{c["big_pre"]}</div>'
            f'<div class="giant" style="font-family:{SERIF};font-size:132px;line-height:.95;font-weight:500;letter-spacing:-.03em;color:{CREAM};">{c["big"]}</div>'
            f'<div style="font-family:{SERIF};font-style:italic;font-size:22px;line-height:1.2;color:{SAND};">{c["big_post"]}</div></td>')
    if c.get("photo"):
        right_img = (f'<img src="{c["photo"][0]}" width="300" alt="{c["photo"][1]}" class="fluid" style="display:block;width:100%;max-width:300px;height:auto;"/>')
        right = f'<td class="col" width="50%" valign="middle" bgcolor="{PAPER}" style="width:50%;background:{PAPER};padding:0;">{right_img}</td>'
    else:
        right = (f'<td class="col" width="50%" valign="middle" bgcolor="{PAPER}" style="width:50%;background:{PAPER};padding:0;">'
                 + src.open + src.if_img + src.image(300) + "{% endif %}" + src.close + '</td>')
    rows = [masthead(g, False),
            f'<tr><td style="padding:0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>{left}{right}</tr></table></td></tr>']
    if not c.get("photo"):
        rows += [src.open + f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:18px 32px 0;">{src.caption(INK, MUTE_L, 22)}</td></tr>' + src.close,
                 src.more(g, MUTE_L)]
    rows += [space(26, g), text(c["lead"], g, INK, size=19)]
    if c.get("photo"):   # her piece gets its own block + button further down, so the second CTA up here is a link
        rows.append(cta(c["primary"], g, None, pad="22px 32px 30px", fill=INK, fill_fg=CREAM,
                        link=("Or " + tlink(c["secondary"][0][0].lower() + c["secondary"][0][1:], c["secondary"][1], INK), None, MUTE_L)))
    else:
        rows.append(cta(c["primary"], g, c["secondary"], INK, INK, pad="22px 32px 30px", fill=INK, fill_fg=CREAM))
    if c.get("code"):
        rows.append(code_field(*c["code"], PAPER, INK, MUTE_L))
    if c.get("photo"):
        rows += [space(30, g), piece_block(src, g, INK, MUTE_L, c["piece_lead"], c["piece_btn"], field=PAPER)]
    rows += [gifts("fullbleed", g, INK, MUTE_L, c["gift_href"], c["gift_label"], fill=INK, fill_fg=CREAM),
             colophon(g, INK, MUTE_L, SAND_TXT), signoff(g, INK, SAND_TXT, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], INK, CREAM), footer()]
    return page(g, c["pre"], rows)


# ================================================================ C  PULL QUOTE + STILL LIFE
def fam_C(src, c):
    """Sand page: one line set huge, the answer, then a still life on bone (her piece, or a brand still life + her piece)."""
    g = SAND
    rows = [masthead(g, False), space(34, g), lettering(c["h"], c["alt"], 520, g, align="center"), space(14, g),
            text(c["lead"], g, INK, pad="0 56px", size=19, align="center"),
            cta(c["primary"], g, None, pad="24px 32px 40px", align="center", fill=INK, fill_fg=CREAM,
                link=("Or " + tlink(c["secondary"][0], c["secondary"][1], INK), None, INK))]
    if c.get("still"):
        # brand still life full-bleed on bone, captioned, then her piece small with its button
        rows += [f'<tr><td style="padding:0;"><img src="{c["still"][0]}" width="600" alt="{c["still"][1]}" class="fluid" style="display:block;width:100%;max-width:600px;height:auto;"/></td></tr>',
                 f'<tr><td bgcolor="{BONE}" class="pad" style="background:{BONE};padding:14px 32px 28px;font-family:{SERIF};font-style:italic;font-size:17px;line-height:1.4;color:{SAND_TXT};">{c["still"][2]}</td></tr>',
                 piece_block(src, BONE, INK, MUTE_L, c["piece_lead"], c["piece_btn"], field=PAPER),
                 space(28, BONE)]
    else:
        rows += [f'<tr><td bgcolor="{BONE}" class="pad" style="background:{BONE};padding:32px;">'
                 f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                 + src.open +
                 f'<td class="col colpad" width="62%" valign="top" style="width:62%;padding-right:22px;">{src.image(330)}</td>'
                 f'<td class="col" valign="bottom" style="padding-bottom:4px;">{src.caption(INK, MUTE_L, 22)}'
                 f'<div style="margin-top:16px;font-family:{SERIF};font-style:italic;font-size:19px;line-height:1.35;color:{SAND_TXT};">'
                 f'{c.get("tag", "Saved, untouched, exactly as you left it.")}</div>'
                 f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin-top:18px;"><tr>{btn(c["piece_btn"][0], c["piece_btn"][1], INK, CREAM)}</tr></table></td>'
                 + src.close + '</tr></table></td></tr>',
                 src.more(BONE, MUTE_L, "0 32px 24px")]
    rows.append(space(28, g))
    if c.get("code"):
        rows.append(code_field(*c["code"], BONE, INK, MUTE_L))
    rows += [gifts("question", g, INK, DARKTXT, c["gift_href"], c["gift_label"], fill=INK, fill_fg=CREAM),
             colophon(g, INK, DARKTXT, INK), signoff(g, INK, INK, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], INK, CREAM), footer()]
    return page(g, c["pre"], rows)


# ================================================================ D  INDEX
def fam_D(src, c):
    g = INK

    def entry(left_html, right_html):
        return (f'<tr><td valign="top" style="padding:16px 0;font-family:{SERIF};font-size:22px;line-height:1.2;color:{CREAM};border-top:1px solid #2A3238;">{left_html}</td>'
                f'<td valign="top" align="right" style="padding:16px 0 16px 16px;font-family:{SANS};font-size:14px;line-height:1.45;color:{MUTE_D};border-top:1px solid #2A3238;">{right_html}</td></tr>')

    thumb = (f'<td width="112" valign="top" style="width:112px;padding:14px 18px 14px 0;"><a href="{src.url}" target="_blank">'
             f'<img src="{src.img}" width="112" alt="{src.title}" style="display:block;width:112px;height:auto;"/></a></td>')
    price = src.price()
    price_html = (f'<div style="margin-top:8px;font-family:{SERIF};font-size:24px;color:{SAND};">{price}</div>' if price else "")
    one = (f'<tr><td colspan="2" style="padding:0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
           + src.if_img + thumb + "{% endif %}" +
           f'<td valign="middle" style="padding:14px 0;">{src.caption(CREAM, MUTE_D, 21)}{price_html}</td></tr></table></td></tr>')
    items = ("{% for item in event.extra.line_items %}" + one + "{% endfor %}") if src.kind == "chk" else one
    entries = "".join(entry(a, b) for a, b in c["entries"])
    index = (f'<tr><td bgcolor="{INK2}" class="pad" style="background:{INK2};padding:26px 32px 22px;">'
             f'<div style="font-family:{SERIF};font-style:italic;font-size:20px;color:{SAND};padding-bottom:4px;">{c.get("index_title", "In this issue, saved for you")}</div>'
             f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">' + items + entries + '</table>'
             f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin-top:14px;"><tr>{btn(c["piece_btn"][0], c["piece_btn"][1], CREAM, INK)}</tr></table>'
             '</td></tr>')
    rows = [masthead(g, True), space(22, g), lettering("h-wear", "Wear it now. Pay over time.", 520, g), space(18, g),
            text(c["lead"], g, CREAM, size=18),
            cta(c["primary"], g, None, pad="24px 32px 34px", link=(c["link"], None, MUTE_D)),
            index, space(26, g)]
    if c.get("code"):
        rows.append(code_field(*c["code"], INK2, CREAM, MUTE_D))
    rows += [gifts("diptych", g, CREAM, MUTE_D, c["gift_href"], c["gift_label"]),
             colophon(g, CREAM, MUTE_D, SAND), signoff(g, CREAM, SAND, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], SAND, INK), footer()]
    return page(g, c["pre"], rows)


# ================================================================ E  EDITOR'S LETTER
def fam_E(src, c):
    g = BONE
    dear = "{% if first_name %}Dear {{ first_name }},{% else %}Hello,{% endif %}"
    paras = c["letter"]
    first = paras[0]
    body = (f'<div style="font-family:{SERIF};font-style:italic;font-size:24px;line-height:1.3;color:{INK};margin-bottom:18px;">{dear}</div>'
            f'<p style="margin:0 0 16px;font-family:{SERIF};font-size:21px;line-height:1.5;color:{INK};">'
            f'<span style="float:left;font-family:{SERIF};font-size:66px;line-height:.82;padding:6px 6px 0 0;color:{INK};">{first[0]}</span>{first[1:]}</p>'
            + "".join(f'<p style="margin:0 0 16px;font-family:{SERIF};font-size:21px;line-height:1.5;color:{INK};">{p}</p>' for p in paras[1:]))
    postcard = (src.open + src.if_img +
                f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:6px 32px 0;">'
                f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                f'<td bgcolor="{PAPER}" style="background:{PAPER};padding:16px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                f'<td class="col colpad" width="230" valign="middle" style="width:230px;padding-right:20px;">{src.image(230)}</td>'
                f'<td class="col" valign="middle"><div style="font-family:{SANS};font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:{MUTE_L};padding-bottom:6px;">{c.get("piece_lead", "The piece")}</div>'
                f'{src.caption(INK, MUTE_L, 22)}</td>'
                f'</tr></table></td></tr></table></td></tr>'
                "{% endif %}" + src.close)
    rows = [masthead(g, False), space(30, g),
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 32px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td class="col" valign="bottom" width="300" style="width:300px;"><img src="{asset(c["h"])}" width="300" alt="{c["alt"]}" '
            f'style="display:block;width:300px;max-width:100%;height:auto;font-family:{SERIF};font-size:40px;color:{INK};"/></td>'
            f'<td class="col hide-m" valign="bottom" align="right" style="font-family:{SERIF};font-style:italic;font-size:17px;line-height:1.4;color:{SAND_TXT};padding-bottom:12px;">'
            f'A letter from Daniel,<br/>Ramat Gan</td></tr></table></td></tr>',
            space(26, g),
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 64px 0 32px;">{body}</td></tr>',
            signoff(g, INK, SAND_TXT, c.get("sign", "With gratitude,"), pad="4px 32px 6px"),
            cta(c["primary"], g, c["secondary"], INK, INK, pad="26px 32px 30px", fill=INK, fill_fg=CREAM),
            code_field(*c["code"], INK, CREAM, MUTE_D), space(30, g), postcard, src.more(g, MUTE_L),
            gifts("fullbleed", g, INK, MUTE_L, c["gift_href"], c["gift_label"], fill=INK, fill_fg=CREAM,
                  intro=f'<div class="h2" style="font-family:{SERIF};font-style:italic;font-size:30px;line-height:1.15;color:{INK};">P.S. Your two gifts are still yours: diamond studs and an engraving.</div>'),
            colophon(g, INK, MUTE_L, SAND_TXT), space(10, g),
            closing(g, c["close"][0], c["close"][1], INK, CREAM), footer()]
    return page(g, c["pre"], rows)


# ================================================================ F  PHOTO ESSAY
def fam_F(src, c):
    """One brand photograph full-bleed under the lettering, a caption like a magazine plate, the story, then her piece small."""
    g = INK
    rows = [masthead(g, True), space(18, g), lettering(c["h"], c["alt"], 520, g), space(24, g),
            f'<tr><td style="padding:0;"><img src="{c["photo"][0]}" width="600" alt="{c["photo"][1]}" class="fluid" style="display:block;width:100%;max-width:600px;height:auto;"/></td></tr>',
            f'<tr><td bgcolor="{INK2}" class="pad" style="background:{INK2};padding:14px 32px;font-family:{SANS};font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:{MUTE_D};">'
            f'<span style="color:{SAND};">Plate I</span> &nbsp;·&nbsp; {c["photo"][2]}</td></tr>',
            space(30, g),
            text(c["lead"], g, CREAM, size=19),
            cta(c["primary"], g, None, pad="24px 32px 34px", link=(c["link"], None, MUTE_D)),
            piece_block(src, g, CREAM, MUTE_D, c["piece_lead"], c["piece_btn"], fill=SAND, fill_fg=INK, field=INK2),
            space(28, g)]
    if c.get("code"):
        rows.append(code_field(*c["code"], INK2, CREAM, MUTE_D))
    rows += [gifts("diptych", g, CREAM, MUTE_D, c["gift_href"], c["gift_label"]),
             colophon(g, CREAM, MUTE_D, SAND), signoff(g, CREAM, SAND, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], SAND, INK), footer()]
    return page(g, c["pre"], rows)


# ================================================================ G  Q&A
def fam_G(src, c):
    """Paper page: her real questions set as headings, short answers, numbered like an interview."""
    g = PAPER

    def qa(n, q, a):
        return (f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 32px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">'
                f'<tr><td width="44" valign="top" style="width:44px;padding:20px 0;border-top:1px solid #D6CBB7;font-family:{SERIF};font-size:22px;color:{SAND_TXT};">{n:02d}</td>'
                f'<td valign="top" style="padding:20px 0;border-top:1px solid #D6CBB7;">'
                f'<div style="font-family:{SERIF};font-size:25px;line-height:1.2;color:{INK};">{q}</div>'
                f'<div style="margin-top:8px;font-family:{SANS};font-size:15px;line-height:1.6;color:{MUTE_L};">{a}</div></td></tr></table></td></tr>')

    rows = [masthead(g, False), space(26, g),
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 32px 10px;font-family:{SANS};font-size:12px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:{SAND_TXT};">{c["kicker"]}</td></tr>',
            lettering(c["h"], c["alt"], 520, g), space(16, g),
            text(c["lead"], g, INK, size=18),
            cta(c["primary"], g, None, pad="24px 32px 34px", fill=INK, fill_fg=CREAM, link=(c["link"], None, MUTE_L))]
    rows += [qa(i + 1, q, a) for i, (q, a) in enumerate(c["qa"])]
    rows += [space(30, g), piece_block(src, g, INK, MUTE_L, c["piece_lead"], c["piece_btn"], field=BONE), space(28, g)]
    if c.get("code"):
        rows.append(code_field(*c["code"], BONE, INK, MUTE_L))
    rows += [gifts("question", g, INK, MUTE_L, c["gift_href"], c["gift_label"], fill=INK, fill_fg=CREAM),
             colophon(g, INK, MUTE_L, SAND_TXT), signoff(g, INK, SAND_TXT, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], INK, CREAM), footer()]
    return page(g, c["pre"], rows)


# ================================================================ H  LETTERS PAGE (real reviews only)
def fam_H(src, c):
    g = BONE
    name, when, quote = c["feature"]
    feature = (f'<tr><td bgcolor="{INK}" class="pad" style="background:{INK};padding:40px 40px 34px;">'
               f'<div style="font-family:{SERIF};font-size:90px;line-height:.6;color:{SAND};">&ldquo;</div>'
               f'<div style="margin-top:6px;font-family:{SERIF};font-style:italic;font-size:27px;line-height:1.35;color:{CREAM};">{quote}</div>'
               f'<div style="margin-top:18px;font-family:{SANS};font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:{SAND};">{name}'
               f'<span style="color:{MUTE_D};font-weight:400;"> &nbsp;·&nbsp; {when}</span></div></td></tr>')

    def small(n, w, q):
        return (f'<td class="col colpad" width="50%" valign="top" style="width:50%;padding:0 10px 0 0;">'
                f'<div style="border-top:2px solid {INK};padding-top:14px;font-family:{SERIF};font-size:19px;line-height:1.4;color:{INK};">&ldquo;{q}&rdquo;</div>'
                f'<div style="margin-top:10px;font-family:{SANS};font-size:12px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:{SAND_TXT};">{n}'
                f'<span style="color:{MUTE_L};font-weight:400;"> · {w}</span></div></td>')

    more = (f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 32px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            + "".join(small(*r) for r in c["more_reviews"]) + '</tr></table></td></tr>')
    rows = [masthead(g, False), space(22, g),
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:0 32px 6px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td valign="bottom" style="font-family:{SANS};font-size:12px;letter-spacing:.2em;text-transform:uppercase;font-weight:700;color:{SAND_TXT};">Letters to the editor</td>'
            f'<td valign="bottom" align="right" style="font-family:{SERIF};font-size:46px;line-height:1;color:{INK};">550+<span style="font-family:{SANS};font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:{MUTE_L};"> &nbsp;reviews</span></td>'
            f'</tr></table></td></tr>',
            lettering(c["h"], c["alt"], 520, g, pad="10px 32px 0"), space(16, g),
            text(c["lead"], g, INK, size=18),
            cta(c["primary"], g, None, pad="22px 32px 34px", fill=INK, fill_fg=CREAM,
                link=("Or " + tlink(c["secondary"][0], c["secondary"][1], INK), None, MUTE_L)),
            feature, space(30, g), more,
            f'<tr><td bgcolor="{g}" class="pad" style="background:{g};padding:16px 32px 30px;font-family:{SANS};font-size:13px;line-height:1.5;color:{MUTE_L};">'
            f'From our customers&#39; reviews page, as they wrote them. {tlink("Read all 550+", REVIEWS, INK)}</td></tr>',
            piece_block(src, g, INK, MUTE_L, c["piece_lead"], c["piece_btn"], field=PAPER), space(28, g)]
    if c.get("code"):
        rows.append(code_field(*c["code"], PAPER, INK, MUTE_L))
    rows += [gifts("diptych", g, INK, MUTE_L, c["gift_href"], c["gift_label"], fill=INK, fill_fg=CREAM),
             colophon(g, INK, MUTE_L, SAND_TXT), signoff(g, INK, SAND_TXT, c.get("sign", "Talk soon,"), pad="22px 32px 6px"),
             closing(g, c["close"][0], c["close"][1], INK, CREAM), footer()]
    return page(g, c["pre"], rows)


FAM = dict(A=fam_A, B=fam_B, C=fam_C, D=fam_D, E=fam_E, F=fam_F, G=fam_G, H=fam_H)
FAM_NAME = dict(A="cover story", B="split spread", C="pull quote + still life", D="index", E="editor's letter", F="photo essay", G="Q&A", H="letters page")
