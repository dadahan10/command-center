"""Swap every live abandon-flow email action onto its new B&W Issue CODE template (live-fix-2026-11-15/swap.py logic,
backups into rollout/backup/ first: the action definition + the old template's html). Subject + preview text unchanged.
Usage: python swap_all.py [flow ...]"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "live-fix-2026-11-15"))
import kl
PLAN = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf-8"))
BK = os.path.join(HERE, "backup"); os.makedirs(BK, exist_ok=True)
log = []
for fid in (sys.argv[1:] or list(PLAN)):
    for e in PLAN[fid]:
        aid = e["aid"]
        s, a = kl.call("GET", f"flow-actions/{aid}"); assert s == 200, a
        dfn = a["data"]["attributes"]["definition"]
        json.dump(dfn, open(os.path.join(BK, f"action-{fid}-{e['n']}-{aid}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        msg = dfn["data"]["message"] if dfn["type"] == "send-email" else dfn["data"]["main_action"]["data"]["message"]
        old = msg["template_id"]
        s, t = kl.call("GET", f"templates/{old}?fields[template]=html,name")
        if s == 200:
            open(os.path.join(BK, f"template-{fid}-{e['n']}-{old}.html"), "w", encoding="utf-8").write(t["data"]["attributes"]["html"] or "")
        html = open(os.path.join(HERE, "out", e["file"] + ".html"), encoding="utf-8").read()
        s, t = kl.call("POST", "templates", {"data": {"type": "template", "attributes": {
            "name": f"B&W 16.11 | {fid} #{e['n']} {e['family']} | {e['subject'][:60]}", "editor_type": "CODE", "html": html}}})
        assert s in (200, 201), t
        new = t["data"]["id"]
        msg["template_id"] = new
        if dfn["type"] == "ab-test":
            for k in ("concluded_experiment_id", "winning_variation_id", "experiment_status"):
                dfn["data"].pop(k, None)
            if dfn["data"].get("current_experiment") is None:
                dfn["data"].pop("current_experiment", None)
        s, r = kl.call("PATCH", f"flow-actions/{aid}", {"data": {"type": "flow-action", "id": aid, "attributes": {"definition": dfn}}})
        ok = s == 200
        line = dict(flow=fid, n=e["n"], aid=aid, old=old, created=new, status=s, err=None if ok else str(r)[:400])
        if ok:
            s2, chk = kl.call("GET", f"flow-actions/{aid}")
            d2 = chk["data"]["attributes"]["definition"]["data"]
            m2 = d2.get("message") or d2["main_action"]["data"]["message"]
            line.update(now=m2["template_id"], subject=m2["subject_line"], action_status=d2.get("status"))
        print(line); log.append(line)
        time.sleep(0.3)
prev = json.load(open(os.path.join(HERE, "swap-log.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "swap-log.json")) else []
json.dump(prev + log, open(os.path.join(HERE, "swap-log.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
