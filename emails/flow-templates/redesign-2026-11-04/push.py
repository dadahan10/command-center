"""push.py <tpl_id> <html_file> [context.json] : PATCH a Klaviyo template's HTML, then render it with a context and save
out/render-<tpl>.html. Key is read from the marketing connector .env inside kl.py (never printed)."""
import sys, json, os
sys.path.insert(0, os.environ["KLPATH"])
import kl
tid, f = sys.argv[1], sys.argv[2]
ctx = json.load(open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else {"first_name": "Sarah"}
html = open(f, encoding="utf-8").read()
s, d = kl.call("PATCH", f"templates/{tid}", {"data": {"type": "template", "id": tid, "attributes": {"html": html}}})
if s >= 300: print("PATCH FAIL", tid, s, str(d)[:300]); sys.exit(1)
s, d = kl.call("POST", "template-render", {"data": {"type": "template", "attributes": {"id": tid, "context": ctx}}})
if s >= 300: print("RENDER FAIL", tid, s, str(d)[:400]); sys.exit(1)
out = os.path.join(os.path.dirname(f), f"render-{tid}.html")
open(out, "w", encoding="utf-8").write(d["data"]["attributes"]["html"])
print("ok", tid, out)
