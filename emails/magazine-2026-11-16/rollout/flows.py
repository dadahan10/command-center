"""Copy + layout family of every live abandon-flow email (the live 15.11/16.11 messages, re-set in the B&W Issue).
Usage: python flows.py -> out/<flow>-<n>-<fam>.html, plan.json"""
import os, json
from mag import Src, FAM, FAM_NAME, OUT, IMG, REFUND, CARE, tlink, INK, MUTE_L
import build as M
from build import BOOK, REVIEWS, wa, nm, HI

CHK, CART, BROWSE = Src("chk"), Src("cart"), Src("browse")
ASK = ("Ask Daniel", wa("Hi Daniel, I have a question about my order."))
ASK_PIECE = ("Ask Daniel", wa("Hi Daniel, I have a question about my piece."))
TALK_NUM = wa("Hi Daniel, can we talk through payment options?")
C5 = ("CART5", 5)
C10 = ("CART10", 10)

# Real reviews, verbatim from dianarafael.com/pages/our-customers-reviews (read 16.11.2026). Only ones without delivery times.
R_EMORY = ("Emory", "Feb 2025", "If you&#39;re considering ordering from this company, DO IT!! This is my second order, and I will forever order black diamonds "
           "from this company! The customer service is PERFECT! I was skeptical of spending so much money on an order through Etsy, but I am SO glad I did!!")
R_NATHAN = ("Nathan", "Jul 2025", "Daniel was absolutely outstanding, answering all of my ridiculous questions and requests. Made me the most gorgeous ring "
            "I&#39;ve seen and cannot wait to show it off to the world.")
R_DAINA = ("Daina", "Feb 2025", "This ring is everything I dreamed of and more! Pictures do not do it justice!")
R_IRMA = ("Irma", "Mar 2025", "Great craftsmanship and the ring matched the description perfectly. Came with a certificate as well!")
R_MOLLY = ("Molly", "Nov 2024", "Daniel was truly a pleasure to work with, he accommodated a few special requests and created the exact necklace I was looking for.")
R_CRAIG = ("Craig", "Dec 2024", "Great craftsmanship on this ring and truly appreciate support from the vendor from purchase to delivery.")


def gift(src, code, label="Check out with my two gifts"):
    return dict(gift_href=src.go(code), gift_label=label)


# ================================================================ checkout copy (shared by XW6UqR and VB4v4q)
def chk_cover():
    return dict(h="h-cover", alt="Is this the one?", pre="Saved exactly as you left it, with an extra 5% and two gifts.",
                lead=HI + "I kept your order exactly as you left it: the piece, the size, the gold.",
                primary=("Return to my order", CHK.go("CART5")), secondary=ASK,
                code=("CART5", 5, "Already applied when you tap the button above. One use, on top of today&#39;s prices."),
                close=("Complete my order, 5% off", CHK.go("CART5")), **gift(CHK, "CART5"))


def chk_split():
    return dict(pre="Your code CART5 is inside, plus two gifts with your order.",
                big_pre=nm("an extra", "An extra"), big="5%", big_post="is yours.",
                lead="Use it on the piece you chose. It is applied for you when you tap the button.",
                primary=("Apply 5% and check out", CHK.go("CART5")), secondary=ASK,
                code=("CART5", 5, "Or enter it at checkout. One use, on top of today&#39;s prices."),
                close=("Use my 5% now", CHK.go("CART5")), **gift(CHK, "CART5"))


def chk_still():
    return dict(h="h-still", alt="Still waiting.", pre="Your extra 5% (CART5) is still here, and so are your gifts.",
                lead=nm("your extra 5% is still on it, and your two gifts too.", "Your extra 5% is still on it, and your two gifts too.")
                + " If something is holding you back, tell me and I&#39;ll fix it.",
                primary=("Apply 5% and check out", CHK.go("CART5")), secondary=("talk to Daniel", BOOK),
                piece_btn=("Complete my order", CHK.go("CART5")),
                code=("CART5", 5, "Applied for you with the buttons in this email. One use."),
                close=("Check out with 5% off", CHK.go("CART5")), **gift(CHK, "CART5", "Claim my two gifts"))


