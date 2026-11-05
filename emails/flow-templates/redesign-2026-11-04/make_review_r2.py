"""Build emails/review-2026-11-05/index.html: round-2 review page (subjects + desktop/mobile renders) for Daniel's approval."""
import html, json, os
import round2

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "review-2026-11-05")
SUBJ = json.load(open(os.path.join(HERE, "subjects.json"), encoding="utf-8"))

FLOWS = [
    ("checkout", "נטישת קופה", "X6ZfPR · 8 מיילים · טיוטה", ["WtYdde", "VdW7XY", "SNvbQS", "VLjUfd", "WiHGws", "V4FBhc", "TNDw3W", "SyBqNG"], True),
    ("cart", "נטישת עגלה", "VWbEYm · 8 מיילים · טיוטה", ["U58x8u", "UBwjpH", "Xzm3N4", "Y7JQ5h", "WRGJQ3", "TPeL6i", "UmCymx", "XjtgKS"], True),
    ("browse", "נטישת צפייה", "XLpiBU · 4 מיילים · טיוטה", ["WwmdnE", "UDi5wM", "XB8MV8", "QXP4ar"], True),
    ("after", "אחרי רכישה ומשלוח", "VydTk7 · R6tiEk · Y6UjZu · 7 מיילים · טיוטה", ["WHCJdX", "Xg2wvc", "RCR6Vz", "V4smfK", "RZYnw2", "TbpdpS", "W9dVNd"], False),
    ("other", "VIP ו-JEWELVERSARY", "RRcbwY פעיל · XrShek טיוטה", ["TLp5wQ", "TLpfRY"], False),
]
SWAPPED = {"SNvbQS": "הוקדם מ-7/8", "TNDw3W": "נדחה מ-3/8", "UBwjpH": "הוקדם מ-7/8", "UmCymx": "נדחה מ-2/8"}

CSS = """
:root{--bg:#f3efe8;--fg:#1f1b16;--mut:#6a6155;--card:#fffdf9;--line:#e3dacb;--gold:#8f6f24;--chip:#efe5d0;
--serif:'Cormorant Garamond',Georgia,serif;--sans:'Assistant','Segoe UI',Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#151311;--fg:#eee6d8;--mut:#a59a89;--card:#1e1b18;--line:#34302a;--gold:#d4b26a;--chip:#2b261f;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#151311;--fg:#eee6d8;--mut:#a59a89;--card:#1e1b18;--line:#34302a;--gold:#d4b26a;--chip:#2b261f;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:16px/1.55 var(--sans);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:1440px;margin:0 auto;padding-block:28px 80px}
h1{font:600 40px/1.1 var(--serif);margin:0 0 6px;text-wrap:balance}
.sub{color:var(--mut);margin:0 0 22px}
.changes{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:0 0 10px;padding:0;list-style:none}
.changes li{background:var(--card);border:1px solid var(--line);padding:12px 14px;border-radius:6px}
.changes b{display:block;font:600 20px var(--serif);color:var(--gold)}
.note{color:var(--mut);font-size:14px;max-width:80ch}
nav{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0}
nav a{color:var(--fg);background:var(--chip);padding:6px 12px;border-radius:99px;text-decoration:none;font-size:14px}
h2{font:600 30px var(--serif);margin:44px 0 2px}
.meta{color:var(--mut);font-size:14px;margin:0 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:18px}
article{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:14px;min-width:0}
.top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.slot{font-weight:700;color:var(--gold);font-variant-numeric:tabular-nums}
.tag{font-size:12px;background:var(--chip);padding:2px 8px;border-radius:99px;white-space:nowrap}
.tag.r2{color:var(--gold)}
.subj{direction:ltr;text-align:left;font:600 19px/1.3 var(--serif);margin:8px 0 2px}
.pre{direction:ltr;text-align:left;color:var(--mut);font-size:13px;margin:0 0 10px}
.shots{display:flex;gap:10px;align-items:flex-start;max-height:760px;overflow:auto;direction:ltr;border-top:1px solid var(--line);padding-top:10px}
.shots img{display:block;width:290px;max-width:100%;border:1px solid var(--line)}
.shots img.m{width:128px}
a:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
@media (max-width:520px){h1{font-size:32px}.shots img.m{display:none}.shots img{width:100%}}
"""


def card(i, tid, r2):
    s = SUBJ.get(tid, {})
    subj = round2.SUBJECT_OVERRIDE.get(tid, s.get("subject") or "")
    pre = s.get("preview") or ""
    tags = ""
    if tid in SWAPPED:
        tags += f'<span class="tag r2">{SWAPPED[tid]}</span> '
    tags += f'<span class="tag{" r2" if r2 else ""}">{"סבב 2" if r2 else "לוגו גדול בלבד"}</span>'
    return (f'<article><div class="top"><span class="slot">{i}</span><span>{tags}</span></div>'
            f'<p class="subj">{html.escape(subj)}</p>' + (f'<p class="pre">{html.escape(pre)}</p>' if pre else "") +
            f'<div class="shots"><a href="shots/render-{tid}-d.jpg" target="_blank"><img loading="lazy" src="shots/render-{tid}-d.jpg" alt="{tid} דסקטופ"></a>'
            f'<a href="shots/render-{tid}-m.jpg" target="_blank"><img loading="lazy" class="m" src="shots/render-{tid}-m.jpg" alt="{tid} מובייל"></a></div></article>')


def main():
    nav, body = [], []
    for key, name, meta, ids, r2 in FLOWS:
        nav.append(f'<a href="#{key}">{name}</a>')
        body.append(f'<section id="{key}"><h2>{name}</h2><p class="meta">{meta}</p><div class="grid">')
        body += [card(("VIP", "JEWELVERSARY")[n - 1] if key == "other" else f"{n}/{len(ids)}", t, r2) for n, t in enumerate(ids, 1)]
        body.append("</div></section>")
    page = f"""<title>מיילי פלואו סבב 2</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Cormorant+Garamond:wght@500;600&display=swap">
<style>{CSS}</style>
<main dir="rtl">
<h1>מיילי פלואו — סבב 2</h1>
<p class="sub">29 מיילים, מרונדרים ע"י Klaviyo עם אירוע אמיתי (Sarah). שום דבר לא נדחף ל-Klaviyo — הכול מחכה לאישור שלך.</p>
<ul class="changes">
<li><b>פחות טקסט</b>כותרת + שורה-שתיים בכל 20 מיילי המכירה</li>
<li><b>כפתורים למעלה</b>מיד מתחת לכותרת, שניים בכל מייל</li>
<li><b>המתנה נראית</b>העגילים מופיעים בכל מייל שמזכיר אותם; במיילי המתנה: "שחור או לבן?"</li>
<li><b>שורת אמון</b>530+ ביקורות · שיחה עם דניאל · מתנה · תשלומים · יהלומים טבעיים (אחרון)</li>
<li><b>לוגו גדול יותר</b>בכל 29 המיילים</li>
</ul>
<p class="note">סדר בפלואו: מייל "יהלום טבעי" עבר לסוף (7/8) ומייל "15 דקות עם דניאל" הוקדם — בקופה (3/8) ובעגלה (2/8). שורות הנושא עוברות איתם. מיילי אחרי-רכישה, VIP ו-JEWELVERSARY לא שוכתבו — רק הלוגו גדל.</p>
<nav>{''.join(nav)}</nav>
{''.join(body)}
</main>"""
    open(os.path.join(R, "index.html"), "w", encoding="utf-8").write(page)
    print("wrote", os.path.join(R, "index.html"))


if __name__ == "__main__":
    main()
