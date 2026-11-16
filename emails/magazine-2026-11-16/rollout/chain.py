"""Walk each flow's main path from the entry action -> chain-<tag>.json: ordered email steps with action id, template, subject, preview, status."""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "live-fix-2026-11-15"))
import kl
FLOWS = ["XW6UqR", "VB4v4q", "VWbEYm", "Y6Zunh"]
tag = sys.argv[1] if len(sys.argv) > 1 else "before"
res = {}
for f in FLOWS:
    s, fl = kl.call("GET", f"flows/{f}?additional-fields[flow]=definition")
    d = fl["data"]["attributes"]["definition"]
    acts = {a["id"]: a for a in d["actions"]}
    seen, order, stack = set(), [], [d["entry_action_id"]]
    while stack:
        i = stack.pop(0)
        if not i or i in seen: continue
        seen.add(i); a = acts[i]; L = a.get("links") or {}
        if a["type"] in ("send-email", "ab-test"):
            m = a["data"]["message"] if a["type"] == "send-email" else a["data"]["main_action"]["data"]["message"]
            order.append(dict(aid=i, type=a["type"], status=a["data"].get("status"), tid=m["template_id"], subject=m["subject_line"], preview=m.get("preview_text"),
                              exp=a["data"].get("experiment_status")))
        elif a["type"] == "send-sms":
            order.append(dict(aid=i, type="sms", status=a["data"].get("status")))
        for k in ("next", "next_if_true", "next_if_false"):
            if L.get(k): stack.append(L[k])
    res[f] = dict(name=fl["data"]["attributes"]["name"], status=fl["data"]["attributes"]["status"], steps=order)
    print(f, res[f]["name"], res[f]["status"])
    for n, r in enumerate(order):
        print("  ", r["aid"], r["type"], r["status"], r.get("tid"), "|", r.get("subject"), "|", r.get("preview"), "| exp", r.get("exp"))
json.dump(res, open(f"chain-{tag}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
