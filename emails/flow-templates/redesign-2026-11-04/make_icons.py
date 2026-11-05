"""Round 2 (4.11 night): draw the 5 trust-strip icons (gold line art on transparent PNG, 2x) and upload them to Klaviyo.
Writes images/icon-*.png and adds their CDN URLs to images.json (keys icon-reviews, icon-consult, icon-diamond, icon-gift, icon-pay)."""
import base64, io, json, math, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
S = 192            # canvas (shown at 48px)
W = 9              # stroke
GOLD = (176, 141, 60, 255)


def canvas():
    im = Image.new("RGBA", (S * 4, S * 4), (0, 0, 0, 0))   # draw 4x, downsample = anti-aliasing
    return im, ImageDraw.Draw(im)


def done(im):
    return im.resize((S, S), Image.LANCZOS)


def P(*xy):
    return [v * 4 for v in xy]


def star():
    im, d = canvas()
    cx, cy, R, r = 96, 100, 70, 29
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = R if i % 2 == 0 else r
        pts.append((4 * (cx + rad * math.cos(a)), 4 * (cy + rad * math.sin(a))))
    d.polygon(pts, outline=GOLD, width=W * 4)
    return done(im)


def calendar():
    im, d = canvas()
    d.rounded_rectangle(P(36, 50, 156, 160), radius=4 * 10, outline=GOLD, width=W * 4)
    d.line(P(36, 84, 156, 84), fill=GOLD, width=W * 4)
    for x in (68, 124):
        d.line(P(x, 34, x, 64), fill=GOLD, width=W * 4)
    # a check mark = booked
    d.line(P(70, 120, 90, 138, 124, 102), fill=GOLD, width=W * 4, joint="curve")
    return done(im)


def diamond():
    im, d = canvas()
    pts = P(48, 70, 72, 42, 120, 42, 144, 70, 96, 156)
    d.polygon(list(zip(pts[::2], pts[1::2])), outline=GOLD, width=W * 4)
    d.line(P(48, 70, 144, 70), fill=GOLD, width=W * 4)
    d.line(P(72, 42, 84, 70, 96, 156), fill=GOLD, width=int(W * 2.6))
    d.line(P(120, 42, 108, 70, 96, 156), fill=GOLD, width=int(W * 2.6))
    d.line(P(84, 70, 96, 42, 108, 70), fill=GOLD, width=int(W * 2.6))
    return done(im)


def gift():
    im, d = canvas()
    d.rectangle(P(42, 78, 150, 104), outline=GOLD, width=W * 4)
    d.rectangle(P(52, 104, 140, 160), outline=GOLD, width=W * 4)
    d.line(P(96, 78, 96, 160), fill=GOLD, width=W * 4)
    # bow
    d.arc(P(56, 40, 98, 82), 150, 400, fill=GOLD, width=W * 4)
    d.arc(P(94, 40, 136, 82), 140, 390, fill=GOLD, width=W * 4)
    return done(im)


def pay():
    im, d = canvas()
    d.rounded_rectangle(P(30, 52, 162, 140), radius=4 * 12, outline=GOLD, width=W * 4)
    d.line(P(30, 78, 162, 78), fill=GOLD, width=W * 4)
    for i, x in enumerate((50, 76, 102)):        # instalment dots
        d.ellipse(P(x - 7, 108, x + 7, 122), fill=GOLD)
    return done(im)


ICONS = {"icon-reviews": star, "icon-consult": calendar, "icon-diamond": diamond, "icon-gift": gift, "icon-pay": pay}

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "images"), exist_ok=True)
    for k, fn in ICONS.items():
        fn().save(os.path.join(HERE, "images", k + ".png"))
    if "--upload" in sys.argv:
        sys.path.insert(0, os.environ["KLPATH"])
        import kl
        imgs = json.load(open(os.path.join(HERE, "images.json"), encoding="utf-8"))
        for k in ICONS:
            raw = open(os.path.join(HERE, "images", k + ".png"), "rb").read()
            uri = "data:image/png;base64," + base64.b64encode(raw).decode()
            s, d = kl.call("POST", "images", {"data": {"type": "image", "attributes": {"import_from_url": uri, "name": "flow-r2-" + k, "hidden": False}}})
            if s not in (200, 201):
                print("FAIL", k, s, str(d)[:300]); sys.exit(1)
            imgs[k] = d["data"]["attributes"]["image_url"]
            print("uploaded", k)
        json.dump(imgs, open(os.path.join(HERE, "images.json"), "w", encoding="utf-8"), indent=1)
