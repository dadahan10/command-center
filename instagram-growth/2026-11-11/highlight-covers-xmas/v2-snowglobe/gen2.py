"""Snow-globe highlight covers v2 (3 concepts x 2). Same method as ../gen.py:
real catalogue piece (cut-out) or real on-hand catalogue photo placed on the canvas -> gpt-image-2 edit builds the
world around it (mask keeps the real pixels) -> the ORIGINAL pixels are re-pasted at the matched position.
Usage: python gen2.py gen <id...> | python gen2.py paste <id...>
"""
import base64, io, os, sys
import numpy as np, requests, cv2
from PIL import Image, ImageFilter, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, RAW, OUT = (os.path.join(HERE, d) for d in ('src', 'raw', 'covers'))
H = 1920

KEEP = ("Every piece of jewelry in the image is a real Diana Rafael piece photographed in a studio. Keep each one EXACTLY as "
        "it is: same position, same size, same angle, same gold colour, same black diamonds, same prongs and details. "
        "Do not redraw, move, resize, duplicate or restyle any jewelry, and do not add any other jewelry. ")
PAL = ("Palette only: deep ink black (#0F1418), warm sand gold (#CFB288) and snow white. No red, no green, no Santa, no "
       "text, no letters, no numbers, no logo, no watermark. Full-bleed vertical photograph edge to edge: no border, no frame, "
       "no inset circle. Photographic, true-to-life colour, subtle film grain, sharp, sophisticated luxury editorial still life. ")

GLOBE = ("A snow globe of smoked dark glass (deep ink tint, still clear enough to see inside), a perfect sphere about 66% of "
         "the frame width, its centre at 45% from the top of the frame, resting on a slim brushed sand-gold base with one thin "
         "bevel. One soft key light from the upper left draws a single crisp curved window highlight on the glass and a thin "
         "warm rim on the gold base. The globe stands on matte black slate with a faint soft reflection. Background: deep ink "
         "black, a gentle cool falloff, nothing else in the frame. ")
P_A_REM = (KEEP + GLOBE +
    "Inside the globe there is no snow: the 'snow' is made of raw black diamond shards - dozens of small rough, angular, "
    "opaque black crystal fragments of different sizes with sharp metallic facet glints, suspended in the clear liquid around "
    "the ring as if they were snowflakes, more of them near the bottom, a low heap of black shards resting on the floor of the "
    "globe. The ring floats in the middle of the globe, untouched; no shard covers the ring or its black diamond. " + PAL)
P_A_BD = (KEEP +
    "This is the same snow globe; keep the glass, the gold base, the slate, the light and the background exactly as they are. "
    "Change only the inside of the globe: the old ring is gone, the ring now in the centre is the only jewel. The snow inside "
    "is now white powder snowflakes mixed with fine black diamond dust - tiny opaque black glinting grains among the white "
    "flakes, a soft mound of white snow speckled with black dust on the floor of the globe. The ring floats in the middle "
    "above the mound; no flake covers its black diamond. " + PAL)

P_B = (KEEP +
    "Wide night shot of a jewelry boutique window on a winter night, seen from the street. One continuous polished black "
    "marble shelf with fine soft white veins runs straight and level across the whole width of the image, its top edge at "
    "exactly 68% from the top, the front edge of the shelf a crisp horizontal line. Standing on the shelf are exactly two "
    "snow globes of different sizes, each with smoked dark glass and a solid brushed sand-gold cylindrical base with a plain "
    "smooth front: a smaller globe centred in the left half and a larger globe centred in the right half; each globe holds "
    "the jewel already placed inside it, floating among slowly falling fine snow. Each globe is lit from above by its own "
    "narrow warm spotlight that leaves a soft pool of light on the marble and a crisp reflection of the base in the polished "
    "shelf. Behind the globes: deep ink darkness of the shop interior; a few out-of-focus snowflakes drift in front of the "
    "window glass, very faint reflection of a street lamp on the glass top right. Nothing else on the shelf. " + PAL)

