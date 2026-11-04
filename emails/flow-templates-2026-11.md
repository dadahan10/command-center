# Flow templates 2026-11: Checkout, Cart, VIP

Created 3.11.2026 as Klaviyo **CODE templates only**. No flows, campaigns or lists were touched. Design: the light 5.11 reintro look (XuuLF8 / QVd3dt): cream background, Duality logo, Cormorant + Manrope, gold buttons, the same footer. The product image is shown large at the top, pulled from the event.

Base: `flows-analysis-2026-11-03.md` §4.3 and §4.4, plus the owner's answers in `feedback_klaviyo_flows_spec.md`.

## Abandoned Checkout
Trigger: Checkout Started (UgasKH). Filter: Placed Order = 0 since start. Re-entry: 7 days.

| # | Template name | ID | Subject | Preview | Delay | Objection |
|---|---|---|---|---|---|---|
| 1 | FLOW 2026-11 \| Checkout 1/8 \| Reminder | TnE3Z5 | Is this the one? 💍 | Your order is saved, exactly as you left it. | 1h | Reminder |
| 2 | FLOW 2026-11 \| Checkout 2/8 \| What stopped you? | YuCbnb | Can I ask what stopped you? | One tap is enough. I read every answer myself. | 1d | Direct "what stopped you?" with 5 answer buttons (WhatsApp, answer pre-filled) + quick answers: shipping paid by us, customs may apply, ships within 10 business days, returns, Affirm |
| 3 | FLOW 2026-11 \| Checkout 3/8 \| Natural diamond + certificate | XKy8hZ | Is it really a natural diamond? | What's in your piece, and the certificate that proves it. | 2d | Natural black diamond / certificate (Black Ice or REMNANT gets the black-diamond story; everything else gets the natural-diamond version) |
| 4 | FLOW 2026-11 \| Checkout 4/8 \| 530+ reviews | S4kGrk | 530+ reviews from people who hesitated too | Read what they wrote once the box was open. | 4d | Trust: 530+ reviews (Etsy + Google), since 2014 |
| 5 | FLOW 2026-11 \| Checkout 5/8 \| Fit, returns, warranty | TekMmy | What if it doesn't fit? | Size, returns and warranty, answered in one minute. | 6d | Fit / resizing / 30-day returns / lifetime warranty |
| 6 | FLOW 2026-11 \| Checkout 6/8 \| Affirm pay over time | VEnXx2 | Wear it now, pay over time | Choose Affirm at checkout and see your plan before you commit. | 8d | Price: Affirm |
| 7 | FLOW 2026-11 \| Checkout 7/8 \| 15 minutes with Daniel | SxSYuf | 15 minutes with me? | Ask anything, see the stones on video, change what you like. | 10d | Human: 15-minute call + WhatsApp |
| 8 | FLOW 2026-11 \| Checkout 8/8 \| A note from Daniel + gift | UXVaDH | A note from me | And a gift I wanted you to know about. | 13d | Personal note + gift featured (studs, now from $2,000, was $3,000) |

The delays follow the analysis (cumulative from the trigger: 1h, 1d, 2d, 4d, 6d, 8d, 10d, 13d). Made to order / shipping has no email of its own in the checkout flow; it is answered inside email 2.

## Abandoned Cart
Trigger: **Shopify Added to Cart (WT7SJV)**. The old onsite RjxRum has been dead since 7.2025. Filter: Checkout Started = 0 and Placed Order = 0 since start. Re-entry: 30 days.

| # | Template name | ID | Subject | Preview | Delay | Objection |
|---|---|---|---|---|---|---|
| 1 | FLOW 2026-11 \| Cart 1/8 \| Reminder | UBvD9B | Still thinking about it? | Your piece is saved, exactly as you chose it. | 4h | Reminder |
| 2 | FLOW 2026-11 \| Cart 2/8 \| Natural diamond + certificate | VA7Hcx | Is it really a natural diamond? | What's in your piece, and the certificate that proves it. | 1d | Natural black diamond / certificate (Black Ice/REMNANT block) |
| 3 | FLOW 2026-11 \| Cart 3/8 \| 530+ reviews | RPaVqY | 530+ reviews from people who hesitated too | Read what they wrote once the box was open. | 3d | Trust: 530+ reviews |
| 4 | FLOW 2026-11 \| Cart 4/8 \| Made to order, insured shipping on us | XfE6bE | Made by hand, for you | How your piece is made, and how it gets to you. | 5d | Made to order by hand, ships within 10 business days, insured shipping paid by us, customs may apply |
| 5 | FLOW 2026-11 \| Cart 5/8 \| Fit, returns, warranty | SyAYw5 | What if it doesn't fit? | Size, returns and warranty, answered in one minute. | 7d | Fit / resizing / returns / warranty |
| 6 | FLOW 2026-11 \| Cart 6/8 \| Affirm pay over time | UqenfM | Wear it now, pay over time | Choose Affirm at checkout and see your plan before you commit. | 9d | Price: Affirm |
| 7 | FLOW 2026-11 \| Cart 7/8 \| 15 minutes with Daniel | WAnMp5 | 15 minutes with me? | Ask anything, see the stones on video, change what you like. | 11d | Human: 15-minute call + WhatsApp |
| 8 | FLOW 2026-11 \| Cart 8/8 \| A note from Daniel + gift | UDhDea | A note from me | And a gift I wanted you to know about. | 14d | Personal note + gift featured |

