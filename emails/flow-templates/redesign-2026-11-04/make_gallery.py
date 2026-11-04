"""Build emails/review-2026-11-04/index.html: every redesigned flow email, rendered by Klaviyo with a real past event."""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "review-2026-11-04")

# (template, email, image job, static/dynamic, source, layout)
PLAN = [
    ("VIP confirmation (RRcbwY)", [
        ("TLp5wQ", "VIP confirm", "Make her feel chosen, on the inside", "Static, new AI scene (no jewelry drawn)", "Sealed black envelope, gold wax seal, brass key, studio after hours", "Noir 'sealed invitation': full-bleed photo + cream invitation card in a gold frame")]),
    ("Abandoned checkout (X6ZfPR)", [
        ("WtYdde", "1/8 Reminder", "Her piece, big and strong", "Dynamic: the chosen variant's image from the checkout", "Checkout Started line item", "Bone 'pedestal': piece on a white mat, name + variant"),
        ("VdW7XY", "2/8 What stopped you", "Question first, piece as context", "Dynamic thumbnail", "Checkout Started line item", "Paper split: piece left, big question right, answer buttons"),
        ("SNvbQS", "3/8 Natural diamond", "Where the stone comes from", "Static new AI scene + dynamic strip", "Rough and polished natural black diamonds in parcel paper, loupe", "Paper editorial, full-bleed photo, 'the stone in your piece' strip"),
        ("VLjUfd", "4/8 Reviews", "The moment the box opens", "Static new AI scene", "Hands with black nails opening a black box on linen", "Bone, left-aligned editorial"),
        ("WiHGws", "5/8 Fit + care", "The size worry, handled", "Static new AI scene + dynamic strip", "Ring mandrel, size gauges, tape on the bench", "Ink (dark), piece strip at the end"),
        ("V4FBhc", "6/8 Affirm", "Wear it now", "Dynamic", "Checkout Started line item", "Noir: piece on a cream mat inside a gold frame"),
        ("TNDw3W", "7/8 15 min with Daniel", "A real person shows the stones", "Static new AI scene + dynamic strip", "Tweezers holding a black diamond up to a phone on the bench", "Paper 'letter', inset photo, left-aligned"),
        ("SyBqNG", "8/8 Note + gift", "Show the studs", "Static, real CAD render (new macro crop)", "E003 1 ct black diamond studs, yellow gold", "Noir gift + 'your order' strip")]),
    ("Abandoned cart (VWbEYm)", [
        ("U58x8u", "1/8 Reminder", "Her piece, big", "Dynamic", "Added to Cart image", "Paper pedestal"),
        ("UBwjpH", "2/8 Natural diamond", "Where the stone comes from", "Static AI + dynamic strip", "Diamonds in parcel paper", "Ink, inset photo"),
        ("Xzm3N4", "3/8 Reviews", "The box-opening moment", "Static AI", "Unboxing", "Paper, inset photo, centred"),
        ("Y7JQ5h", "4/8 Made to order", "The bench and the making", "Static AI + dynamic strip", "Jeweler setting a black diamond", "Ink full-bleed"),
        ("WRGJQ3", "5/8 Fit + care", "The size worry, handled", "Static AI", "Sizing tools", "Bone, left-aligned"),
        ("TPeL6i", "6/8 Affirm", "Wear it now", "Dynamic", "Added to Cart image", "Noir gold frame"),
        ("UmCymx", "7/8 15 min with Daniel", "A real person", "Static AI + dynamic strip", "Stone held to a phone camera", "Ink full-bleed"),
        ("XjtgKS", "8/8 Note + gift", "Show the studs", "Static real render", "E003 studs macro", "Bone, gold frame + 'your piece' strip")]),
    ("Browse abandonment (XLpiBU)", [
        ("WwmdnE", "1/4 The piece you viewed", "The piece, big", "Dynamic", "Viewed Product image", "Bone pedestal"),
        ("UDi5wM", "2/4 Why us", "Made by hand since 2014", "Static AI + dynamic strip", "The bench", "Noir full-bleed"),
        ("XB8MV8", "3/4 Studs gift", "Show the studs", "Static real render + dynamic strip", "E003 studs macro", "Noir gift"),
        ("QXP4ar", "4/4 15 min with Daniel", "A real person", "Static AI + dynamic strip", "Stone held to a phone camera", "Paper letter")]),
    ("Post-purchase and delivered (VydTk7, R6tiEk, Y6UjZu)", [
        ("WHCJdX", "PP1 Order confirmed", "It's hers now", "Dynamic (chosen variant image)", "Placed Order line item", "Bone pedestal, 'now being made for you'"),
        ("Xg2wvc", "PP2 Inside the studio", "The bench and the making", "Static AI + dynamic strip", "Jeweler setting a stone + 'on the bench now: your piece'", "Ink full-bleed"),
        ("RCR6Vz", "PP3 Shipped", "Only her piece, with the shipping box", "Dynamic piece + static AI box", "Her piece above, the packed courier box below", "Paper, two stacked frames"),
        ("V4smfK", "PP4 Google review", "How does it feel", "Dynamic (delivered)", "Delivered Shipment line item", "Noir gold frame"),
        ("RZYnw2", "XS1 Made to go with yours", "Start from hers, then the pair", "Dynamic + catalog cards", "Her piece + matching products", "Bone pedestal (small)"),
        ("TbpdpS", "XS2 Worn together", "Hers as the anchor", "Dynamic + catalog cards", "Her piece + pairings", "Paper pedestal"),
        ("W9dVNd", "XS3 Designed to match", "A person designs the match", "Static AI + dynamic", "Stone held to a phone + her piece", "Ink")]),
    ("JEWELVERSARY (XrShek)", [
        ("TLpfRY", "One year", "HER ring, nothing else", "Dynamic (chosen variant image); no fallback to any other ring", "Placed Order line item", "Noir, giant gold '1', her piece in a gold frame")]),
]

