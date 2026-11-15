"""Writes week 16-22.11.2026 into diana-rafael-marketing/social/week-plan.json (+ planned ledger rows). Idempotent.
Status of every item: "לאישור דניאל". Nothing goes to social_queue before Daniel approves.
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.join(HERE, "..", "..", "..", "diana-rafael-marketing", "social")
B = "2026-11-16-week"
M0 = "Musinova - Minimal Underscore Piano Pulse, Drumless (Pixabay Content License, not Content-ID registered)"
M1 = "Musinova - Minimal Underscore Piano Pulse (Pixabay Content License, not Content-ID registered)"
ST = "מתוקן — מאושר לפרסום"
cap = io.open(os.path.join(HERE, "captions.md"), encoding="utf-8").read()
he = io.open(os.path.join(HERE, "פוסטים-עברית-FB-X-LinkedIn.md"), encoding="utf-8").read()
priv = io.open(os.path.join(HERE, "פייסבוק-פרטי-עברית.txt"), encoding="utf-8").read()


def section(text, head, stop):
    i = text.index(head) + len(head)
    j = text.find(stop, i)
    return text[i:j if j > 0 else None].strip()


def en(day):
    return section(cap, f"### {day}", "\n### ").split("\n", 1)[1].split("\n## ")[0].strip()


def he_fb(day):
    s = section(he, f"## {day}", "\n## ")
    return section(s, "### פייסבוק", "\n### ")


def he_priv(day):
    s = section(priv, f"=== {day}", "\n=== ")
    return s.split("\n", 1)[1].strip()


def story(i, date, time, name, piece, hook, angle, music):
    return {"id": f"w1116-{name}", "batch": B, "date": date, "time": time, "platform": "ig_story", "format": "9:16",
            "piece": piece, "hook": hook, "angle": angle, "music": music,
            "thumbs": [f"{B}/{name}.jpg", f"{B}/{name}-f1.jpg", f"{B}/{name}-f2.jpg"], "images": [], "status": ST,
            "caption": "", "video": f"{B}/{name}.mp4"}


def feed(date, time, name, n, piece, hook, angle, caption, platforms=("ig_carousel", "fb_album")):
    th = [f"{B}/{name}-{k}.jpg" for k in range(1, n + 1)] if n > 1 else [f"{B}/{name}.jpg"]
    out = []
    for p in platforms:
        out.append({"id": f"w1116-{name}" + ("-fb" if p.startswith("fb") else ""), "batch": B, "date": date, "time": time,
                    "platform": p, "format": "4:5", "piece": piece, "hook": hook, "angle": angle, "music": "",
                    "thumbs": th, "images": [], "status": ST, "caption": caption})
    return out


def hepost(date, time, name, img, piece, hook, angle, caption, private):
    return {"id": f"w1116-{name}", "batch": B, "date": date, "time": time, "platform": "fb_post", "format": "4:5",
            "piece": piece, "hook": hook, "angle": angle, "music": "", "thumbs": [f"{B}/{img}"], "images": [],
            "status": ST, "caption": caption, "fb_caption": "לפרופיל הפרטי של דניאל (בגוף ראשון):\n\n" + private}


items = [
    story(1, "2026-11-16", "11:00", "mon-16-studs", "Free 1 ct black diamond studs (render), macro pull-back",
          "Over $2,000? / THE STUDS ARE ON US.", "מבצע: עגילים במתנה מעל $2,000 (הוק: אור שעובר על פאות היהלום מהפריים הראשון)", M0),
    story(2, "2026-11-16", "19:00", "mon-16-earring", "2026 DROP: black pear sunburst earring, worn — one photo, macro on the stone -> her ear",
          "It doesn't sparkle. / IT REFLECTS. -> Light, held / IN THE DARK. · for her, this season, 15% off",
          "תיקון 15.11: רעיון אחד, צילום אחד. היהלום השחור לא זורק אש, הוא מחזיר אור כמו מראה (ברק ועומק); השתקפות עוברת על האבן ואז נסוגים לאוזן. בלי פוטאג' של יהלום לבן ובלי שורת-מפרט", M1),
    *feed("2026-11-16", "13:00", "mon-16-post", 4, "Carousel: studs + Centauri, Selkie, Spindle (all over $2,000)",
          "The studs are on us.", "פיד: שתי מתנות בקופסה אחת, בלי מחירים בפיד", en("Mon 16.11")),
    hepost("2026-11-16", "13:00", "he-mon-16", "mon-16-post-2.jpg", "פוסט עברית: עונת המתנות",
           "עונת המתנות התחילה אצלנו", "15% על הכול + עגילים במתנה בהזמנות גדולות, בלי מחירים", he_fb("שני 16.11"), he_priv("שני 16.11")),
    story(3, "2026-11-17", "10:30", "tue-17-gifts", "Six pieces in one ink world: Spindle, Hyades, Cor Caroli, Pleiades, Polaris, Umbra",
          "Gift season. / ALREADY 15% OFF. -> Every piece on the site.", "הרבה תכשיטים יחד (הדפוס החזק שלנו), קצב חיתוכים מהפריים הראשון", M0),
    story(4, "2026-11-17", "20:00", "tue-17-centauri", "Centauri R513 (yellow) cutout in the night sky, price card",
          "$2,600 struck -> $2,210 · ALREADY 15% OFF -> CENTAURI · over $2,000: free studs included",
          "מבצע: מחיר המבצע 15% עם המחיר המקורי מחוק (עבר משני לשלישי; רקע שמי לילה במקום שחור)", M1),
    story(5, "2026-11-18", "11:00", "wed-18-eternity", "2026 DROP: white cushion eternity band, macro pull-back",
          "One stone / AT A TIME. -> Made to order. Still 15% off.", "עבודת יד + המבצע (לא מקצרים את העבודה, רק את המחיר)", M0),
    story(6, "2026-11-18", "19:30", "wed-18-returning", "2026 DROP: black cushion ring + black pavé bands in the box",
          "Ordered from us before? -> 25% OFF. That's your total. Use the email you ordered with.", "מבצע: קונים חוזרים 25% בסך הכול", M1),
    *feed("2026-11-18", "13:00", "wed-18-post", 3, "Carousel: Hyades, Noir Eclipse, Umbra (night sky)",
          "15% off. Every piece.", "פיד: מחיר המבצע על כל האתר + קונים חוזרים בכיתוב", en("Wed 18.11")),
    hepost("2026-11-18", "13:00", "he-wed-18", "wed-18-post-1.jpg", "פוסט עברית: יהלום אחד בכל פעם",
           "שום דבר לא מתקצר בגלל מבצע", "עבודת יד + 15% + קונים חוזרים 25%", he_fb("רביעי 18.11"), he_priv("רביעי 18.11")),
    story(7, "2026-11-19", "11:00", "thu-19-zodiac", "Four rings, four elements: Cor Caroli, Pleiades, Polaris, Selkie (white)",
          "Fire, earth, / AIR OR WATER? -> Tell us her sign. We'll tell you her ring.", "עונת ההצעות: טבעת לפי המזל (תומך במייל של חמישי)", M1),
    story(8, "2026-11-19", "20:00", "thu-19-algol", "Algol R541 (yellow): the stone fills the frame, pull back",
          "ALGOL -> $3,600 struck -> $3,060 + FREE STUDS IN THE BOX", "מבצע: 15% + עגילים (הוק: האבן ממלאת את המסך)", M0),
    story(9, "2026-11-20", "11:00", "fri-20-pendant", "Noir Eclipse pendant swings in on its chain (floating display)",
          "For under the tree: / SOMETHING THAT STAYS. -> $1,400 struck -> $1,190", "מתנה לחג + מחיר מבצע (תנועת מטוטלת מהפריים הראשון)", M1),
    story(9.5, "2026-11-20", "14:00", "fri-20-bench", "2026 DROP: match cut — loose stones laid out -> the starburst in the vise -> APPROVED on-hand render (Algol, rose gold)",
          "Some pieces take WEEKS / to look EFFORTLESS. -> MADE AT OUR BENCH · Message us to make yours.",
          "הריל מ-12.11 שדניאל השאיר + תמונת סיום: הדמיה על יד שאושרה (R541 Algol, 21.10 approved)", M0),
    story(10, "2026-11-20", "18:30", "fri-20-halo", "2026 DROP: white diamond halo ring in its box, macro pull-back",
          "A white diamond / FOR THE HOLIDAYS. -> 15% off already.", "לא רק יהלומים שחורים: לבן לחג + המבצע", M0),
    story(11, "2026-11-21", "20:00", "sat-21-review", "2026 DROP: white marquise ring + verbatim review",
          "550+ REVIEWS. -> “The ring is beautiful, my fiancee loves it. Daniel was very helpful when I had questions.”",
          "הוכחה חברתית (550+, ציטוט מילה במילה); בלי שורת מבצע כדי שהטקסט לא יעלה על הטבעת", M1),
    story(12, "2026-11-22", "11:00", "sun-22-bf", "Night sky + 30% reveal, then six black-diamond pieces rise together (Centauri, Hyades, Cor Caroli, Selkie, Spindle, Umbra)",
          "Black Friday / 30% / OFF EVERYTHING -> From Friday, November 27 through January.",
          "טיזר בלאק פריידי: 30% על הכול מ-27.11 עד סוף ינואר, בלי קוד. תיקון 15.11: שמי לילה + הרבה תכשיטים יחד במקום פוטאג' של יהלום לבן על רקע כהה", M0),
    story(13, "2026-11-22", "19:00", "sun-22-all", "2026 DROP: black emerald-cut ring in its box",
          "Engagement rings. Bands. Earrings. Pendants. / ALL OF IT. -> 30% off from Nov 27 through January.",
          "טיזר בלאק פריידי 2: מה נכלל (הכול) + עד אז 15%", M1),
    *feed("2026-11-22", "13:00", "sun-22-post", 1, "Single image: black emerald-cut ring in its box + 30% announcement",
          "30% off everything. From Black Friday, through January.", "פיד: הכרזת הבלאק פריידי", en("Sun 22.11"),
          platforms=("ig_post", "fb_post")),
    hepost("2026-11-22", "13:00", "he-sun-22", "sun-22-post.jpg", "פוסט עברית: הכרזת הבלאק פריידי",
           "ביום שישי, 27 בנובמבר, מתחיל אצלנו הבלאק פריידי", "30% על הכול עד סוף ינואר, בלי קוד", he_fb("ראשון 22.11"), he_priv("ראשון 22.11")),
]

# 15.11: queued (queue_social.py --batch 2026-11-16-week, 20 rows); HE posts stay manual
for it in items:
    if it["id"].startswith("w1116-he-"):
        it["note"] = "ידני: פייסבוק פרטי / X / לינקדאין (לא בתור Meta)"
    else:
        it["status"] = "בתור"
wp_path = os.path.join(SOC, "week-plan.json")
wp = json.load(io.open(wp_path, encoding="utf-8"))
for w in wp["weeks"]:
    if w["week_of"] == "2026-11-15":
        keep, moved = [], []
        for it in w.get("items", []):
            if it["id"] in ("w1115-gift-1-v2", "w1115-fri-20-bench-v2"):
                it = dict(it, status="superseded", reason="15.11: replaced in the fixed promotions week (gift-1 -> mon-16-earring, one idea; bench -> fri-20-bench with an on-hand closing image)")
                moved.append(it)
            else:
                keep.append(it)
        w["items"] = keep
        w.setdefault("superseded", []).extend([m for m in moved if m["id"] not in {x["id"] for x in w.get("superseded", [])}])
wp["weeks"] = [w for w in wp["weeks"] if w["week_of"] != "2026-11-16"]
wp["weeks"].append({"week_of": "2026-11-16",
                    "label": "שבוע המבצעים 16–22.11 (נבנה 15.11, תוקן 15.11 לפי דניאל: עגיל שני = רעיון אחד של ברק ועומק, שמי לילה במקום רקע שחור, Algol נחתך מחדש, ריל שולחן העבודה עם תמונת סיום על יד): 13 סטוריז, 3 פוסטים לפיד, 3 פוסטים בעברית. המבצעים במרכז: 15% על הכול, עגילים במתנה מעל $2,000, קונים חוזרים 25%, וטיזר בלאק פריידי 30% מ-22.11. בסגנון הדוגמאות מ-12.11: הוק בשנייה הראשונה, Champie, צילומים אמיתיים ערוכים, בלי AI",
                    "approved": "מתוקן — מאושר לפרסום (דניאל 15.11) · בתור batch 2026-11-16-week", "items": items})
wp["next_placeholder"] = "השבוע שאחרי (23–29.11, בלאק פריידי + עולם החורף) יוצג ביום רביעי 18.11"
json.dump(wp, io.open(wp_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

lg_path = os.path.join(SOC, "ledger.json")
lg = json.load(io.open(lg_path, encoding="utf-8"))
lg["entries"] = [e for e in lg["entries"] if not str(e.get("asset", "")).startswith(B + "/")]
for it in items:
    if it["platform"] in ("fb_album",) or it["id"].endswith("-fb"):
        continue
    plat = {"ig_story": "Instagram story (EN)", "ig_carousel": "Instagram carousel + Facebook album",
            "ig_post": "Instagram post + Facebook post", "fb_post": "Facebook post (HE) + X + LinkedIn"}[it["platform"]]
    lg["entries"].append({"date": it["date"], "platform": plat, "piece": it["piece"], "hook": it["hook"],
                          "message_angle": it["angle"], "asset": B + "/" + it["thumbs"][0].split("/")[-1], "status": "planned"})
json.dump(lg, io.open(lg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(items), "items")
