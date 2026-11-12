"""3 sample stories for Daniel (12.11.2026) — the quality bar after his 12.11 review.

Rules applied (memory feedback_social_weekly_and_hooks, 12.11 block):
  1. visual hook in the first second (motion from frame 0: sparkle footage / macro move / match cut)
  2. Champie Light + Bold duality, >=40px, never on the jewel, inside IG safe zone (top 260 / bottom 340 free)
  3. edited premium image: real photos only, cut out or graded, jewel large
  4. H.264 yuv420p 1080x1920 30fps + faststart so it plays in the notebook

usage: python render.py [gift|engrave|bench ...]   (default: all)
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = HERE
DROP = r"C:\Users\USER\Dropbox\שיווק Marketing\Images & Videos\2026 drop"
FONTS = os.path.join(HERE, "..", "..", "instagram-growth", "2026-11-11", "highlight-covers", "fonts")
MUSIC = os.path.join(HERE, "..", "..", "..", "remnant-launch", "q4", "social-week-1021", "_music",
                     "musinova-minimal-underscore-piano-pulse-drumless-518249.mp3")
W, H, FPS = 1080, 1920, 30
INK = (15, 20, 24)
SAND = (214, 185, 140)
CREAM = (243, 238, 230)


def font(w, size):
    return ImageFont.truetype(os.path.join(FONTS, f"CHAMPIE-{w}.ttf"), size)


def ease(t):  # easeInOutCubic
    t = min(max(t, 0.0), 1.0)
    return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def eout(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def seg(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)


def text_layer(lines, alpha_fn, t):
    """lines: [(text, weight, size, color, y, tracking, t_in)] -> RGBA layer, each line fades+rises in."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    for (txt, wgt, size, col, y, track, t_in) in lines:
        p = eout(seg(t, t_in, t_in + .45)) * alpha_fn
        if p <= 0:
            continue
        f = font(wgt, size)
        widths = [d.textlength(c, font=f) for c in txt]
        total = sum(widths) + track * (len(txt) - 1)
        x = (W - total) / 2
        yy = y + (1 - p) * 26
        for c, cw in zip(txt, widths):
            d.text((x, yy), c, font=f, fill=col + (int(255 * p),))
            x += cw + track
    return L


def vignette(strength=.55):
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / (W * .75)) ** 2 + ((y - H / 2) / (H * .62)) ** 2)
    v = np.clip(1 - strength * np.clip(r - .35, 0, 1) ** 1.4, 0, 1)
    return v[..., None]


VIG = None


def glow_bg(color=INK, glow=SAND, cy=.5, rad=.42, amt=.16):
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H * cy) / W) ** 2) / rad
    g = np.clip(1 - r, 0, 1) ** 2 * amt
    base = np.array(color, float)[None, None] * (1 - g[..., None]) + np.array(glow, float)[None, None] * g[..., None]
    return base


def glint(alpha, t, t0, dur=.9, width=140, amt=.55):
    """diagonal light sweep restricted to the jewel alpha (H,W) float -> additive (H,W)."""
    p = seg(t, t0, t0 + dur)
    if p <= 0 or p >= 1:
        return np.zeros((H, W))
    y, x = np.ogrid[:H, :W]
    pos = -400 + p * (W + H * .6 + 800)
    d = (x + y * .6) - pos
    band = np.exp(-(d / width) ** 2) * amt
    return band * alpha


def grade(im, warm=1.0, sat=1.0, con=1.0, bri=1.0):
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(con)
    im = ImageEnhance.Brightness(im).enhance(bri)
    if warm != 1.0:
        r, g, b = im.split()
        r = r.point(lambda v: min(255, v * warm))
        b = b.point(lambda v: v / warm)
        im = Image.merge("RGB", (r, g, b))
    return im