def P_C(scene):
    return (KEEP +
        "The real hand and its ring are untouched: keep the hand, the fingers wearing the ring, the black nails, the tattoos "
        "and the ring exactly. " + scene +
        " The snow globe is smoked dark glass, a perfect sphere slightly larger than the palm, held naturally with a relaxed "
        "grip - fingers resting on its lower curve with soft contact shadows, the hand's weight caught mid-movement, not frozen. "
        "The piece of jewelry already in the globe floats inside it among fine falling snow, with a soft white snow mound on the "
        "floor of the globe; the glass shows one crisp curved highlight from the window. Real skin: pores, fine lines, knuckle "
        "creases, natural texture, no smoothing. Overcast winter daylight from a window, soft and directional, no golden hour, "
        "no orange cast. " + PAL)

P_C_GIFT = P_C("Two hands cradle a small snow globe in front of a black knit sweater, the way she held the warm cup - the "
               "cup is gone, the globe takes its place. Beyond, a softly blurred bright window with a few snowflakes.")
P_C_REV = P_C("The hand rests on a dark walnut table and curls around a small snow globe standing on the table - the cup is "
              "gone, the globe takes its place, its gold base on the wood. Soft window light from the upper left.")


def cut(name, cut_y=None):
    im = Image.open(os.path.join(SRC, name)).convert('RGBA')
    a = np.array(im)
    al = a[:, :, 3].astype(np.float32)
    al[al < 40] = 0
    if cut_y:
        al *= np.clip((cut_y - np.arange(a.shape[0])) / 12.0, 0, 1)[:, None]
    # keep only the big components (drop marble specks)
    n, lab, st, _ = cv2.connectedComponentsWithStats((al > 128).astype(np.uint8))
    big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 0.02 * st[1:, cv2.CC_STAT_AREA].max()]
    keep = cv2.dilate(np.isin(lab, big).astype(np.uint8), np.ones((9, 9), np.uint8))
    al *= keep
    a[:, :, 3] = al.astype(np.uint8)
    im = Image.fromarray(a)
    return im.crop(Image.fromarray((al > 128).astype(np.uint8) * 255).getbbox())


def photo_patch(name, scale, box, feather=18):
    """Crop of a real on-hand photo (box in source px) with a feathered elliptical alpha - the real ring + its finger."""
    im = Image.open(os.path.join(SRC, name)).convert('RGBA')
    im = im.crop(box)
    w, h = im.size
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).ellipse((feather, feather, w - feather, h - feather), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(feather / 2))
    im.putalpha(m)
    return im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)


