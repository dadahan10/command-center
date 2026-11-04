"""Build the 28 non-VIP flow emails (4.11.2026 redesign). VIP lives in vip.py.

Source of the copy: backup-before/<tpl>.html (the live flow-message templates as of 4.11 morning, which already
carry the corrected return-policy wording). From each one we keep the body ("middle": everything after the
headline down to the trust line) and its headline/kicker, and rebuild the frame around it: theme, hero image,
product presentation and layout differ per email, according to PLAN below.

Usage:  python build_all.py            -> writes out/<tpl>.html for every email in PLAN
"""
import os, re, sys
from rd import *

SRC = os.path.join(HERE, "backup-before")
OUT = os.path.join(HERE, "out")

# ---------------------------------------------------------------- dynamic product blocks (the customer's own piece)
# Checkout Started: loop over line items; the chosen variant's image first (their metal), product image as fallback.
CHK_IMG = ("{% if item.product.variant.images.0.src %}{{ item.product.variant.images.0.src }}"
           "{% else %}{{ item.product.images.0.src }}{% endif %}")
CART_URL = ("{% if 'myshopify.com' in event.URL %}https://dianarafael.com{{ event.URL|slice:'34:' }}"
            "{% else %}{{ event.URL|default:'https://dianarafael.com/cart' }}{% endif %}")
# Placed / Fulfilled Order: first line item, variant image first.
ORD_IF = "event.extra.line_items.0.product.variant.images.0.src or event.extra.line_items.0.product.images.0.src"
ORD_IMG = ("{% if event.extra.line_items.0.product.variant.images.0.src %}{{ event.extra.line_items.0.product.variant.images.0.src }}"
           "{% else %}{{ event.extra.line_items.0.product.images.0.src }}{% endif %}")
ORD_NAME = "{{ event.extra.line_items.0.product.title|default:event.Items.0 }}"
# Delivered Shipment: fulfillment line item first, then order line item (template also works on Placed Order).
DEL_IF = ("event.extra.fulfillment.line_items.0.product.variant.images.0.src or event.extra.fulfillment.line_items.0.product.images.0.src"
          " or " + ORD_IF)
DEL_IMG = ("{% if event.extra.fulfillment.line_items.0.product.variant.images.0.src %}{{ event.extra.fulfillment.line_items.0.product.variant.images.0.src }}"
           "{% elif event.extra.fulfillment.line_items.0.product.images.0.src %}{{ event.extra.fulfillment.line_items.0.product.images.0.src }}"
           "{% elif event.extra.line_items.0.product.variant.images.0.src %}{{ event.extra.line_items.0.product.variant.images.0.src }}"
           "{% else %}{{ event.extra.line_items.0.product.images.0.src }}{% endif %}")
DEL_NAME = "{{ event.Items.0|default:'your piece' }}"


def frame_img(t, src, alt, href=None, w=440, pad="0 40px", mat=None, border=None):
    """The customer's piece on a 'pedestal': a mat colour behind it and a hairline frame, never full-bleed."""
    th = THEMES[t]
    mat = mat or ("#ffffff" if t in ("bone", "paper") else "#f6f1e7")
    border = border or (th["rule"] if t in ("bone", "paper") else GOLD)
    img = f'<img src="{src}" alt="{alt}" width="{w}" style="display:block;width:100%;max-width:{w}px;height:auto;border:0;"/>'
    if href:
        img = f'<a href="{href}" target="_blank">{img}</a>'
    return (f'<tr><td align="center" class="pad" style="padding:{pad};"><table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" '
            f'bgcolor="{mat}" style="background:{mat};border:1px solid {border};"><tr><td align="center" style="padding:22px;">{img}</td></tr></table></td></tr>')


def caption(t, name, sub="", pad="14px 40px 0", size=24):
    th = THEMES[t]
    s = f'<br/><span style="font-family:{SANS};font-size:13px;letter-spacing:.06em;color:{th["muted"]};">{sub}</span>' if sub else ""
    return (f'<tr><td align="center" class="pad" style="padding:{pad};font-family:{SERIF};font-size:{size}px;line-height:1.25;'
            f'color:{th["text"]};">{name}{s}</td></tr>')


