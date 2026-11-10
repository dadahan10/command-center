"""Round 2 (Daniel 4.11.2026 evening) for the 20 sales-flow emails: checkout X6ZfPR, cart VWbEYm, browse XLpiBU.

What changes against build_all.py (round 1):
1. Much less copy: a headline, one or two short lines, done.
2. CTAs high: the buttons sit right under the headline, more than one per email.
3. The gift is shown: every email that mentions the free studs shows the studs (photo strip; big in the gift emails,
   with the "black or white?" question as WhatsApp buttons).
4. Trust icons from the first email of every flow: 550+ reviews · talk to Daniel · free gift · pay over time ·
   natural diamonds (last). Natural-diamond copy moves to the bottom; in the flow order the natural-diamond email
   swaps places with the 15-minutes-with-Daniel email (consultation earlier, diamonds late) -> SWAP below, subjects too.
5. Bigger logo (rd.logo, all emails).
The other 9 emails (VIP, post-purchase, JEWELVERSARY) keep their round-1 builders; they only get the bigger logo.

Usage:  python round2.py   -> out/<tpl>.html for all 29 (round-1 builders for the non-sales ones)
"""
import os, sys
import build_all as B
from rd import *

OUT = B.OUT
WA = "https://wa.me/97235755066"
BOOK = "https://dianarafael.com/pages/new-website-book-online-appointment"
REVIEWS = "https://dianarafael.com/pages/our-customers-reviews"
CARE = "https://dianarafael.com/pages/new-website-jewelry-care-program"
REFUND = "https://dianarafael.com/policies/refund-policy"
CHK_URL = "{{ event.extra.responsive_checkout_url|default:'https://dianarafael.com/cart' }}"
CART_URL = B.CART_URL
VIEW_URL = "{{ event.URL }}"

# flow position swap: the natural-diamond email moves late, the 15-minutes email moves early
SWAP = {"SNvbQS": "TNDw3W", "TNDw3W": "SNvbQS",   # checkout 3/8 <-> 7/8
        "UBwjpH": "UmCymx", "UmCymx": "UBwjpH"}   # cart 2/8 <-> 7/8


def wa(text):
    return WA + "?text=" + text.replace(" ", "%20").replace(",", "%2C").replace("'", "%27").replace("?", "%3F")


# ---------------------------------------------------------------- new shared blocks
def lead(t, html, align="center", pad="4px 48px 4px"):
    th = THEMES[t]
    return (f'<tr><td align="{align}" class="pad" style="padding:{pad};font-family:{SANS};font-size:16px;line-height:1.6;color:{th["text"]};">'
            f'{html}</td></tr>')


def btn_cell(t, label, href, primary=True):
    th = THEMES[t]
    if primary:
        return (f'<td align="center" bgcolor="{th["btn_bg"]}" style="background:{th["btn_bg"]};border-radius:2px;">'
                f'<a href="{href}" target="_blank" style="display:inline-block;padding:15px 26px;font-family:{SANS};font-size:12px;font-weight:700;'
                f'letter-spacing:.14em;text-transform:uppercase;color:{th["btn_fg"]};text-decoration:none;">{label}</a></td>')
    return (f'<td align="center" style="border:1px solid {th["accent"]};border-radius:2px;">'
            f'<a href="{href}" target="_blank" style="display:inline-block;padding:14px 24px;font-family:{SANS};font-size:12px;font-weight:700;'
            f'letter-spacing:.14em;text-transform:uppercase;color:{th["text"]};text-decoration:none;">{label}</a></td>')


def buttons(t, items, pad="18px 32px 6px"):
    """items: [(label, href, primary)] side by side on desktop, stacked on mobile."""
    cells = "".join(f'<td class="col colpad" align="center" style="padding:0 6px 10px;"><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center"><tr>'
                    f'{btn_cell(t, l, h, p)}</tr></table></td>' for l, h, p in items)
    return (f'<tr><td align="center" class="pad" style="padding:{pad};"><table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center">'
            f'<tr>{cells}</tr></table></td></tr>')


