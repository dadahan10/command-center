"""Highlight covers (xmas samples) - real ring cut-out placed on a canvas, gpt-image-2 builds the world
around it (mask keeps the ring), then the ORIGINAL ring pixels are re-pasted so the jewel is always real.
Usage: python gen.py <cover-id> [<cover-id> ...]   (ids in COVERS)   |  python gen.py --paste <cover-id>
"""
import base64, io, os, sys, json
import numpy as np, requests
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
W, H = 1088, 1920  # API canvas (multiple of 16); final crop to 1080x1920

RINGS = {
    'r117': ('r117-f1-yg-cut.png', None),        # REMNANT Kintsugi, 14K yellow
    'portal': ('portal-1-cut.png', 1072),        # Portal cushion, rose gold (cut reflection below y)
}

KEEP = ("The ring in the image is a real Diana Rafael ring photographed in a studio. Keep it EXACTLY as it is: "
        "same position, same size, same angle, same gold colour, same black diamond, same prongs and band details. "
        "Do not redraw, move, resize or restyle it. Build the scene around it so that it sits in the scene naturally, "
        "with a real contact shadow where it touches a surface. ")
COMMON = ("Palette only: deep ink black (#0F1418), warm sand gold (#CFB288) and snow white. No red, no green, no Santa, "
          "no text, no letters, no logo, no watermark. Full-bleed vertical photograph edge to edge: no border, no frame, no circle, no vignette shape, no inset. "
          "The subject sits in the middle band of the frame; the top fifth and bottom fifth are calm dark background. Photographic, 100mm macro lens, true-to-life colour, "
          "subtle film grain, sharp and clean, sophisticated luxury editorial still life.")

P_GLOBE = (KEEP +
    "The ring stands inside a small snow globe. The globe is a sphere of smoked dark glass (deep ink tint, still "
    "transparent enough to see the ring clearly) centred around the ring, about 82% of the frame width, resting on a "
    "slim, fine brushed sand-gold base with a single thin bevel, no engraving. Inside, the ring stands upright in a low "
    "mound of fine powder snow, the bottom of its band sunk into the snow (no gap under it); a few tiny snow particles float in the liquid around it, none covering the black "
    "diamond. One soft key light from the upper left draws a single crisp curved highlight on the glass and a thin "
    "warm rim on the gold base. The globe sits on matte black slate with a faint soft reflection. Background: deep ink "
    "black with a gentle cool vignette. One object, quiet, restrained. " + COMMON)

P_NIGHT = (KEEP +
    "Macro still life at night: the ring rests on deep black velvet (fine pile visible) dusted with powder snow, tiny "
    "individual ice crystals catching the light, a few on the gold band, none on the black diamond. Behind the ring "
    "the snowy velvet becomes a dark snowfield that ends in a perfectly straight, level, soft horizon line at exactly "
    "38% from the top of the frame, running the full width edge to edge; above it a deep ink night sky, almost black, with a very faint cool glow just above "
    "the horizon and a few tiny faint stars. Light: cold blue-white moonlight from the upper right, low and hard, "
    "casting a soft long shadow of the ring toward the lower left on the snow; the black diamond reads deep black with "
    "sharp mirror-like facet reflections. Shallow depth of field: the horizon is softly out of focus. " + COMMON)

P_ORN = (KEEP +
    "Above the ring, one glass Christmas bauble (about 40% of the frame width, its centre at 42% from the top of the frame, "
    "fully visible with its cap and a short gold thread) hangs from a dark fir branch that crosses just above it: the bauble is split exactly in half vertically - the left half "
    "glossy jet-black glass, the right half milky snow-white glass, meeting in one clean seam - with a slim brushed "
    "sand-gold cap and a fine gold thread. The ring stands nestled into a lower fir bough dusted with frost directly below the "
    "bauble, the bottom of its band sunk between the needles with a few frosted needles crossing in front of it, needles crisp and dark, fine hoarfrost crystals on the needle tips. One soft key light from the upper "
    "left: a crisp window highlight on the black half and a soft glow on the white half. Background: deep ink black "
    "with a few out-of-focus dark fir needles at the edges, no lights, no other ornaments. " + COMMON)

# id: (ring, prompt, ring width px, ring centre (x, y))
COVERS = {
    'globe-remnant': ('r117', P_GLOBE, 300, (544, 900)),
    'globe-gifts':   ('portal', P_GLOBE, 420, (544, 960)),
    'night-remnant': ('r117', P_NIGHT, 440, (544, 1080)),
    'night-gifts':   ('portal', P_NIGHT, 660, (544, 1130)),
    'orn-remnant':   ('r117', P_ORN, 280, (544, 1200)),
    'orn-gifts':     ('portal', P_ORN, 440, (544, 1250)),
}
FOLDER = {'globe': '1-snowglobe', 'night': '2-night', 'orn': '3-ornament'}


def key():
    for l in open(r'C:\Users\USER\.claude-secrets\customizeai\api\.env', encoding='utf8'):
        if l.startswith('OPENAI_API_KEY'):
            return l.split('=', 1)[1].strip().strip('"')