def chk_index():
    return dict(pre="Choose Affirm at checkout, keep your extra 5%, and your gifts.",
                lead=nm("choose Affirm at checkout and see your monthly plan before you commit.",
                        "Choose Affirm at checkout and see your monthly plan before you commit.")
                + " Checking won&#39;t affect your credit score. Your extra 5% still applies.",
                primary=("See my Affirm options", CHK.go("CART5")),
                link="Rather talk it through? " + tlink("Talk numbers with me", TALK_NUM, "#CFB288"),
                entries=[("Your extra 5%", "CART5, applied with the button"), ("Affirm at checkout", "See your monthly plan first"),
                         ("Two gifts", "Diamond studs + an engraving")],
                piece_btn=("Check out with Affirm", CHK.go("CART5")),
                code=("CART5", 5, "Applied for you with the buttons in this email. Works with Affirm."),
                close=("Pay over time with Affirm", CHK.go("CART5")), **gift(CHK, "CART5"))


def chk_letter():
    return dict(h="h-letter", alt="My best offer.", pre="Your code CART10 is inside: an extra 10% off, plus your gifts.",
                letter=["This is my last email about this piece, so here is my best offer: an extra 10%, on top of today&#39;s prices. "
                        "Pay in full or over time with Affirm.",
                        "Some pieces finish a story. If this one is yours, it is ready when you are. And if you have a question, "
                        "you&#39;ll always get a real person, never an AI. That&#39;s a promise."],
                primary=("Apply 10% and check out", CHK.go("CART10")), secondary=("Talk to Daniel", BOOK),
                code=("CART10", 10, "Applied for you with the buttons in this email. One use, on top of today&#39;s prices."),
                piece_lead="Your piece", close=("Use my 10% before it&#39;s gone", CHK.go("CART10")),
                **gift(CHK, "CART10", "Check out with 10% and my gifts"))


def chk_letters():
    return dict(h="h-trust", alt="Why people trust us.", pre="550+ reviews, made by hand since 2014, plus an extra 5% and two gifts.",
                lead=nm("here&#39;s why people trust us.", "Here&#39;s why people trust us.")
                + " Since 2014, in the Diamond Trading Center in Ramat Gan. Made by hand to order. 550+ reviews from people who hesitated too.",
                primary=("Return to my order", CHK.go("CART5")), secondary=("read the reviews", REVIEWS),
                feature=R_NATHAN, more_reviews=[R_DAINA, R_IRMA],
                piece_lead="Your order", piece_btn=("Complete my order", CHK.go("CART5")),
                code=("CART5", 5, "Applied for you with the buttons in this email. One use, on top of today&#39;s prices."),
                close=("Check out with 5% off", CHK.go("CART5")), **gift(CHK, "CART5"))


def chk_meet():
    return dict(h="h-meet", alt="Any questions? Let's meet.", kicker="Let&#39;s talk", sign="Hope to see you soon,",
                pre="15 minutes on video with Daniel, plus an extra 5% and two gifts.",
                lead=nm("any questions? Let&#39;s meet.", "Any questions? Let&#39;s meet.")
                + " Stones, size, gold, changes. On a short video call I show you everything live. No script, no pressure.",
                primary=("Book 15 minutes", BOOK),
                link="Ready without the call? " + tlink("Return to my order", CHK.go("CART5"), INK),
                qa=[("Can I see the stones first?", "Yes. On a short video call I show you everything live, in the light."),
                    ("Can you change the gold or the size?", "Tell me what you have in mind. Every piece is made by hand to order."),
                    ("Is every diamond natural?", "Yes, never lab-grown, moissanite or a simulant. Your piece ships with a certificate for its diamonds and solid gold."),
                    ("Will you push me to buy?", "No script, no pressure. Fifteen minutes, just us.")],
                piece_lead="We can talk about", piece_btn=("Return to my order", CHK.go("CART5")),
                code=("CART5", 5, "Applied for you with the buttons in this email. One use."),
                close=("Book my 15 minutes", BOOK), **gift(CHK, "CART5"))


# ================================================================ cart copy (VWbEYm, 16.11 ladder: 1-2 no code, 3-6 CART5, 7-8 CART10)
BLACK_IF = "'Black Ice' in event.Categories or 'REMNANT' in event.Categories"


