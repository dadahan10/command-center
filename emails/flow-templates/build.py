# Builds the FLOW 2026-11 Post-purchase / Browse / Cross-sell / JEWELVERSARY Klaviyo templates.
# Look based on Klaviyo template XuuLF8 (reintro-light). Output: one .html per template in this folder.
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))
SERIF = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "'Manrope','Helvetica Neue',Arial,sans-serif"
BOOK = "https://dianarafael.com/pages/new-website-book-online-appointment"
WA = "https://wa.me/97235755066"
IG = "https://www.instagram.com/dianarafaeljewelry/"
GOOGLE = ("https://www.google.com/maps/place/Diana+Rafael+Jewelry/@32.0841095,34.8015372,17z/data=!4m8!3m7!1s0x151d4b965649920f:"
          "0x3653bfb6c08f9745!8m2!3d32.0841095!4d34.8015372!9m1!1b1!16s%2Fg%2F11j_z1lj8z?entry=ttu")
FALLBACK_IMG = "https://cdn.shopify.com/s/files/1/2469/5441/files/r117-kintsugi-f1-yg.jpg?v=1791445879&width=1200"
LOGO = "https://dadahan10.github.io/diana-rafael-remnant/assets/email/logo-duality-dark.png?v=20261102a"


def utm(url, camp, content):
    if not url.startswith("https://dianarafael.com"):
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source=klaviyo&utm_medium=email&utm_campaign={camp}&utm_content={content}"


def p(text, size=16, color="#1f1b16"):
    return f'<p style="margin:0 0 14px;font-family:{SANS};font-size:{size}px;line-height:1.6;color:{color};">{text}</p>'


def a(href, label):
    return f'<a href="{href}" style="color:#7a5d1e;text-decoration:underline;" target="_blank">{label}</a>'


def button(href, label):
    return (f'<tr><td align="center" style="padding:8px 40px 30px;"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"><tr>'
            f'<td align="center" bgcolor="#b08d3c" style="border:2px solid #b08d3c;background:#b08d3c;border-radius:2px;">'
            f'<a href="{href}" style="display:inline-block;padding:13px 30px;font-family:{SANS};font-size:13px;font-weight:600;letter-spacing:0.14em;'
            f'text-transform:uppercase;color:#1f1b16;text-decoration:none;" target="_blank">{label}</a></td></tr></table></td></tr>')


def img(src_expr, alt, href=None):
    tag = (f'<img alt="{alt}" src="{src_expr}" style="display:block;width:100%;max-width:552px;height:auto;border:0;border-radius:6px;" width="552"/>')
    return f'<a href="{href}" target="_blank">{tag}</a>' if href else tag


def hero_event(paths, alt, href=None):
    """Image from the first event path that exists, else the brand fallback."""
    out = ""
    for i, pth in enumerate(paths):
        out += ("{% if " if i == 0 else "{% elif ") + pth + " %}" + img("{{ " + pth + " }}", alt, href)
    out += "{% else %}" + img(FALLBACK_IMG, "Diana Rafael ring in gold with a natural black diamond", href) + "{% endif %}"
    return out


def card(href, src, name):
    return (f'<td class="col" style="padding:6px;" valign="top" width="50%"><a href="{href}" style="text-decoration:none;display:block;background:#f3ead9;'
            f'border:1px solid #e6dccb;border-radius:6px;padding:10px 10px 0;" target="_blank"><img alt="{name}" src="{src}" style="display:block;width:100%;'
            f'max-width:250px;height:auto;border:0;margin:0 auto;border-radius:4px;" width="250"/><div style="font-family:{SERIF};font-size:19px;line-height:24px;'
            f'color:#1f1b16;text-align:center;padding:10px 4px 14px;">{name}</div></a></td>')


def cards(c1, c2):
    return f'<tr><td style="padding:0 24px 10px;"><table cellpadding="0" cellspacing="0" role="presentation" width="100%"><tr>{card(*c1)}{card(*c2)}</tr></table></td></tr>'