def cover_crop(im, cx, cy, w):
    """crop a 9:16 window of width w centred at (cx,cy) in source px, resized to WxH."""
    w = min(w, im.width, im.height * W / H)
    h = w * H / W
    cx = min(max(cx, w / 2), im.width - w / 2)
    cy = min(max(cy, h / 2), im.height - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return im.resize((W, H), Image.LANCZOS, box=box)


def video_frames(path, t0, dur, vf):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(dur), "-i", path, "-vf", vf + f",fps={FPS}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return [np.frombuffer(raw[i * W * H * 3:(i + 1) * W * H * 3], np.uint8).reshape(H, W, 3) for i in range(n)]


def encode(name, frames_iter, nframes):
    out = os.path.join(OUT, name + ".mp4")
    dur = nframes / FPS
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-ss", "3", "-i", MUSIC, "-filter_complex",
           f"[1:a]atrim=0:{dur},afade=t=in:d=0.3,afade=t=out:st={dur - 0.8:.2f}:d=0.8,volume=.8[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-level", "4.1", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
           "-shortest", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    keep = {}
    for i, fr in enumerate(frames_iter):
        p.stdin.write(fr.tobytes())
        for k in (6, int(nframes * .45), int(nframes * .85)):
            if i == k:
                keep[k] = fr
    p.stdin.close()
    p.wait()
    for j, (k, fr) in enumerate(sorted(keep.items())):
        Image.fromarray(fr).save(os.path.join(OUT, f"{name}-f{j + 1}.jpg"), quality=90)
    Image.fromarray(sorted(keep.items())[-1][1]).save(os.path.join(OUT, f"{name}.jpg"), quality=90)
    print(name, "->", out)


def comp(base, layer):
    """base float HxWx3 0-255, layer RGBA PIL -> float"""
    a = np.asarray(layer, float)
    al = a[..., 3:4] / 255
    return base * (1 - al) + a[..., :3] * al


def paste_cut(base, cut, cx, cy, scale, blur=0.0, shadow=True):
    """cut: RGBA PIL (trimmed). returns (new_base, alpha_full HxW)."""
    w, h = int(cut.width * scale), int(cut.height * scale)
    c = cut.resize((w, h), Image.LANCZOS)
    if blur > .3:
        c = c.filter(ImageFilter.GaussianBlur(blur))
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    L.paste(c, (int(cx - w / 2), int(cy - h / 2)), c)
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a = L.split()[3].filter(ImageFilter.GaussianBlur(28))
        sh.putalpha(a.point(lambda v: int(v * .55)))
        sh = sh.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -22))
        base = comp(base, sh)
    alpha = np.asarray(L.split()[3], float) / 255
    return comp(base, L), alpha


