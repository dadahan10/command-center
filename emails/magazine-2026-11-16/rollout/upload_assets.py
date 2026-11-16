"""Upload assets/*.png (Champie lettering + flattened logos) to the Klaviyo image library -> assets-klaviyo.json {name: hosted url}.
Already-uploaded files (same name + same bytes hash) are skipped. Usage: python upload_assets.py"""
import os, sys, json, glob, hashlib, requests
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "live-fix-2026-11-15"))
import kl
MAP = os.path.join(HERE, "assets-klaviyo.json")
done = json.load(open(MAP, encoding="utf-8")) if os.path.exists(MAP) else {}
for p in sorted(glob.glob(os.path.join(HERE, "..", "assets", "*.png"))):
    name = os.path.splitext(os.path.basename(p))[0]
    h = hashlib.sha1(open(p, "rb").read()).hexdigest()[:10]
    if name in done and done[name].get("sha") == h:
        continue
    r = requests.post("https://a.klaviyo.com/api/image-upload", headers={"Authorization": f"Klaviyo-API-Key {kl.KEY}", "revision": kl.REV, "accept": "application/vnd.api+json"},
                      files={"file": (f"bw-issue-{name}-{h}.png", open(p, "rb"), "image/png")}, data={"name": f"B&W Issue 2026-11 | {name} {h}", "hidden": "false"})
    if r.status_code not in (200, 201):
        print(name, r.status_code, r.text[:300]); continue
    a = r.json()["data"]
    done[name] = {"url": a["attributes"]["image_url"], "id": a["id"], "sha": h}
    print(name, a["attributes"]["image_url"])
json.dump(done, open(MAP, "w", encoding="utf-8"), indent=1)
print(len(done), "assets hosted")