def page(title, preview, kicker, hero, h1, body, cta, camp, show_help=True):
    help_line = ""
    if show_help:
        help_line = (f'<tr><td align="center" class="pad" style="padding:0 48px 26px;font-family:{SANS};font-size:13px;line-height:1.6;color:#5c544a;">'
                     f'Questions? A person answers you, not AI: {a(WA, "WhatsApp +972-3-575-5066")} or '
                     f'{a(utm(BOOK, camp, "help_book"), "book 15 minutes with Daniel")}.</td></tr>')
    return f'''<!DOCTYPE html>
<html dir="ltr" lang="en"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><meta name="color-scheme" content="light only"/><meta name="supported-color-schemes" content="light only"/>
<title>{title}</title>
<style>:root{{color-scheme:light only;}}
@media only screen and (max-width:620px){{.col{{display:block !important;width:100% !important}}h1{{font-size:30px !important}}.pad{{padding-left:24px !important;padding-right:24px !important}}}}</style></head>
<body style="margin:0;padding:0;background:#f7f3ec;color:#1f1b16;">
<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{preview}</div>
<table border="0" cellpadding="0" cellspacing="0" role="presentation" bgcolor="#f7f3ec" style="background:#f7f3ec;" width="100%"><tr><td align="center" style="padding:24px 10px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;max-width:600px;background:#ffffff;border:1px solid #e6dccb;" bgcolor="#ffffff" width="600">
<tr><td align="center" bgcolor="#f3ead9" style="background:#f3ead9;border-bottom:1px solid #e6dccb;padding:9px 16px;font-family:{SANS};font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:#7a5d1e;">{kicker}</td></tr>
<tr><td align="center" style="padding:24px 40px 20px;"><a href="{utm("https://dianarafael.com/", camp, "logo")}" target="_blank"><img alt="Diana Rafael" src="{LOGO}" style="display:block;width:220px;height:auto;border:0;" width="220"/></a></td></tr>
<tr><td style="padding:0 24px;">{hero}</td></tr>
<tr><td align="center" class="pad" style="padding:30px 48px 4px;"><h1 style="font-family:{SERIF};font-size:36px;line-height:1.15;margin:0 0 16px;color:#1f1b16;font-weight:500;">{h1}</h1></td></tr>
<tr><td class="pad" style="padding:0 48px 8px;">{body}</td></tr>
{cta}
{help_line}
<tr><td class="pad" style="padding:0 48px 30px;"><p style="margin:0;font-family:{SANS};font-size:15px;line-height:1.6;color:#7a5d1e;">Daniel, Diana Rafael</p></td></tr>
<tr><td align="center" bgcolor="#efe8dc" style="padding:24px 40px 28px;background:#efe8dc;border-top:1px solid #e6dccb;font-family:{SANS};">
<div style="font-family:{SERIF};color:#7a5d1e;font-size:22px;font-weight:600;">Diana Rafael</div>
<div style="font-size:12px;color:#4a4339;margin-top:10px;line-height:1.6;">23 Tuval St., Suite 10-01, Diamond Trading Center, Ramat-Gan, Israel 5252238<br/>9454 Wilshire Blvd M3, Beverly Hills, CA 90212</div>
<div style="font-size:12px;color:#4a4339;margin-top:10px;">No longer want to receive these emails? {{% unsubscribe 'Unsubscribe' %}}</div>
</td></tr>
<tr><td bgcolor="#b08d3c" style="height:6px;line-height:6px;font-size:6px;background:#b08d3c;"> </td></tr>
</table></td></tr></table>
</body></html>'''


HI = "Hi {{ first_name|default:'there' }},"
T = {}

# ---------------- POST-PURCHASE ----------------
c = "flow-postpurchase"
PO_IMG = ["event.extra.line_items.0.product.images.0.src"]
PO_URL = "https://dianarafael.com/products/{{ event.extra.line_items.0.product.handle }}"

T["pp1-order-confirmed"] = page(
    "Your order is confirmed. Here's what happens now.",
    "Made by hand in our studio, checked, and shipped insured within 10 business days.",
    "Order {{ event.extra.name }} confirmed",
    hero_event(PO_IMG, "{{ event.Items.0 }}"),
    "Thank you. Here's what happens now.",
    p(HI) +
    p("It's Daniel. Thank you for choosing us for the {{ event.Items.0|default:'piece you ordered' }}. Every piece is made to order, so here is exactly what happens next:") +
    p("<b>1. We confirm the details.</b> If anything needs checking, like your ring size or gold color, we'll write to you personally before we start.<br/>"
      "<b>2. It's made by hand</b> in our studio, by the same people who have made every Diana Rafael piece.<br/>"
      "<b>3. Quality check.</b> Every stone, prong and surface is inspected before it leaves us.<br/>"
      "<b>4. Insured shipping with tracking.</b> Your order ships within 10 business days, and you'll get an email with the tracking number the day it leaves.") +
    p("If you have a question at any point, just reply to this email. A person answers you, not AI.") +
    p("Want to see the studio while your piece is being made? We share the bench, the stones and the finished work on Instagram."),
    button(IG, "Follow us on Instagram"), c, show_help=False)