def chk_piece(t, w=440):
    th = THEMES[t]
    return ("{% for item in event.extra.line_items %}{% if forloop.first %}"
            "{% if item.product.variant.images.0.src or item.product.images.0.src %}"
            + frame_img(t, CHK_IMG, "{{ item.product.title }}", "https://dianarafael.com/products/{{ item.product.handle }}", w=w)
            + "{% endif %}" + caption(t, "{{ item.product.title }}", "{{ item.variant_title }}")
            + "{% else %}" + f'<tr><td align="center" class="pad" style="padding:6px 40px 0;font-family:{SANS};font-size:14px;color:{th["muted"]};">+ {{{{ item.product.title }}}}</td></tr>'
            + "{% endif %}{% endfor %}")


def chk_thumb_row(t, lead):
    """Small 'your piece' strip used under a story image (checkout)."""
    th = THEMES[t]
    return ("{% for item in event.extra.line_items %}{% if forloop.first %}"
            f'<tr><td class="pad" style="padding:6px 48px 18px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="border-top:1px solid {th["rule"]};border-bottom:1px solid {th["rule"]};"><tr>'
            f'<td width="96" style="padding:14px 16px 14px 0;"><a href="https://dianarafael.com/products/{{{{ item.product.handle }}}}" target="_blank"><img src="{CHK_IMG}" width="96" alt="{{{{ item.product.title }}}}" style="display:block;width:96px;height:auto;border:0;background:#fff;"/></a></td>'
            f'<td style="padding:14px 0;font-family:{SANS};font-size:13px;line-height:1.5;color:{th["muted"]};">{lead}<br/>'
            f'<a href="https://dianarafael.com/products/{{{{ item.product.handle }}}}" target="_blank" style="font-family:{SERIF};font-size:20px;color:{th["text"]};text-decoration:none;">{{{{ item.product.title }}}}</a></td></tr></table></td></tr>'
            "{% endif %}{% endfor %}")


def cart_piece(t, w=440):
    return ("{% if event.ImageURL %}" + frame_img(t, "{{ event.ImageURL }}", "{{ event|lookup:'Product Name' }}", CART_URL, w=w) + "{% endif %}"
            + caption(t, "{{ event|lookup:'Product Name'|default:'Your piece' }}", "{{ event|lookup:'Variant Name' }}"))


def cart_thumb_row(t, lead):
    th = THEMES[t]
    return ("{% if event.ImageURL %}"
            f'<tr><td class="pad" style="padding:6px 48px 18px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="border-top:1px solid {th["rule"]};border-bottom:1px solid {th["rule"]};"><tr>'
            f'<td width="96" style="padding:14px 16px 14px 0;"><a href="{CART_URL}" target="_blank"><img src="{{{{ event.ImageURL }}}}" width="96" alt="{{{{ event|lookup:\'Product Name\' }}}}" style="display:block;width:96px;height:auto;border:0;background:#fff;"/></a></td>'
            f'<td style="padding:14px 0;font-family:{SANS};font-size:13px;line-height:1.5;color:{th["muted"]};">{lead}<br/>'
            f'<a href="{CART_URL}" target="_blank" style="font-family:{SERIF};font-size:20px;color:{th["text"]};text-decoration:none;">{{{{ event|lookup:\'Product Name\'|default:\'Your piece\' }}}}</a></td></tr></table></td></tr>'
            "{% endif %}")


def browse_piece(t, w=440):
    return ("{% if event.ImageURL %}" + frame_img(t, "{{ event.ImageURL }}", "{{ event.Name }}", "{{ event.URL }}", w=w) + "{% endif %}"
            + caption(t, "{{ event.Name }}"))


