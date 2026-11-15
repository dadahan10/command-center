"""15.11.2026 part 2: the other two abandonment flows that actually send (last 30 days):
VB4v4q Abandoned Checkout - NOT Black Ice (Checkout Started) and Y6Zunh Browse Abandonment (Viewed Product RdGtZY).
Same rules as build_live.py: first name, real code where a discount is promised, gifts (studs black/white + engraving).
Cart flows UrfQ29 / Y3ZV7x are not touched: their trigger (RjxRum) has not fired since 30.7.2025.
Usage: python build_more.py -> out/<key>.html
"""
import os
import build_live as L
from build_live import B, R, THEMES, IMG, kicker, logo, h1, head, trust, foot, page, code_card, name, HI, apply_url, ASK, OUT

VIEW = "{{ event.URL|default:'https://dianarafael.com/collections/black-ice' }}"


def apply_view(code):
    return ("https://dianarafael.com/discount/" + code + "?redirect="
            "{% if event.URL %}{{ event.URL|slice:'23:'|urlencode }}{% else %}%2Fcollections%2Fblack-ice{% endif %}")


def browse_top(t, kick):
    return [logo(t, pad="22px 40px 16px"), kicker(t, kick, pad="0 40px 16px"),
            "{% if event.ImageURL %}" + B.frame_img(t, "{{ event.ImageURL }}", "{{ event.Name }}", VIEW, w=460) + "{% endif %}"
            + B.caption(t, "{{ event.Name }}")]


E = {}
# ---- VB4v4q  Abandoned Checkout - NOT Black Ice (same Checkout Started event as XW6UqR)
E["c1"] = L.EMAILS["RGSj5h"]                                   # Is This the One?
E["c2"] = L.EMAILS["U3FYQZ"]                                   # cart about to expire -> extra 5%
E["c4"] = lambda: page("bone", "550+ reviews, made by hand since 2014, plus an extra 5% and two gifts.",
    [logo("bone", pad="22px 40px 18px"), B.hero(IMG["reviews-oval"], "A natural black diamond oval ring with two white diamonds, in its box"),
     kicker("bone", "Why Diana Rafael", pad="26px 40px 0")],
    name("here's why people trust us.", "Here's why people trust us."),
    "Since 2014, in the Diamond Trading Center in Ramat Gan. Made by hand to order. 550+ reviews from people who hesitated too.",
    [("Return to my order", apply_url("CART5"), True), ("Read the reviews", R.REVIEWS, False)],
    extra=[B.chk_thumb_row("bone", "Your order"), code_card("bone", "CART5", 5, "Applied for you with the button above. One use, on top of today&#39;s prices.")])
E["c5"] = L.EMAILS["TDAQrS"]                                   # sparkle about to fade -> still waiting
E["c6"] = lambda: page("paper", "15 minutes on video with Daniel, plus an extra 5% and two gifts.",
    [logo("paper", pad="22px 40px 16px"), B.hero(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call", pad="0 24px"),
     kicker("paper", "Let&#39;s talk", pad="26px 40px 0")],
    name("any questions? Let's meet.", "Any questions? Let's meet."),
    "Stones, size, gold, changes. On a short video call I show you everything live. No script, no pressure.",
    [("Book 15 minutes", R.BOOK, True), ("Return to my order", apply_url("CART5"), False)],
    extra=[B.chk_thumb_row("paper", "We can talk about"), code_card("paper", "CART5", 5, "Applied for you with the button above. One use.")],
    sign_line="Hope to see you soon,")
E["c7"] = L.EMAILS["Re9UiL"]                                   # Affirm
E["c8"] = L.EMAILS["UNZFjJ"]                                   # Affirm & save 10% -> CART10

# ---- Y6Zunh  Browse Abandonment (Viewed Product)
E["b1"] = lambda: page("bone", "Made to order for you, plus two gifts with your order.", browse_top("bone", "You were looking at"),
    name("did you see something you like?", "Did you see something you like?"),
    "Made to order in solid gold, shipped insured on us. Another gold, a different stone or an engraving? Just ask.",
    [("See it again", VIEW, True), ("Customize it with Daniel", R.BOOK, False)], url=VIEW, h1_size=34)
E["b2"] = lambda: page("paper", "15 minutes on video with Daniel, plus two gifts with your order.", browse_top("paper", "Still thinking about it?"),
    name("let's talk it through.", "Let's talk it through."),
    "Size, white or yellow gold, a bigger stone, a thinner band: 15 minutes with me and we design it together.",
    [("Book 15 minutes", R.BOOK, True), ("See it again", VIEW, False)], url=VIEW, sign_line="Hope to see you soon,")
E["b3"] = lambda: page("noir", "Natural diamonds, solid gold, made by hand since 2014.",
    [logo("noir", pad="24px 40px 20px"), B.hero(IMG["studio"], "A jeweler setting a black diamond at the bench"), kicker("noir", "Why Diana Rafael", pad="28px 40px 0")],
    name("why count on us?", "Why count on us?"),
    "Since 2014, in the Diamond Trading Center in Ramat Gan. Made by hand to order. 550+ reviews.",
    [("Read the reviews", R.REVIEWS, True), ("Back to the piece", VIEW, False)],
    extra=[B.browse_thumb_row("noir", "The piece you looked at")], url=VIEW)
E["b4"] = lambda: page("ink", "Choose Affirm at checkout and see your plan before you commit, plus two gifts.", browse_top("ink", "Wear it now"),
    name("wear it now, pay over time.", "Wear it now. Pay over time."),
    "Choose Affirm at checkout and see your monthly plan before you commit. Checking won&#39;t affect your credit score.",
    [("See it again", VIEW, True), ("Talk numbers with me", R.wa("Hi Daniel, can we talk through payment options?"), False)], url=VIEW)
E["b5"] = lambda: page("noir", "Your code CART10 is inside: an extra 10% off, plus two gifts.", browse_top("noir", "An extra 10% for you"),
    name("here's an extra 10%.", "Here's an extra 10%."),
    "On the piece you were looking at, or anything else you love. Applied for you when you tap the button.",
    [("Apply 10% and shop", apply_view("CART10"), True), ("Talk to Daniel", R.BOOK, False)],
    extra=[code_card("noir", "CART10", 10, "Applied for you with the button above. One use, on top of today&#39;s prices.")], url=VIEW)

if __name__ == "__main__":
    for k, f in E.items():
        open(os.path.join(OUT, k + ".html"), "w", encoding="utf-8").write(f())
        print(k)
