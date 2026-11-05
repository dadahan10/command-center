"""Render out/<tpl>.html with Klaviyo WITHOUT touching the flows: create a throwaway template (not attached to anything),
render it with a real past event context, save out/render-<tpl>.html, delete the throwaway. Usage: python render_preview.py [tpl ...]"""
import json, os, re, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = r"C:\Users\USER\OneDrive\Desktop\CLAUDE CODE PROJECTS\diana-rafael-marketing\connectors\klaviyo\.env"
KEY = re.search(r"KLAVIYO[A-Z_]*KEY\s*=\s*['\"]?([^\s'\"]+)", open(ENV, encoding="utf-8").read()).group(1)
CTX = dict(WtYdde="checkout", VdW7XY="checkout", SNvbQS="checkout", VLjUfd="checkout", WiHGws="checkout", V4FBhc="checkout", TNDw3W="checkout", SyBqNG="checkout",
           U58x8u="cart", UBwjpH="cart", Xzm3N4="cart", Y7JQ5h="cart", WRGJQ3="cart", TPeL6i="cart", UmCymx="cart", XjtgKS="cart",
           WwmdnE="viewed", UDi5wM="viewed", XB8MV8="viewed", QXP4ar="viewed", WHCJdX="placed", Xg2wvc="placed", RCR6Vz="fulfilled",
           V4smfK="delivered", RZYnw2="delivered", TbpdpS="delivered", W9dVNd="delivered", TLpfRY="placed", TLp5wQ=None)


def call(method, path, body=None):
    req = urllib.request.Request("https://a.klaviyo.com/api/" + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Klaviyo-API-Key " + KEY, "revision": "2025-04-15", "accept": "application/json", "content-type": "application/json"})
    try:
        r = urllib.request.urlopen(req)
        raw = r.read()
        return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


for tpl in (sys.argv[1:] or CTX):
    html = open(os.path.join(HERE, "out", tpl + ".html"), encoding="utf-8").read()
    ctx = json.load(open(os.path.join(HERE, "contexts", CTX[tpl] + ".json"), encoding="utf-8")) if CTX[tpl] else {"first_name": "Sarah"}
    s, d = call("POST", "templates", {"data": {"type": "template", "attributes": {"name": f"ZZ preview {tpl} (temp, delete)", "editor_type": "CODE", "html": html}}})
    if s >= 300: print("CREATE FAIL", tpl, s, d); continue
    tid = d["data"]["id"]
    s, r = call("POST", "template-render", {"data": {"type": "template", "attributes": {"id": tid, "context": ctx}}})
    call("DELETE", f"templates/{tid}")
    if s >= 300: print("RENDER FAIL", tpl, s, r); continue
    open(os.path.join(HERE, "out", f"render-{tpl}.html"), "w", encoding="utf-8").write(r["data"]["attributes"]["html"])
    print("ok", tpl)
