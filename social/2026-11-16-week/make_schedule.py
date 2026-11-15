"""schedule.json for queue_social.py from week-plan.json (week 2026-11-16, batch 2026-11-16-week). Daniel approved 15.11 after fixes.
Times = the plan's times: stories spread morning / evening (IL peaks 10:30-11:00 and 19:00-20:00), feed at 13:00
(reach of 143 past posts, 10.11). Hebrew posts (FB private profile, X, LinkedIn) stay manual, as in every week so far:
the FB Page already gets the EN album/photo at 13:00 and X/LinkedIn are not connected.
  export PYTHONUTF8=1 && python make_schedule.py  -> schedule.json"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
WP = os.path.join(HERE, "..", "..", "..", "diana-rafael-marketing", "social", "week-plan.json")
wp = json.load(io.open(WP, encoding="utf-8"))
week = [w for w in wp["weeks"] if w["week_of"] == "2026-11-16"][0]
out = []
for it in week["items"]:
    when = f'{it["date"]} {it["time"]}'
    p = it["platform"]
    if p == "ig_story":
        out.append({"kind": "instagram_story", "file": os.path.basename(it["video"]), "publish_at": when, "lang": "en"})
    elif p == "ig_carousel":
        out.append({"kind": ["instagram_carousel", "facebook_page_album"],
                    "files": [os.path.basename(t) for t in it["thumbs"]], "caption": it["caption"], "publish_at": when})
    elif p == "ig_post":
        out.append({"kind": ["instagram_post", "facebook_page_photo"], "file": os.path.basename(it["thumbs"][0]),
                    "caption": it["caption"], "publish_at": when})
    # fb_album / fb_post twins are covered by the combined kinds above; HE posts are manual
json.dump(out, io.open(os.path.join(HERE, "schedule.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "rows ->", os.path.join(HERE, "schedule.json"))
