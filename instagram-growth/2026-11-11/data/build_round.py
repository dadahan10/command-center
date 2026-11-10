"""Lint the engagement round and render 02-engagement-round.md. Run: python data/build_round.py [pool.json]"""
import re, sys, json, collections, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from comments import ROUND
here = pathlib.Path(__file__).parent.parent
errs = []
days = collections.Counter(r[0] for r in ROUND)
for d in range(1, 8):
    if days[d] != 20: errs.append(f"day {d} has {days[d]} targets")
per_acct = collections.Counter(r[1] for r in ROUND)
for a, n in per_acct.items():
    if n > 4: errs.append(f"{a} used {n} times")
seen = collections.Counter((r[0], r[1]) for r in ROUND)
for k, n in seen.items():
    if n > 1: errs.append(f"{k} twice in one day")
urls = collections.Counter(r[4] for r in ROUND)
for u, n in urls.items():
    if n > 1: errs.append(f"duplicate post {u}")
banned = re.compile(r"^(great post|love this|so true|this |needed this|amazing|obsessed|wow)", re.I)
emoji = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
for r in ROUND:
    c = r[7]
    if "—" in c or "–" in c: errs.append(f"dash in {r[1]}")
    if banned.search(c): errs.append(f"banned opener {r[1]}: {c[:30]}")
    if emoji.search(c): errs.append(f"emoji in {r[1]}")
    if len(re.findall(r"[.!?](\s|$)", c)) > 3: errs.append(f"more than 3 sentences {r[1]}")
    if re.search(r"diana|dianarafael|link in bio|check out|our page|dm us", c, re.I): errs.append(f"pitch in {r[1]}")
if len(sys.argv) > 1:
    pool = {p["url"] for p in json.load(open(sys.argv[1], encoding="utf-8"))}
    for r in ROUND:
        if r[4] not in pool: errs.append(f"url not in verified pool: {r[4]}")
print("LINT:", "PASS" if not errs else "\n".join(errs))
names = {1:"Wed 11.11",2:"Thu 12.11",3:"Fri 13.11",4:"Sat 14.11",5:"Sun 15.11",6:"Mon 16.11",7:"Tue 17.11"}
out = ["# Engagement round, 7 days x 20", "",
 "Every account and post below was checked on 10.11.2026 through the Instagram Graph API (read-only business discovery): the account exists, the post exists, and the comment answers its caption. Follower counts are from that check.", "",
 "**How to run a day (10 minutes):** open the link on your phone, read the post for 5 seconds, paste the comment, like the post. If the account has posted something newer and better, comment there instead with the same idea in your own words. Never paste the same comment twice. Never add a link, our name or \"check out our page\". Days 4 to 7 point at posts that will be 1 to 3 weeks old: the creator still gets the notification, which is the point (the relationship), but the crowd under the post has moved on. To get fresh posts for next week run `python data/refresh_targets.py` (read-only).", "",
 "**Mix per day:** about 8 jewelry and gem creators, 6 bridal and alt-bridal media, 4 jewelers with engaged US audiences, 2 planners or one-liners. No account more than 3 times in the week, never twice on one day.", ""]
for d in range(1, 8):
    out += [f"## Day {d} | {names[d]}", "", "| # | Account | Post | What it is | Comment to paste |", "|---|---|---|---|---|"]
    i = 0
    for r in ROUND:
        if r[0] != d: continue
        i += 1
        f = f"{r[2]/1000:.0f}K" if r[2] < 1_000_000 else f"{r[2]/1e6:.1f}M"
        out.append(f"| {i} | @{r[1]} ({f}) | [{r[3][5:]}]({r[4]}) | {r[5]} | {r[7]} |")
    out.append("")
out += ["## After each round (2 minutes)", "", "- Reply to anyone who answered one of your comments. A reply thread under a big account is where profile taps actually come from.",
 "- If a creator replies or follows back twice in the week, they move to the warm list: next time, a short DM about their work (use the ig-dm skill). Never a pitch in the first message.", ""]
(here / "02-engagement-round.md").write_text("\n".join(out), encoding="utf-8")
print("accounts:", len(per_acct), "targets:", len(ROUND))