The first cart email waits 4h, not 1h, so the person has time to reach checkout on their own. If they do, the checkout flow takes over. The rest follows the analysis.

## VIP confirmation
| Template name | ID | Subject | Preview | Delay | Content |
|---|---|---|---|---|---|
| FLOW 2026-11 \| VIP confirm | WcqZJP | You're on the VIP list | Black Friday offers reach you days before everyone else. | 0 (on the click on "Join the VIP list") | Early access to Black Friday + "gifts above certain amounts are coming". No discount amount revealed. CTA: new arrivals |

## Event variables used
**Checkout Started (UgasKH), Shopify:**
- `event.extra.line_items`: loop. The first item is the large hero; any further items appear as a "+ name" line.
- `item.product.title`, `item.variant_title`, `item.product.images.0.src`, `item.product.handle` → link `https://dianarafael.com/products/{{ item.product.handle }}`
- `event.extra.responsive_checkout_url` (on the dianarafael.com domain) with `|default:'https://dianarafael.com/cart'`
- `event.Collections`: `{% if 'Black Ice' in event.Collections or 'REMNANT' in event.Collections %}`

**Added to Cart (WT7SJV), Shopify:**
- `event|lookup:'Product Name'` (the key contains a space), `event|lookup:'Variant Name'`, `event.ImageURL`
- `event.URL`: arrives as `diana-rafael.myshopify.com`. It is rewritten to the site domain: `{% if 'myshopify.com' in event.URL %}https://dianarafael.com{{ event.URL|slice:'34:' }}{% else %}{{ event.URL|default:'https://dianarafael.com/cart' }}{% endif %}` (verified in a render).
- `event.Categories`: the same Black Ice / REMNANT condition.

General: `{{ first_name|default:'there' }}`, `{% unsubscribe 'Unsubscribe' %}`.

## Discount decision
**No code.** DIAMOND appears in the existing emails at 10% in one place and 5% in another, so its value is inconsistent. On top of that, the 15% sitewide automatic discount (30% from 27.11) cannot be combined with a code, so a code in the email would fail at checkout or confuse people. The last email of each flow features the **gift** instead: free 1 ct black diamond studs, "Now with orders from $2,000 / It used to be $3,000", in the body. Every other email has a gift strip: "Now from $2,000 (was $3,000)". No subject mentions a discount.

## Rules kept
- 530+ reviews.
- No delivery date. No fake deadlines.
- Every link goes to dianarafael.com, or to WhatsApp `wa.me/97235755066` and the booking page `/pages/new-website-book-online-appointment`.
- Reviews link to `/pages/our-customers-reviews` (no Google reviews page was found in the existing templates).
- Returns link to `/policies/refund-policy`; warranty links to `/pages/lifetime-manufacturer-warranty`.

## Before turning the flows on
- Subject and preview text are set in the flow message settings. They are not stored in the template.
- Turn on UTM tracking at the flow level. No manual UTMs were added.
- Fill in the From address for each message. A personal from (daniel@) is recommended.
- CSS is in a `<style>` block plus inline styles. Leave Klaviyo's "inline CSS" option on.
- Check the true collection name of REMNANT in Collections/Categories. The condition looks for the exact string `REMNANT`.
- Confirm these facts with Daniel: resizing ("We can resize most of our rings later on"; no claim that it is free), 30-day returns, "since 2014", and that every piece comes with a certificate.
- The gift: the email doesn't say whether the studs are added automatically or need a code or a note. Make sure the mechanism works at checkout.
- Send a preview from a real event (Klaviyo "Preview as" a profile with a real Checkout Started / Added to Cart event) before going live.

---

## Post-purchase, Browse, Cross-sell, JEWELVERSARY: templates (3.11.2026)

These are templates only. No flow, campaign or list was created or changed. The design is based on XuuLF8 (light): logo, the jewelry big at the top, one gold CTA, signed "Daniel, Diana Rafael". Every email is 120 to 250 words. The subject and preview text go in the flow (the preview text is also built into each template as a preheader). The generator and the HTML for each template are in `emails/flow-templates/` (`build.py`).

