import json, re, html as H, sys, kl
ctx = {"first_name": "Katherine", "person": {"first_name": "Katherine"}, "organization": {"url": "https://dianarafael.com"},
  "event": {"$value": 4208.0, "extra": {"responsive_checkout_url": "https://dianarafael.com/24695441/checkouts/ac/hWNJAi918OJwJmYLWF5lSDAp/recover?key=9e63b&locale=en-US",
   "line_items": [{"title": "Sparks", "variant_title": "14K / 9", "quantity": 1, "line_price": 1530,
     "product": {"title": "Sparks - Eternity Natural Round cut Diamond Wedding Band", "handle": "0-9-carats-round-diamond-wedding-band-2", "images": [{"src": "https://cdn.shopify.com/s/files/1/2469/5441/products/20276ad6-b6f0-5a57-812d-15167ae25360.jpg?v=1680509762"}], "variant": {"images": []}}},
    {"title": "Hidden Halo", "variant_title": "9 / White Gold", "quantity": 1, "line_price": 2678,
     "product": {"title": "Hidden Halo Natural Black Diamond Pear Engagement Ring in Yellow Gold", "handle": "forbidden-fruit-hidden-halo-natural-black-diamond-pear-engagement-ring-in-yellow-gold", "images": [{"src": "https://cdn.shopify.com/s/files/1/2469/5441/files/5f71a449-1651-5de6-b6b7-1d9d8aa6bdcf.jpg?v=1723112726"}], "variant": {"images": []}}}]}}}
import os
os.makedirs("preview", exist_ok=True)
ids = sys.argv[1:]
for tid in ids:
    src = open(f"out/{tid}.html", encoding="utf-8").read()
    s, d = kl.call("POST", "templates", {"data": {"type": "template", "attributes": {"name": f"TEST live-fix {tid} (delete)", "editor_type": "CODE", "html": src}}})
    if s not in (200, 201): print(tid, "create", s, d); continue
    tmp = d["data"]["id"]
    s, r = kl.call("POST", "template-render", {"data": {"type": "template", "id": tmp, "attributes": {"context": ctx}}})
    kl.call("DELETE", f"templates/{tmp}")
    if s not in (200, 201): print(tid, "render", s, r); continue
    out = r["data"]["attributes"]["html"]
    open(f"preview/{tid}.html", "w", encoding="utf-8").write(out)
    txt = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>", "", out, flags=re.S))))
    links = sorted(set(re.findall(r'href="([^"]+)"', out)))
    print("=====", tid); print(txt[:900]); print("LINKS:"); [print("  ", l[:160]) for l in links]
