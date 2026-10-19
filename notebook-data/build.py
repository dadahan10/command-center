"""Build the notebook: merge chapter parts, apply CSS, stage into the scratchpad dir for publishing.
Usage: python -I build.py <stage_dir>
"""
import json, glob, os, re, shutil, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
stage = sys.argv[1]

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

# 1. chapters = all parts, minus topics Daniel asked not to track as status
SKIP = {"month-closing"}  # shown as a flow (agents.json), not as a status chapter
chapters, seen = [], set()
for p in sorted(glob.glob(os.path.join(HERE, "parts", "part*.json"))):
    for c in load(p):
        if c["id"] in SKIP or c["id"] in seen:
            continue
        seen.add(c["id"])
        chapters.append(c)

extras = load(os.path.join(HERE, "extras.json"))

# 2. management system: recent changes come from the mgmt changelog
mg = extras.get("mgmt_changes", {})
for c in chapters:
    if c["id"] == "management-system" and mg.get("changes"):
        c["recent_changes"] = [f'{x["date"]} — {x["what"]}' for x in mg["changes"]]
        arts = c.setdefault("artifacts", [])
        if mg.get("vercel_url") and not any(a.get("url") == mg["vercel_url"] for a in arts):
            arts.insert(0, {"label": "מערכת הניהול (Vercel)", "url": mg["vercel_url"], "type": "site"})

# 2b. social weekly: next-week plan + message ledger come from the marketing repo (source of truth)
SOCIAL = os.path.join(os.path.dirname(ROOT), "diana-rafael-marketing", "social")
def dmy(s):
    return ".".join(reversed(s.split("-")[1:])) if s and s.count("-") == 2 else (s or "")
LEDGER_ST = {"published": "פורסם", "made": "מוכן, לא פורסם", "scheduled": "בתור"}
for c in chapters:
    if c["id"] != "social-weekly":
        continue
    tables = []
    wp_path, lg_path = os.path.join(SOCIAL, "week-plan.json"), os.path.join(SOCIAL, "ledger.json")
    if os.path.exists(wp_path):
        wp = load(wp_path)
        tables.append({"title": "השבוע הבא" + (f" ({wp['week_of']})" if wp.get("week_of") else ""),
                       "cols": ["מתי", "פלטפורמה", "תכשיט", "Hook / מסר", "כיתוב", "סטטוס"],
                       "rows": [[f'{dmy(x.get("date",""))} {x.get("time","")}'.strip(), x.get("platform", ""), x.get("piece", ""),
                                 x.get("hook", ""), x.get("caption", ""), x.get("status", "ממתין לאישור")] for x in wp.get("items", [])],
                       "empty": wp.get("placeholder") or "יוצג ביום רביעי"})
    if os.path.exists(lg_path):
        lg = sorted(load(lg_path).get("entries", []), key=lambda x: x.get("date", ""), reverse=True)
        tables.append({"title": f"יומן המסרים ({len(lg)})",
                       "note": "כל מה שיצא או הוכן. בודקים כאן לפני כל פוסט חדש, כדי לא לחזור על מסר.",
                       "cols": ["תאריך", "פלטפורמה", "תכשיט", "Hook", "זווית המסר", "מצב"],
                       "rows": [[dmy(x.get("date")), x.get("platform", ""), x.get("piece", ""), x.get("hook", ""),
                                 x.get("message_angle", ""), LEDGER_ST.get(x.get("status"), x.get("status", ""))] for x in lg],
                       "empty": "עוד לא נרשם כלום"})
    c["tables"] = tables

assert len({c["id"] for c in chapters}) == len(chapters)
with open(os.path.join(HERE, "chapters.json"), "w", encoding="utf-8") as f:
    json.dump(chapters, f, ensure_ascii=False, indent=1)

extras["generated"] = datetime.date.today().strftime("%d.%m.%Y")

# 3. page: inject notebook.css into notebook.html
html = open(os.path.join(ROOT, "notebook.html"), encoding="utf-8").read()
css = open(os.path.join(ROOT, "notebook.css"), encoding="utf-8").read()
html = re.sub(r"<style>.*?</style>", lambda m: "<style>" + css + "</style>", html, count=1, flags=re.S)
with open(os.path.join(ROOT, "notebook.html"), "w", encoding="utf-8") as f:
    f.write(html)

# 4. stage
os.makedirs(os.path.join(stage, "data"), exist_ok=True)
shutil.copy(os.path.join(ROOT, "notebook.html"), os.path.join(stage, "notebook.html"))
for name, obj in [("chapters", chapters), ("extras", extras),
                  ("skills", load(os.path.join(HERE, "skills.json"))),
                  ("agents", load(os.path.join(HERE, "agents.json")))]:
    with open(os.path.join(stage, "data", name + ".json"), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)

done = sum(1 for c in chapters if c.get("status") == "done")
office = sum(1 for c in chapters if c.get("office_only"))
print(f"{len(chapters)} chapters ({done} done, {office} office-only) -> {stage}")