def ring_layer(cid, rw=None, c=None):
    ring, _, rw0, c0 = COVERS[cid]
    rw = rw or rw0; cx, cy = c or c0
    f, cut_y = RINGS[ring]
    im = Image.open(os.path.join(SRC, f)).convert('RGBA')
    if cut_y:
        a = np.array(im)
        ramp = np.clip((cut_y - np.arange(a.shape[0])) / 12.0, 0, 1)
        a[:, :, 3] = (a[:, :, 3] * ramp[:, None]).astype(np.uint8)
        im = Image.fromarray(a)
    a = np.array(im); a[:, :, 3][a[:, :, 3] < 8] = 0; im = Image.fromarray(a)
    im = im.crop(im.getbbox())
    s = rw / im.width
    im = im.resize((rw, round(im.height * s)), Image.LANCZOS)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(im, (cx - im.width // 2, cy - im.height // 2), im)
    return layer


def generate(cid):
    _, prompt, _, _ = COVERS[cid]
    layer = ring_layer(cid)
    canvas = Image.new('RGBA', (W, H), (15, 20, 24, 255))
    canvas.alpha_composite(layer)
    a = np.array(layer)[:, :, 3]
    keep = np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(5)))
    mask = np.zeros((H, W, 4), np.uint8)
    ys = np.where(a > 0)[0]; contact = ys.max() - int(0.10 * (ys.max() - ys.min()))
    keep[contact:, :] = 0  # contact zone: the model may bury / shadow the band bottom
    mask[:, :, 3] = np.where(keep > 30, 255, 0)  # opaque = keep, transparent = edit
    out_dir = os.path.join(HERE, FOLDER[cid.split('-')[0]])
    def png(img):
        b = io.BytesIO(); img.save(b, 'PNG'); return b.getvalue()
    r = requests.post('https://api.openai.com/v1/images/edits',
                      headers={'Authorization': 'Bearer ' + key()},
                      files={'image': ('in.png', png(canvas), 'image/png'),
                             'mask': ('mask.png', png(Image.fromarray(mask)), 'image/png')},
                      data={'model': 'gpt-image-2', 'prompt': prompt, 'size': f'{W}x{H}',
                            'quality': 'high', 'n': '1'}, timeout=600)
    if r.status_code != 200:
        print(cid, r.status_code, r.text[:400]); return
    img = Image.open(io.BytesIO(base64.b64decode(r.json()['data'][0]['b64_json']))).convert('RGB')
    raw = os.path.join(out_dir, f'_raw-{cid}.png')
    img.save(raw)
    print(cid, 'raw', img.size)
    paste(cid)


def locate(cid, img):
    """Find where (and how big) the model drew the ring: masked template match over scales."""
    import cv2
    _, _, rw0, (cx0, cy0) = COVERS[cid]
    g = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY).astype(np.float32)
    best = (-2, None, None)
    for s in np.arange(0.55, 1.36, 0.04):
        rw = int(rw0 * s)
        lay = np.array(ring_layer(cid, rw, (W // 2, H // 2)))
        ys, xs = np.where(lay[:, :, 3] > 0)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        t = cv2.cvtColor(lay[y0:y1, x0:x1, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
        m = (lay[y0:y1, x0:x1, 3] > 128).astype(np.float32)
        r = cv2.matchTemplate(g, t, cv2.TM_CCORR_NORMED, mask=m)
        r[~np.isfinite(r)] = -1
        _, v, _, loc = cv2.minMaxLoc(r)
        if v > best[0]:
            cx = loc[0] + (W // 2 - x0); cy = loc[1] + (H // 2 - y0)
            best = (v, rw, (cx, cy))
    print(cid, 'match', round(best[0], 3), best[1], best[2])
    v, rw, c = best
    return int(rw * 1.03), c


def paste(cid, glass=False):
    out_dir = os.path.join(HERE, FOLDER[cid.split('-')[0]])
    img = Image.open(os.path.join(out_dir, f'_raw-{cid}.png')).convert('RGBA')
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    layer = ring_layer(cid, *locate(cid, img))
    # soften the cut-out edge 1px so it sits in the plate
    r, g, b, a = layer.split()
    a = a.filter(ImageFilter.GaussianBlur(0.7))
    an = np.array(a).astype(float); ys = np.where(an > 0)[0]; h = ys.max() - ys.min()
    ramp = np.clip((ys.max() - np.arange(H)) / max(1, 0.12 * h), 0, 1)  # fade the bottom 12% into the AI contact
    a = Image.fromarray((an * ramp[:, None]).astype(np.uint8))
    layer = Image.merge('RGBA', (r, g, b, a))
    out = img.copy()
    out.alpha_composite(layer)
    if cid.startswith('globe'):
        # keep the glass: screen the generated glass highlights back over the ring at low strength
        A = np.array(img).astype(float)[:, :, :3]; O = np.array(out).astype(float)[:, :, :3]
        m = np.array(layer)[:, :, 3:4] / 255.0
        hi = np.clip((A - 150) / 105, 0, 1) * 0.35 * m
        O = O + (255 - O) * hi
        out = Image.fromarray(np.clip(O, 0, 255).astype(np.uint8)).convert('RGBA')
    out = out.convert('RGB').crop((4, 0, 4 + 1080, H))
    out.save(os.path.join(out_dir, f'{cid}.png'))
    print(cid, 'final')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--paste':
        for c in args[1:]: paste(c)
    else:
        for c in args: generate(c)
