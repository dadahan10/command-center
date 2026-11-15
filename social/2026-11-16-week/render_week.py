"""Social week Mon 16.11 - Sun 22.11.2026 — promotions week (Daniel 15.11: "we're in money time").

Recipe = the 12.11 samples (../samples-2026-11-12/render.py), reused through import:
  hook in the first second (motion from frame 0), Champie Light/Bold duality >=40px, never on the jewel,
  IG safe zones (top 260 / bottom 340 free), real photos / real catalog renders only (no AI jewelry),
  H.264 yuv420p 1080x1920 30fps + faststart (plays in the notebook).
Promotions used are the ones live on 15.11 (verified in Shopify): 15% sale price with compare-at strike,
free black diamond studs over $2,000 (manual), returning buyers 25% total, 30% off everything from 27.11.
No Archive mention (not before 27.11), no fake deadlines, no stacking language.

usage: python render_week.py [name ...]     (default: all stories + feed images)
"""
import importlib.util, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("R", os.path.join(HERE, "..", "samples-2026-11-12", "render.py"))
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
R.OUT = HERE
W, H, FPS = R.W, R.H, R.FPS
INK, SAND, CREAM = R.INK, R.SAND, R.CREAM
GOLD = (201, 168, 76)
SRC = os.path.join(HERE, "src")
DROP = R.DROP
MUSIC_DIR = os.path.dirname(R.MUSIC)
TRACKS = [R.MUSIC, os.path.join(MUSIC_DIR, "musinova-minimal-underscore-piano-pulse-518251.mp3")]
STUDS = os.path.join(HERE, "..", "..", "emails", "flow-templates", "redesign-2026-11-04", "images", "studs.jpg")
seg, ease, eout, comp, glint = R.seg, R.ease, R.eout, R.comp, R.glint
sys.path.insert(0, HERE)
from sky import Sky, plate  # noqa: E402  15.11 fix: night-sky world instead of flat black (Daniel)

_SKY = {}


def skybg(t, T, seed=7, cy=.5, amt=.10):
    """the night-sky world, drifting slowly (the world moves, the jewel stays), with a soft warm halo behind the jewel."""
    if seed not in _SKY:
        _SKY[seed] = (Sky("story", seed=seed), R.glow_bg(color=(0, 0, 0), glow=SAND, cy=cy, amt=amt))
    sk, halo = _SKY[seed]
    return sk.frame(t, T) + halo


def cut(name):
    clean = os.path.join(SRC, name + "-cut-clean.png")   # hand-checked re-cut (15.11: Algol leftover)
    im = Image.open(clean if os.path.exists(clean) else os.path.join(SRC, name + "-cut.png")).convert("RGBA")
    a = np.asarray(im.split()[3])
    # keep only the main blob (drops the stray reflection rembg keeps under some renders)
    from scipy import ndimage
    lab, n = ndimage.label(a > 40)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * 0.04])
        arr = np.asarray(im).copy()
        arr[..., 3] = np.where(keep, arr[..., 3], 0)
        im = Image.fromarray(arr)
    arr = np.asarray(im).copy()
    arr[..., 3] = np.where(arr[..., 3] < 14, 0, arr[..., 3])   # faint rembg haze would inflate the bbox
    im = Image.fromarray(arr)
    bb = Image.fromarray((arr[..., 3] > 30).astype(np.uint8) * 255).getbbox()
    return im.crop(bb)


def photo(fname):
    return ImageOps.exif_transpose(Image.open(os.path.join(DROP, fname))).convert("RGB")


CORM = os.path.join(HERE, "..", "..", "..", "remnant-launch", "q4", "banner", "_src", "fonts", "CormorantGaramond.ttf")
_fc = {}


def dfont(wgt, size):
    """Champie (trial) has watermark glyphs for digits -> digits fall back to Cormorant Garamond, same weight feel."""
    k = (wgt, size)
    if k not in _fc:
        f = ImageFont.truetype(CORM, int(size * 1.12))
        f.set_variation_by_name({"LIGHT": "Regular", "MEDIUM": "SemiBold", "BOLD": "Bold"}[wgt])
        _fc[k] = f
    return _fc[k]


def text_layer(lines, alpha_fn, t):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    for (txt, wgt, size, col, y, track, t_in) in lines:
        p = eout(seg(t, t_in, t_in + .45)) * alpha_fn
        if p <= 0:
            continue
        f = R.font(wgt, size); fd = dfont(wgt, size)
        fonts = [fd if c.isdigit() else f for c in txt]
        widths = [d.textlength(c, font=ff) for c, ff in zip(txt, fonts)]
        x = (W - sum(widths) - track * (len(txt) - 1)) / 2
        yy = y + (1 - p) * 26
        for c, cw, ff in zip(txt, widths, fonts):
            dy = -size * .10 if ff is fd else 0
            d.text((x, yy + dy), c, font=ff, fill=col + (int(255 * p),))
            x += cw + track
    return L


def text(lines, t, a=1.0):
    # IG safe zone: keep text clear of the reply bar (Daniel 12.11: IG safe zones)
    # the whole bottom block moves up together so the last line starts at <=1560 (no overlaps)
    over = max([y for (_, _, _, _, y, _, _) in lines] + [0]) - 1560
    if over > 0:
        lines = [(tx, w, sz, col, (y - over if y > 1300 else y), tr, t0) for (tx, w, sz, col, y, tr, t0) in lines]
    return text_layer(lines, a, t)


def strike_layer(cx, cy, width, p, color=GOLD, thick=7):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if p > 0:
        d = ImageDraw.Draw(L)
        x0 = cx - width / 2
        d.line([(x0, cy), (x0 + width * min(p, 1), cy - 6 * min(p, 1))], fill=color + (255,), width=thick)
    return L