def browse_thumb_row(t, lead):
    th = THEMES[t]
    return ("{% if event.ImageURL %}"
            f'<tr><td class="pad" style="padding:6px 48px 18px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="border-top:1px solid {th["rule"]};border-bottom:1px solid {th["rule"]};"><tr>'
            f'<td width="96" style="padding:14px 16px 14px 0;"><a href="{{{{ event.URL }}}}" target="_blank"><img src="{{{{ event.ImageURL }}}}" width="96" alt="{{{{ event.Name }}}}" style="display:block;width:96px;height:auto;border:0;background:#fff;"/></a></td>'
            f'<td style="padding:14px 0;font-family:{SANS};font-size:13px;line-height:1.5;color:{th["muted"]};">{lead}<br/>'
            f'<a href="{{{{ event.URL }}}}" target="_blank" style="font-family:{SERIF};font-size:20px;color:{th["text"]};text-decoration:none;">{{{{ event.Name }}}}</a></td></tr></table></td></tr>'
            "{% endif %}")


def order_piece(t, w=440, sub=""):
    return ("{% if " + ORD_IF + " %}" + frame_img(t, ORD_IMG, ORD_NAME, w=w) + "{% endif %}" + caption(t, ORD_NAME, sub))


def deliv_piece(t, w=440, sub=""):
    return ("{% if " + DEL_IF + " %}" + frame_img(t, DEL_IMG, DEL_NAME, w=w) + "{% endif %}" + caption(t, DEL_NAME, sub))


