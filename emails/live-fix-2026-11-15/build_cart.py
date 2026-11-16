"""Live abandoned-CART flow VWbEYm "2026-11 | Abandoned Cart (8)" (trigger: Shopify Added to Cart, metric WT7SJV),
rebuilt 16.11.2026 to the 15.11 checkout standard (Daniel approved 16.11):
first name in every email (with fallback), the discount an email promises as a REAL code with an apply link,
the gifts big (studs black OR white + inside engraving, from $2,000), 550+ reviews, no delivery date, no AFFIRM10.

Cart events carry event.URL (myshopify product URL), event.ImageURL, event["Product Name"], event["Variant Name"],
event.Price, event.$value, event.Categories. No line-item list, so every product block uses those fields.

Code ladder (cumulative delays 4h, 1d, 3d, 5d, 7d, 9d, 11d, 14d):
  1 reminder, 2 natural diamond     -> no code (gifts only)
  3 reviews, 4 made, 5 fit, 6 Affirm -> CART5  (extra 5%)
  7 call, 8 last note                -> CART10 (extra 10%, best offer)

Each email has its own hero structure and the theme alternates light/dark, so consecutive emails never look alike:
  1 paper  framed piece leads              5 paper  fit photo full-bleed ABOVE the logo, left-aligned text
  2 ink    stone photo full-bleed          6 ink    split row: piece left, price + Affirm right
  3 bone   giant "550+" numeral            7 bone   video-call photo, inset
  4 noir   piece + bench photo below       8 noir   letter: the gifts ARE the hero, code card, piece as a thumb
Usage: python build_cart.py -> out/<template_id>.html (keyed by the template each action uses today)
"""
import os
import build_live as L
from build_live import B, R, THEMES, IMG, SERIF, SANS, kicker, logo, h1, head, trust, foot, code_card, name, HI, OUT

CART_URL = B.CART_URL   # myshopify URL rewritten to dianarafael.com, /cart as fallback
VALUE = "event|lookup:'$value'"
PNAME = "{{ event|lookup:'Product Name'|default:'Your piece' }}"
VNAME = "{{ event|lookup:'Variant Name' }}"
BLACK_IF = "'Black Ice' in event.Categories or 'REMNANT' in event.Categories"


def apply_url(code):
    """Sets the code (Shopify shareable discount link), then returns her to the piece she added."""
    return ("https://dianarafael.com/discount/" + code + "?redirect="
            "{% if 'myshopify.com' in event.URL %}{{ event.URL|slice:'34:'|urlencode }}{% else %}%2Fcart{% endif %}")


def gifts(t):
    """Same gifts block as the checkout flow, but the qualification line reads the cart event's $value."""
    return L.gifts(t)   # L.gifts already uses event|lookup:'$value', which Added to Cart events carry


def split_piece(t):
    """Email 6: piece on the left, name + price + Affirm line on the right (stacks on mobile)."""
    th = THEMES[t]
    return ("{% if event.ImageURL %}"
            f'<tr><td class="pad" style="padding:6px 40px 6px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" '
            f'style="border:1px solid {th["rule"]};"><tr>'
            f'<td class="col colpad" width="50%" valign="middle" bgcolor="#f6f1e7" style="width:50%;background:#f6f1e7;padding:18px;">'
            f'<a href="{CART_URL}" target="_blank"><img src="{{{{ event.ImageURL }}}}" width="230" alt="{PNAME}" '
            f'style="display:block;width:100%;max-width:230px;height:auto;border:0;margin:0 auto;"/></a></td>'
            f'<td class="col" width="50%" valign="middle" style="width:50%;padding:20px 22px;font-family:{SANS};">'
            f'<div style="font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:700;color:{th["accent"]};">Your piece</div>'
            f'<div style="margin-top:8px;font-family:{SERIF};font-size:22px;line-height:1.2;color:{th["text"]};">{PNAME}</div>'
            "{% if event.Price %}"
            f'<div style="margin-top:12px;font-family:{SERIF};font-size:30px;color:{th["text"]};">${{{{ event.Price|floatformat:"0g" }}}}</div>'
            "{% endif %}"
            f'<div style="margin-top:8px;font-size:13px;line-height:1.5;color:{th["muted"]};">Or split it into monthly payments with Affirm. '
            f'You see the plan before you commit.</div></td></tr></table></td></tr>'
            "{% endif %}")


def big_number(t, num, label):
    th = THEMES[t]
    return (f'<tr><td align="center" class="pad" style="padding:6px 40px 0;font-family:{SERIF};">'
            f'<div class="big" style="font-size:150px;line-height:1;font-weight:500;color:{th["text"]};">{num}</div>'
            f'<div style="margin-top:4px;font-family:{SANS};font-size:12px;letter-spacing:.26em;text-transform:uppercase;font-weight:700;color:{th["accent"]};">{label}</div></td></tr>')