T["pp2-studio"] = page(
    "Inside the studio while your piece is made",
    "A look at the bench: setting, polishing and the final check.",
    "From our studio",
    hero_event(PO_IMG, "{{ event.Items.0 }}"),
    "A look inside the studio.",
    p(HI) +
    p("While your {{ event.Items.0|default:'piece' }} is in the studio, I wanted to show you what happens to it on the bench.") +
    p("It starts in solid gold, cast and shaped to your size. Then every natural diamond is set by hand, one by one, under the microscope, so each stone sits exactly where it should. "
      "After setting comes polishing, a slow job that gives the gold its finish without dulling a single edge.") +
    p("The last step is the one we never rush: a full quality check of every stone and every prong, before the piece is packed and insured for its trip to you. "
      "Your order ships within 10 business days, and the tracking email follows the same day.") +
    p("We share these moments, the stones, the bench and the finished pieces, on Instagram. Come take a look, and reply to this email if you have any question about your order."),
    button(IG, "See the studio on Instagram"), c, show_help=False)

FO_IMG = ["event.extra.line_items.0.product.images.0.src"]
T["pp3-shipped"] = page(
    "Your piece has shipped. Tracking inside.",
    "Your tracking number, a short note on customs, and how to care for your piece.",
    "Order {{ event.extra.name }} has shipped",
    hero_event(FO_IMG, "{{ event.extra.line_items.0.name }}"),
    "Your piece is on its way.",
    p(HI) +
    p("Good news: your order has left our studio, fully insured. A signature may be required on delivery.") +
    p('{% if event.extra.fulfillments.0.tracking_company %}<b>Carrier:</b> {{ event.extra.fulfillments.0.tracking_company }}<br/>{% endif %}'
      '<b>Tracking number:</b> {{ event.extra.fulfillments.0.tracking_number }}') +
    p("<b>About customs.</b> Diana Rafael covered and paid all shipping costs. Depending on where you live and the order value, customs duties may be required in your country, so please check this yourself with your local customs office or the carrier.", 15) +
    '{% if event.extra.shipping_address.country_code == "US" and event|lookup:"$value" >= 2500 %}' +
    p('<b>US orders over $2,500:</b> US Customs asks for Form 5106 (Importer ID). Please fill it in here so your package clears without delay: '
      + a(utm("https://dianarafael.com/pages/new-website-form-5106-importer-id-input-record", c, "form5106"), "Form 5106") + ".", 15) +
    '{% endif %}' +
    p("<b>Caring for your piece.</b> Take it off for the gym, swimming and cleaning products. Clean it with warm water, mild soap and a soft brush, and store it on its own so diamonds don't scratch other pieces.", 15),
    button("{{ event.extra.fulfillments.0.tracking_url }}", "Track your package"), c)

DS_IMG = ["event.extra.fulfillment.line_items.0.product.images.0.src", "event.extra.line_items.0.product.images.0.src"]
T["pp4-review"] = page(
    "How does it feel to wear it?",
    "One minute on Google helps the next person trust a studio they've never met.",
    "A small favor",
    hero_event(DS_IMG, "{{ event.Items.0 }}"),
    "How does it feel to wear it?",
    p(HI) +
    p("Your {{ event.Items.0|default:'piece' }} arrived a few days ago, and I hope it already feels like yours.") +
    p("Most of the people who buy from us have never visited our studio. They decide to trust us because of what customers like you wrote. "
      "If you have a minute, a short Google review would mean a lot to us: what you ordered, how it looks in person, how the experience felt.") +
    p("And if anything isn't right, please don't keep it to yourself. Reply to this email and I'll take care of it personally."),
    button(GOOGLE, "Leave a Google review"), c)

# ---------------- BROWSE ----------------
c = "flow-browse"
BV_HERO = img("{{ event.ImageURL }}", "{{ event.Name }}", "{{ event.URL }}?utm_source=klaviyo&utm_medium=email&utm_campaign=flow-browse&utm_content=hero")
BV_URL = "{{ event.URL }}?utm_source=klaviyo&utm_medium=email&utm_campaign=flow-browse&utm_content=cta"

