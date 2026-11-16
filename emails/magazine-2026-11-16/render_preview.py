"""Render out/*.html with sample Checkout Started data LOCALLY (Django templates stand in for Klaviyo's renderer;
nothing is sent to Klaviyo), then screenshot each email at 600 and 390 px, plus a forced-dark simulation at 390,
and write preview/index.html with the five side by side.
Usage: python render_preview.py
"""
import os, re, sys, glob
import django
from django.conf import settings
from django import template as djt

HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(HERE, "preview"); os.makedirs(PREV, exist_ok=True)

settings.configure(TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}])
django.setup()
from django.template import Engine, Context

lib = djt.Library()


@lib.filter
def lookup(obj, key):
    try:
        return obj.get(key)
    except Exception:
        return None


@lib.simple_tag
def unsubscribe(label="Unsubscribe"):
    from django.utils.safestring import mark_safe
    return mark_safe(f'<a class="unsubscribe-link" href="#unsubscribe">{label}</a>')


sys.modules["kl_lib"] = type(sys)("kl_lib"); sys.modules["kl_lib"].register = lib
ENGINE = Engine(builtins=["kl_lib"], autoescape=True)

# A real Black Ice checkout: the Hidden Halo pear black diamond ring + a wedding band (two line items).
CTX = {"first_name": "Katherine", "person": {"first_name": "Katherine"},
       "event": {"$value": 4208.0, "extra": {
           "responsive_checkout_url": "https://dianarafael.com/24695441/checkouts/ac/hWNJAi918OJwJmYLWF5lSDAp/recover?key=9e63b&locale=en-US",
           "line_items": [
               {"title": "Hidden Halo", "variant_title": "9 / Yellow Gold", "quantity": 1, "line_price": 2678,
                "product": {"title": "Hidden Halo Natural Black Diamond Pear Engagement Ring in Yellow Gold",
                            "handle": "forbidden-fruit-hidden-halo-natural-black-diamond-pear-engagement-ring-in-yellow-gold",
                            "images": [{"src": "https://cdn.shopify.com/s/files/1/2469/5441/files/5f71a449-1651-5de6-b6b7-1d9d8aa6bdcf.jpg?v=1723112726"}],
                            "variant": {"images": []}}},
               {"title": "Sparks", "variant_title": "14K / 9", "quantity": 1, "line_price": 1530,
                "product": {"title": "Sparks - Eternity Natural Round cut Diamond Wedding Band", "handle": "0-9-carats-round-diamond-wedding-band-2",
                            "images": [{"src": "https://cdn.shopify.com/s/files/1/2469/5441/products/20276ad6-b6f0-5a57-812d-15167ae25360.jpg?v=1680509762"}],
                            "variant": {"images": []}}}]}}}

DARK_SIM = ("<style>/* forced-dark simulation (Gmail iOS style full inversion; images re-inverted) */"
            "html{filter:invert(1) hue-rotate(180deg);background:#fff;} img{filter:invert(1) hue-rotate(180deg);}</style>")

TITLES = {"1": ("Cover story", "Ink cover: Champie cover line, her piece full-bleed, cover lines under it."),
          "2": ("Split spread", "Black | bone diptych: a giant 5% on ink beside her piece on bone."),
          "3": ("Pull quote + still life", "Sand page: 'Still waiting.' set huge, then her piece as a captioned still life."),
          "4": ("The index", "Ink contents page: every item in her checkout, then the 5%, Affirm and gifts as entries."),
          "5": ("Editor's letter", "Bone letter from Daniel with a drop cap and signature; her piece as a postcard.")}
SUBJ = {"1": "Is This the One?", "2": "Extra 5% Off Inside", "3": "Still waiting (tonight)", "4": "Affirm: wear it now", "5": "Unlock 10% Off"}


def render_all(ctx, suffix=""):
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "out", "*.html"))):
        name = os.path.splitext(os.path.basename(f))[0]
        html = ENGINE.from_string(open(f, encoding="utf-8").read()).render(Context(ctx))
        p = os.path.join(PREV, name + suffix + ".html")
        open(p, "w", encoding="utf-8").write(html)
        out.append((name, p, html))
    return out


def shoot(items):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, p, html in items:
            for w in (600, 390):
                pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1 if w == 600 else 2)
                pg.goto("file:///" + p.replace("\\", "/"), wait_until="load")
                pg.wait_for_timeout(600)
                pg.screenshot(path=os.path.join(PREV, f"{name}-{w}.png"), full_page=True)
                if w == 390:
                    pg.add_style_tag(content=DARK_SIM.replace("<style>", "").replace("</style>", ""))
                    pg.wait_for_timeout(200)
                    pg.screenshot(path=os.path.join(PREV, f"{name}-390-dark.png"), full_page=True)
                pg.close()
        b.close()


def index(items):
    cols = []
    for name, p, html in items:
        n = name.split("-")[0]
        t, d = TITLES[n]
        cols.append(f'<figure><figcaption><b>{n}. {t}</b><span>Subject today: {SUBJ[n]} · {len(open(os.path.join(HERE, "out", name + ".html"), encoding="utf-8").read().encode())//1024} KB template</span>'
                    f'<span>{d}</span><span><a href="{name}.html">open HTML</a> · <a href="{name}-390.png">390 px</a> · '
                    f'<a href="{name}-390-dark.png">dark sim</a></span></figcaption>'
                    f'<a href="{name}.html"><img src="{name}-600.png" alt="{t}" loading="lazy"/></a></figure>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Black &amp; White Issue</title>
<style>
:root{{--ink:#0F1418;--sand:#CFB288;--bone:#F4EFE6;--mute:#564F46;}}
body{{margin:0;background:var(--bone);color:var(--ink);font:15px/1.5 'Helvetica Neue',Arial,sans-serif;}}
header{{padding:28px 24px 8px;}} h1{{font:500 34px/1.1 Georgia,serif;margin:0 0 6px;}} header p{{margin:0;color:var(--mute);max-width:70ch;}}
.row{{display:flex;gap:18px;overflow-x:auto;padding:20px 24px 40px;align-items:flex-start;}}
figure{{margin:0;flex:0 0 340px;}} figure img{{width:340px;display:block;}}
figcaption{{display:flex;flex-direction:column;gap:2px;min-height:150px;margin-bottom:10px;}}
figcaption b{{font:500 21px/1.2 Georgia,serif;}} figcaption span{{font-size:13px;color:var(--mute);}}
a{{color:var(--ink);}}
</style></head><body>
<header><h1>The Black &amp; White Issue: checkout flow XW6UqR, 5 emails</h1>
<p>Preview only, sample data (Katherine, Hidden Halo black diamond pear ring + Sparks band, $4,208). Nothing here is live or pushed to Klaviyo.
One masthead, one palette, one type system; a different editorial layout in every email. Scroll sideways.</p></header>
<div class="row">{''.join(cols)}</div></body></html>"""
    open(os.path.join(PREV, "index.html"), "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    items = render_all(CTX)
    # fallback check: no first name, empty cart extra (must render without errors or 'None')
    for name, p, html in render_all({"event": {"$value": 900, "extra": {"line_items": []}}}, suffix="-noname"):
        assert "None" not in re.sub(r"<[^>]+>", " ", html), name
        os.remove(p)
    shoot(items)
    index(items)
    for name, p, html in items:
        links = sorted(set(re.findall(r'href="([^"]+)"', html)))
        print(name, len(html) // 1024, "KB rendered;", len(links), "links")