def cpage(t, pre, rows, sign_line="Talk soon,", gifts_end=True, sign_align="center"):
    out = list(rows)
    if gifts_end:
        out.append(gifts(t))
    out.append(R.icon_strip(t, pay_href=CART_URL, gift_href=CART_URL))
    out.append(R.signoff(t, line=sign_line, align=sign_align, pad="14px 48px 26px"))
    out.append(R.diamond_line(t))
    html = head(t, pre).replace("</style>", B.class_css(t) + "</style>", 1)
    return html + "".join(out) + trust(t) + foot(t)


ASK = ("Ask Daniel", R.wa("Hi Daniel, I have a question about my piece."), False)
BACK = "Back to my piece"
E = {}   # template id currently on the action -> (builder, preview text)

# 1/8  Still thinking about it?  (4h)  paper, the piece framed big
E["U58x8u"] = (lambda: cpage("paper", "Saved exactly as you left it, plus two gifts with your order.", [
    kicker("paper", "Saved for you", pad="24px 40px 0"), logo("paper", pad="16px 40px 22px"), B.cart_piece("paper", w=480),
    h1("paper", name("still thinking about it?", "Still thinking about it?"), size=38, pad="28px 48px 10px"),
    R.lead("paper", HI + "I kept it exactly as you left it: the piece, the size, the gold."),
    R.buttons("paper", [(BACK, CART_URL, True), ASK])]),
    "Saved exactly as you left it, plus two gifts with your order.")

# 2/8  Is it really a natural diamond?  (+20h)  ink, stone photo full-bleed, conditional answer
E["UBwjpH"] = (lambda: cpage("ink", "What's in your piece, and the certificate that proves it.", [
    logo("ink", pad="24px 40px 20px"),
    B.hero(IMG["diamonds"], "Natural black diamonds in a diamond parcel paper, with tweezers and a loupe"),
    kicker("ink", "About the stone", pad="28px 40px 0"),
    "{% if " + BLACK_IF + " %}"
    + h1("ink", name("yes, it&#39;s a natural black diamond.", "Yes, it&#39;s a natural black diamond."), size=34, pad="20px 48px 10px")
    + R.lead("ink", "Formed in the earth like a white diamond, black from tiny graphite inclusions. Not spinel, onyx, moissanite or lab-grown.")
    + "{% else %}"
    + h1("ink", name("yes, every diamond is natural.", "Yes, every diamond is natural."), size=34, pad="20px 48px 10px")
    + R.lead("ink", "Formed in the earth. Not lab-grown, not moissanite, not a simulant. Chosen one by one for how it handles light.")
    + "{% endif %}",
    R.lead("ink", "Every piece ships with a certificate for its diamonds and its solid gold.", pad="6px 48px 4px"),
    R.buttons("ink", [(BACK, CART_URL, True), ("See a certificate", R.wa("Hi Daniel, can you send me an example certificate?"), False)]),
    B.cart_thumb_row("ink", "The stone in your piece")]),
    "What's in your piece, the certificate that proves it, and two gifts.")

# 3/8  550+ reviews  (+2d)  bone, typographic hero: giant 550+
E["Xzm3N4"] = (lambda: cpage("bone", "Read what they wrote once the box was open, plus an extra 5% (CART5).", [
    logo("bone", pad="24px 40px 8px"), kicker("bone", "In their words", pad="14px 40px 4px"),
    big_number("bone", "550+", "Reviews on Etsy, Google &amp; Facebook"),
    h1("bone", name("don&#39;t take my word for it.", "Don&#39;t take my word for it."), size=34, pad="26px 48px 10px"),
    R.lead("bone", "From people who hesitated too, written after the box was open. And to make it easier, an extra 5% is yours."),
    R.buttons("bone", [("Apply 5% to my piece", apply_url("CART5"), True), ("Read the reviews", R.REVIEWS, False)]),
    code_card("bone", "CART5", 5, "Already applied when you tap the button above. One use, on top of today&#39;s prices."),
    B.hero(IMG["reviews-emerald"], "A natural black diamond emerald-cut ring in rose gold, in its box", pad="18px 40px 6px"),
    B.cart_thumb_row("bone", "Your piece")]),
    "Read what they wrote once the box was open, plus an extra 5% (CART5).")

# 4/8  Made by hand, for you  (+2d)  noir, the piece leads, bench photo under the CTA
E["Y7JQ5h"] = (lambda: cpage("noir", "Your piece, made by hand after you order. Your extra 5% is still on it.", [
    logo("noir", pad="24px 40px 18px"), kicker("noir", "The piece we&#39;d make for you", pad="0 40px 16px"),
    R.linked_cart_piece("noir", CART_URL, w=460),
    h1("noir", name("made by hand, for you.", "Made by hand, for you."), size=36, pad="28px 48px 10px"),
    R.lead("noir", "After you order, in your size and your gold, set stone by stone at our bench in the Diamond Trading Center. Shipped insured, on us."),
    R.buttons("noir", [("Apply 5% to my piece", apply_url("CART5"), True), ASK]),
    code_card("noir", "CART5", 5, "Already applied when you tap the button above. One use."),
    B.hero(IMG["studio"], "A jeweler setting a black diamond at the bench", pad="18px 32px 0")]),
    "Your piece, made by hand after you order. Your extra 5% is still on it.")

