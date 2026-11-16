"""Snapshot the live state of the 4 abandon flows (actions, template ids, subjects, status) -> state-<tag>.json"""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "live-fix-2026-11-15"))
import kl
FLOWS = ["XW6UqR", "VB4v4q", "VWbEYm", "Y6Zunh"]
tag = sys.argv[1] if len(sys.argv) > 1 else "before"
out = {}
for f in FLOWS:
    s, fl = kl.call("GET", f"flows/{f}")
    s, acts = kl.call("GET", f"flows/{f}/flow-actions?page[size]=50")
    rows = []
    for a in acts["data"]:
        aid = a["id"]
        d = a["attributes"]["definition"]
        t = d["type"]
        m = None
        if t == "send-email": m = d["data"]["message"]
        elif t == "ab-test": m = d["data"]["main_action"]["data"]["message"]
        rows.append(dict(aid=aid, type=t, status=d["data"].get("status") if isinstance(d.get("data"), dict) else None,
                         tid=m.get("template_id") if m else None, subject=m.get("subject_line") if m else None,
                         preview=m.get("preview_text") if m else None, links=d.get("links")))
    out[f] = dict(name=fl["data"]["attributes"]["name"], status=fl["data"]["attributes"]["status"], trigger=fl["data"]["attributes"].get("trigger_type"), actions=rows)
json.dump(out, open(f"state-{tag}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for f, v in out.items():
    print(f, v["name"], v["status"])
    for r in v["actions"]:
        if r["type"] in ("send-email", "ab-test"):
            print("  ", r["aid"], r["type"], r["status"], r["tid"], "|", r["subject"], "|", r["links"])