def cart():
    E = []
    E.append(("A", dict(h="h-thinking", alt="Still thinking about it?", pre="Saved exactly as you left it, plus two gifts with your order.",
                        tag="Kept exactly as you chose it.",
                        lead=HI + "I kept it exactly as you left it: the piece, the size, the gold.",
                        primary=("Back to my piece", CART.go()), secondary=ASK_PIECE,
                        close=("Take me back to my piece", CART.go()), **gift(CART, None, "Order it with my two gifts"))))
    E.append(("C", dict(h="h-natural", alt="Is it really natural?", pre="What's in your piece, the certificate that proves it, and two gifts.",
                        lead="{% if " + BLACK_IF + " %}"
                        + nm("yes, it&#39;s a natural black diamond.", "Yes, it&#39;s a natural black diamond.")
                        + " Formed in the earth like a white diamond, black from tiny graphite inclusions. Not spinel, onyx, moissanite or lab-grown."
                        + "{% else %}"
                        + nm("yes, every diamond is natural.", "Yes, every diamond is natural.")
                        + " Formed in the earth. Not lab-grown, not moissanite, not a simulant. Chosen one by one for how it handles light."
                        + "{% endif %} Every piece ships with a certificate for its diamonds and its solid gold.",
                        primary=("Back to my piece", CART.go()), secondary=("see a certificate", wa("Hi Daniel, can you send me an example certificate?")),
                        still=(IMG["diamonds"], "Natural black diamonds in a diamond parcel paper, with tweezers and a loupe",
                               "Natural diamonds in their parcel paper, before they are chosen one by one."),
                        piece_lead="The stone in your piece", piece_btn=("See my piece", CART.go()),
                        close=("Order my piece", CART.go()), **gift(CART, None, "Order it with my two gifts"))))
    E.append(("H", dict(h="h-word", alt="Don't take my word for it.", pre="Read what they wrote once the box was open, plus an extra 5% (CART5).",
                        lead=nm("don&#39;t take my word for it.", "Don&#39;t take my word for it.")
                        + " From people who hesitated too, written after the box was open. And to make it easier, an extra 5% is yours.",
                        primary=("Apply 5% to my piece", CART.go("CART5")), secondary=("read the reviews", REVIEWS),
                        feature=R_EMORY, more_reviews=[R_CRAIG, R_MOLLY],
                        piece_lead="Your piece", piece_btn=("Back to my piece, 5% off", CART.go("CART5")),
                        code=("CART5", 5, "Already applied when you tap a button in this email. One use, on top of today&#39;s prices."),
                        close=("Use my 5% now", CART.go("CART5")), **gift(CART, "CART5", "Order with my two gifts"))))
    E.append(("F", dict(h="h-made", alt="Made by hand, for you.", pre="Your piece, made by hand after you order. Your extra 5% is still on it.",
                        photo=(IMG["studio"], "A jeweler setting a black diamond at the bench", "At the bench, a black diamond set by hand"),
                        lead=nm("made by hand, for you.", "Made by hand, for you.")
                        + " After you order, in your size and your gold, set stone by stone at our bench in the Diamond Trading Center. Shipped insured, on us.",
                        primary=("Apply 5% to my piece", CART.go("CART5")),
                        link="A question first? " + tlink("Ask Daniel", ASK_PIECE[1], "#CFB288"),
                        piece_lead="The piece we&#39;d make for you", piece_btn=("Make it for me", CART.go("CART5")),
                        code=("CART5", 5, "Already applied when you tap a button in this email. One use."),
                        close=("Order my piece, 5% off", CART.go("CART5")), **gift(CART, "CART5", "Order with my two gifts"))))
    E.append(("G", dict(h="h-fit", alt="What if it doesn't fit?", kicker="Size and peace of mind",
                        pre="Size, returns and care, answered in one minute. CART5 still applies.",
                        lead=nm("what if it doesn&#39;t fit?", "What if it doesn&#39;t fit?") + " Here are the answers, in one minute.",
                        primary=("Apply 5% to my piece", CART.go("CART5")),
                        link="Not sure of your size? " + tlink("Help me with my size", wa("Hi Daniel, can you help me with my ring size?"), INK),
                        qa=[("Not sure of your size?", "I help you measure at home."),
                            ("And if it still doesn&#39;t fit?", "One resizing is included."),
                            ("Changed your mind?", f'You have 30 days ({tlink("return policy", REFUND, MUTE_L)}).'),
                            ("And after that?", f'{tlink("Lifetime care", CARE, MUTE_L)} for your piece, and a certificate for its diamonds and solid gold.')],
                        piece_lead="Your piece, kept as you chose it", piece_btn=("Back to my piece, 5% off", CART.go("CART5")),
                        code=("CART5", 5, "Already applied when you tap a button in this email. One use."),
                        close=("Order my piece, 5% off", CART.go("CART5")), **gift(CART, "CART5", "Order with my two gifts"))))
    E.append(("D", dict(pre="Choose Affirm at checkout, keep your extra 5%, and your gifts.",
                        lead=nm("choose Affirm at checkout and see your monthly plan before you commit.",
                                "Choose Affirm at checkout and see your monthly plan before you commit.")
                        + " Checking won&#39;t affect your credit score. Your extra 5% still applies.",
                        primary=("See my Affirm options", CART.go("CART5")),
                        link="Rather talk it through? " + tlink("Talk numbers with me", TALK_NUM, "#CFB288"),
                        index_title="Your piece, and what comes with it",
                        entries=[("Affirm at checkout", "Monthly payments, plan shown first"), ("Your extra 5%", "CART5, applied with the button"),
                                 ("Two gifts", "Diamond studs + an engraving")],
                        piece_btn=("Wear it now with Affirm", CART.go("CART5")),
                        code=("CART5", 5, "Applied for you with the buttons in this email. Works with Affirm."),
                        close=("Pay over time with Affirm", CART.go("CART5")), **gift(CART, "CART5", "Order with my two gifts"))))
    E.append(("B", dict(pre="Ask anything on video, plus an extra 10% (CART10) and two gifts.", sign="Hope to see you soon,",
                        big_pre=nm("just", "Just"), big="15", big_post="minutes, just us?",
                        photo=(IMG["call"], "A jeweler showing a black diamond to a phone camera on a video call"),
                        lead="Stones, size, gold, changes. On a short video call I show you everything live. No script, no pressure. "
                             "And if you&#39;re ready without the call, here is an extra 10%.",
                        primary=("Book 15 minutes", BOOK), secondary=("Apply 10% to my piece", CART.go("CART10")),
                        code=("CART10", 10, "Applied for you with the buttons in this email. One use, on top of today&#39;s prices."),
                        piece_lead="We can talk about", piece_btn=("My piece, 10% off", CART.go("CART10")),
                        close=("Book my 15 minutes", BOOK), **gift(CART, "CART10", "Order with 10% and my gifts"))))
    E.append(("E", dict(h="h-note", alt="One last note from me.", pre="My best offer, an extra 10% (CART10), and two gifts I wanted you to know about.",
                        letter=["This is my last email about your piece, so here is my best offer: an extra 10%, and the two gifts below.",
                                "If it&#39;s no longer the one, just reply and tell me why. I read every answer myself."],
                        primary=("Apply 10% to my piece", CART.go("CART10")), secondary=("Talk to Daniel", BOOK),
                        code=("CART10", 10, "Applied for you with the buttons in this email. One use, on top of today&#39;s prices."),
                        piece_lead="Your piece", close=("Use my 10% before it&#39;s gone", CART.go("CART10")),
                        **gift(CART, "CART10", "Order with 10% and my gifts"))))
    return E