# 5/8  What if it doesn't fit?  (+2d)  paper, photo full-bleed above the logo, left-aligned
E["WRGJQ3"] = (lambda: cpage("paper", "Size, returns and care, answered in one minute. CART5 still applies.", [
    B.hero(IMG["fit"], "A ring mandrel and ring size gauges on a jeweler's bench"),
    logo("paper", pad="22px 48px 4px", align="left", width=160), kicker("paper", "Size and peace of mind", align="left", pad="18px 48px 0"),
    h1("paper", name("what if it doesn&#39;t fit?", "What if it doesn&#39;t fit?"), align="left", size=36, pad="14px 48px 10px"),
    R.lead("paper", "Not sure of your size? I help you measure at home. One resizing is included, and you have 30 days "
           f'(<a class="l" href="{R.REFUND}" target="_blank">return policy</a>).', align="left"),
    R.buttons("paper", [("Apply 5% to my piece", apply_url("CART5"), True), ("Help me with my size", R.wa("Hi Daniel, can you help me with my ring size?"), False)]),
    code_card("paper", "CART5", 5, "Already applied when you tap the button above. One use."),
    B.cart_thumb_row("paper", "Your piece, kept as you chose it")], sign_align="left"),
    "Size, returns and care, answered in one minute. CART5 still applies.")

# 6/8  Wear it now, pay over time  (+2d)  ink, split row piece | price + Affirm
E["TPeL6i"] = (lambda: cpage("ink", "Choose Affirm at checkout, keep your extra 5%, and your gifts.", [
    logo("ink", pad="24px 40px 14px"), kicker("ink", "Wear it now", pad="0 40px 0"),
    h1("ink", name("wear it now, pay over time.", "Wear it now. Pay over time."), size=36, pad="18px 48px 14px"),
    split_piece("ink"),
    R.lead("ink", "Choose Affirm at checkout and see your monthly plan before you commit. Checking won&#39;t affect your credit score. "
           "Your extra 5% still applies.", pad="16px 48px 4px"),
    R.buttons("ink", [("See my Affirm options", apply_url("CART5"), True), ("Talk numbers with me", R.wa("Hi Daniel, can we talk through payment options?"), False)]),
    code_card("ink", "CART5", 5, "Applied for you with the button above. Works with Affirm.")]),
    "Choose Affirm at checkout, keep your extra 5%, and your gifts.")

# 7/8  15 minutes with me?  (+2d)  bone, video-call photo inset, first CART10
E["UmCymx"] = (lambda: cpage("bone", "Ask anything on video, plus an extra 10% (CART10) and two gifts.", [
    logo("bone", pad="22px 40px 16px"),
    B.hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
    kicker("bone", "Let&#39;s talk", pad="26px 40px 0"),
    h1("bone", name("15 minutes, just us?", "15 minutes, just us?"), size=38, pad="14px 48px 10px"),
    R.lead("bone", "Stones, size, gold, changes. On a short video call I show you everything live. No script, no pressure. "
           "And if you&#39;re ready without the call, here is an extra 10%."),
    R.buttons("bone", [("Book 15 minutes", R.BOOK, True), ("Apply 10% to my piece", apply_url("CART10"), False)]),
    code_card("bone", "CART10", 10, "Applied for you with the second button. One use, on top of today&#39;s prices."),
    B.cart_thumb_row("bone", "We can talk about")], sign_line="Hope to see you soon,"),
    "Ask anything on video, plus an extra 10% (CART10) and two gifts.")

# 8/8  A note from me  (+3d)  noir, a letter: the gifts are the hero, then the best offer
E["XjtgKS"] = (lambda: cpage("noir", "My best offer, an extra 10% (CART10), and two gifts I wanted you to know about.", [
    kicker("noir", "A note from me", pad="26px 40px 0"), logo("noir", pad="14px 40px 6px"),
    h1("noir", name("one last note from me.", "One last note from me."), size=36, pad="18px 48px 10px", italic=True),
    R.lead("noir", "This is my last email about your piece, so here is my best offer: an extra 10%, and the two gifts below. "
           "If it&#39;s no longer the one, just reply and tell me why. I read every answer myself."),
    gifts("noir"),
    code_card("noir", "CART10", 10, "Applied for you with the button below. One use, on top of today&#39;s prices."),
    R.buttons("noir", [("Apply 10% to my piece", apply_url("CART10"), True), ("Talk to Daniel", R.BOOK, False)]),
    B.cart_thumb_row("noir", "Your piece")], sign_line="With gratitude,", gifts_end=False),
    "My best offer, an extra 10% (CART10), and two gifts I wanted you to know about.")

# action id -> template id it points to today (16.11 morning)
ACTIONS = [("123488071", "U58x8u"), ("123488075", "UBwjpH"), ("123488078", "Xzm3N4"), ("123488082", "Y7JQ5h"),
           ("123488084", "WRGJQ3"), ("123488087", "TPeL6i"), ("123488094", "UmCymx"), ("123488097", "XjtgKS")]

if __name__ == "__main__":
    for tid, (f, pre) in E.items():
        html = f()
        open(os.path.join(OUT, tid + ".html"), "w", encoding="utf-8").write(html)
        print(tid, len(html))