T["br1-reminder"] = page(
    "Still thinking about the {{ event.Name }}?",
    "Made to order for you, shipped insured on us, with 30 days to decide.",
    "You were looking at",
    BV_HERO,
    "{{ event.Name }}",
    p(HI) +
    p("You were looking at this piece earlier, so here it is again, with the things people usually want to know before they decide:") +
    p("<b>It's made for you.</b> Every piece is made to order in our studio, in solid gold with natural diamonds, and ships within 10 business days.<br/>"
      "<b>Shipping is on us.</b> Fully insured express shipping, with tracking.<br/>"
      "<b>You're covered.</b> 30 days for returns and exchanges, and a certificate with your piece.<br/>"
      "<b>It can change.</b> Another gold color, stone shape or an engraving: tap Customize this product on the page and ask in your own words.") +
    p("If it's the one, it's waiting for you."),
    button(BV_URL, "See it again"), c)

T["br2-why-us"] = page(
    "Why 530+ customers trusted a studio they'd never visited",
    "Natural diamonds, solid gold, made by hand since 2014.",
    "Why Diana Rafael",
    BV_HERO,
    "Why people trust us with the big ones.",
    p(HI) +
    p("Buying a piece like the {{ event.Name }} online, from a studio you've never visited, is a real decision. Here's why people make it with us:") +
    p("<b>Since 2014.</b> Our studio is in the Diamond Trading Center in Ramat-Gan, with an office in Beverly Hills.<br/>"
      "<b>Natural diamonds only.</b> Every black and white diamond is natural, and every piece comes with a certificate.<br/>"
      "<b>Made by hand, to order.</b> Nothing sits in a warehouse. Your piece is made for you.<br/>"
      "<b>530+ reviews.</b> From customers who were exactly where you are now, and decided to trust us.") +
    p("Read what they wrote, in their own words, then decide."),
    button(utm("https://dianarafael.com/pages/our-customers-reviews", c, "reviews"), "Read the 530+ reviews"), c)

T["br3-studs-gift"] = page(
    "A gift with the {{ event.Name }}: 1 ct studs",
    "Free 1 ct natural black diamond studs, now from $2,000 (was $3,000).",
    "A gift with your order",
    BV_HERO,
    "A pair of studs, on us.",
    p(HI) +
    p("If you're still thinking about the {{ event.Name }}, here's one more reason to say yes.") +
    p("<b>Free 1 ct natural black diamond studs with your order, now from $2,000 (was $3,000).</b> "
      "We lowered the threshold, so more of our customers walk away with a second piece. "
      "They're made in our studio like everything else, in solid gold.") +
    p("Everything else stays the same: made to order, ships within 10 business days, fully insured shipping paid by us, and 30 days for returns and exchanges.") +
    p("The studs are added to orders from $2,000. If you have any question about how it works, reply and I'll answer you myself."),
    button(BV_URL, "Make it yours"), c)

T["br4-daniel"] = page(
    "Questions about the {{ event.Name }}? 15 minutes with Daniel",
    "Size, gold, stone, budget: ask a person, not a chatbot.",
    "A letter from Daniel",
    BV_HERO,
    "Let's talk it through.",
    p(HI) +
    p("It's Daniel. When someone looks at a piece like the {{ event.Name }} more than once, there's usually a question behind it. "
      "What size do I order? Can it be in white gold? Can the center stone be bigger, or the band thinner? Will it look right next to my other ring?") +
    p("Those are exactly the questions I like answering. Book 15 minutes with me. We'll talk through stones and sizes, and we can change the design together if you want. "
      "No pressure and no script, just a conversation with the person who'll make sure your piece is right.") +
    p("Prefer to write? Message us on " + a(WA, "WhatsApp") + " and a person will answer you, not AI."),
    button(utm(BOOK, c, "book_cta"), "Book 15 minutes"), c, show_help=False)

# ---------------- CROSS-SELL ----------------
c = "flow-crosssell"
ALL = 'event.Collections|join:" "|lower'
ITEMS = 'event.Items|join:" "|lower'
IS_ENG = f'"engagement" in {ALL}'
IS_NECK = f'"necklace" in {ITEMS} or "pendant" in {ITEMS} or "necklace" in {ALL}'
IS_BRAC = f'"bracelet" in {ITEMS} or "bracelet" in {ALL}'
IS_EAR = f'"earring" in {ITEMS} or "earring" in {ALL}'

