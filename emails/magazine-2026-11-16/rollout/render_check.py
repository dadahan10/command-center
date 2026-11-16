"""Render every built email through Klaviyo's template-render with a REAL recent event (named profile) and a second real
event with no first name, check text / variables / links / images / codes / buttons / size, screenshot the named
render at 390 px and build one contact sheet per flow.
Usage: python render_check.py [flow ...]  -> preview/<file>.html|png, preview/<flow>-contact.png, check-report.json"""
import os, sys, re, json, time, html as H, urllib.request
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "live-fix-2026-11-15"))
import kl
from PIL import Image, ImageDraw, ImageFont

PREV = os.path.join(HERE, "preview"); os.makedirs(PREV, exist_ok=True)
EV = json.load(open(os.path.join(HERE, "recent-events.json"), encoding="utf-8"))
PLAN = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))


def ctx(metric, pick):
    e = [x for x in EV[metric] if pick(x)][0]
    p = dict(e["props"])
    if "$extra" in p:
        p["extra"] = p.pop("$extra")
    fn = e["first_name"] or ""
    c = {"first_name": fn, "person": {"first_name": fn} if fn else {}, "organization": {"url": "https://dianarafael.com", "name": "Diana Rafael"}, "event": p}
    return c, e["dt"], fn or "(no name)", (p.get("Product Name") or p.get("Name") or [li["product"]["title"] for li in p.get("extra", {}).get("line_items", [])])


CTX = {
    "chk": (ctx("UgasKH", lambda x: x["first_name"] == "Katherine"), ctx("UgasKH", lambda x: not x["first_name"] and x["props"]["$value"] < 1000)),
    "cart": (ctx("WT7SJV", lambda x: x["first_name"] == "Katherine" and x["props"]["$value"] == 2678.0), ctx("WT7SJV", lambda x: not x["first_name"] and x["props"]["$value"] == 2380.0)),
    "browse": (ctx("RdGtZY", lambda x: x["first_name"] == "Morgan"), ctx("RdGtZY", lambda x: not x["first_name"])),
}
KIND = {"XW6UqR": "chk", "VB4v4q": "chk", "VWbEYm": "cart", "Y6Zunh": "browse"}
CODE = {"XW6UqR": ["CART5"] * 4 + ["CART10"], "VB4v4q": ["CART5"] * 6 + ["CART10"],
        "VWbEYm": [None, None, "CART5", "CART5", "CART5", "CART5", "CART10", "CART10"], "Y6Zunh": [None] * 4 + ["CART10"]}


def call(*a, **k):
    for i in range(6):
        s, r = kl.call(*a, **k)
        if s != 429:
            return s, r
        time.sleep(2 + 2 * i)
    return s, r


def render(src, c):
    s, d = call("POST", "templates", {"data": {"type": "template", "attributes": {"name": "TEST B&W render (delete)", "editor_type": "CODE", "html": src}}})
    assert s in (200, 201), d
    tmp = d["data"]["id"]
    try:
        s, r = call("POST", "template-render", {"data": {"type": "template", "id": tmp, "attributes": {"context": c}}})
        assert s in (200, 201), r
        return r["data"]["attributes"]["html"]
    finally:
        call("DELETE", f"templates/{tmp}")


def text(h):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(style|title)[^>]*>.*?</\1>", "", h, flags=re.S))))


def check(fid, n, out, label, name):
    bad = []
    txt = text(out)
    links = sorted(set(H.unescape(l) for l in re.findall(r'href="([^"]+)"', out)))
    srcs = sorted(set(re.findall(r'<img[^>]+src="([^"]+)"', out)))
    for l in links:
        if l in ("[unsubscribe_tag]",) or "unsubscribe" in l or "manage_preferences" in l:
            continue
        if not l.startswith("http") or "{" in l or "myshopify" in l or " " in l:
            bad.append("link " + l[:120])
    for s in srcs:
        if not s.startswith("https://") or "{" in s or s.startswith("../"):
            bad.append("img " + s[:120])
    for k in ("{{", "{%", "AFFIRM10", "myshopify", "business days", "None", "../assets"):
        if k in txt or (k == "../assets" and k in out):
            bad.append("contains " + k)
    if label == "named" and name not in txt:
        bad.append("first name missing")
    if label == "noname" and re.search(r"\b(Hi|Dear) ,", txt):
        bad.append("empty name greeting")
    if "550+" not in txt:
        bad.append("no 550+")
    if "diamond studs" not in txt:
        bad.append("no gifts")
    code = CODE[fid][n - 1]
    for cd in ("CART5", "CART10"):
        if cd == code and cd not in txt:
            bad.append("missing " + cd)
        if cd != code and re.search(r"\b" + cd + r"\b", txt):
            bad.append("unexpected " + cd)
    nb = out.count('class="btn"')
    if not 2 <= nb <= 4:
        bad.append(f"{nb} buttons")
    kb = len(out.encode("utf-8")) / 1024
    if kb >= 100:
        bad.append(f"{kb:.0f} KB (Gmail clips at 102)")
    return bad, links, srcs, round(kb, 1), nb