# ---------------------------------------------------------------- 1. GIFT
def story_gift():
    T = 7.0
    n = int(T * FPS)
    vid = os.path.join(DROP, "VID20260728120423.mp4")   # bench footage: diamond-light bokeh, 1080x1920
    spark = video_frames(vid, 0.3, 1.6, "scale=1188:2112,crop=1080:1920,eq=saturation=1.15:contrast=1.45:brightness=-0.16:gamma=0.9")
    cut = Image.open(os.path.join(SRC, "ear-2.0-cut.png"))
    cut = cut.crop(cut.getbbox())
    cut = grade(cut.convert("RGB"), warm=1.03, sat=1.05, con=1.12, bri=1.04).convert("RGBA")
    cut.putalpha(Image.open(os.path.join(SRC, "ear-2.0-cut.png")).crop(Image.open(os.path.join(SRC, "ear-2.0-cut.png")).getbbox()).split()[3])
    s_fit = 860 / cut.width
    bg = glow_bg(cy=.53, amt=.20)
    vig = vignette(.5)

    def frames():
        for i in range(n):
            t = i / FPS
            if t < 1.25:
                f = spark[min(i, len(spark) - 1)].astype(float)
                z = 1.12 - .08 * ease(t / 1.25)
                im = Image.fromarray(f.astype(np.uint8)).resize((int(W * z), int(H * z)), Image.LANCZOS)
                ox, oy = (im.width - W) // 2, (im.height - H) // 2
                base = np.asarray(im.crop((ox, oy, ox + W, oy + H)), float) * .78
                # bloom out to white-gold at the cut
                fl = seg(t, 1.0, 1.25)
                base = base * (1 - fl) + np.array(CREAM, float) * fl
                txt_a = 1.0
            else:
                fl = 1 - seg(t, 1.25, 1.6)  # flash decays into the ink set
                k = ease(seg(t, 1.25, 3.2))
                sc = s_fit * (1.28 - .28 * k)
                blur = (1 - seg(t, 1.25, 2.0)) * 9
                base, al = paste_cut(bg.copy(), cut, W / 2, 1010 - 10 * math.sin(t * 1.3), sc, blur)
                base = base + (glint(al, t, 3.3, 1.0)[..., None] * 255)
                base = base * vig
                base = base * (1 - fl) + np.array(CREAM, float) * fl
                txt_a = 1.0
            lay = text_layer([
                ("Buying jewelry", "LIGHT", 74, CREAM, 300, 2, -1),
                ("AS A GIFT?", "BOLD", 128, SAND if t >= 1.25 else CREAM, 392, 6, .12),
                ("Four things", "LIGHT", 66, CREAM, 1462, 2, 2.6),
                ("that make it easy.", "BOLD", 72, CREAM, 1540, 1, 2.85),
                ("SAVE THIS ONE", "MEDIUM", 40, SAND, 1660, 9, 4.6),
            ], txt_a, t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    encode("gift-1", frames(), n)


# ---------------------------------------------------------------- 2. ENGRAVING
def story_engrave():
    T = 7.5
    n = int(T * FPS)
    src = Image.open(os.path.join(SRC, "emerald.jpg")).convert("RGB")   # 3072x3072, engraving "באהבה" on the inner shank
    # clean the backdrop speck (top centre) with a soft blurred patch of the same backdrop
    patch = src.crop((1300, 330, 1750, 620)).filter(ImageFilter.GaussianBlur(30))
    src.paste(patch, (1300, 330))
    src = grade(src, warm=1.04, sat=1.08, con=1.10, bri=1.02)
    sharp = src.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=3))
    # macro window on the engraving (letters approx x 830-1250, y 1020-1110) -> full ring
    A = dict(cx=1020, cy=1080, w=540)
    B = dict(cx=1530, cy=1345, w=1500)

    def frames():
        for i in range(n):
            t = i / FPS
            k = ease(seg(t, 2.3, 4.3))
            drift = (1 - seg(t, 0, 2.3)) * 60   # slow pan along the letters while in macro
            cx = A["cx"] + drift + (B["cx"] - A["cx"]) * k
            cy = A["cy"] + (B["cy"] - A["cy"]) * k
            w = A["w"] * (B["w"] / A["w"]) ** k     # log zoom = constant perceived speed
            im = cover_crop(sharp if k < .6 else src, cx, cy, w)
            base = np.asarray(im, float)
            # top + bottom cream veil so type sits on calm ground
            y = np.arange(H)[:, None, None]
            veil = np.clip((330 - y) / 330, 0, 1) * .55 + np.clip((y - 1330) / 420, 0, 1) * .6
            base = base * (1 - veil) + np.array(CREAM, float) * veil
            lay = text_layer([
                ("ADD A WORD", "BOLD", 120, INK, 300, 5, -.2),
                ("inside.", "LIGHT", 84, INK, 430, 2, .25),
                ("Only the two of you", "LIGHT", 66, INK, 1470, 1, 4.4),
                ("will read it.", "BOLD", 80, INK, 1552, 2, 4.7),
                ("ENGRAVED AT OUR BENCH", "MEDIUM", 40, (150, 118, 72), 1676, 8, 5.6),
            ], 1.0, t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    encode("band-4", frames(), n)


# ---------------------------------------------------------------- 3. BENCH (match cut)
def story_bench():
    T = 8.0
    n = int(T * FPS)
    blue = Image.open(os.path.join(SRC, "blue.jpg")).convert("RGB")               # 1880x4096, stones laid out
    vise = Image.open(os.path.join(DROP, "IMG20260610140233.jpg")).convert("RGB")  # 2704x5888, setting in the vise
    blue = grade(blue, warm=.98, sat=.9, con=1.15, bri=.82).filter(ImageFilter.UnsharpMask(2, 120, 2))
    vise = grade(vise, warm=1.03, sat=.92, con=1.12, bri=.92).filter(ImageFilter.UnsharpMask(2, 110, 2))
    # the same starburst footprint in both frames (match-cut anchor)
    BA = dict(cx=950, cy=1864, w0=900, w1=760)       # stones: push in
    VA = dict(cx=1043, cy=2604, w0=1050, w1=2700)    # vise: pull out to reveal the tool
    vig = vignette(.6)
    yy = np.arange(H)[:, None, None]
    SCRIM = np.clip((620 - yy) / 520, 0, 1) ** 1.3 * .78 + np.clip((yy - 1300) / 480, 0, 1) ** 1.3 * .78

    def frames():
        for i in range(n):
            t = i / FPS
            if t < 2.4:
                k = ease(t / 2.4)
                im = cover_crop(blue, BA["cx"], BA["cy"], BA["w0"] + (BA["w1"] - BA["w0"]) * k)
                base = np.asarray(im, float)
                lines = [("Some pieces take", "LIGHT", 74, CREAM, 300, 2, -1),
                         ("WEEKS", "BOLD", 150, SAND, 392, 14, .1)]
            elif t < 6.4:
                k = ease(seg(t, 2.4, 6.2))
                w = VA["w0"] * (VA["w1"] / VA["w0"]) ** k
                cy = VA["cy"] - 300 * k
                im = cover_crop(vise, VA["cx"], cy, w)
                base = np.asarray(im, float)
                fl = 1 - seg(t, 2.4, 2.62)
                base = base * (1 - .5 * fl) + 255 * .5 * fl
                lines = [("Some pieces take", "LIGHT", 74, CREAM, 300, 2, -1),
                         ("WEEKS", "BOLD", 150, SAND, 392, 14, -1),
                         ("to look", "LIGHT", 74, CREAM, 1440, 2, 3.4),
                         ("EFFORTLESS.", "BOLD", 120, CREAM, 1524, 6, 3.65)]
            else:
                p = seg(t, 6.4, 6.9)
                im = cover_crop(vise, VA["cx"], VA["cy"] - 300, VA["w1"])
                base = np.asarray(im, float) * (1 - .82 * p) + np.array(INK, float) * .82 * p
                lines = [("MADE AT OUR BENCH", "MEDIUM", 52, SAND, 860, 10, 6.55),
                         ("Message us to make yours.", "LIGHT", 60, CREAM, 960, 1, 6.8)]
            base = base * vig
            if t < 6.4:   # ink scrims so type never sits on the busy bench
                base = base * (1 - SCRIM) + np.array(INK, float) * SCRIM
            lay = text_layer(lines, 1.0, t)
            yield np.clip(comp(base, lay), 0, 255).astype(np.uint8)
    encode("fri-20-bench", frames(), n)


if __name__ == "__main__":
    which = sys.argv[1:] or ["gift", "engrave", "bench"]
    for w in which:
        {"gift": story_gift, "engrave": story_engrave, "bench": story_bench}[w]()