CSS = """
:root{--bg:#f4efe6;--fg:#1f1b16;--mut:#6b6256;--card:#fff;--gold:#9a7a2c}
@media (prefers-color-scheme:dark){:root{--bg:#141210;--fg:#efe8dc;--mut:#a69c8c;--card:#1f1c19;--gold:#d4b26a}}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1500px;margin:0 auto;padding:24px 16px 80px}
h1{font:500 34px Georgia,serif;margin:0 0 6px}
h2{font:500 26px Georgia,serif;margin:46px 0 14px;border-bottom:1px solid var(--gold);padding-bottom:6px}
nav{display:flex;flex-wrap:wrap;gap:8px 18px;margin:12px 0 4px} nav a{color:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:22px}
article{background:var(--card);border-radius:10px;padding:14px;box-shadow:0 1px 3px #0002}
header{display:flex;justify-content:space-between;margin-bottom:6px} header span{color:var(--mut);font-family:monospace}
dl{display:grid;grid-template-columns:90px 1fr;gap:2px 10px;margin:0 0 10px;font-size:13px} dt{color:var(--mut)} dd{margin:0}
.pair{display:flex;gap:10px;align-items:flex-start;max-height:900px;overflow:auto}
.pair img{width:300px;display:block;border:1px solid #0001} .pair img.m{width:130px}
p.note{color:var(--mut);max-width:900px}
@media (max-width:520px){.grid{grid-template-columns:1fr} .pair img{width:100%} .pair img.m{display:none}}
"""


def main():
    toc, body = [], []
    for sec, items in PLAN:
        sid = "s" + str(len(toc))
        toc.append(f'<a href="#{sid}">{html.escape(sec)}</a>')
        body.append(f'<h2 id="{sid}">{html.escape(sec)}</h2><div class="grid">')
        for tid, name, job, kind, src, layout in items:
            body.append(
                f'<article><header><b>{html.escape(name)}</b><span>{tid}</span></header>'
                f'<dl><dt>Image job</dt><dd>{html.escape(job)}</dd><dt>Type</dt><dd>{html.escape(kind)}</dd>'
                f'<dt>Source</dt><dd>{html.escape(src)}</dd><dt>Layout</dt><dd>{html.escape(layout)}</dd></dl>'
                f'<div class="pair"><a href="html/render-{tid}.html" target="_blank"><img loading="lazy" src="shots/render-{tid}-d.jpg" alt="{tid} desktop"></a>'
                f'<a href="html/render-{tid}.html" target="_blank"><img loading="lazy" class="m" src="shots/render-{tid}-m.jpg" alt="{tid} mobile"></a></div></article>')
        body.append("</div>")
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Flow emails review</title><style>{CSS}</style></head><body><main>'
            '<h1>Flow emails, redesigned (4.11.2026)</h1>'
            '<p class="note">Each email is rendered by Klaviyo from its DRAFT flow template with a real past event '
            '(a checkout, a cart, a viewed product, order #1250 placed / fulfilled / delivered). First name is set to "Sarah" and the tracking '
            'number is masked. Desktop on the left, mobile on the right; click to open the full HTML. All flows are still DRAFT and nothing was sent.</p>'
            f'<nav>{" ".join(toc)}</nav>{"".join(body)}</main></body></html>')
    os.makedirs(R, exist_ok=True)
    open(os.path.join(R, "index.html"), "w", encoding="utf-8").write(page)
    print("gallery written:", os.path.abspath(os.path.join(R, "index.html")))


if __name__ == "__main__":
    main()