def answer_buttons(t, answers, pad="14px 48px 6px"):
    """Stacked full-width outline buttons (one tap = WhatsApp with the answer written in)."""
    th = THEMES[t]
    rows = "".join(f'<tr><td style="padding:0 0 8px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
                   f'<td align="center" style="border:1px solid {th["accent"]};border-radius:2px;"><a href="{h}" target="_blank" style="display:block;padding:13px 16px;'
                   f'font-family:{SANS};font-size:14px;color:{th["text"]};text-decoration:none;">{l}</a></td></tr></table></td></tr>' for l, h in answers)
    return (f'<tr><td class="pad" style="padding:{pad};"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">{rows}</table></td></tr>')


ICONS = [("icon-reviews", "550+ reviews", REVIEWS), ("icon-consult", "Talk to Daniel", BOOK), ("icon-gift", "Free gift", None),
         ("icon-pay", "Pay over time", None), ("icon-diamond", "Natural diamonds", None)]


def icon_strip(t, pad="22px 24px 22px", pay_href=None, gift_href=None):
    th = THEMES[t]
    cells = []
    for key, label, href in ICONS:
        href = href or (pay_href if key == "icon-pay" else gift_href if key == "icon-gift" else None)
        img = f'<img src="{IMG[key]}" width="40" height="40" alt="" style="display:block;margin:0 auto;width:40px;height:40px;border:0;"/>'
        txt = (f'<div style="margin-top:8px;font-family:{SANS};font-size:11px;line-height:1.3;letter-spacing:.04em;color:{th["text"]};">{label}</div>')
        inner = img + txt
        if href:
            inner = f'<a href="{href}" target="_blank" style="text-decoration:none;">{inner}</a>'
        cells.append(f'<td align="center" valign="top" width="20%" style="width:20%;padding:0 4px;">{inner}</td>')
    return (f'<tr><td class="pad" style="padding:{pad};"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" '
            f'style="border-top:1px solid {th["rule"]};border-bottom:1px solid {th["rule"]};"><tr><td style="padding:18px 0;">'
            f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>{"".join(cells)}</tr></table></td></tr></table></td></tr>')


def gift_strip(t, href, pad="6px 40px 18px"):
    """Compact: the studs photo + one line. Shown in every sales email (they all mention the gift)."""
    th = THEMES[t]
    return (f'<tr><td class="pad" style="padding:{pad};"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td width="150" valign="middle" style="width:150px;padding-right:18px;"><a href="{href}" target="_blank"><img src="{IMG["studs"]}" width="150" '
            f'alt="Free 1 ct natural black diamond studs" style="display:block;width:150px;height:auto;border:0;"/></a></td>'
            f'<td valign="middle" style="font-family:{SANS};font-size:13px;line-height:1.5;color:{th["muted"]};">'
            f'<div style="font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:700;color:{th["accent"]};">A gift with your order</div>'
            f'<div style="margin-top:6px;font-family:{SERIF};font-size:21px;line-height:1.2;color:{th["text"]};">Free 1 ct black diamond studs</div>'
            f'<div style="margin-top:4px;">With orders from $2,000 (was $3,000)</div></td></tr></table></td></tr>')


def gift_hero(t, href):
    """Gift emails: the studs big + 'black or white?' (engagement; answers open WhatsApp)."""
    return (B.frame_img(t, IMG["studs"], "Free 1 ct natural black diamond studs in yellow gold", href=href, w=520, pad="0 28px", border=GOLD))


def diamond_line(t, pad="4px 48px 10px"):
    th = THEMES[t]
    return (f'<tr><td align="center" class="pad" style="padding:{pad};font-family:{SANS};font-size:12px;line-height:1.6;color:{th["muted"]};">'
            f'Every diamond we set is natural, never lab-grown, moissanite or a simulant. Your piece ships with a certificate for its diamonds and solid gold.</td></tr>')


def sign(t, line="Talk soon,", align="center"):
    return signoff(t, line=line, align=align, pad="14px 48px 26px")


def sales_page(t, pre, top, h1t, lead_html, btns, extra=(), url="", h1_align="center", sign_line="Talk soon,", gift=True, h1_size=38):
    rows = list(top)
    rows.append(h1(t, h1t, align=h1_align, size=h1_size, pad="28px 48px 10px"))
    if lead_html:
        rows.append(lead(t, lead_html, align=h1_align))
    rows.append(buttons(t, btns))
    rows += list(extra)
    rows.append(icon_strip(t, pay_href=url, gift_href=url))
    if gift:
        rows.append(gift_strip(t, url))
    rows.append(sign(t, sign_line, align="center" if h1_align == "center" else "left"))
    rows.append(diamond_line(t))
    html = head(t, pre).replace("</style>", B.class_css(t) + "</style>", 1)
    return html + "".join(rows) + trust(t) + foot(t)


HI = "Hi {{ first_name|default:'there' }}, "

# ---------------------------------------------------------------- content by role (url = where the main CTA goes)
def role_reminder(flow, t, url, piece, back):
    top = [kicker(t, "Saved for you", pad="24px 40px 0"), logo(t, pad="16px 40px 22px"), piece]
    h = "You were one step away." if flow == "chk" else "Still thinking about it?"
    return sales_page(t, "Saved exactly as you left it. One tap takes you back.", top, h,
                      HI + "I kept it exactly as you left it: the piece, the size, the gold.",
                      [(back, url, True), ("Ask Daniel", wa("Hi Daniel, I have a question about my piece."), False)], url=url)


def role_question(t, url, thumb):
    top = [logo(t, pad="22px 40px 16px"), kicker(t, "A quick question", pad="0 40px 0")]
    ans = [("The final price", wa("Hi Daniel, what stopped me at checkout was the price.")),
           ("Shipping or customs", wa("Hi Daniel, what stopped me at checkout was shipping or customs.")),
           ("Not sure about the size", wa("Hi Daniel, I'm not sure about the size.")),
           ("I want to change something", wa("Hi Daniel, I'd like to change something in the piece.")),
           ("Just not ready yet", wa("Hi Daniel, I'm just not ready yet."))]
    t_ = THEMES[t]
    rows = list(top) + [h1(t, "What stopped you at checkout?", pad="16px 48px 8px"),
                        lead(t, "Tap the closest answer. It opens WhatsApp with me, and it's usually a one-minute fix."),
                        answer_buttons(t, ans),
                        buttons(t, [("Back to my order", url, True)], pad="8px 32px 6px"),
                        thumb, icon_strip(t, pay_href=url, gift_href=url), gift_strip(t, url),
                        sign(t, "Thank you for telling me,"), diamond_line(t)]
    html = head(t, "One tap is enough. I read every answer myself.").replace("</style>", B.class_css(t) + "</style>", 1)
    return html + "".join(rows) + trust(t) + foot(t)


def role_call(t, url, thumb, browse=False):
    top = [logo(t, pad="22px 40px 16px"), B.hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
           kicker(t, "Let's talk", pad="26px 40px 0")]
    h = "Let's talk it through." if browse else "15 minutes, just us and your piece."
    return sales_page(t, "See the stones on camera, find your size, change what you like.", top, h,
                      "Stones, size, gold, changes. On a short video call I show you everything live. No script, no pressure.",
                      [("Book 15 minutes", BOOK, True), ("WhatsApp me", WA, False)], extra=[thumb], url=url, sign_line="Hope to see you soon,")


def role_reviews(t, url, back, top_extra):
    top = top_extra + [B.kicker(t, "In their words", pad="26px 40px 0")]
    return sales_page(t, "Read what they wrote once the box was open.", top, "Don't take my word for it.",
                      "550+ reviews on Etsy, Google and Facebook, from people who hesitated too, written after the box was open.",
                      [("Read the reviews", REVIEWS, True), (back, url, False)], url=url)


def role_fit(t, url, back, top, thumb=None):
    lead_html = (f'Not sure of your size? I help you measure at home. One resizing is included, and you have 30 days '
                 f'(<a class="l" href="{REFUND}" target="_blank">return policy</a>).')
    return sales_page(t, "Size, returns and care, answered in one minute.", top, "What if it doesn't fit?", lead_html,
                      [(back, url, True), ("Help me with my size", wa("Hi Daniel, can you help me with my ring size?"), False)],
                      extra=[thumb] if thumb else [], url=url)


def role_affirm(t, url, back, piece):
    top = [logo(t, pad="24px 40px 22px"), kicker(t, "Wear it now", pad="0 40px 18px"), piece]
    return sales_page(t, "Choose Affirm at checkout and see your plan before you commit.", top, "Wear it now. Pay over time.",
                      "Choose Affirm at checkout and see your monthly plan before you commit. Checking won't affect your credit score.",
                      [("See my Affirm options", url, True), ("Talk numbers with me", wa("Hi Daniel, can we talk through payment options?"), False)], url=url)


def role_made(t, url, back, thumb):
    top = [logo(t, pad="24px 40px 20px"), B.hero(IMG["studio"], "A jeweler setting a black diamond at the bench"), kicker(t, "How we make it", pad="28px 40px 0")]
    return sales_page(t, "How your piece is made, and how it gets to you.", top, "Made by hand, after you order.",
                      "In your size and your gold, set stone by stone, shipped within 10 business days, insured, on us.",
                      [(back, url, True), ("Ask Daniel", WA, False)], extra=[thumb], url=url)


def linked_cart_piece(t, url, w=460):
    th = THEMES[t]
    name = (f'<a href="{url}" target="_blank" style="color:{th["text"]};text-decoration:none;">'
            "{{ event|lookup:'Product Name'|default:'Your piece' }}</a>")
    return ("{% if event.ImageURL %}" + B.frame_img(t, "{{ event.ImageURL }}", "{{ event|lookup:'Product Name' }}", url, w=w) + "{% endif %}"
            + B.caption(t, name, "{{ event|lookup:'Variant Name' }}"))


def role_made_piece(t, url, piece):
    """Cart 4/8: the chosen piece big at the top (image + name link to its product page), the bench photo below."""
    top = [logo(t, pad="24px 40px 18px"), kicker(t, "The piece we'd make for you", pad="0 40px 16px"), piece]
    bench = [B.hero(IMG["studio"], "A jeweler setting a black diamond at the bench", pad="10px 32px 0")]
    return sales_page(t, "Your piece, made by hand after you order.", top, "Made by hand, after you order.",
                      "In your size and your gold, set stone by stone, shipped within 10 business days, insured, on us.",
                      [("See my piece", url, True), ("Ask Daniel", WA, False)], extra=bench, url=url)


def role_diamond(t, url, back, top, thumb):
    """Now late in the flow. Short, both branches (Black Ice / REMNANT vs everything else) kept."""
    th = THEMES[t]
    body_ = ("{% if 'Black Ice' in event.Collections or 'REMNANT' in event.Collections %}"
             + h1(t, "Yes, it's a natural black diamond.", pad="28px 48px 10px")
             + lead(t, "Formed in the earth like a white diamond, black from tiny graphite inclusions. Not spinel, onyx, moissanite or lab-grown.")
             + "{% else %}"
             + h1(t, "Yes, every diamond is natural.", pad="28px 48px 10px")
             + lead(t, "Formed in the earth. Not lab-grown, not moissanite, not a simulant. Chosen one by one for how it handles light.")
             + "{% endif %}")
    rows = list(top) + [body_, lead(t, "Every piece ships with a certificate for its diamonds and its solid gold.", pad="6px 48px 4px"),
                        buttons(t, [(back, url, True), ("See a certificate", wa("Hi Daniel, can you send me an example certificate?"), False)]),
                        thumb, icon_strip(t, pay_href=url, gift_href=url), gift_strip(t, url), sign(t)]
    html = head(t, "What's in your piece, and the certificate that proves it.").replace("</style>", B.class_css(t) + "</style>", 1)
    return html + "".join(rows) + trust(t) + foot(t)


def role_gift(t, url, back, thumb):
    top = [kicker(t, "A gift with your order", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"), gift_hero(t, url)]
    ask = [lead(t, "<b>Black or white studs, which would you choose?</b> Tap one, I'd love to know.", pad="16px 48px 2px"),
           buttons(t, [("Black", wa("Hi Daniel, I'd choose the black studs."), False), ("White", wa("Hi Daniel, I'd choose the white studs."), False)], pad="10px 32px 4px")]
    return sales_page(t, "And a gift I wanted you to know about.", top, "One last note from me.",
                      "Free 1 ct natural black diamond studs with orders from $2,000 (it used to be $3,000). "
                      "This is the last email about this piece. If it's no longer the one, just reply and tell me why.",
                      [(back, url, True)], extra=ask + [thumb], url=url, gift=False, sign_line="With gratitude,")


# ---------------------------------------------------------------- the 20 sales emails
R2 = {}

# checkout
R2["WtYdde"] = lambda: role_reminder("chk", "bone", CHK_URL, B.chk_piece("bone", w=480), "Return to my order")
R2["VdW7XY"] = lambda: role_question("paper", CHK_URL, B.chk_thumb_row("paper", "Your order"))
R2["SNvbQS"] = lambda: role_call("paper", CHK_URL, B.chk_thumb_row("paper", "We can talk about"))           # 3/8 now: talk
R2["VLjUfd"] = lambda: role_reviews("bone", CHK_URL, "Return to my order",
                                    [logo("bone", pad="22px 40px 18px"), B.hero(IMG["reviews-oval"], "A natural black diamond oval ring with two white diamonds, in its box")])
R2["WiHGws"] = lambda: role_fit("ink", CHK_URL, "Return to my order",
                                [logo("ink", pad="24px 40px 20px"), B.hero(IMG["fit"], "A ring mandrel and ring size gauges on a jeweler's bench"),
                                 kicker("ink", "Size and peace of mind", pad="28px 40px 0")], B.chk_thumb_row("ink", "Your piece, kept as you chose it"))
R2["V4FBhc"] = lambda: role_affirm("noir", CHK_URL, "Return to my order", B.chk_piece("noir", w=420))
R2["TNDw3W"] = lambda: role_diamond("paper", CHK_URL, "Return to my order",                                  # 7/8 now: diamonds
                                    [logo("paper", pad="22px 40px 18px"), B.hero(IMG["diamonds"], "Natural black diamonds in a diamond parcel paper, with tweezers and a loupe"),
                                     kicker("paper", "About the stone", pad="26px 40px 0")], B.chk_thumb_row("paper", "The stone in your piece"))
R2["SyBqNG"] = lambda: role_gift("noir", CHK_URL, "Return to my order", B.chk_thumb_row("noir", "Your order"))

# cart
R2["U58x8u"] = lambda: role_reminder("cart", "paper", CART_URL, B.cart_piece("paper", w=480), "Back to my piece")
R2["UBwjpH"] = lambda: role_call("ink", CART_URL, B.cart_thumb_row("ink", "We can talk about"))              # 2/8 now: talk
R2["Xzm3N4"] = lambda: role_reviews("paper", CART_URL, "Back to my piece",
                                    [logo("paper", pad="24px 40px 20px"),
                                     B.hero(IMG["reviews-emerald"], "A natural black diamond emerald-cut ring in rose gold, in its box", pad="0 32px")])
# 4/8 (Daniel 5.11): the piece the customer chose leads the email and every CTA goes to its product page
R2["Y7JQ5h"] = lambda: role_made_piece("ink", CART_URL, linked_cart_piece("ink", CART_URL, w=460))
R2["WRGJQ3"] = lambda: role_fit("bone", CART_URL, "Back to my piece",
                                [logo("bone", pad="22px 40px 18px"), B.hero(IMG["fit"], "A ring mandrel and ring size gauges on a jeweler's bench"),
                                 kicker("bone", "Size and peace of mind", pad="26px 40px 0")], B.cart_thumb_row("bone", "Your piece"))
R2["TPeL6i"] = lambda: role_affirm("noir", CART_URL, "Back to my piece", B.cart_piece("noir", w=420))
R2["UmCymx"] = lambda: role_diamond("ink", CART_URL, "Back to my piece",                                     # 7/8 now: diamonds
                                    [logo("ink", pad="24px 40px 20px"), kicker("ink", "About the stone", pad="0 40px 16px"),
                                     B.hero(IMG["diamonds"], "Natural black diamonds in a diamond parcel paper, with tweezers and a loupe", pad="0 32px")],
                                    B.cart_thumb_row("ink", "The stone in your piece"))
R2["XjtgKS"] = lambda: role_gift("bone", CART_URL, "Back to my piece", B.cart_thumb_row("bone", "Your piece"))


# browse
def _browse1():
    t = "bone"
    top = [logo(t, pad="22px 40px 18px"), kicker(t, "You were looking at", pad="0 40px 16px"),
           "{% if event.ImageURL %}" + B.frame_img(t, "{{ event.ImageURL }}", "{{ event.Name }}", VIEW_URL, w=480) + "{% endif %}"]
    return sales_page(t, "Made to order for you, shipped insured on us, with lifetime care.", top, "{{ event.Name }}",
                      "Made to order in solid gold, shipped insured on us. Another gold, stone or an engraving? Just ask.",
                      [("See it again", VIEW_URL, True), ("Customize it with Daniel", BOOK, False)], url=VIEW_URL, h1_size=34)


def _browse2():
    t = "noir"
    top = [logo(t, pad="24px 40px 20px"), B.hero(IMG["studio"], "A jeweler setting a black diamond at the bench"), kicker(t, "Why Diana Rafael", pad="28px 40px 0")]
    return sales_page(t, "Natural diamonds, solid gold, made by hand since 2014.", top, "Why people trust us with the big ones.",
                      "Since 2014, in the Diamond Trading Center in Ramat Gan. Made by hand to order. 550+ reviews.",
                      [("Read the reviews", REVIEWS, True), ("Back to the {{ event.Name }}", VIEW_URL, False)],
                      extra=[B.browse_thumb_row(t, "The piece you looked at")], url=VIEW_URL)


def _browse3():
    t = "noir"
    top = [kicker(t, "A gift with your order", pad="24px 40px 0"), logo(t, pad="14px 40px 20px"), gift_hero(t, VIEW_URL)]
    ask = [lead(t, "<b>Black or white studs, which would you choose?</b>", pad="16px 48px 2px"),
           buttons(t, [("Black", wa("Hi Daniel, I'd choose the black studs."), False), ("White", wa("Hi Daniel, I'd choose the white studs."), False)], pad="10px 32px 4px"),
           B.browse_thumb_row(t, "With the piece you looked at")]
    return sales_page(t, "Free 1 ct natural black diamond studs, now from $2,000 (was $3,000).", top, "A pair of studs, on us.",
                      "Free 1 ct natural black diamond studs with orders from $2,000 (was $3,000), in solid gold, made in our studio.",
                      [("Make it yours", VIEW_URL, True)], extra=ask, url=VIEW_URL, gift=False)


def _browse4():
    t = "paper"
    top = [logo(t, pad="22px 48px 16px", align="left", width=160), B.hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
           kicker(t, "A letter from Daniel", align="left", pad="26px 48px 0")]
    return sales_page(t, "Size, gold, stone, budget: ask a person, not a chatbot.", top, "Let's talk it through.",
                      "Size, white or yellow gold, a bigger stone, a thinner band: 15 minutes with me and we design it together.",
                      [("Book 15 minutes", BOOK, True), ("WhatsApp me", WA, False)], extra=[B.browse_thumb_row(t, "We can talk about")],
                      url=VIEW_URL, h1_align="left", sign_line="Daniel,")


R2["WwmdnE"] = _browse1
R2["UDi5wM"] = _browse2
R2["XB8MV8"] = _browse3
R2["QXP4ar"] = _browse4

# subjects for the swapped slots (Klaviyo subject lives on the flow message, so these change with the content)
SUBJECT_OVERRIDE = {"SNvbQS": "15 minutes with me?", "TNDw3W": "Is it really a natural diamond?",
                    "UBwjpH": "15 minutes with me?", "UmCymx": "Is it really a natural diamond?"}

if __name__ == "__main__":
    import vip
    os.makedirs(OUT, exist_ok=True)
    built = {"TLp5wQ": vip.build()}
    for tpl, fn in B.P.items():
        built[tpl] = (R2.get(tpl) or fn)()
    for tpl, html in built.items():
        open(os.path.join(OUT, tpl + ".html"), "w", encoding="utf-8").write(html)
    print("built", len(built), "(round 2 for", len(R2), "sales emails)")
