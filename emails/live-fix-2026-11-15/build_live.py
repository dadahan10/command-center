"""Live abandoned-checkout flow XW6UqR + Book-appointment flow Sd7zsb, rebuilt 15.11.2026 (Daniel):
first name in every email, a REAL code wherever a discount is promised, the gifts shown big (studs black or white +
inside engraving, from $2,000), no broken buttons. Built on the 4.11 round-2 blocks (redesign-2026-11-04).
Codes (Shopify, created 15.11, once per customer, not combinable, total-off rule):
  CART5  = 5.88% on sale price  -> 20% total off compare-at  ("an extra 5%")
  CART10 = 11.76% on sale price -> 25% total off compare-at  ("an extra 10%")
Usage: python build_live.py -> out/<template_id>.html
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.join(HERE, "..", "flow-templates", "redesign-2026-11-04")
sys.path.insert(0, RD); os.chdir(RD)
import build_all as B
import round2 as R
from rd import *
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)

STUDS_BLACK = "https://cdn.klaviyomail.com/company/UEHusj/images/d40d6d65-4a9c-4977-ad32-43b1fcbc87b2.jpeg"
STUDS_WHITE = "https://cdn.klaviyomail.com/company/UEHusj/images/66a849f8-e6f6-4cd4-8415-36c8f1ef8dd1.jpeg"
CHK = "{{ event.extra.responsive_checkout_url|default:'https://dianarafael.com/cart' }}"
VALUE = "event|lookup:'$value'"


def name(lower, upper):
    """'Katherine, lower' when we know the name, otherwise 'Upper'."""
    return "{% if first_name %}{{ first_name }}, " + lower + "{% else %}" + upper + "{% endif %}"


HI = "{% if first_name %}Hi {{ first_name }}, {% else %}Hi, {% endif %}"


def apply_url(code):
    # Shopify shareable discount link: sets the code, then returns her to her own saved checkout
    return ("https://dianarafael.com/discount/" + code + "?redirect="
            "{% if event.extra.responsive_checkout_url %}{{ event.extra.responsive_checkout_url|slice:'23:'|urlencode }}{% else %}%2Fcart{% endif %}")


def code_card(t, code, pct, line):
    th = THEMES[t]
    return (f'<tr><td class="pad" style="padding:18px 48px 8px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" '
            f'style="border:1px dashed {th["accent"]};"><tr><td align="center" style="padding:22px 18px 20px;font-family:{SANS};">'
            f'<div style="font-size:11px;letter-spacing:.26em;text-transform:uppercase;font-weight:700;color:{th["accent"]};">An extra {pct}% off, just for you</div>'
            f'<div style="margin:10px 0 6px;font-family:{SERIF};font-size:44px;line-height:1;letter-spacing:.12em;color:{th["text"]};">{code}</div>'
            f'<div style="font-size:13px;line-height:1.5;color:{th["muted"]};">{line}</div>'
            f'</td></tr></table></td></tr>')


def gifts(t):
    """The gifts, big: studs black or white (tap = tell Daniel on WhatsApp) + inside engraving. From $2,000."""
    th = THEMES[t]
    q = "{% if " + VALUE + " >= 2000 %}Your order already qualifies.{% else %}With orders from $2,000.{% endif %}"

    def stud(img, label, msg):
        return (f'<td class="col colpad" width="50%" valign="top" align="center" style="width:50%;padding:0 8px;">'
                f'<a href="{R.wa(msg)}" target="_blank" style="text-decoration:none;"><img src="{img}" width="230" alt="Free natural {label.lower()} diamond studs" '
                f'style="display:block;width:100%;max-width:230px;height:auto;border:0;margin:0 auto;"/>'
                f'<div style="margin-top:10px;display:inline-block;padding:11px 20px;border:1px solid {th["accent"]};font-family:{SANS};font-size:12px;'
                f'font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{th["text"]};">I&#39;d choose {label}</div></a></td>')

    return (f'<tr><td class="pad" style="padding:26px 32px 6px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" '
            f'style="border-top:1px solid {th["rule"]};"><tr><td align="center" style="padding:24px 8px 4px;font-family:{SANS};">'
            f'<div style="font-size:11px;letter-spacing:.26em;text-transform:uppercase;font-weight:700;color:{th["accent"]};">Two gifts with your order</div>'
            f'<div style="margin-top:8px;font-family:{SERIF};font-size:30px;line-height:1.15;color:{th["text"]};">Free diamond studs + free engraving</div>'
            f'<div style="margin-top:6px;font-size:14px;line-height:1.5;color:{th["muted"]};">{q} Natural diamond studs in 14K gold, '
            f'and a date, initials or a word engraved inside your ring.</div>'
            f'<div style="margin-top:16px;font-family:{SERIF};font-size:21px;color:{th["text"]};">Black or white studs, which would you choose?</div>'
            f'</td></tr><tr><td style="padding:14px 0 6px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr>'
            + stud(STUDS_BLACK, "Black", "Hi Daniel, I'd choose the black studs.")
            + stud(STUDS_WHITE, "White", "Hi Daniel, I'd choose the white studs.")
            + '</tr></table></td></tr></table></td></tr>')


def page(t, pre, top, h1t, lead_html, btns, extra=(), url=CHK, sign_line="Talk soon,", h1_size=38):
    rows = list(top) + [h1(t, h1t, size=h1_size, pad="28px 48px 10px")]
    if lead_html:
        rows.append(R.lead(t, lead_html))
    rows.append(R.buttons(t, btns))
    rows += list(extra)
    rows.append(gifts(t))
    rows.append(R.icon_strip(t, pay_href=url, gift_href=url))
    rows.append(R.sign(t, sign_line))
    rows.append(R.diamond_line(t))
    html = head(t, pre).replace("</style>", B.class_css(t) + "</style>", 1)
    return html + "".join(rows) + trust(t) + foot(t)


ASK = ("Ask Daniel", R.wa("Hi Daniel, I have a question about my order."), False)
EMAILS = {}

# 1/5  Is This the One? (2h)
EMAILS["RGSj5h"] = lambda: page("bone", "Saved exactly as you left it, with an extra 5% and two gifts.",
    [kicker("bone", "Saved for you", pad="24px 40px 0"), logo("bone", pad="16px 40px 22px"), B.chk_piece("bone", w=480)],
    name("is this the one?", "Is this the one?"),
    HI + "I kept your order exactly as you left it: the piece, the size, the gold.",
    [("Return to my order", apply_url("CART5"), True), ASK],
    extra=[code_card("bone", "CART5", 5, "Already applied when you tap the button above. One use, on top of today&#39;s prices.")])

# 2/5  Extra 5% Off Inside (about 2d 20h)
EMAILS["U3FYQZ"] = lambda: page("paper", "Your code CART5 is inside, plus two gifts with your order.",
    [logo("paper", pad="22px 40px 14px"), kicker("paper", "Your cart is saved", pad="0 40px 18px"), B.chk_piece("paper", w=440)],
    name("an extra 5% is yours.", "An extra 5% is yours."),
    "Use it on the piece you chose. It is applied for you when you tap the button.",
    [("Apply 5% and check out", apply_url("CART5"), True), ASK],
    extra=[code_card("paper", "CART5", 5, "Or enter it at checkout. One use, on top of today&#39;s prices.")])

# 3/5  Last chance (about 3d 20h)
EMAILS["TDAQrS"] = lambda: page("noir", "Your extra 5% (CART5) is still here, and so are your gifts.",
    [kicker("noir", "Still saved for you", pad="24px 40px 0"), logo("noir", pad="16px 40px 22px"), B.chk_piece("noir", w=440)],
    name("your piece is still waiting.", "Your piece is still waiting."),
    "Your extra 5% is still on it, and your two gifts too. If something is holding you back, tell me and I&#39;ll fix it.",
    [("Apply 5% and check out", apply_url("CART5"), True), ("Talk to Daniel", R.BOOK, False)],
    extra=[code_card("noir", "CART5", 5, "Applied for you with the button above. One use.")])

# 4/5  Affirm (about 5d 20h)
EMAILS["Re9UiL"] = lambda: page("ink", "Choose Affirm at checkout, keep your extra 5%, and your gifts.",
    [logo("ink", pad="24px 40px 18px"), kicker("ink", "Wear it now", pad="0 40px 18px"), B.chk_piece("ink", w=420)],
    name("wear it now, pay over time.", "Wear it now. Pay over time."),
    "Choose Affirm at checkout and see your monthly plan before you commit. Checking won&#39;t affect your credit score. Your extra 5% still applies.",
    [("See my Affirm options", apply_url("CART5"), True), ("Talk numbers with me", R.wa("Hi Daniel, can we talk through payment options?"), False)],
    extra=[code_card("ink", "CART5", 5, "Applied for you with the button above. Works with Affirm.")])

# 5/5  Unlock 10% Off (about 6d 20h): the last and best offer
EMAILS["UNZFjJ"] = lambda: page("noir", "Your code CART10 is inside: an extra 10% off, plus your gifts.",
    [kicker("noir", "My best offer", pad="24px 40px 0"), logo("noir", pad="16px 40px 22px"), B.chk_piece("noir", w=440)],
    name("here&#39;s an extra 10%.", "Here&#39;s an extra 10%."),
    "This is my last email about this piece, so here is my best offer. Pay in full or over time with Affirm.",
    [("Apply 10% and check out", apply_url("CART10"), True), ("Talk to Daniel", R.BOOK, False)],
    extra=[code_card("noir", "CART10", 10, "Applied for you with the button above. One use, on top of today&#39;s prices.")],
    sign_line="With gratitude,")

# Book-appointment flow Sd7zsb email 1 (opened emails, no orders): no cart, no code. The gifts + a consultation.
EMAILS["TTiY7x"] = lambda: page("paper", "15 minutes on video with Daniel, plus two gifts with your order.",
    [logo("paper", pad="22px 40px 16px"), B.hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
     kicker("paper", "Let&#39;s talk", pad="26px 40px 0")],
    name("15 minutes, just us?", "15 minutes, just us?"),
    "Stones, size, gold, changes. On a short video call I show you everything live. No script, no pressure.",
    [("Book 15 minutes", R.BOOK, True), ("WhatsApp me", R.WA, False)],
    url="https://dianarafael.com/collections/black-ice", sign_line="Hope to see you soon,")

if __name__ == "__main__":
    for tid, f in EMAILS.items():
        html = f()
        open(os.path.join(OUT, tid + ".html"), "w", encoding="utf-8").write(html)
        print(tid, len(html))