# ---------------------------------------------------------------- extraction + recolouring of the kept body
def extract(tpl):
    h = open(os.path.join(SRC, tpl + ".html"), encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    h1_text = m.group(1).strip()
    start = h.find("</tr>", m.end()) + 5
    cond = h.rfind("{% if 'Black Ice' in event.", 0, m.start())
    if cond > 0 and h.rfind("</tr>", 0, m.start()) < cond:   # headline itself is inside a Black Ice / other branch
        h1_text, start = None, cond
    ends = []
    for marker in ("Insured express shipping, paid by us", "23 Tuval St."):
        i = h.find(marker, start)
        if i > 0:
            ends.append(h.rfind("<tr", 0, i))
    middle = h[start:min(ends)]
    k = re.search(r'text-transform:uppercase;color:#7a5d1e;">([^<]+)</td>', h)
    return h1_text, middle, (k.group(1).strip() if k else "")


DARK_MAP = [("#1f1b16", "{text}"), ("#5c544a", "{muted}"), ("#4a4339", "{muted}"), ("#7a5d1e", "{accent}"),
            ("#f3ead9", "#1d1b18"), ("#e6dccb", "{rule}"), ("#ffffff", "{card}"), ("#f7f3ec", "{card}"), ("#efe8dc", "#1d1b18")]
PAPER_MAP = [("#ffffff", "#fbf7ef"), ("#f7f3ec", "{card}")]


def recolor(t, html):
    th = THEMES[t]
    mp = DARK_MAP if t in ("noir", "ink") else PAPER_MAP if t == "paper" else []
    # gold-button labels stay dark whatever the theme
    html = html.replace("text-transform:uppercase;color:#1f1b16;text-decoration:none", "text-transform:uppercase;color:@@BTN@@;text-decoration:none")
    table = {a.lower(): b.format(**th) for a, b in mp}
    if table:   # single pass, so a replaced colour is never replaced again
        html = re.sub("|".join(re.escape(a) for a in table), lambda m: table[m.group(0).lower()], html, flags=re.I)
    html = html.replace("@@BTN@@", "#1f1b16")
    if t in ("noir", "ink"):
        # gold-filled CTAs keep dark text; outline answer buttons (now card-coloured) need light text
        html = html.replace('bgcolor="%s" style="border:2px solid #b08d3c' % th["card"],
                            'bgcolor="%s" style="background:%s;border:2px solid #b08d3c' % (th["card"], th["card"]))
    return html


def class_css(t):
    th = THEMES[t]
    dark = t in ("noir", "ink")
    return (f".p{{margin:0 0 14px;font-family:{SANS};font-size:16px;line-height:1.65;color:{th['text']};}}"
            f".g{{font-family:{SERIF};}} .s{{font-family:{SANS};}}"
            f".k{{font-family:{SANS};font-size:11px;letter-spacing:.24em;font-weight:700;text-transform:uppercase;color:{th['accent']};}}"
            f".b{{display:inline-block;padding:14px 30px;font-family:{SANS};font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;"
            f"color:{'#efe8dc' if dark else '#1f1b16'};text-decoration:none;}}"
            f"td[bgcolor='#b08d3c'] .b{{color:#1f1b16 !important;}}"
            f".l{{color:{th['accent']};text-decoration:underline;}}")


def page(t, pre, rows):
    html = head(t, pre).replace("</style>", class_css(t) + "</style>", 1)
    return html + "".join(rows) + trust(t) + foot(t)


def h1_left(t, text, pad="30px 48px 8px", size=38):
    return h1(t, text, align="left", pad=pad, size=size)


# ---------------------------------------------------------------- the plan: one entry per email
P = {}  # tpl -> builder


def reg(tpl):
    def deco(fn):
        P[tpl] = fn
        return fn
    return deco


def std(tpl, t, pre, top_rows, h1_align="center", h1_size=38, after_h1=None, end_rows=None, h1_override=None):
    h1t, mid, kick = extract(tpl)
    h1t = h1_override or h1t
    rows = list(top_rows)
    if h1t:
        rows.append(h1(t, h1t, align=h1_align, size=h1_size, pad="30px 48px 10px" if h1_align == "center" else "30px 48px 8px"))
    if after_h1:
        rows += after_h1
    rows.append(recolor(t, mid))
    if end_rows:
        rows += end_rows
    return page(t, pre, rows)


# ---- Abandoned checkout (X6ZfPR)
@reg("WtYdde")  # 1/8 reminder: their piece, big, on a white pedestal (bone)
def _():
    t = "bone"
    return std("WtYdde", t, "Your order is saved, exactly as you left it.",
               [kicker(t, "Saved for you", pad="24px 40px 0"), logo(t, pad="16px 40px 24px"), chk_piece(t, w=480)])


@reg("VdW7XY")  # 2/8 what stopped you: question-first, piece as a side thumbnail (paper)
def _():
    t = "paper"
    th = THEMES[t]
    h1t, mid, kick = extract("VdW7XY")
    split = ("{% for item in event.extra.line_items %}{% if forloop.first %}"
             f'<tr><td class="pad" style="padding:8px 40px 0;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
             f'<td class="col colpad" width="220" valign="middle" style="width:220px;padding-right:22px;"><a href="https://dianarafael.com/products/{{{{ item.product.handle }}}}" target="_blank">'
             f'<img src="{CHK_IMG}" width="220" alt="{{{{ item.product.title }}}}" style="display:block;width:100%;max-width:220px;height:auto;border:1px solid {th["rule"]};background:#fff;"/></a></td>'
             f'<td class="col" valign="middle"><div style="font-family:{SANS};font-size:11px;letter-spacing:.28em;text-transform:uppercase;font-weight:700;color:{th["accent"]};">A quick question</div>'
             f'<h1 class="h1" style="margin:10px 0 8px;font-family:{SERIF};font-size:40px;line-height:1.08;font-weight:500;color:{th["text"]};">{h1t}</h1>'
             f'<div style="font-family:{SANS};font-size:13px;color:{th["muted"]};">{{{{ item.product.title }}}}</div></td></tr></table></td></tr>'
             "{% endif %}{% endfor %}")
    return page(t, "One tap is enough. I read every answer myself.", [logo(t, pad="24px 40px 18px", align="left", width=170), split, spacer(18), recolor(t, mid)])


@reg("SNvbQS")  # 3/8 natural diamond: rough black diamonds in parcel paper (paper), piece as a strip below
def _():
    t = "paper"
    return std("SNvbQS", t, "What's in your piece, and the certificate that proves it.",
               [logo(t, pad="22px 40px 18px"), hero(IMG["diamonds"], "Natural black diamonds in a diamond parcel paper, with tweezers and a loupe"),
                kicker(t, "About the stone", pad="26px 40px 0")],
               end_rows=[chk_thumb_row(t, "The stone in your piece")])


@reg("VLjUfd")  # 4/8 reviews: the unboxing moment (bone), editorial left
def _():
    t = "bone"
    return std("VLjUfd", t, "Read what they wrote once the box was open.",
               [logo(t, pad="22px 40px 18px"), hero(IMG["unbox"], "Hands with black nails opening a black jewelry box", pad="0 0"),
                kicker(t, "In their words", align="left", pad="28px 48px 0")], h1_align="left")


@reg("WiHGws")  # 5/8 fit + care: sizing tools on the bench (ink)
def _():
    t = "ink"
    return std("WiHGws", t, "Size, returns and care, answered in one minute.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["fit"], "A ring mandrel and ring size gauges on a jeweler's bench"),
                kicker(t, "Size and peace of mind", pad="28px 40px 0")],
               end_rows=[chk_thumb_row(t, "Your piece, kept as you chose it")])