def place(size, piece, width, centre):
    W, H_ = size
    s = width / piece.width
    p = piece.resize((width, round(piece.height * s)), Image.LANCZOS)
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    layer.paste(p, (centre[0] - p.width // 2, centre[1] - p.height // 2), p)
    return layer


# ---------------- cover specs ----------------
# pieces: (key, source, width, centre, glass)
PIECES = {
    'disturbed': lambda: cut('disturbed-0-cut.png'),
    'pera':      lambda: cut('pera-scura-0-cut.png'),
    'huggie':    lambda: cut('kintsugi-huggie-0-cut.png'),
    'blackmagic': lambda: cut('black-magic-3s-5-cut.png'),
    'triangulum': lambda: cut('triangulum-0-cut.png'),
    'soiree':    lambda: cut('mystery-soiree-0-cut.png'),
}

# C: photo placement on the 1088x1920 canvas
C_PHOTO = {
    'C-gifts':   dict(photo='accretion-hand-5.jpg', s=0.68, off=(82, 416), globe=((680, 250), 400),
                      cup=(360, 260, 1000, 780), ring_box=(750, 690, 900, 930), inner=('triangulum', 180, (544, 538))),
    'C-reviews': dict(photo='gravwave-hand-1.jpg', s=0.68, off=(204, 416), globe=((520, 330), 400),
                      cup=(250, 280, 900, 1000), ring_box=(700, 690, 900, 930), inner=('soiree', 170, (558, 572))),
}


def hand_layer(cid):
    """The real hand(s) + ring from the catalogue photo: rembg isnet mask minus the cup (cream, low saturation)."""
    c = C_PHOTO[cid]
    ph = np.array(Image.open(os.path.join(SRC, c['photo'])).convert('RGB'))
    m = np.array(Image.open(os.path.join(SRC, c['photo'].replace('.jpg', '-mask-isnet.png'))).convert('L')).astype(np.float32)
    P = ph.astype(np.int32)
    hsv = cv2.cvtColor(ph, cv2.COLOR_RGB2HSV)
    skin = ((P[:, :, 0] - P[:, :, 2]) > 28) | (hsv[:, :, 2] < 100)   # skin is warm, nails dark; the cup is neutral
    skin = cv2.morphologyEx(skin.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    inv = (1 - skin).astype(np.uint8)
    n_, lab_, st_, _ = cv2.connectedComponentsWithStats(inv)
    small = [i for i in range(1, n_) if st_[i, cv2.CC_STAT_AREA] < 2500]   # tattoos / nail glints = small holes
    skin = (skin.astype(bool) | np.isin(lab_, small)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)).astype(bool)
    x0, y0, x1, y1 = c['cup']
    zone = np.zeros(skin.shape, bool); zone[y0:y1, x0:x1] = True
    cupish = zone & ~skin
    m[cupish] = 0
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    rgba = np.dstack([ph, m.astype(np.uint8)])
    im = Image.fromarray(rgba, 'RGBA')
    s, (ox, oy) = c['s'], c['off']
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    lay = Image.new('RGBA', (1088, H), (0, 0, 0, 0))
    lay.alpha_composite(im, (max(0, ox), oy)) if ox >= 0 else None
    return lay


def key():
    for l in open(r'C:\Users\USER\.claude-secrets\customizeai\api\.env', encoding='utf8'):
        if l.startswith('OPENAI_API_KEY'):
            return l.split('=', 1)[1].strip().strip('"')


def png(img):
    b = io.BytesIO(); img.save(b, 'PNG'); return b.getvalue()


def edit(canvas, keep_alpha, prompt, out):
    W, H_ = canvas.size
    mask = np.zeros((H_, W, 4), np.uint8)
    mask[:, :, 3] = np.where(keep_alpha > 30, 255, 0)
    r = requests.post('https://api.openai.com/v1/images/edits',
                      headers={'Authorization': 'Bearer ' + key()},
                      files={'image': ('in.png', png(canvas.convert('RGBA')), 'image/png'),
                             'mask': ('mask.png', png(Image.fromarray(mask)), 'image/png')},
                      data={'model': 'gpt-image-2', 'prompt': prompt, 'size': f'{W}x{H_}', 'quality': 'high', 'n': '1'},
                      timeout=900)
    if r.status_code != 200:
        print(out, r.status_code, r.text[:400]); return None
    img = Image.open(io.BytesIO(base64.b64decode(r.json()['data'][0]['b64_json']))).convert('RGB')
    if img.size != (W, H_):
        img = img.resize((W, H_), Image.LANCZOS)
    img.save(os.path.join(RAW, out + '.png'))
    print(out, 'raw', img.size)
    return img


def layers_for(cid):
    """[(layer RGBA full-canvas, glass?)] for the real pixels of a cover."""
    if cid == 'A-remnant':
        return [(place((1088, H), PIECES['disturbed'](), 330, (544, 860)), True)]
    if cid == 'A-bd':
        return [(place((1088, H), PIECES['pera'](), 250, (544, 850)), True)]
    if cid == 'B':
        return [(place((2176, H), PIECES['huggie'](), 300, (544, 1000)), True),
                (place((2176, H), PIECES['blackmagic'](), 400, (1632, 900)), True)]
    c = C_PHOTO[cid]
    k, w, ctr = c['inner']
    return [(hand_layer(cid), False), (place((1088, H), PIECES[k](), w, ctr), True)]


def ring_layer(cid):
    """Only the real ring (+ a little finger) from the catalogue photo, for the re-paste."""
    c = C_PHOTO[cid]
    s, (ox, oy) = c['s'], c['off']
    bx = c['ring_box']
    patch = photo_patch(c['photo'], s, bx, feather=10)
    lay = Image.new('RGBA', (1088, H), (0, 0, 0, 0))
    lay.paste(patch, (ox + round(bx[0] * s), oy + round(bx[1] * s)), patch)
    return lay


def generate(cid):
    if cid == 'A-bd':
        base = Image.open(os.path.join(RAW, 'A-remnant.png')).convert('RGBA')
        lay = layers_for(cid)[0][0]
        canvas = base.copy(); canvas.alpha_composite(lay)
        # editable = the inside of the globe (found on the A-remnant plate) minus the new ring
        keep = np.full((H, 1088), 255, np.uint8)
        cv2.circle(keep, (544, 860), 335, 0, -1)
        la = np.array(lay)[:, :, 3]
        keep = np.maximum(keep, cv2.dilate(la, np.ones((5, 5), np.uint8)))
        return edit(canvas, keep, P_A_BD, cid)
    if cid.startswith('C'):
        c = C_PHOTO[cid]
        ph = Image.open(os.path.join(SRC, c['photo'])).convert('RGBA')
        s, (ox, oy) = c['s'], c['off']
        ph = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
        canvas = Image.new('RGBA', (1088, H), (15, 20, 24, 255))
        canvas.alpha_composite(ph, (ox, oy))
        keep = np.zeros((H, 1088), np.uint8)
        keep[oy:oy + ph.height, max(0, ox):ox + ph.width] = 255
        (gx, gy), gr = c['globe']
        cv2.circle(keep, (ox + round(gx * s), oy + round(gy * s)), round(gr * s), 0, -1)
        # soft margin so the outpaint can blend the photo edges
        keep[oy:oy + 24, :] = 0; keep[oy + ph.height - 24:oy + ph.height, :] = 0
        if ox > 0: keep[:, ox:ox + 24] = 0
        hand, inner = layers_for(cid)[0][0], layers_for(cid)[1][0]
        x0, y0, x1, y1 = c['cup']   # the cup goes: its whole zone is editable except the real hand
        keep[oy + round(y0 * s):oy + round(y1 * s), ox + round(x0 * s):ox + round(x1 * s)] = 0
        keep = np.maximum(keep, np.array(hand)[:, :, 3])
        canvas.alpha_composite(inner)
        keep = np.maximum(keep, cv2.dilate(np.array(inner)[:, :, 3], np.ones((5, 5), np.uint8)))
        return edit(canvas, keep, P_C_GIFT if cid == 'C-gifts' else P_C_REV, cid)
    W = 2176 if cid == 'B' else 1088
    canvas = Image.new('RGBA', (W, H), (15, 20, 24, 255))
    keep = np.zeros((H, W), np.uint8)
    for lay, _ in layers_for(cid):
        canvas.alpha_composite(lay)
        keep = np.maximum(keep, cv2.dilate(np.array(lay)[:, :, 3], np.ones((5, 5), np.uint8)))
    return edit(canvas, keep, P_A_REM if cid == 'A-remnant' else P_B, cid)


def locate(img, lay, scales=np.arange(0.80, 1.21, 0.03), pad=160):
    """Where (and how big) did the model put this real piece? masked template match over scales."""
    g = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY).astype(np.float32)
    L = np.array(lay)
    ys, xs = np.where(L[:, :, 3] > 0)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    piece = Image.fromarray(L[y0:y1, x0:x1])
    cx0, cy0 = (x0 + x1) / 2, (y0 + y1) / 2
    best = (-2, 1.0, (cx0, cy0), piece)
    for s in scales:
        p = piece.resize((max(4, round(piece.width * s)), max(4, round(piece.height * s))), Image.LANCZOS)
        P = np.array(p)
        t = cv2.cvtColor(P[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
        m = (P[:, :, 3] > 128).astype(np.float32)
        # search only near the intended spot
        sx0 = int(max(0, cx0 - p.width / 2 - pad)); sy0 = int(max(0, cy0 - p.height / 2 - pad))
        sx1 = int(min(g.shape[1], cx0 + p.width / 2 + pad)); sy1 = int(min(g.shape[0], cy0 + p.height / 2 + pad))
        reg = g[sy0:sy1, sx0:sx1]
        if reg.shape[0] < t.shape[0] or reg.shape[1] < t.shape[1]:
            continue
        r = cv2.matchTemplate(reg, t, cv2.TM_CCORR_NORMED, mask=m)
        r[~np.isfinite(r)] = -1
        _, v, _, loc = cv2.minMaxLoc(r)
        if v > best[0]:
            best = (v, s, (sx0 + loc[0] + p.width / 2, sy0 + loc[1] + p.height / 2), p)
    v, s, c, p = best
    print('  match', round(v, 3), 'scale', round(s, 2), 'at', (round(c[0]), round(c[1])))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste(p, (round(c[0] - p.width / 2), round(c[1] - p.height / 2)), p)
    return out


def paste(cid):
    img = Image.open(os.path.join(RAW, cid + '.png')).convert('RGBA')
    out = img.copy()
    for i, (lay, glass) in enumerate(layers_for(cid)):
        if cid.startswith('C') and i == 0:
            lay = locate(img, ring_layer(cid), np.arange(0.90, 1.11, 0.02), 140)
            L = np.array(lay); al = L[:, :, 3]
            ys, xs = np.where(al > 0)
            ctr = (int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2))
            O = np.array(out.convert('RGB'))
            m = ((al > 60) * 255).astype(np.uint8)
            O = cv2.seamlessClone(L[:, :, :3], O, m, ctr, cv2.NORMAL_CLONE)
            out = Image.fromarray(O).convert('RGBA')
            continue
        elif cid == 'B' and i == 0:   # the model shrank the huggies to ~half and set them on the snow
            lay = locate(img, place((2176, H), PIECES['huggie'](), 300, (582, 935)), np.arange(0.44, 0.62, 0.02), 90)
        elif cid in ('B',) or cid.startswith('C'):
            lay = locate(img, lay, np.arange(0.5, 1.26, 0.03), 320)
        else:
            lay = locate(img, lay)
        r, g, b, a = lay.split()
        a = a.filter(ImageFilter.GaussianBlur(0.7))
        lay = Image.merge('RGBA', (r, g, b, a))
        out.alpha_composite(lay)
        if glass:  # the jewel sits behind glass: screen the generated glass highlights back over it
            A = np.array(img).astype(float)[:, :, :3]; O = np.array(out).astype(float)[:, :, :3]
            m = np.array(lay)[:, :, 3:4] / 255.0
            hi = np.clip((A - 150) / 105, 0, 1) * 0.35 * m
            O = O + (255 - O) * hi
            out = Image.fromarray(np.clip(O, 0, 255).astype(np.uint8)).convert('RGBA')
    out = out.convert('RGB')
    if cid == 'B':
        out.crop((4, 0, 1084, H)).save(os.path.join(OUT, 'B-gifts.png'))
        out.crop((1092, 0, 2172, H)).save(os.path.join(OUT, 'B-bd.png'))
        out.save(os.path.join(RAW, 'B-pasted.png'))
    else:
        out.crop((4, 0, 1084, H)).save(os.path.join(OUT, cid + '.png'))
    print(cid, 'final')


if __name__ == '__main__':
    mode, ids = sys.argv[1], sys.argv[2:]
    for c in ids:
        if mode == 'gen':
            if generate(c) is not None:
                paste(c)
        else:
            paste(c)
