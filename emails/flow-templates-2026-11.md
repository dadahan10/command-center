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
