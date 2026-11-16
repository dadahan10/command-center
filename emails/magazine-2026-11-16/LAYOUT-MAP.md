# The Black & White Issue: layout map (16.11.2026)

Preview only. Nothing is live or in Klaviyo. One masthead (black/sand bar + logo + "The Black & White Issue"),
one palette (ink #0F1418, sand #CFB288, bone #F4EFE6), one type system (Champie lettering as images, Cormorant + Manrope).
Each email takes one **layout family**. The rule: two emails in a row never share a family.

## Layout families

| Family | Name | What the reader sees first |
|---|---|---|
| A | Cover story | A Champie cover line on ink, then her piece full-bleed, with cover lines under it |
| B | Split spread | A black/bone diptych: a large figure or word on ink, her piece on bone |
| C | Pull quote + still life | One short line set huge on sand, then her piece as a captioned still life |
| D | Index | A contents page: every item she chose, then the offer, Affirm and gifts listed as entries |
| E | Editor's letter | A letter from Daniel: drop cap, signature, her piece shown small like a postcard |
| F | Photo essay | One brand photograph full-bleed (bench, diamonds in parcel paper, unboxing), a caption, then her piece small |
| G | Q&A | The customer's real questions set as headings ("What if it doesn't fit?"), short answers, then a call-to-action |
| H | Letters page | One customer review set large as the feature, "550+ reviews" as the standfirst, then her piece |

Built so far: A, B, C, D, E (checkout XW6UqR below). F, G and H have not been designed yet; they get built in the full rollout.

## Checkout, Black Ice: XW6UqR (5 emails, built in this folder)

| # | Template | Email | Family |
|---|---|---|---|
| 1 | RGSj5h | Is this the one? (2h) | A Cover story |
| 2 | U3FYQZ | Extra 5% (CART5) | B Split spread |
| 3 | TDAQrS | Still waiting (tonight) | C Pull quote + still life |
| 4 | Re9UiL | Affirm: wear it now | D Index |
| 5 | UNZFjJ | Extra 10% (CART10), last email | E Editor's letter |

The gift block changes with the email too: a black/bone diptych in 1 and 4, full-bleed bands in 2 and 5 ("P.S." in 5), and "Black or white?" set large in 3.

## Checkout, not Black Ice: VB4v4q (7 emails)

| # | Email (live subject) | Family |
|---|---|---|
| 1 | Is This the One? | A Cover story |
| 2 | Your cart is about to expire (CART5) | B Split spread |
| 3 | Why Diana Rafael? (reviews) | H Letters page |
| 4 | Your Sparkle is About to Fade Away | C Pull quote + still life |
| 5 | Have Any Questions? Let's Meet! | G Q&A |
| 6 | Flexible Layaway Options with Affirm | D Index |
| 7 | Shop Now with Affirm & Save 10% (CART10) | E Editor's letter |

## Abandoned cart: VWbEYm (8 emails, order after the 4.11 swap)

| # | Email | Family |
|---|---|---|
| 1 | Reminder: Still thinking about it? | A Cover story |
| 2 | 15 minutes with me? | G Q&A |
| 3 | 550+ reviews | H Letters page |
| 4 | Made by hand, for you | F Photo essay (bench) |
| 5 | What if it doesn't fit? | G Q&A |
| 6 | Wear it now, pay over time | D Index |
| 7 | Is it really a natural diamond? | C Pull quote + still life (diamonds in parcel paper) |
| 8 | A note from me + gift | E Editor's letter |

## Browse abandonment: Y6Zunh (5 emails)

| # | Email | Family |
|---|---|---|
| 1 | Did you see something you like? | A Cover story (the piece she viewed) |
| 2 | Let's talk it through (15 minutes) | G Q&A |
| 3 | Why count on us? | F Photo essay (studio) |
| 4 | Wear it now, pay over time | D Index |
| 5 | An extra 10% (CART10) | B Split spread (a large 10% on ink) |

No family repeats back to back in any flow. A customer who gets two flows still sees different layouts, because each flow starts with A and then moves to a different second family (B, G or G).

## Before rollout
- The Champie lettering PNGs and the flattened logos in `assets/` must be uploaded to the Klaviyo image library. Then set `ASSET_BASE` and rebuild.
- Each live template is swapped with `live-fix-2026-11-15/swap.py` only after Daniel approves.