@reg("V4FBhc")  # 6/8 Affirm: their piece framed in gold on noir, 'wear it now'
def _():
    t = "noir"
    return std("V4FBhc", t, "Choose Affirm at checkout and see your plan before you commit.",
               [logo(t, pad="24px 40px 22px"), kicker(t, "Wear it now", pad="0 40px 18px"), chk_piece(t, w=420)])


@reg("TNDw3W")  # 7/8 Daniel call: stone held up to a phone on the bench (paper, letter feel)
def _():
    t = "paper"
    return std("TNDw3W", t, "Ask anything, see the stones on video, change what you like.",
               [logo(t, pad="22px 48px 16px", align="left", width=160), hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
                kicker(t, "Let's talk", align="left", pad="26px 48px 0")], h1_align="left", h1_size=40,
               end_rows=[chk_thumb_row(t, "We can talk about")])


@reg("SyBqNG")  # 8/8 note + gift: the real studs, macro, on noir
def _():
    t = "noir"
    return std("SyBqNG", t, "And a gift I wanted you to know about.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["studs"], "Free 1 ct natural black diamond studs in yellow gold"),
                kicker(t, "A gift with your order", pad="26px 40px 0")],
               end_rows=[chk_thumb_row(t, "Your order")])


# ---- Abandoned cart (VWbEYm)
@reg("U58x8u")  # 1/8 reminder: their piece, editorial-left on paper
def _():
    t = "paper"
    return std("U58x8u", t, "Your piece is saved, exactly as you chose it.",
               [logo(t, pad="22px 40px 20px"), kicker(t, "Saved for you", pad="0 40px 16px"), cart_piece(t, w=480)])


@reg("UBwjpH")  # 2/8 natural diamond: same diamonds image on ink (different frame from checkout)
def _():
    t = "ink"
    return std("UBwjpH", t, "What's in your piece, and the certificate that proves it.",
               [logo(t, pad="24px 40px 20px"), kicker(t, "About the stone", pad="0 40px 16px"),
                hero(IMG["diamonds"], "Natural black diamonds in a diamond parcel paper, with tweezers and a loupe", pad="0 32px")],
               end_rows=[cart_thumb_row(t, "The stone in your piece")])


@reg("Xzm3N4")  # 3/8 reviews: unboxing on paper, centered
def _():
    t = "paper"
    return std("Xzm3N4", t, "Read what they wrote once the box was open.",
               [kicker(t, "In their words", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"),
                hero(IMG["unbox"], "Hands with black nails opening a black jewelry box", pad="0 32px")])


@reg("Y7JQ5h")  # 4/8 made to order: the bench (ink)
def _():
    t = "ink"
    return std("Y7JQ5h", t, "How your piece is made, and how it gets to you.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["studio"], "A jeweler setting a black diamond at the bench"),
                kicker(t, "How we make it", pad="28px 40px 0")],
               end_rows=[cart_thumb_row(t, "The piece we'd make for you")])


@reg("WRGJQ3")  # 5/8 fit + care: sizing tools, bone, left
def _():
    t = "bone"
    return std("WRGJQ3", t, "Size, returns and care, answered in one minute.",
               [logo(t, pad="22px 48px 18px", align="left", width=170), hero(IMG["fit"], "A ring mandrel and ring size gauges on a jeweler's bench"),
                kicker(t, "Size and peace of mind", align="left", pad="26px 48px 0")], h1_align="left")