| Template | ID | Subject | Preview | Trigger / delay | Purpose |
|---|---|---|---|---|---|
| FLOW 2026-11 \| PostPurchase 1/4 \| Order confirmed, what happens now | Wz5xiT | Your order is confirmed. Here's what happens now. | Made by hand in our studio, checked, and shipped insured within 10 business days. | Placed Order (T6KBRR), immediately | Thank-you note and the 4 steps: confirm details and size, made by hand, quality check, insured shipping with tracking. Ships within 10 business days, no arrival date. "A person answers you, not AI." CTA: Instagram |
| FLOW 2026-11 \| PostPurchase 2/4 \| Inside the studio (day 5) | R7aCs4 | Inside the studio while your piece is made | A look at the bench: setting, polishing and the final check. | Placed Order, +5d (filter: Fulfilled Order = 0 since start) | Behind the scenes while the piece is being made. CTA: Instagram |
| FLOW 2026-11 \| PostPurchase 3/4 \| Shipped, tracking + customs + care | VWquHb | Your piece has shipped. Tracking inside. | Your tracking number, a short note on customs, and how to care for your piece. | Fulfilled Order (Yu3gpi), immediately | Carrier and tracking number. The exact sentence "Diana Rafael covered and paid all shipping costs." Customs duties may be required, so check them yourself. US orders ≥ $2,500 get a Form 5106 block (link to the page on the website). Care tips. CTA: track package |
| FLOW 2026-11 \| PostPurchase 4/4 \| Google review (delivered + 3d) | VM9Y2p | How does it feel to wear it? | One minute on Google helps the next person trust a studio they've never met. | Delivered Shipment (Uin4Gb), +3d | Short Google review request (Google Maps link from S43ETz, not Etsy) |
| FLOW 2026-11 \| Browse 1/4 \| The piece you viewed (2h) | TQqPSp | Still thinking about the {{ event.Name }}? | Made to order for you, shipped insured on us, with 30 days to decide. | Viewed Product (RdGtZY), +2h | The product plus the answers to the main objections: made to order, shipping on us, 30-day returns and certificate, customization. CTA: the product |
| FLOW 2026-11 \| Browse 2/4 \| Why us, 530+ reviews (1d) | UibmNe | Why 530+ customers trusted a studio they'd never visited | Natural diamonds, solid gold, made by hand since 2014. | +1d | Why us: since 2014, natural diamonds, made by hand, 530+ reviews. CTA: /pages/our-customers-reviews |
| FLOW 2026-11 \| Browse 3/4 \| Gift 1 ct studs from $2,000 (3d) | XbnPRb | A gift with the {{ event.Name }}: 1 ct studs | Free 1 ct natural black diamond studs, now from $2,000 (was $3,000). | +3d (from the previous email: +2d) | The gift: studs now from $2,000 (was $3,000). The gift is in the subject and in the body. CTA: the product |
| FLOW 2026-11 \| Browse 4/4 \| 15 minutes with Daniel (5d) | SNfvwN | Questions about the {{ event.Name }}? 15 minutes with Daniel | Size, gold, stone, budget: ask a person, not a chatbot. | +5d (from the previous email: +2d) | A person: 15 minutes with Daniel, plus WhatsApp. CTA: new-website-book-online-appointment |
| FLOW 2026-11 \| CrossSell 1/3 \| Made to go with yours (delivered + 60d) | SnRXLp | Made to go with yours | A few pieces we'd pair with what you're already wearing. | Delivered Shipment, +60d | A block by product type: ring → wedding bands, necklace → earrings, bracelet → ring and earrings, earrings → necklace, other → new arrivals. 2 product cards and a CTA |
| FLOW 2026-11 \| CrossSell 2/3 \| How customers wear them together (+4d) | U4qkKw | How our customers wear theirs | Same gold, same diamonds, worn together. | +4d | How to wear them together, by type, with the same blocks |
| FLOW 2026-11 \| CrossSell 3/3 \| Designed to match, 15 min with Daniel | YsXbez | Want it designed to match? 15 minutes with Daniel | We can make the second piece to fit the first exactly. | +5d | A matching piece built from the original design. A sentence by type. CTA: 15 minutes |
| FLOW 2026-11 \| Jewelversary | Tg23sD | Happy JEWELVERSARY, {{ first_name\|default:'friend' }} | One year ago today, you chose a piece from our studio. | Placed Order, +365d (or a yearly date-based flow) | Congratulations on one year, a check-in, and what's new (REMNANT plus new arrivals). No discount and no referral ask. CTA: REMNANT |