def text_width(txt, wgt, size, track):
    f = R.font(wgt, size); fd = dfont(wgt, size)
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    return sum(d.textlength(c, font=fd if c.isdigit() else f) for c in txt) + track * (len(txt) - 1)


def scrim(top=520, bottom=1150, amt=.82):
    yy = np.arange(H)[:, None, None]
    return np.clip((top - yy) / (top - 80), 0, 1) ** 1.3 * amt + np.clip((yy - bottom) / 480, 0, 1) ** 1.3 * amt


def run(name, frames, n, track=0):
    R.MUSIC = TRACKS[track % 2]
    R.encode(name, frames(), n)


# ============================================================ MON 16 — free studs over $2,000
def mon_studs():
    T = 7.0; n = int(T * FPS)
    src = R.grade(Image.open(STUDS).convert("RGB"), warm=1.02, sat=1.0, con=1.08, bri=.95)
    vig = R.vignette(.5)
    yy = np.arange(H)[:, None]
    # band of the studs photo, feathered top/bottom so it sits inside the ink world
    def band(scale, cx_off):
        w = int(1400 * scale); h = int(1000 * scale)
        im = src.resize((w, h), Image.LANCZOS)
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        x = int(W / 2 - w / 2 + cx_off); y = int(980 - h / 2)
        mask = Image.new("L", (w, h), 255)
        m = np.asarray(mask, float)
        fy = np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / (h * .18), 0, 1)[:, None]
        fx = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / (w * .10), 0, 1)[None, :]
        im.putalpha(Image.fromarray((m * fy * fx).astype(np.uint8)))
        L.paste(im, (x, y), im)
        return L, (x, y, w, h)

    def frames():
        for i in range(n):
            t = i / FPS
            k = ease(seg(t, 0, 1.6))
            s = 2.1 - (2.1 - .95) * k + .04 * seg(t, 1.6, T)          # tight on the left stud's facets -> pull back
            off = (1 - k) * 380                                         # start centred on the left stud
            L, (x, y, w, h) = band(s, off)
            base = R.comp(skybg(t, T, 3), L)
            # light sweep over the stones (hook at frame 0, again at 4.2 s)
            a = np.zeros((H, W)); a[max(0, y):min(H, y + h), max(0, x):min(W, x + w)] = 1
            base = base + (glint(a, t, -.1, .9, 160, .35) + glint(a, t, 4.2, 1.1, 160, .28))[..., None] * 255
            base = base * vig
            lay = text([
                ("Over $2,000?", "LIGHT", 78, CREAM, 300, 2, .9),
                ("THE STUDS", "BOLD", 120, SAND, 400, 6, 1.25),
                ("ARE ON US.", "BOLD", 120, SAND, 526, 6, 1.45),
                ("Black diamond studs, free", "LIGHT", 56, CREAM, 1420, 1, 2.6),
                ("with every order over $2,000.", "LIGHT", 56, CREAM, 1490, 1, 2.75),
                ("WE ADD THEM TO THE BOX BY HAND", "MEDIUM", 40, SAND, 1590, 6, 3.6),
            ], t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    run("mon-16-studs", frames, n, 0)


# ============================================================ price card (15% sale, real compare-at)
def price_card(name, cutname, old, new, title, sub, extra=None, track=1):
    T = 7.5; n = int(T * FPS)
    c = cut(cutname)
    c = R.grade(c.convert("RGB"), warm=1.02, sat=1.04, con=1.08, bri=1.03).convert("RGBA")
    c.putalpha(cut(cutname).split()[3])
    s_fit = 820 / max(c.width, c.height * .9)
    vig = R.vignette(.5)
    wo = text_width(old, "LIGHT", 150, 3)

    def frames():
        for i in range(n):
            t = i / FPS
            mv = ease(seg(t, 1.5, 2.3))                   # prices travel up, ring arrives
            bg = skybg(t, T, 5, .52, .12)
            if t < 1.5:
                base = bg.copy()
                al = np.zeros((H, W))
            else:
                k = ease(seg(t, 1.5, 3.0))
                sc = s_fit * (1.25 - .25 * k)
                blur = (1 - seg(t, 1.5, 2.2)) * 10
                base, al = R.paste_cut(bg, c, W / 2, 1000 - 8 * math.sin(t * 1.2), sc, blur)
                base = base + glint(al, t, 3.6, 1.0)[..., None] * 255
            base = base * vig
            y_old = 640 - 330 * mv; y_new = 820 - 360 * mv
            sz_o = int(150 - 50 * mv); sz_n = int(190 - 70 * mv)
            lines = [(old, "LIGHT", sz_o, (150, 140, 128), y_old, 3, -1),
                     (new, "BOLD", sz_n, SAND, y_new, 4, .55)]
            if t > 1.9:
                lines += [("ALREADY 15% OFF", "MEDIUM", 44, CREAM, 610, 8, 1.9)]
            lines += [(title, "BOLD", 70, CREAM, 1440, 6, 3.0), (sub, "LIGHT", 52, CREAM, 1528, 1, 3.2)]
            if extra:
                lines += [(extra, "MEDIUM", 40, SAND, 1612, 5, 4.0)]
            lay = text(lines, t)
            ws = wo * (sz_o / 150)
            st = strike_layer(W / 2, y_old + sz_o * .62, ws + 30, ease(seg(t, .12, .7)))
            out = comp(comp(base, st), lay)
            yield np.clip(out, 0, 255).astype(np.uint8)
    run(name, frames, n, track)


# ============================================================ many jewels, one ink world
def many(name, cuts, top, bottom, track=0):
    T = 7.5; n = int(T * FPS)
    cs = []
    for cn in cuts:
        c = cut(cn)
        g = R.grade(c.convert("RGB"), warm=1.02, sat=1.03, con=1.08, bri=1.03).convert("RGBA"); g.putalpha(c.split()[3])
        cs.append(g)
    vig = R.vignette(.5)
    beat = .42
    cols, rows = 2, 3
    cell_w, cell_h = 430, 300
    gx = [W / 2 - 230, W / 2 + 230]; gy = [760, 1030, 1300]

    def frames():
        for i in range(n):
            t = i / FPS
            base = skybg(t, T, 11)
            if t < beat * len(cs):
                j = int(t / beat); tt = t - j * beat
                c = cs[j]; s = 780 / max(c.width, c.height)
                sc = s * (1.08 - .08 * eout(tt / beat))
                base, al = R.paste_cut(base, c, W / 2, 1000, sc)
                fl = 1 - seg(tt, 0, .09)
                base = base * (1 - .35 * fl) + 255 * .35 * fl * (j > 0)
            else:
                for j, c in enumerate(cs):
                    p = eout(seg(t, beat * len(cs) + j * .08, beat * len(cs) + j * .08 + .45))
                    if p <= 0:
                        continue
                    s = min(cell_w / c.width, cell_h / c.height) * (.9 + .1 * p)
                    x, y = gx[j % 2], gy[j // 2] + (1 - p) * 40
                    base, al = R.paste_cut(base, c, x, y, s, shadow=True)
            base = base * vig
            lay = text(top + bottom, t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    run(name, frames, n, track)


# ============================================================ real photo, log-zoom between two windows
def push(name, fname, A, B, lines, T=7.0, veil=(CREAM, .55), warm=1.03, track=0, sharpen=True, ink_scrim=False):
    n = int(T * FPS)
    src = R.grade(photo(fname), warm=warm, sat=1.04, con=1.10, bri=1.0)
    if sharpen:
        src = src.filter(ImageFilter.UnsharpMask(2, 70, 3))
    vig = R.vignette(.45)
    SC = scrim() if ink_scrim else None

    def frames():
        for i in range(n):
            t = i / FPS
            k = ease(seg(t, 0, T * .62))
            w = A["w"] * (B["w"] / A["w"]) ** k
            cx = A["cx"] + (B["cx"] - A["cx"]) * k; cy = A["cy"] + (B["cy"] - A["cy"]) * k
            base = np.asarray(R.cover_crop(src, cx, cy, w), float)
            if ink_scrim:
                base = base * (1 - SC) + np.array(INK, float) * SC
            else:
                y = np.arange(H)[:, None, None]
                v = np.clip((360 - y) / 360, 0, 1) * veil[1] + np.clip((y - 1300) / 420, 0, 1) * (veil[1] + .05)
                base = base * (1 - v) + np.array(veil[0], float) * v
            base = base * vig
            lay = text(lines, t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    run(name, frames, n, track)


# ============================================================ THU 19 — zodiac, four elements
def zodiac():
    T = 8.0; n = int(T * FPS)
    items = [("FIRE", "corcaroli-r34"), ("EARTH", "pleiades-y"), ("AIR", "polaris-y"), ("WATER", "selkie-w")]
    cs = [cut(c) for _, c in items]
    vig = R.vignette(.5)
    pos = [(W * .28, 800), (W * .72, 800), (W * .28, 1190), (W * .72, 1190)]

    def frames():
        for i in range(n):
            t = i / FPS
            base = skybg(t, T, 13, .52, .08); lines = []; labs = []
            for j, (el, _) in enumerate(items):
                t0 = j * .6
                if t < t0:
                    continue
                p = eout(seg(t, t0, t0 + .35))
                c = cs[j]; s = min(400 / c.width, 330 / c.height) * (1.35 - .35 * p)
                base, al = R.paste_cut(base, c, pos[j][0], pos[j][1], s, blur=(1 - p) * 6)
                base = base + glint(al, t, 4.4 + j * .15, .8)[..., None] * 255
                lab = text([(el, "MEDIUM", 40, SAND, pos[j][1] + 175, 9, t0 + .2)], t)
                labs.append((lab, int(pos[j][0] - W / 2)))
            base = base * vig
            lines = [("Fire, earth,", "LIGHT", 76, CREAM, 300, 2, -1),
                     ("AIR OR WATER?", "BOLD", 104, SAND, 392, 5, .1)] + lines + \
                    [("Tell us her sign.", "LIGHT", 60, CREAM, 1500, 1, 3.0),
                     ("We'll tell you her ring.", "BOLD", 66, CREAM, 1576, 1, 3.3)]
            lay = text(lines, t)
            for lab, dx in labs:
                L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L.alpha_composite(lab, (dx, 0)) if dx >= 0 else L.alpha_composite(lab.crop((-dx, 0, W, H)), (0, 0))
                lay.alpha_composite(L)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    run("thu-19-zodiac", frames, n, 1)


# ============================================================ THU 19 — Algol: the stone fills the frame, pull back
def algol():
    T = 7.5; n = int(T * FPS)
    c = cut("algol-y")
    vig = R.vignette(.5)
    s_fit = 820 / c.width
    s_native = 1.0
    wo = text_width("$3,600", "LIGHT", 96, 3)

    def frames():
        for i in range(n):
            t = i / FPS
            k = ease(seg(t, 0, 2.2))
            sc = s_native * (1 - k) + s_fit * k
            cy = 1000 + (1 - k) * 60
            base, al = R.paste_cut(skybg(t, T, 17, .5, .12), c, W / 2, cy, sc, shadow=False)
            base = base + (glint(al, t, .05, .8, 150, .5) + glint(al, t, 4.6, 1.0))[..., None] * 255
            base = base * vig
            lay = text([("ALGOL", "BOLD", 110, CREAM, 300, 14, 2.0),
                        ("East-west black oval, set in gold", "LIGHT", 50, CREAM, 430, 1, 2.3),
                        ("$3,600", "LIGHT", 96, (150, 140, 128), 1290, 3, 2.9),
                        ("$3,060", "BOLD", 120, SAND, 1390, 4, 3.5),
                        ("+ FREE STUDS IN THE BOX", "MEDIUM", 42, CREAM, 1545, 6, 4.2)], t)
            st = strike_layer(W / 2, 1290 + 56, wo + 30, ease(seg(t, 3.1, 3.5)))
            yield np.clip(comp(comp(base, st), lay), 0, 255).astype(np.uint8)
    run("thu-19-algol", frames, n, 0)


# ============================================================ FRI 20 — pendant swings in (floating display)
def pendant():
    T = 7.5; n = int(T * FPS)
    c = cut("noireclipse")
    vig = R.vignette(.5)
    s = 1080 / c.height
    wo = text_width("$1,400", "LIGHT", 70, 3)

    def frames():
        for i in range(n):
            t = i / FPS
            drop = eout(seg(t, 0, .9))
            ang = 9 * math.exp(-1.1 * t) * math.cos(5.2 * t)
            r = c.rotate(ang, resample=Image.BICUBIC, expand=True)
            cy = -700 + (860 + 700) * drop
            base, al = R.paste_cut(skybg(t, T, 19, .46, .10), r, W / 2, cy, s)
            base = base + glint(al, t, 3.2, 1.0, 120, .5)[..., None] * 255
            base = base * vig
            head = text([("For under the tree:", "LIGHT", 70, CREAM, 1380, 1, 1.4),
                         ("SOMETHING THAT STAYS.", "BOLD", 82, SAND, 1462, 4, 1.7)], t)
            old = text([("$1,400", "LIGHT", 70, (150, 140, 128), 1560, 3, 2.4)], t)
            new = text([("$1,190", "BOLD", 76, CREAM, 1556, 3, 3.2)], t)
            L1 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L1.alpha_composite(old, (-150, 0))
            L2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L2.alpha_composite(new, (150, 0))
            st = strike_layer(W / 2 - 150, 1560 + 46, wo + 24, ease(seg(t, 2.8, 3.15)))
            out = comp(comp(comp(comp(base, head), L1), st), L2)
            yield np.clip(out, 0, 255).astype(np.uint8)
    run("fri-20-pendant", frames, n, 1)


# ============================================================ SUN 22 — Black Friday reveal (real sparkle footage)
def bf_reveal():
    T = 7.5; n = int(T * FPS)
    vid = os.path.join(DROP, "VID20260505111317.mp4")   # loose round diamond in tweezers (white diamond light)
    fr = R.video_frames(vid, 1.0, T + .2, "crop=607:1080:520:0,scale=1080:1920,gblur=sigma=16,eq=contrast=1.25:brightness=-0.22:saturation=0.7")
    vig = R.vignette(.6)
    w30 = text_width("30%", "BOLD", 400, 8)

    def frames():
        for i in range(n):
            t = i / FPS
            f = fr[min(i, len(fr) - 1)].astype(float) * .55 + np.array(INK, float) * .45
            base = f * vig
            # "30%" revealed by a light sweep: alpha = sweep front
            L = text([("30%", "BOLD", 400, SAND, 640, 8, -5)], t)
            a = np.asarray(L, float)
            x = np.arange(W)[None, :]
            front = -200 + eout(seg(t, .05, .9)) * (W + 400)
            m = np.clip((front - x) / 160, 0, 1)
            a[..., 3] *= m
            base = comp(base, Image.fromarray(a.astype(np.uint8), "RGBA"))
            base = base + glint(a[..., 3] / 255, t, .9, .8, 120, .4)[..., None] * 255
            lay = text([("Black Friday", "LIGHT", 70, CREAM, 380, 3, .3),
                        ("OFF EVERYTHING", "BOLD", 96, CREAM, 1110, 6, 1.0),
                        ("From Friday, November 27", "LIGHT", 60, CREAM, 1420, 1, 1.8),
                        ("through January.", "LIGHT", 60, CREAM, 1492, 1, 2.0),
                        ("NO CODE · AUTOMATIC AT CHECKOUT", "MEDIUM", 40, SAND, 1600, 6, 2.8)], t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    run("sun-22-bf", frames, n, 0)


# ============================================================ feed images 1080x1350 (static)
FW, FH = 1080, 1350


def fglow(cy=.5, amt=.18):
    """15.11: the feed sits in the same night sky as the stories (no flat black)."""
    import cv2
    p = cv2.resize(plate("feed", 1280, 1600), (FW, FH), interpolation=cv2.INTER_AREA).astype(float)
    y, x = np.ogrid[:FH, :FW]
    r = np.sqrt(((x - FW / 2) / FW) ** 2 + ((y - FH * cy) / FW) ** 2) / .45
    return p + np.array(SAND, float)[None, None] * (np.clip(1 - r, 0, 1) ** 2 * amt * .5)[..., None]


def _fglow_flat(cy=.5, amt=.18):
    y, x = np.ogrid[:FH, :FW]
    r = np.sqrt(((x - FW / 2) / FW) ** 2 + ((y - FH * cy) / FW) ** 2) / .45
    g = np.clip(1 - r, 0, 1) ** 2 * amt
    return np.array(INK, float)[None, None] * (1 - g[..., None]) + np.array(SAND, float)[None, None] * g[..., None]


def ftext(img, lines):
    d = ImageDraw.Draw(img)
    for (txt, wgt, size, col, y, track) in lines:
        f = R.font(wgt, size); fd = dfont(wgt, size)
        fs = [fd if ch.isdigit() else f for ch in txt]
        ws = [d.textlength(ch, font=ff) for ch, ff in zip(txt, fs)]
        x = (FW - sum(ws) - track * (len(txt) - 1)) / 2
        for ch, cw, ff in zip(txt, ws, fs):
            d.text((x, y - (size * .10 if ff is fd else 0)), ch, font=ff, fill=col)
            x += cw + track
    return img


def fcut(cutname, cy=700, maxw=760, maxh=640, lines=(), out=None):
    c = cut(cutname)
    g = R.grade(c.convert("RGB"), warm=1.02, sat=1.04, con=1.08, bri=1.03).convert("RGBA"); g.putalpha(c.split()[3])
    s = min(maxw / g.width, maxh / g.height)
    g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
    base = Image.fromarray(fglow(cy / FH).astype(np.uint8)).convert("RGBA")
    sh = Image.new("RGBA", (FW, FH), (0, 0, 0, 0)); tmp = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    tmp.paste(g, (int(FW / 2 - g.width / 2), int(cy - g.height / 2)), g)
    a = tmp.split()[3].filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * .5))
    sh.putalpha(a); base.alpha_composite(sh, (0, 20)); base.alpha_composite(tmp)
    img = ftext(base.convert("RGB"), lines)
    img.save(os.path.join(HERE, out), quality=92)
    return img


def fstuds(out, lines):
    base = Image.fromarray(fglow(.5, .12).astype(np.uint8))
    s = R.grade(Image.open(STUDS).convert("RGB"), warm=1.02, con=1.08, bri=.95)
    s = s.resize((FW, int(1000 * FW / 1400)), Image.LANCZOS)
    m = np.ones((s.height, s.width))
    fy = np.clip(np.minimum(np.arange(s.height), s.height - 1 - np.arange(s.height)) / (s.height * .16), 0, 1)[:, None]
    mask = Image.fromarray((m * fy * 255).astype(np.uint8))
    base.paste(s, (0, int(FH / 2 - s.height / 2 + 40)), mask)
    ftext(base, lines).save(os.path.join(HERE, out), quality=92)


def fphoto(fname, cx, cy, w, out, lines, veil_top=.0, veil_bottom=.0, col=INK):
    src = R.grade(photo(fname), warm=1.03, sat=1.04, con=1.1).filter(ImageFilter.UnsharpMask(2, 60, 3))
    h = w * FH / FW
    img = src.resize((FW, FH), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
    a = np.asarray(img, float); y = np.arange(FH)[:, None, None]
    v = np.clip((420 - y) / 420, 0, 1) ** 1.2 * veil_top + np.clip((y - 930) / 420, 0, 1) ** 1.2 * veil_bottom
    a = a * (1 - v) + np.array(col, float) * v
    ftext(Image.fromarray(a.astype(np.uint8)), lines).save(os.path.join(HERE, out), quality=92)


def feed():
    # MON 16 carousel: the gift that comes with a gift (studs + three pieces over $2,000)
    fstuds("mon-16-post-1.jpg", [("THE STUDS", "BOLD", 104, SAND, 70, 6), ("ARE ON US.", "BOLD", 104, SAND, 190, 6),
                                 ("Every order over $2,000 comes", "LIGHT", 50, CREAM, 1140, 1),
                                 ("with black diamond studs. Free.", "LIGHT", 50, CREAM, 1204, 1)])
    fcut("centauri-r34", out="mon-16-post-2.jpg", lines=[("CENTAURI", "BOLD", 60, CREAM, 1110, 12),
                                                          ("Black oval, two side stones", "LIGHT", 46, CREAM, 1190, 1)])
    fcut("selkie-y", out="mon-16-post-3.jpg", lines=[("SELKIE", "BOLD", 60, CREAM, 1110, 12),
                                                      ("A bypass that holds the oval", "LIGHT", 46, CREAM, 1190, 1)])
    fcut("spindle-y", out="mon-16-post-4.jpg", maxh=700, lines=[("SPINDLE", "BOLD", 60, CREAM, 1110, 12),
                                                                ("Pavé black diamond cones", "LIGHT", 46, CREAM, 1190, 1)])
    # WED 18 carousel: 15% off, every piece
    fcut("hyades-y", out="wed-18-post-1.jpg", cy=740, lines=[("15% OFF.", "BOLD", 120, SAND, 110, 6),
                                                              ("EVERY PIECE.", "BOLD", 74, CREAM, 250, 8),
                                                              ("HYADES", "BOLD", 56, CREAM, 1150, 12),
                                                              ("Chevron band, black diamonds", "LIGHT", 44, CREAM, 1226, 1)])
    fcut("noireclipse", out="wed-18-post-2.jpg", cy=640, maxh=900, lines=[("NOIR ECLIPSE", "BOLD", 56, CREAM, 1150, 12),
                                                                           ("Halo pendant on its chain", "LIGHT", 44, CREAM, 1226, 1)])
    fcut("umbra", out="wed-18-post-3.jpg", lines=[("UMBRA", "BOLD", 56, CREAM, 1150, 12),
                                                   ("Faceted pear drops", "LIGHT", 44, CREAM, 1226, 1)])
    # SUN 22: Black Friday announcement (real photo, black emerald ring in its box)
    fphoto("IMG20260907095037.jpg", 1520, 1800, 2000, "sun-22-post.jpg",
           [("30% OFF EVERYTHING", "BOLD", 84, CREAM, 110, 4),
            ("From Black Friday, Nov 27, through January.", "LIGHT", 44, CREAM, 220, 1),
            ("NO CODE · AUTOMATIC AT CHECKOUT", "MEDIUM", 36, SAND, 1250, 6)], veil_top=.82, veil_bottom=.7)


# ============================================================ MON 16 — the earring on her: black that reflects (15.11 rebuild)
EAR = "IMG20260901233401.jpg"          # 2026 DROP, black pear sunburst earring, worn (3072x4096)
STONE = dict(x0=1570, x1=1812, y0=2060, y1=2395)   # the black pear, source px


def stone_mask(src):
    """the black pear centre stone: dark pixels inside its bezel, largest blob, holes filled, soft 2px edge."""
    from scipy import ndimage
    g = np.asarray(src.convert("L"), float)
    m = np.zeros(g.shape, bool)
    sub = g[STONE["y0"]:STONE["y1"], STONE["x0"]:STONE["x1"]] < 70
    lab, n = ndimage.label(sub)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    sub = ndimage.binary_fill_holes(lab == (np.argmax(sizes) + 1))
    sub = ndimage.binary_erosion(sub, iterations=3)
    m[STONE["y0"]:STONE["y1"], STONE["x0"]:STONE["x1"]] = sub
    return Image.fromarray((ndimage.gaussian_filter(m.astype(float), 2) * 255).astype(np.uint8))


def mon_earring():
    """ONE idea, ONE photo: a black diamond does not throw fire, it reflects like a mirror.
    Beat 1: tight on the black pear, a mirror reflection slides across its facets (the lustre, not sparkle).
    Beat 2: the same frame pulls back to the earring on her ear; the reflection passes once more. No white-diamond footage."""
    T = 8.0; n = int(T * FPS)
    raw = photo(EAR)
    src = R.grade(raw, warm=1.03, sat=1.02, con=1.10, bri=1.0).filter(ImageFilter.UnsharpMask(2, 60, 3))
    msk = stone_mask(raw)
    a = np.asarray(src, float); mm = np.asarray(msk, float)[..., None] / 255
    a = a * (1 - mm) + (a * .78 + np.array((2, 4, 9), float)) * mm      # richer black, a whisper of cool depth
    src = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    gl = raw.convert("L")
    detail = Image.fromarray(np.clip(128 + (np.asarray(gl, float) - np.asarray(gl.filter(ImageFilter.GaussianBlur(6)), float)) * 6,
                                     0, 255).astype(np.uint8))
    A = dict(cx=1690, cy=2540, w=880)      # tight: the stone high in frame, clear skin below for the type
    B = dict(cx=1650, cy=1850, w=1700)     # her ear and the earring, the necklace stays right of the type
    vig = R.vignette(.42)
    yy = np.arange(H)[:, None, None]

    def win(t):
        k = ease(seg(t, 1.9, 5.0))
        w = A["w"] * (B["w"] / A["w"]) ** k * (1 - .03 * seg(t, 0, 1.9))
        return A["cx"] + (B["cx"] - A["cx"]) * k, A["cy"] + (B["cy"] - A["cy"]) * k, w, k

    def reflection(m, d, t, t0, dur, amt):
        p = seg(t, t0, t0 + dur)
        if p <= 0 or p >= 1:
            return None
        ys, xs = np.nonzero(m > .5)
        if len(xs) == 0:
            return None
        x = np.arange(W)[None, :]; y = np.arange(H)[:, None]
        span = (xs.max() - xs.min()) + (ys.max() - ys.min()) * .5
        pos = xs.min() + ys.min() * .5 - span * .4 + p * span * 1.8
        dd = (x + y * .5) - pos
        wide = np.exp(-(dd / (span * .16)) ** 2)                            # the soft mirror band
        edge = np.exp(-((dd - span * .10) / (span * .016)) ** 2) * 1.3       # its crisp leading edge
        fac = .55 + 1.1 * np.clip((d - 128) / 60, -.4, 1)                   # facets break it like planes of a mirror
        return (wide * .65 + edge) * fac * m * amt

    def frames():
        for i in range(n):
            t = i / FPS
            cx, cy, w, k = win(t)
            base = np.asarray(R.cover_crop(src, cx, cy, w), float)
            m = np.asarray(R.cover_crop(msk.convert("RGB"), cx, cy, w), float)[..., 0] / 255
            d = np.asarray(R.cover_crop(detail.convert("RGB"), cx, cy, w), float)[..., 0]
            for r in (reflection(m, d, t, .10, 1.35, .62), reflection(m, d, t, 5.5, 1.2, .55)):
                if r is not None:
                    base = base + r[..., None] * np.array((222, 228, 238), float)
            v = np.clip((yy - 1300) / 440, 0, 1) * .55
            base = base * (1 - v) + np.array(CREAM, float) * v
            base = base * vig
            top = 1 - seg(t, 1.7, 2.1)
            out = base
            if top > 0:
                out = comp(out, text_layer([("It doesn't sparkle.", "LIGHT", 74, INK, 1440, 2, .25),
                                            ("IT REFLECTS.", "BOLD", 120, INK, 1522, 7, .6)], top, t))
            out = comp(out, text([("Light, held", "LIGHT", 74, INK, 1440, 2, 4.6),
                                  ("IN THE DARK.", "BOLD", 104, INK, 1526, 6, 4.9),
                                  ("FOR HER, THIS SEASON · 15% OFF", "MEDIUM", 40, (110, 84, 46), 1650, 6, 5.4)], t))
            yield np.clip(out, 0, 255).astype(np.uint8)
    run("mon-16-earring", frames, n, 1)


# ============================================================ SUN 22 — Black Friday, in the night sky (15.11 rebuild)
def bf_sky():
    """No white-diamond footage, no flat black: the night sky moves, 30% is uncovered by a light sweep,
    then the black jewels rise into the sky together (many jewels at once = 'everything')."""
    T = 8.0; n = int(T * FPS)
    names = ["centauri-y", "hyades-y", "corcaroli-y", "selkie-y", "spindle-y", "umbra"]
    cs = []
    for cn in names:
        c = cut(cn)
        g = R.grade(c.convert("RGB"), warm=1.02, sat=1.03, con=1.08, bri=1.03).convert("RGBA"); g.putalpha(c.split()[3])
        cs.append(g)
    pos = [(W * .17, 1200), (W * .39, 1150), (W * .61, 1150), (W * .83, 1200), (W * .30, 1365), (W * .70, 1365)]
    vig = R.vignette(.5)

    def frames():
        for i in range(n):
            t = i / FPS
            base = skybg(t, T, 23, .36, .10)
            L = text([("30%", "BOLD", 380, SAND, 520, 8, -5)], t)
            a = np.asarray(L, float)
            x = np.arange(W)[None, :]
            front = -200 + eout(seg(t, .05, 1.0)) * (W + 400)
            a[..., 3] *= np.clip((front - x) / 160, 0, 1)
            base = comp(base, Image.fromarray(a.astype(np.uint8), "RGBA"))
            base = base + glint(a[..., 3] / 255, t, 1.0, .8, 120, .4)[..., None] * 255
            for j, c in enumerate(cs):
                t0 = 1.9 + j * .14
                p = eout(seg(t, t0, t0 + .7))
                if p <= 0:
                    continue
                s = min(300 / c.width, 230 / c.height)
                base, al = R.paste_cut(base, c, pos[j][0], pos[j][1] + (1 - p) * 120, s * (.92 + .08 * p),
                                       blur=(1 - p) * 5, shadow=False)
                base = base + glint(al, t, 4.6 + j * .12, .8, 110, .45)[..., None] * 255
            base = base * vig
            lay = text([("Black Friday", "LIGHT", 70, CREAM, 300, 3, .3),
                        ("OFF EVERYTHING", "BOLD", 92, CREAM, 940, 6, 1.1),
                        ("From Friday, November 27", "LIGHT", 58, CREAM, 1500, 1, 3.0),
                        ("through January.", "LIGHT", 58, CREAM, 1570, 1, 3.2),
                        ("NO CODE · AUTOMATIC AT CHECKOUT", "MEDIUM", 40, SAND, 1660, 6, 3.9)], t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    run("sun-22-bf", frames, n, 0)


# ============================================================ FRI 20 — the bench reel Daniel kept + a closing image (15.11)
ONHAND = r"C:\Users\USER\Dropbox\שיווק Marketing\On-body AI\2026-10-21 scale fix\approved\R541-R-S7-closeup-LARGE-3ct.jpg"


def fri_bench():
    """12.11 sample (kept by Daniel) unchanged up to 6.4 s; the ending no longer fades to ink: it lands on an APPROVED
    on-hand render (Algol, rose gold, 21.10 'approved' folder), slow push-in, with the bench line on a soft scrim."""
    T = 9.6; n = int(T * FPS)
    blue = Image.open(os.path.join(HERE, "..", "samples-2026-11-12", "src", "blue.jpg")).convert("RGB")
    vise = Image.open(os.path.join(DROP, "IMG20260610140233.jpg")).convert("RGB")
    blue = R.grade(blue, warm=.98, sat=.9, con=1.15, bri=.82).filter(ImageFilter.UnsharpMask(2, 120, 2))
    vise = R.grade(vise, warm=1.03, sat=.92, con=1.12, bri=.92).filter(ImageFilter.UnsharpMask(2, 110, 2))
    hand = R.grade(Image.open(ONHAND).convert("RGB"), warm=1.0, sat=1.0, con=1.04, bri=1.0)
    BA = dict(cx=950, cy=1864, w0=900, w1=760)
    VA = dict(cx=1043, cy=2604, w0=1050, w1=2700)
    HA = dict(cx=2080, cy=2900, w0=2400, w1=2050)
    vig = R.vignette(.6)
    yy = np.arange(H)[:, None, None]
    SCRIM = np.clip((620 - yy) / 520, 0, 1) ** 1.3 * .78 + np.clip((yy - 1300) / 480, 0, 1) ** 1.3 * .78
    END = np.clip((yy - 1250) / 520, 0, 1) ** 1.2 * .80

    def frames():
        for i in range(n):
            t = i / FPS
            if t < 2.4:
                k = ease(t / 2.4)
                base = np.asarray(R.cover_crop(blue, BA["cx"], BA["cy"], BA["w0"] + (BA["w1"] - BA["w0"]) * k), float)
                lines = [("Some pieces take", "LIGHT", 74, CREAM, 300, 2, -1), ("WEEKS", "BOLD", 150, SAND, 392, 14, .1)]
            elif t < 6.4:
                k = ease(seg(t, 2.4, 6.2))
                w = VA["w0"] * (VA["w1"] / VA["w0"]) ** k
                base = np.asarray(R.cover_crop(vise, VA["cx"], VA["cy"] - 300 * k, w), float)
                fl = 1 - seg(t, 2.4, 2.62)
                base = base * (1 - .5 * fl) + 255 * .5 * fl
                lines = [("Some pieces take", "LIGHT", 74, CREAM, 300, 2, -1), ("WEEKS", "BOLD", 150, SAND, 392, 14, -1),
                         ("to look", "LIGHT", 74, CREAM, 1440, 2, 3.4), ("EFFORTLESS.", "BOLD", 120, CREAM, 1524, 6, 3.65)]
            else:
                k = ease(seg(t, 6.4, T))
                base = np.asarray(R.cover_crop(hand, HA["cx"], HA["cy"], HA["w0"] + (HA["w1"] - HA["w0"]) * k), float)
                fl = 1 - seg(t, 6.4, 6.62)
                base = base * (1 - .5 * fl) + 255 * .5 * fl
                base = base * (1 - END) + np.array(INK, float) * END
                lines = [("MADE AT OUR BENCH", "MEDIUM", 50, SAND, 1500, 10, 7.0),
                         ("Message us to make yours.", "LIGHT", 62, CREAM, 1580, 1, 7.3)]
            base = base * vig
            if t < 6.4:
                base = base * (1 - SCRIM) + np.array(INK, float) * SCRIM
            yield np.clip(comp(base, text(lines, t)), 0, 255).astype(np.uint8)
    run("fri-20-bench", frames, n, 0)


STORIES = {
    "mon-16-studs": mon_studs,
    "mon-16-earring": mon_earring,
    "tue-17-centauri": lambda: price_card("tue-17-centauri", "centauri-y", "$2,600", "$2,210", "CENTAURI",
                                          "Black oval, two side stones", "OVER $2,000: FREE STUDS INCLUDED", 1),
    "tue-17-gifts": lambda: many("tue-17-gifts", ["spindle-y", "hyades-r34", "corcaroli-r34", "pleiades-y", "polaris-y", "umbra"],
                                 [("Gift season.", "LIGHT", 80, CREAM, 300, 2, 2.7), ("ALREADY 15% OFF.", "BOLD", 100, SAND, 392, 5, 2.9)],
                                 [("Every piece on the site.", "LIGHT", 58, CREAM, 1530, 1, 3.6),
                                  ("MADE TO ORDER, FOR HER", "MEDIUM", 40, SAND, 1620, 7, 4.2)], 0),
    "wed-18-eternity": lambda: push("wed-18-eternity", "IMG20260617173617.jpg", dict(cx=1330, cy=1560, w=950),
                                    dict(cx=1620, cy=1650, w=2700),
                                    [("One stone", "LIGHT", 84, INK, 300, 2, -1), ("AT A TIME.", "BOLD", 124, INK, 396, 6, .2),
                                     ("Made to order.", "LIGHT", 64, INK, 1450, 1, 3.6),
                                     ("Still 15% off.", "BOLD", 74, INK, 1530, 1, 3.9),
                                     ("EVERY PIECE ON THE SITE", "MEDIUM", 40, (120, 92, 52), 1640, 7, 4.6)], track=0),
    "wed-18-returning": lambda: push("wed-18-returning", "IMG20260831121842.jpg", dict(cx=1075, cy=1230, w=820),
                                     dict(cx=1150, cy=1536, w=1728),
                                     [("Ordered from us before?", "LIGHT", 66, CREAM, 300, 1, -1),
                                      ("25% OFF.", "BOLD", 150, SAND, 1200, 8, 2.4),
                                      ("That's your total, on anything.", "LIGHT", 56, CREAM, 1400, 1, 3.0),
                                      ("Use the email you ordered with.", "BOLD", 58, CREAM, 1468, 1, 3.4),
                                      ("THANK YOU FOR COMING BACK", "MEDIUM", 40, SAND, 1556, 7, 4.2)],
                                     ink_scrim=True, track=1, sharpen=False),
    "thu-19-zodiac": zodiac,
    "thu-19-algol": algol,
    "fri-20-pendant": pendant,
    "fri-20-halo": lambda: push("fri-20-halo", "IMG20260519181117.jpg", dict(cx=950, cy=1720, w=620),
                                dict(cx=940, cy=1950, w=1880),
                                [("A white diamond", "LIGHT", 76, INK, 300, 2, .4), ("FOR THE HOLIDAYS.", "BOLD", 100, INK, 392, 5, .7),
                                 ("Made for her hand,", "LIGHT", 60, INK, 1450, 1, 3.4),
                                 ("15% off already.", "BOLD", 70, INK, 1526, 1, 3.7),
                                 ("WHITE DIAMONDS TOO, NOT ONLY BLACK", "MEDIUM", 38, (120, 92, 52), 1636, 5, 4.4)], track=0),
    "sat-21-review": lambda: push("sat-21-review", "IMG20261001124943.jpg", dict(cx=930, cy=1300, w=760),
                                  dict(cx=940, cy=1333, w=1500),
                                  [("550+ REVIEWS.", "BOLD", 110, INK, 300, 6, .3),
                                   ("“The ring is beautiful, my fiancee loves it.", "LIGHT", 48, INK, 422, 1, .8),
                                   ("Daniel was very helpful when I had questions.”", "LIGHT", 48, INK, 478, 1, 1.1),
                                   ], track=1),
    "sun-22-bf": bf_sky,
    "fri-20-bench": fri_bench,
    "sun-22-all": lambda: push("sun-22-all", "IMG20260907095037.jpg", dict(cx=1500, cy=1620, w=760),
                               dict(cx=1520, cy=1900, w=2900),
                               [("Engagement rings. Bands.", "LIGHT", 64, CREAM, 300, 1, .3),
                                ("Earrings. Pendants.", "LIGHT", 64, CREAM, 376, 1, .6),
                                ("ALL OF IT.", "BOLD", 130, SAND, 466, 6, 1.0),
                                ("30% off from Nov 27", "BOLD", 70, CREAM, 1450, 1, 3.4),
                                ("through January.", "LIGHT", 64, CREAM, 1530, 1, 3.7),
                                ("UNTIL THEN: 15% OFF, NOW", "MEDIUM", 40, SAND, 1636, 7, 4.4)], ink_scrim=True, track=1),
}

if __name__ == "__main__":
    which = sys.argv[1:] or list(STORIES) + ["feed"]
    for w in which:
        if w == "feed":
            feed()
        else:
            STORIES[w]()