@reg("TPeL6i")  # 6/8 Affirm: their piece on noir
def _():
    t = "noir"
    return std("TPeL6i", t, "Choose Affirm at checkout and see your plan before you commit.",
               [logo(t, pad="24px 40px 22px"), kicker(t, "Wear it now", pad="0 40px 18px"), cart_piece(t, w=420)])


@reg("UmCymx")  # 7/8 Daniel call: ink
def _():
    t = "ink"
    return std("UmCymx", t, "Ask anything, see the stones on video, change what you like.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call"),
                kicker(t, "Let's talk", pad="26px 40px 0")],
               end_rows=[cart_thumb_row(t, "We can talk about")])


@reg("XjtgKS")  # 8/8 note + gift: studs on bone with a gold frame
def _():
    t = "bone"
    return std("XjtgKS", t, "And a gift I wanted you to know about.",
               [kicker(t, "A gift with your order", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"),
                frame_img(t, IMG["studs"], "Free 1 ct natural black diamond studs in yellow gold", w=520, pad="0 28px", border=GOLD)],
               end_rows=[cart_thumb_row(t, "Your piece")])


# ---- Browse abandonment (XLpiBU)
@reg("WwmdnE")  # 1/4 the piece viewed, big on bone
def _():
    t = "bone"
    return std("WwmdnE", t, "Made to order for you, shipped insured on us, with lifetime care.",
               [logo(t, pad="22px 40px 18px"), kicker(t, "You were looking at", pad="0 40px 16px"), "{% if event.ImageURL %}" + frame_img(t, "{{ event.ImageURL }}", "{{ event.Name }}", "{{ event.URL }}", w=480) + "{% endif %}"])


@reg("UDi5wM")  # 2/4 why us: the bench (noir)
def _():
    t = "noir"
    return std("UDi5wM", t, "Natural diamonds, solid gold, made by hand since 2014.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["studio"], "A jeweler setting a black diamond at the bench"),
                kicker(t, "Why Diana Rafael", pad="28px 40px 0")],
               end_rows=[browse_thumb_row(t, "The piece you looked at")])


@reg("XB8MV8")  # 3/4 studs gift: the studs on noir + their viewed piece
def _():
    t = "noir"
    return std("XB8MV8", t, "Free 1 ct natural black diamond studs, now from $2,000 (was $3,000).",
               [kicker(t, "A gift with your order", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"),
                hero(IMG["studs"], "Free 1 ct natural black diamond studs in yellow gold")],
               after_h1=[browse_thumb_row(t, "With the piece you looked at")])


@reg("QXP4ar")  # 4/4 Daniel: call image on paper, letter
def _():
    t = "paper"
    return std("QXP4ar", t, "Size, gold, stone, budget: ask a person, not a chatbot.",
               [logo(t, pad="22px 48px 16px", align="left", width=160), hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
                kicker(t, "A letter from Daniel", align="left", pad="26px 48px 0")], h1_align="left",
               end_rows=[browse_thumb_row(t, "We can talk about")])


# ---- Post-purchase (VydTk7, R6tiEk, Y6UjZu)
@reg("WHCJdX")  # PP1 order confirmed: their piece on bone, 'it's yours'
def _():
    t = "bone"
    return std("WHCJdX", t, "Made by hand in our studio, checked, and shipped insured within 10 business days.",
               [kicker(t, "Order {{ event.extra.name }} confirmed", pad="24px 40px 0"), logo(t, pad="14px 40px 22px"), order_piece(t, w=460, sub="Now being made for you")])


@reg("Xg2wvc")  # PP2 inside the studio: the bench, ink, + 'yours is on the bench'
def _():
    t = "ink"
    th = THEMES[t]
    strip = ("{% if " + ORD_IF + " %}"
             f'<tr><td class="pad" style="padding:6px 48px 18px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="border-top:1px solid {th["rule"]};border-bottom:1px solid {th["rule"]};"><tr>'
             f'<td width="96" style="padding:14px 16px 14px 0;"><img src="{ORD_IMG}" width="96" alt="{ORD_NAME}" style="display:block;width:96px;height:auto;border:0;background:#fff;"/></td>'
             f'<td style="padding:14px 0;font-family:{SANS};font-size:13px;line-height:1.5;color:{th["muted"]};">On the bench now<br/><span style="font-family:{SERIF};font-size:20px;color:{th["text"]};">{ORD_NAME}</span></td></tr></table></td></tr>'
             "{% endif %}")
    return std("Xg2wvc", t, "A look at the bench: setting, polishing and the final check.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["studio"], "A jeweler setting a black diamond at the bench"),
                kicker(t, "From our studio", pad="28px 40px 0")], after_h1=[strip])


