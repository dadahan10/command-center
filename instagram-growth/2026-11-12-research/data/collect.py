"""Read-only: pull last N posts of public business/creator accounts via Graph API business_discovery.
Token from diana-rafael/.env, never written to output. Run: python collect.py handle [n]"""
import json, sys, urllib.request, urllib.parse, pathlib, datetime, time
env = {}
for l in open(r"C:\Users\USER\OneDrive\Desktop\diana-rafael\.env", encoding="utf-8"):
    if "=" in l and not l.startswith("#"):
        k, v = l.strip().split("=", 1); env[k] = v.strip('"')
T, IG = env["META_SYSTEM_USER_TOKEN"], env["IG_USER_ID"]
h = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 150
F = "caption,media_type,media_product_type,like_count,comments_count,timestamp,permalink,media_url,thumbnail_url,children{media_type,media_url}"
media, after, info = [], None, {}
while len(media) < N:
    m = f"media.limit(50){'.after('+after+')' if after else ''}{{{F}}}"
    f = f"business_discovery.username({h}){{username,name,biography,followers_count,follows_count,media_count,{m}}}"
    u = f"https://graph.facebook.com/v21.0/{IG}?" + urllib.parse.urlencode({"fields": f, "access_token": T})
    try:
        bd = json.load(urllib.request.urlopen(u, timeout=90))["business_discovery"]
    except urllib.error.HTTPError as e:
        print("ERR", e.read()[:300].decode(errors="replace")); break
    info = {k: bd.get(k) for k in ("username","name","biography","followers_count","follows_count","media_count")}
    d = bd.get("media", {}); media += d.get("data", [])
    after = d.get("paging", {}).get("cursors", {}).get("after")
    if not after or not d.get("data"): break
    time.sleep(1)
out = pathlib.Path(__file__).parent / f"{h}-posts.json"
out.write_text(json.dumps({"pulled": datetime.datetime.now().isoformat(timespec="minutes"), "account": info, "media": media}, ensure_ascii=False, indent=1), encoding="utf-8")
print(h, info.get("followers_count"), len(media), "saved")
