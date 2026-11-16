"""Render the 8 cart emails through Klaviyo's template-render with a real Added to Cart event (12.11, Black Magic ring),
save preview/CART-<n>-<tid>.html + 390px PNG, and sanity-check links/variables.
Also renders a second context (no first name, non-Black-Ice band, $1,530) to check fallbacks.
Usage: python render_cart.py"""
import re, os, html as H, kl
from build_cart import ACTIONS
from playwright.sync_api import sync_playwright

EV = {"Product Name": "3.44 Carats Double Hidden Halo Three-Sided Black & White Natural Diamond Cushion Cut - 6.5 / Yellow Gold",
      "Variant Name": "6.5 / Yellow Gold", "ImageURL": "https://cdn.shopify.com/s/files/1/2469/5441/products/d268a725-432c-5dab-928b-959b1bd51aa9.jpg?v=1679921656",
      "Price": 2465.0, "$value": 2465.0, "Quantity": 1.0, "CompareAtPrice": 2900.0,
      "URL": "https://diana-rafael.myshopify.com/products/black-magic-black-diamond-engagement-ring",
      "Categories": ["BLACK ICE - Engagement Rings", "Black Ice", "Black Magic", "all"]}
EV2 = {"Product Name": "Sparks - Eternity Natural Round cut Diamond Wedding Band", "Variant Name": "14K / 9",
       "ImageURL": "https://cdn.shopify.com/s/files/1/2469/5441/products/20276ad6-b6f0-5a57-812d-15167ae25360.jpg?v=1680509762",
       "Price": 1530.0, "$value": 1530.0, "URL": "https://diana-rafael.myshopify.com/products/0-9-carats-round-diamond-wedding-band-2",
       "Categories": ["ALL WEDDING BANDS", "all"]}
CTX = {"first_name": "Katherine", "person": {"first_name": "Katherine"}, "organization": {"url": "https://dianarafael.com"}, "event": EV}
CTX2 = {"first_name": "", "person": {}, "organization": {"url": "https://dianarafael.com"}, "event": EV2}
os.makedirs("preview", exist_ok=True)


def render(src, ctx):
    s, d = kl.call("POST", "templates", {"data": {"type": "template", "attributes": {"name": "TEST cart render (delete)", "editor_type": "CODE", "html": src}}})
    assert s in (200, 201), d
    tmp = d["data"]["id"]
    s, r = kl.call("POST", "template-render", {"data": {"type": "template", "id": tmp, "attributes": {"context": ctx}}})
    kl.call("DELETE", f"templates/{tmp}")
    assert s in (200, 201), r
    return r["data"]["attributes"]["html"]


def text(h):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>", "", h, flags=re.S))))


if __name__ != "__main__": raise SystemExit
problems, files = [], []
for n, (aid, tid) in enumerate(ACTIONS, 1):
    src = open(f"out/{tid}.html", encoding="utf-8").read()
    for label, ctx in (("A", CTX), ("B", CTX2)):
        out = render(src, ctx)
        txt = text(out)
        links = sorted(set(re.findall(r'href="([^"]+)"', out)))
        srcs = sorted(set(re.findall(r'src="([^"]+)"', out)))
        bad = [l for l in links + srcs if l != "[unsubscribe_tag]" and ("{" in l or "%" in l and "discount" not in l and "wa.me" not in l or "myshopify" in l or not l.startswith("http"))]
        for k in ("{{", "{%", "AFFIRM10", "myshopify", "business days", "None"):
            if k in txt: bad.append("text contains " + k)
        if label == "A" and "Katherine" not in txt: bad.append("no first name")
        if label == "B" and ("Hi, " not in txt and "Hi there" not in txt and n != 0) and n == 1: bad.append("fallback greeting")
        if label == "A" and "550+" not in txt: bad.append("no 550+")
        if "Free diamond studs" not in txt: bad.append("no gifts block")
        if bad: problems.append((n, tid, label, bad))
        if label == "A":
            p = f"preview/CART-{n}-{tid}.html"
            open(p, "w", encoding="utf-8").write(out); files.append(p)
            print(f"===== {n} {tid}"); print(txt[:700])
            for l in links: print("   ", l[:170])
        else:
            open(f"preview/CART-{n}-{tid}-noname.html", "w", encoding="utf-8").write(out)
            print(f"  [B] {n}: {txt[txt.find('Diana Rafael'):][:260]}")

with sync_playwright() as p:
    b = p.chromium.launch()
    for f in files:
        pg = b.new_page(viewport={"width": 390, "height": 900}, device_scale_factor=1)
        pg.goto("file:///" + os.path.abspath(f).replace("\\", "/"))
        pg.wait_for_timeout(1500)
        pg.screenshot(path=f.replace(".html", ".png"), full_page=True)
        pg.close()
    b.close()
print("PROBLEMS:", problems or "none")
