"""Read-only: pull the latest posts of every target account (Instagram Graph API business_discovery)
so next week's engagement round can be written on fresh posts. Never posts, likes, follows or comments.
Token: META_SYSTEM_USER_TOKEN + IG_USER_ID from C:/Users/USER/OneDrive/Desktop/diana-rafael/.env
Run:  python data/refresh_targets.py  ->  data/targets-latest.json"""
import json, sys, urllib.request, urllib.parse, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from comments import ROUND
env = {}
for l in open(r"C:\Users\USER\OneDrive\Desktop\diana-rafael\.env", encoding="utf-8"):
    if "=" in l and not l.startswith("#"):
        k, v = l.strip().split("=", 1); env[k] = v.strip('"')
T, IG = env["META_SYSTEM_USER_TOKEN"], env["IG_USER_ID"]
out = {}
for h in sorted({r[1] for r in ROUND}):
    f = f"business_discovery.username({h}){{followers_count,media.limit(6){{caption,permalink,timestamp,like_count,comments_count,media_product_type}}}}"
    u = f"https://graph.facebook.com/v21.0/{IG}?" + urllib.parse.urlencode({"fields": f, "access_token": T})
    try:
        out[h] = json.load(urllib.request.urlopen(u, timeout=60))["business_discovery"]
    except Exception as e:
        out[h] = {"error": str(e)[:120]}
    print(h, "ok" if "error" not in out[h] else out[h]["error"])
p = pathlib.Path(__file__).parent / "targets-latest.json"
p.write_text(json.dumps({"pulled": datetime.datetime.now().isoformat(timespec="minutes"), "accounts": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print("saved", p)