@reg("RCR6Vz")  # PP3 shipped: their piece + the packed box (paper)
def _():
    t = "paper"
    return std("RCR6Vz", t, "Your tracking number, a short note on customs, and how to care for your piece.",
               [kicker(t, "Order {{ event.extra.name }} has shipped", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"),
                order_piece(t, w=420, sub="Packed, insured and on its way"), spacer(18),
                hero(IMG["ship"], "A white courier box with a black jewelry box nested in tissue", pad="0 40px")])


@reg("V4smfK")  # PP4 review: their piece on noir, 'how does it feel'
def _():
    t = "noir"
    return std("V4smfK", t, "One minute on Google helps the next person trust a studio they've never met.",
               [logo(t, pad="24px 40px 22px"), kicker(t, "A small favor", pad="0 40px 18px"), deliv_piece(t, w=420)])


@reg("RZYnw2")  # XS1 made to go with yours: their piece small + recommendations (bone)
def _():
    t = "bone"
    return std("RZYnw2", t, "A few pieces we'd pair with what you're already wearing.",
               [logo(t, pad="22px 40px 18px"), kicker(t, "Made to go with yours", pad="0 40px 16px"), deliv_piece(t, w=300, sub="Yours")])


@reg("TbpdpS")  # XS2 worn together: their piece on ink
def _():
    t = "paper"
    return std("TbpdpS", t, "Same gold, same diamonds, worn together.",
               [kicker(t, "Wearing them together", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"), deliv_piece(t, w=340, sub="Start from the one you have")])


@reg("W9dVNd")  # XS3 designed to match: call image + their piece (ink)
def _():
    t = "ink"
    return std("W9dVNd", t, "We can make the second piece to fit the first exactly.",
               [logo(t, pad="24px 40px 20px"), hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call"),
                kicker(t, "A letter from Daniel", pad="26px 40px 0")],
               end_rows=["{% if " + DEL_IF + " %}" + frame_img(t, DEL_IMG, DEL_NAME, w=260, pad="6px 40px 4px") + caption(t, DEL_NAME, "The piece we'd match", size=20) + spacer(10) + "{% endif %}"])


# ---- JEWELVERSARY (XrShek): THEIR piece only; no fallback to any other ring
@reg("TLpfRY")
def _():
    t = "noir"
    th = THEMES[t]
    h1t, mid, kick = extract("TLpfRY")
    big = (f'<tr><td align="center" style="padding:6px 40px 0;font-family:{SERIF};font-size:150px;line-height:1;font-weight:400;color:{GOLD_LT};" class="big">1</td></tr>'
           f'<tr><td align="center" style="padding:0 40px 26px;font-family:{SANS};font-size:12px;letter-spacing:.42em;text-transform:uppercase;font-weight:700;color:{th["muted"]};">year together</td></tr>')
    rows = [logo(t, pad="26px 40px 10px"), kicker(t, "Happy JEWELVERSARY", pad="10px 40px 0"), big,
            "{% if " + ORD_IF + " %}" + frame_img(t, ORD_IMG, ORD_NAME, w=400) + "{% endif %}",
            caption(t, ORD_NAME, "Chosen a year ago today"),
            h1(t, h1t, pad="30px 48px 10px"), recolor(t, mid)]
    return page(t, "One year ago today, you chose a piece from our studio.", rows)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    for tpl, fn in P.items():
        if only and tpl not in only:
            continue
        open(os.path.join(OUT, tpl + ".html"), "w", encoding="utf-8").write(fn())
        print("built", tpl)