### Event variables used (checked against real events with get_events)
- **Placed Order T6KBRR / Fulfilled Order:** `event.Items.0`, `event.Collections`, `event.extra.name` (#1251), `event.extra.line_items.0.product.images.0.src`, `event.extra.line_items.0.name`, `event.extra.fulfillments.0.tracking_number`, `.tracking_url`, `.tracking_company` (taken from the existing tracking template TEMYFw), `event.extra.shipping_address.country_code`, `event|lookup:"$value"`.
- **Delivered Shipment Uin4Gb:** `event.Items`, `event.Collections`, `event.extra.fulfillment.line_items.0.product.images.0.src`. The cross-sell and review templates try this path first and then fall back to the Placed Order path, so they work on either trigger.
- **Viewed Product RdGtZY:** `event.Name`, `event.URL`, `event.ImageURL`. `event.Price` is left out because it sometimes contains `<span class=money>`.
- **Product type in cross-sell:** `{% if "engagement" in event.Collections|join:" "|lower %}` … `elif` necklace/pendant … bracelet … earring (on `event.Items` and `event.Collections`) … `else`. One template per email, no variants. This was checked in a render: the necklace branch and the engagement branch both work. Ordered Product (RijJmn) is not needed.

### Notes for building the flows
- **Links outside dianarafael.com:** Instagram, WhatsApp (wa.me), Google review and the carrier tracking link. All of them are required by the brief.
- **PostPurchase 2:** add the filter "Fulfilled Order = 0 since flow start" so the "while it's being made" email doesn't go out after the piece has shipped.
- **Form 5106:** the block appears in PostPurchase 3 for US orders ≥ $2,500 (render checked). If the separate VQTTX3 email is kept, remove one of them so the customer doesn't get it twice.
- **Browse 3, studs:** the copy says "added to orders from $2,000". Make sure the mechanism actually works (automatic, a code, or a note).
- **Cross-sell:** the WhatsApp/booking strip appears in emails 1 and 2. Email 3 is itself the booking email.
- The JEWELVERSARY template says "A year ago today". It fits both a one-time Placed Order +365d flow and a yearly date-based flow.

## Flows created as DRAFTS via API (3.11.2026 evening, full-access key)
All messages draft, from daniel@, UTM on. Templates were fixed to the real refund policy BEFORE the flows copied them. Builders: `flow-templates/buildflows.py`, `buildflows2.py`.
| Flow | ID | Trigger | Emails |
|---|---|---|---|
| 2026-11 \| Abandoned Checkout (8) | X6ZfPR | Checkout Started; Placed Order=0; not in flow 7d | 1h,1d,2d,4d,6d,8d,10d,13d |
| 2026-11 \| Abandoned Cart (8) | VWbEYm | Shopify Added to Cart; Checkout=0, Order=0; not in flow 30d | 4h,1d,3d,5d,7d,9d,11d,14d |
| Post-purchase: confirmed + studio | VydTk7 | Placed Order | now; +5d (msg filter Fulfilled=0) |
| Post-purchase: shipped | R6tiEk | Fulfilled Order | now |
| Delivered: review + cross-sell | Y6UjZu | Delivered Shipment | +3d review; +60d,+64d,+69d cross-sell |
| Browse abandonment (4) | XLpiBU | Viewed Product; no order/checkout/cart; not in flow 14d | 2h,1d,3d,5d |
| JEWELVERSARY | XrShek | Placed Order | +365d |
| VIP confirmation | RRcbwY | Added to segment Yvkrmu | now (template TLp5wQ fixed) |
Still to build: evergreen Welcome. Old flows stay ON until the new ones go live.

## Redesign 4.11.2026: one purpose-made image + layout per email
Daniel rejected the one-template look. All 29 flow-message templates were rebuilt and pushed into the existing DRAFT flows (no flow set live, nothing sent).
- Code: `flow-templates/redesign-2026-11-04/` (`vip.py`, `build_all.py` with the per-email PLAN, `rd.py` blocks, `push.py`/`push_all.sh`, `shot.py`, `make_gallery.py`; `backup-before/` = the templates as they were).
- Review gallery: `emails/review-2026-11-04/index.html` (each email rendered by Klaviyo with a real past event).
- Images (Klaviyo CDN, map in `images.json`): new AI scenes with NO jewelry drawn (VIP sealed envelope, bench/making, natural diamonds in parcel paper, unboxing, sizing tools, packed courier box, stone-to-phone call), made in Canva because Gemini = 402 (credits) and Higgsfield = 401 (re-auth). The jewelry is always real: the customer's own item from the event (chosen variant image first) or the E003 studs render.
- JEWELVERSARY / post-purchase no longer fall back to another ring (R117): no image -> no product photo.
- VIP flow message preview text is empty in the flow settings (API cannot set it); the template carries a hidden preheader with the same line.
