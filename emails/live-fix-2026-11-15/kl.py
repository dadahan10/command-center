"""Tiny Klaviyo REST helper (key from diana-rafael-marketing/connectors/klaviyo/.env)."""
import glob, json, os, urllib.request, urllib.error
envp = glob.glob(os.path.expanduser("~/OneDrive/Desktop/CLAUDE CODE PROJECTS/diana-rafael-marketing/connectors/klaviyo/.env"))[0]
KEY = [l.split("=", 1)[1].strip().strip('"') for l in open(envp) if l.startswith("KLAVIYO") and "KEY=" in l][0]
REV = "2026-10-15"
def call(method, path, body=None):
    req = urllib.request.Request("https://a.klaviyo.com/api/" + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Klaviyo-API-Key {KEY}", "revision": REV, "accept": "application/vnd.api+json",
                 "content-type": "application/vnd.api+json"})
    try:
        with urllib.request.urlopen(req) as r:
            t = r.read().decode(); return r.status, (json.loads(t) if t else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:1500]