# ================================================================ browse copy (Y6Zunh)
def browse():
    V = BROWSE
    E = []
    E.append(("A", dict(h="h-see", alt="Did you see something you like?", pre="Made to order for you, plus two gifts with your order.",
                        tag="Made to order, in solid gold.",
                        lead=nm("did you see something you like?", "Did you see something you like?")
                        + " Made to order in solid gold, shipped insured on us. Another gold, a different stone or an engraving? Just ask.",
                        primary=("See it again", V.go()), secondary=("Customize it with Daniel", BOOK),
                        close=("Take me back to it", V.go()), **gift(V, None, "Choose it with my two gifts"))))
    E.append(("G", dict(h="h-talk", alt="Let's talk it through.", kicker="Still thinking about it?", sign="Hope to see you soon,",
                        pre="15 minutes on video with Daniel, plus two gifts with your order.",
                        lead=nm("let&#39;s talk it through.", "Let&#39;s talk it through.")
                        + " Size, white or yellow gold, a bigger stone, a thinner band: 15 minutes with me and we design it together.",
                        primary=("Book 15 minutes", BOOK),
                        link="Or first " + tlink("see it again", V.go(), INK),
                        qa=[("Can it be made in my size?", "Yes. Every piece is made by hand to order, in your size."),
                            ("White or yellow gold?", "Your choice, in solid gold."),
                            ("A bigger stone, a thinner band?", "Tell me on the call and we design it together."),
                            ("How long is the call?", "15 minutes on video. No script, no pressure.")],
                        piece_lead="The piece you looked at", piece_btn=("See it again", V.go()),
                        close=("Book my 15 minutes", BOOK), **gift(V, None, "Choose it with my two gifts"))))
    E.append(("F", dict(h="h-count", alt="Why count on us?", pre="Natural diamonds, solid gold, made by hand since 2014.",
                        photo=(IMG["studio"], "A jeweler setting a black diamond at the bench", "Our bench in the Diamond Trading Center, Ramat Gan"),
                        lead=nm("why count on us?", "Why count on us?") + " Since 2014, in the Diamond Trading Center in Ramat Gan. Made by hand to order. 550+ reviews.",
                        primary=("Read the reviews", REVIEWS),
                        link="Or go " + tlink("back to the piece", V.go(), "#CFB288"),
                        piece_lead="The piece you looked at", piece_btn=("Back to the piece", V.go()),
                        close=("See the piece again", V.go()), **gift(V, None, "Choose it with my two gifts"))))
    E.append(("D", dict(pre="Choose Affirm at checkout and see your plan before you commit, plus two gifts.",
                        lead=nm("choose Affirm at checkout and see your monthly plan before you commit.",
                                "Choose Affirm at checkout and see your monthly plan before you commit.")
                        + " Checking won&#39;t affect your credit score.",
                        primary=("See it again", V.go()),
                        link="Rather talk it through? " + tlink("Talk numbers with me", TALK_NUM, "#CFB288"),
                        index_title="The piece you looked at, and what comes with it",
                        entries=[("Affirm at checkout", "Monthly payments, plan shown first"), ("Two gifts", "Diamond studs + an engraving"),
                                 ("Made to order", "In solid gold, shipped insured on us")],
                        piece_btn=("Wear it now with Affirm", V.go()),
                        close=("Pay over time with Affirm", V.go()), **gift(V, None, "Choose it with my two gifts"))))
    E.append(("B", dict(pre="Your code CART10 is inside, plus two gifts.",
                        big_pre=nm("here&#39;s an extra", "Here&#39;s an extra"), big="10%", big_post="for you.",
                        lead="On the piece you were looking at, or anything else you love. Applied for you when you tap the button.",
                        primary=("Apply 10% and shop", V.go("CART10")), secondary=("Talk to Daniel", BOOK),
                        code=("CART10", 10, "Applied for you with the buttons in this email. One use, on top of today&#39;s prices."),
                        close=("Use my 10% now", V.go("CART10")), **gift(V, "CART10", "Shop with 10% and my gifts"))))
    return E


