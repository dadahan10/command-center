"""Swap a live flow email onto a new CODE template built from out/<tid>.html (+ optional new subject/preview).
The old template stays untouched (backup/). Usage: python swap.py <action_id> <old_tid> [subject] [preview]"""
import kl, json, sys
aid, old = sys.argv[1], sys.argv[2]
subj = sys.argv[3] if len(sys.argv) > 3 else None
prev = sys.argv[4] if len(sys.argv) > 4 else None
s, a = kl.call("GET", f"flow-actions/{aid}")
assert s == 200, a
dfn = a["data"]["attributes"]["definition"]
json.dump(dfn, open(f"backup/action-{aid}.json", "w", encoding="utf-8"), indent=1)
html = open(f"out/{old}.html", encoding="utf-8").read()
msgname = dfn["data"]["message"]["name"] if dfn["type"] == "send-email" else dfn["data"]["main_action"]["data"]["message"]["name"]
s, t = kl.call("POST", "templates", {"data": {"type": "template", "attributes": {"name": f"LIVE 15.11 | {msgname}", "editor_type": "CODE", "html": html}}})
assert s in (200, 201), t
new = t["data"]["id"]
msg = dfn["data"]["message"] if dfn["type"] == "send-email" else dfn["data"]["main_action"]["data"]["message"]
msg["template_id"] = new
if dfn["type"] == "ab-test":
    for k in ("concluded_experiment_id", "winning_variation_id", "experiment_status"):
        dfn["data"].pop(k, None)
    if dfn["data"].get("current_experiment") is None: dfn["data"].pop("current_experiment", None)
if subj: msg["subject_line"] = subj
if prev: msg["preview_text"] = prev
s, r = kl.call("PATCH", f"flow-actions/{aid}", {"data": {"type": "flow-action", "id": aid, "attributes": {"definition": dfn}}})
print(aid, old, "->", new, s, "" if s == 200 else str(r)[:600])
if s == 200:
    s, chk = kl.call("GET", f"flow-actions/{aid}")
    m = chk["data"]["attributes"]["definition"]["data"]
    m = m.get("message") or m["main_action"]["data"]["message"]
    print("  now:", m["template_id"], "|", m["subject_line"], "|", m["preview_text"], "| status", chk["data"]["attributes"]["definition"]["data"].get("status"))