def shoot(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for p in paths:
            pg = b.new_page(viewport={"width": 390, "height": 900}, device_scale_factor=1)
            pg.goto("file:///" + p.replace("\\", "/"), wait_until="load")
            pg.wait_for_timeout(1200)
            pg.screenshot(path=p.replace(".html", ".png"), full_page=True)
            pg.close()
        b.close()


def contact(fid, items):
    ims = [Image.open(p.replace(".html", ".png")).convert("RGB") for p, _ in items]
    W = 300
    ims = [im.resize((W, int(im.height * W / im.width))) for im in ims]
    gap, top = 24, 70
    sheet = Image.new("RGB", (len(ims) * (W + gap) + gap, max(i.height for i in ims) + top + gap), "#E9E4DA")
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("arial.ttf", 15); fb = ImageFont.truetype("arialbd.ttf", 16)
    except Exception:
        f = fb = ImageFont.load_default()
    for i, (im, (p, lab)) in enumerate(zip(ims, items)):
        x = gap + i * (W + gap)
        d.text((x, 14), lab[0], font=fb, fill="#0F1418")
        d.text((x, 38), lab[1][:40], font=f, fill="#564F46")
        sheet.paste(im, (x, top))
    out = os.path.join(PREV, f"{fid}-contact.png")
    sheet.save(out, optimize=True)
    return out


def link_status(urls):
    def one(u):
        if "wa.me" in u:
            return u, "skip"
        try:
            req = urllib.request.Request(u, method="GET", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return u, r.status
        except urllib.error.HTTPError as e:
            return u, e.code
        except Exception as e:
            return u, str(e)[:60]
    with ThreadPoolExecutor(8) as ex:
        return dict(ex.map(one, urls))


if __name__ == "__main__":
    flows = sys.argv[1:] or list(PLAN)
    report = json.load(open(os.path.join(HERE, "check-report.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "check-report.json")) else {}
    for fid in flows:
        kind = KIND[fid]
        (cA, dtA, nameA, prodA), (cB, dtB, nameB, prodB) = CTX[kind]
        print(f"== {fid}: named = {nameA} {dtA[:10]} {prodA} | fallback = {nameB} {dtB[:10]} {prodB}")
        items, all_links, rep = [], set(), []
        for e in PLAN[fid]:
            src = open(os.path.join(HERE, "out", e["file"] + ".html"), encoding="utf-8").read()
            outA = render(src, cA); outB = render(src, cB)
            pA = os.path.join(PREV, e["file"] + ".html"); open(pA, "w", encoding="utf-8").write(outA)
            open(os.path.join(PREV, e["file"] + "-noname.html"), "w", encoding="utf-8").write(outB)
            bA, links, srcs, kb, nb = check(fid, e["n"], outA, "named", nameA)
            bB, linksB, _, _, _ = check(fid, e["n"], outB, "noname", nameB)
            all_links |= set(links) | set(linksB)
            rep.append(dict(n=e["n"], file=e["file"], family=e["family"], kb=kb, buttons=nb, problems_named=bA, problems_noname=bB, links=links))
            print(f"  {e['n']} {e['family']:24s} {kb:5.1f} KB {nb} btn  named:{bA or 'ok'}  noname:{bB or 'ok'}")
            items.append((pA, (f"{e['n']}. {e['family']}", e["subject"])))
        shoot([p for p, _ in items])
        sheet = contact(fid, items)
        st = link_status(sorted(l for l in all_links if l.startswith("http")))
        dead = {u: s for u, s in st.items() if s not in (200, "skip")}
        print("  contact sheet:", sheet)
        print("  links checked:", len(st), "not-200:", dead or "none")
        report[fid] = dict(context_named=[nameA, dtA], context_noname=[nameB, dtB], emails=rep, contact=sheet, link_status=st, dead_links=dead)
    json.dump(report, open(os.path.join(HERE, "check-report.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