BANDS = utm("https://dianarafael.com/collections/all-wedding-bands", c, "bands")
EARS = utm("https://dianarafael.com/collections/black-ice-earring-collection", c, "earrings")
NECK = utm("https://dianarafael.com/products/orions-belt-natural-diamond-tennis-pendant-with-a-rose-gold-gold-necklace", c, "necklace")
RINGS = utm("https://dianarafael.com/collections/all-engagement-rings", c, "rings")
NEW = utm("https://dianarafael.com/collections/new-arrivals", c, "new")

C_BAND1 = (utm("https://dianarafael.com/products/hyades-chevron-natural-black-diamond-contour-wedding-band", c, "card_hyades"),
           "https://cdn.shopify.com/s/files/1/2469/5441/files/R520-01-R520-Y.jpg?v=1792921068&width=600", "Hyades chevron band")
C_BAND2 = (utm("https://dianarafael.com/products/accretion-black-diamond-shard-wedding-band", c, "card_accretion"),
           "https://cdn.shopify.com/s/files/1/2469/5441/files/R114-R-pack-front-sq.jpg?v=1793193292&width=600", "Accretion band")
C_EAR1 = (utm("https://dianarafael.com/products/1-carats-round-diamond-earrings-1", c, "card_martini"),
          "https://dianarafael.com/cdn/shop/files/Rose-1_21a7ee9b-96f2-4e6d-ae59-e9eb0a7f6a66_grande.jpg?v=1729526568", "Martini studs")
C_EAR2 = (utm("https://dianarafael.com/products/ananke-1-carat-hoop-natural-black-diamond-2-sided-earrings", c, "card_ananke"),
          "https://dianarafael.com/cdn/shop/files/44112672-e4e4-5693-af15-c4af4f9003ff_grande.jpg?v=1733902301", "Ananke hoops")
C_NECK1 = (NECK, "https://dianarafael.com/cdn/shop/files/P088_grande.jpg?v=1718692498", "Orion's Belt tennis necklace")
C_NECK2 = (utm("https://dianarafael.com/products/2-carats-round-diamond-pendant-necklace-6", c, "card_godrays"),
           "https://dianarafael.com/cdn/shop/products/401491cf-6ec5-568d-970c-3e6c3a090873_82a38594-636c-4101-a964-a2bb466453b0_grande.jpg?v=1631526620",
           "God Rays solitaire pendant")
C_RING1 = (utm("https://dianarafael.com/products/phoenix-marquise-natural-black-diamond-bypass-engagement-ring", c, "card_phoenix"),
           "https://cdn.shopify.com/s/files/1/2469/5441/files/R499-01-R499-Y.jpg?v=1792921166&width=600", "Phoenix ring")


def by_type(eng, neck, brac, ear, other):
    return (f"{{% if {IS_ENG} %}}{eng}{{% elif {IS_NECK} %}}{neck}{{% elif {IS_BRAC} %}}{brac}"
            f"{{% elif {IS_EAR} %}}{ear}{{% else %}}{other}{{% endif %}}")


HERO_X = hero_event(DS_IMG, "{{ event.Items.0 }}")
CLOSE = "</td></tr>"
OPEN = '<tr><td class="pad" style="padding:0 48px 8px;">'
XS_SETS = [(C_BAND1, C_BAND2, BANDS, "See the wedding bands"), (C_EAR1, C_EAR2, EARS, "See the earrings"),
           (C_RING1, C_EAR1, EARS, "See the earrings"), (C_NECK1, C_NECK2, NECK, "See the necklace"),
           (C_EAR1, C_NECK1, NEW, "See what's new")]


def xs_body(intro, outro, *texts):
    blocks = [p(t) + CLOSE + cards(s[0], s[1]) + button(s[2], s[3]) + OPEN for t, s in zip(texts, XS_SETS)]
    return p(HI) + p(intro) + p(outro) + by_type(*blocks)