def checkout_black():
    return [("A", chk_cover()), ("B", chk_split()), ("C", chk_still()), ("D", chk_index()), ("E", chk_letter())]


def checkout_other():
    return [("A", chk_cover()), ("B", chk_split()), ("H", chk_letters()), ("C", chk_still()), ("G", chk_meet()), ("D", chk_index()), ("E", chk_letter())]


FLOWS = {"XW6UqR": (CHK, checkout_black), "VB4v4q": (CHK, checkout_other), "VWbEYm": (CART, cart), "Y6Zunh": (BROWSE, browse)}


def build_all():
    chain = json.load(open(os.path.join(os.path.dirname(OUT), "chain-before.json"), encoding="utf-8"))
    plan = {}
    for fid, (src, fn) in FLOWS.items():
        emails = fn()
        steps = [s for s in chain[fid]["steps"] if s["type"] in ("send-email", "ab-test")]
        assert len(steps) == len(emails), (fid, len(steps), len(emails))
        fams = [f for f, _ in emails]
        assert all(a != b for a, b in zip(fams, fams[1:])), (fid, fams)
        plan[fid] = []
        for n, ((fam, c), st) in enumerate(zip(emails, steps), 1):
            c["pre"] = st.get("preview") or c["pre"]   # the hidden preheader = the live preview text of the action
            html = FAM[fam](src, c)
            name = f"{fid}-{n}-{fam}"
            open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(html)
            nb = html.count('class="btn"')
            kb = len(html.encode("utf-8")) / 1024
            plan[fid].append(dict(n=n, fam=fam, family=FAM_NAME[fam], file=name, aid=st["aid"], old_tid=st["tid"], subject=st["subject"],
                                  preview=c["pre"], buttons=nb, kb=round(kb, 1)))
            print(f"{name:16s} {FAM_NAME[fam]:24s} {nb} buttons {kb:5.1f} KB | {st['subject']}")
    json.dump(plan, open(os.path.join(os.path.dirname(OUT), "plan.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return plan


if __name__ == "__main__":
    build_all()