T["xs1-match"] = page(
    "Made to go with yours",
    "A few pieces we'd pair with what you're already wearing.",
    "Made to go with yours",
    HERO_X,
    "Made to go with yours.",
    xs_body("It's been about two months since your {{ event.Items.0|default:'piece' }} arrived. I hope you're wearing it a lot.",
            "Every piece below is made to order, in the gold color you choose.",
            "An engagement ring is half of a pair. Our wedding bands are designed to sit flush against it, follow its curve, or frame it with a line of natural black diamonds, so the two read as one.",
            "The easiest piece to pair with a necklace is a pair of earrings in the same gold and the same diamonds. It finishes the look without competing with it.",
            "A bracelet looks best with one more point of light: a ring in the same gold, or a pair of earrings that echo its diamonds.",
            "Earrings frame the face, and a necklace in the same gold and diamonds ties the whole look together at the neckline.",
            "Here are a few pieces that sit beautifully next to what you already have."),
    "", c)

T["xs2-stack"] = page(
    "How our customers wear theirs",
    "Same gold, same diamonds, worn together.",
    "Wearing them together",
    HERO_X,
    "One piece looks good. Two tell a story.",
    xs_body("The pieces our customers wear every day are rarely worn alone. Here's how they put them together.",
            "Matching gold and matching diamonds is the simplest rule, and it always works. Want to see a pairing first? Reply with a photo of yours and I'll suggest one.",
            "Most of our brides choose their band after living with the ring for a while. Some match the gold and stone exactly. Others pick a chevron that hugs the ring, or a thin line of black diamonds that makes the center stone look bigger.",
            "With a necklace, stay close to your face: small studs or a slim hoop in the same gold, so the light moves from the neckline to the ears.",
            "With a bracelet, add a ring on the same hand, or earrings that repeat its diamonds. When the gold matches, the pieces look like they were always meant to be together.",
            "With earrings, a pendant or tennis necklace in the same gold completes the frame around your face.",
            "Start with one piece in the same gold as yours, and build from there."),
    "", c)

T["xs3-daniel"] = page(
    "Want it designed to match? 15 minutes with Daniel",
    "We can make the second piece to fit the first exactly.",
    "A letter from Daniel",
    HERO_X,
    "Want it made to match yours?",
    p(HI) +
    p("It's Daniel. Sometimes the right match isn't on the website yet. Because we made your {{ event.Items.0|default:'piece' }}, we have its exact design, "
      "so we can make a second piece that fits it perfectly.") +
    by_type(p("For an engagement ring, that means a band shaped to its exact curve, so the two sit flush with no gap."),
            p("For a necklace, that means earrings built from the same diamonds and the same setting."),
            p("For a bracelet, that means a ring or earrings that repeat its pattern and its gold."),
            p("For earrings, that means a pendant or necklace that carries the same design up to the neckline."),
            p("That means a second piece built around the one you already wear.")) +
    p("Book 15 minutes with me and we'll sketch it together. Or send us a message on " + a(WA, "WhatsApp") + "; a person answers you, not AI."),
    button(utm(BOOK, c, "book_cta"), "Book 15 minutes"), c, show_help=False)

# ---------------- JEWELVERSARY ----------------
c = "flow-jewelversary"
T["jewelversary"] = page(
    "Happy JEWELVERSARY, {{ first_name|default:'friend' }}",
    "One year ago today, you chose a piece from our studio.",
    "Happy JEWELVERSARY",
    hero_event(PO_IMG, "{{ event.Items.0 }}"),
    "One year together.",
    p(HI) +
    p("It's Daniel. A year ago today you ordered the {{ event.Items.0|default:'piece' }} from us, and I wanted to say happy JEWELVERSARY.") +
    p("I'm just touching base. How is it wearing? Has it been to places worth remembering? If it needs a polish, a size check or anything at all, reply to this email and we'll look after it.") +
    p("A lot has happened in the studio this year. Our newest collection, REMNANT, is built around a break that was mended in gold, not hidden: rings, bands and earrings with natural black diamonds and a gold line where the piece was put back together. "
      "And there are " + a(utm("https://dianarafael.com/collections/new-arrivals", c, "new_arrivals"), "new arrivals") + " fresh from the bench.") +
    p("I'd love to hear how your year with it went. Reply anytime, I read every one."),
    button(utm("https://dianarafael.com/collections/remnant", c, "remnant"), "Explore REMNANT"), c, show_help=False)

for k, v in T.items():
    with open(os.path.join(OUT, k + ".html"), "w", encoding="utf-8") as f:
        f.write(v)
    words = len(re.sub(r"<[^>]+>|\{[%{][^}]*[%}]\}", " ", v.split("<body", 1)[1]).split())
    print(k, len(v), "chars, ~", words, "visible words incl. footer")
