"""v3 highlight-cover set (7 covers, 1080x1080) - "the snow is made of our material".
One empty smoked-glass globe plate is generated once (gpt-image-2); every cover is an edit of THAT plate in which only
the inside of the sphere may change (snow + fill level), the real catalogue jewel is placed on the canvas and masked as
keep, and after the edit the ORIGINAL jewel pixels are re-pasted (template-matched) over a soft contact shadow.
Usage: python gen3.py plate | python gen3.py gen <id...> | python gen3.py paste <id...> | python gen3.py cuts
"""
import base64, io, os, sys, json
import numpy as np, requests, cv2
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, RAW, OUT, LOG = (os.path.join(HERE, d) for d in ('src', 'raw', 'covers', 'logs'))
N = 1088            # API canvas
CROP = (86, 46, 920)  # final = this square (x0, y0, side) of the canvas, resized to 1080

PAL = ("Palette only: deep ink black, warm sand gold and the colour of the snow described. No Santa, no tree, no "
       "text, no letters, no numbers, no logo, no watermark, no border, no frame. Photographic, true-to-life colour, "
       "subtle film grain, sharp, sophisticated luxury editorial still life. ")

P_PLATE = ("Square luxury product photograph of one single empty snow globe. The globe is a perfect sphere of smoked "
           "dark glass - deep ink-grey tint like smoked quartz, still transparent enough to see the inside - filled "
           "with perfectly clear liquid and NOTHING inside it: no snow, no objects, no figure. The sphere is large: its "
           "diameter is 80% of the frame width, centred horizontally, its centre at 43% from the top of the frame. It "
           "sits in a slim brushed sand-gold base: a low cylinder with one thin bevel and a plain smooth front, the "
           "bottom of the base at 93% from the top. One soft key light from the upper left draws a single crisp curved "
           "window highlight on the upper-left of the glass and a thin warm rim light on the base. The globe stands "
           "on matte black slate with a faint soft reflection. Background: deep ink black, gentle falloff, nothing "
           "else in the frame. " + PAL)

KEEP = ("This is an edit of an existing photograph. Keep the glass sphere outline, the gold base, the slate, the "
        "light and the background exactly as they are. The piece of jewelry inside the globe is a real Diana Rafael "
        "piece photographed in a studio: keep it EXACTLY as it is - same position, same size, same angle, same gold, "
        "same black diamonds - do not redraw, move, duplicate or restyle it, do not draw any second copy, outline, halo or ghost of it, and do not add any other jewelry. Change "
        "only the inside of the globe: ")
REST = ("The jewel RESTS on the snow surface: its lower edge sinks a few millimetres into the snow, with a soft dark "
        "contact shadow on the snow right under it and a faint warm bounce of gold on the snow. Nothing covers the "
        "jewel's black diamonds. The smoked glass keeps its crisp curved highlight at the upper left. ")

# id: piece, jewel width (px on the 1088 canvas), jewel centre, hole-fill, snow prompt
COVERS = {
    'gifts': dict(piece='noir-eclipse', w=380, floor=0.74, fill=True, force=((550, 528), 1.0), snow=(
        "the snow is GOLD: hundreds of thin flakes of beaten 24k gold leaf, crinkled, catching the light, drifting "
        "through the liquid around the jewel, densest in the upper half, and a low glittering drift of gold flakes on "
        "the floor of the globe (the floor sits at 74% of the sphere height). The whole globe glows warm gold. ")),
    'sale': dict(piece='king-cobra-yg', w=620, floor=0.60, force=((546, 492), 1.0), shadow=0.5, fill=False, snow=(
        "the snow has almost all SETTLED: a deep, smooth bed of fine white powder snow fills the lower part of the "
        "globe, and its flat surface is exactly level with the lower edge of the tennis bracelet, which lies on top of "
        "the bed where it already is; only a handful of last flakes still drift in the clear dark liquid above. ")),
    'remnant': dict(piece='disturbed', w=480, floor=0.64, wide=True, fill=False, snow=(
        "the snow is made of raw BLACK DIAMOND SHARDS - dozens of rough, angular, opaque black crystal fragments of "
        "different sizes with sharp metallic facet glints, falling like snowflakes through the liquid, and a heap of "
        "black shards that rises up to the ring: the ring is nested in the top of the heap where it already is, shards "
        "touching its band. No white snow at all. ")),
    'bd': dict(piece='abyssal2', w=450, floor=0.70, fill=False, snow=(
        "the snow is BLACK AND WHITE mixed half and half: white powder snowflakes and equally many black diamond "
        "grains falling together, and a salt-and-pepper mound of white snow heavily speckled with black grains on the "
        "floor of the globe up to 68% of the sphere height. ")),
    'reviews': dict(piece='cor-caroli', w=400, floor=0.72, fill=True, snow=(
        "the snow is deep BURGUNDY: fine flakes of wine-red (#7a1f2e) glass glitter and tiny four-pointed silver star "
        "sparkles drifting around the jewel, and a soft burgundy drift on the floor of the globe up to 72% of the "
        "sphere height. Elegant, dark, jewel-toned; no pink, no bright red. ")),
    'mto': dict(piece='pallas', w=440, floor=0.70, fill=False, grade=(1.12, 0.86, 0.74), snow=(
        "the snow is from the jeweller's bench: fine bright silvery platinum and white-gold FILINGS - tiny glinting "
        "metal grains and a few very small flat metal slivers - drift through the liquid like snow, and a smooth mound "
        "of fine silver-grey metal filings lies on the floor of the globe up to 70% of the sphere height. Cool silver "
        "tone, metallic sparkle, no gold in the snow, no curls, no pasta-like shapes. ")),
    'care': dict(piece='melusine', w=420, floor=0.70, fill=False, snow=(
        "the snow is a soft, very fine WHITE POWDER suspended everywhere in the liquid like a luminous milky mist, "
        "brighter towards the bottom, so the whole globe glows soft white around the jewel, and a smooth pale cushion "
        "of powder on the floor of the globe up to 70% of the sphere height. ")),
}


def key():
    for l in open(r'C:\Users\USER\.claude-secrets\customizeai\api\.env', encoding='utf8'):
        if l.startswith('OPENAI_API_KEY'):
            return l.split('=', 1)[1].strip().strip('"')


def png(img):
    b = io.BytesIO(); img.save(b, 'PNG'); return b.getvalue()


def call(canvas, keep, prompt, out):
    files = {'image': ('in.png', png(canvas.convert('RGBA')), 'image/png')}
    if keep is not None:
        m = np.zeros((N, N, 4), np.uint8); m[:, :, 3] = np.where(keep > 30, 255, 0)
        files['mask'] = ('mask.png', png(Image.fromarray(m)), 'image/png')
    r = requests.post('https://api.openai.com/v1/images/edits', headers={'Authorization': 'Bearer ' + key()},
                      files=files, data={'model': 'gpt-image-2', 'prompt': prompt, 'size': f'{N}x{N}',
                                         'quality': 'high', 'n': '1'}, timeout=900)
    if r.status_code != 200:
        print(out, r.status_code, r.text[:400]); return None
    img = Image.open(io.BytesIO(base64.b64decode(r.json()['data'][0]['b64_json']))).convert('RGB')
    if img.size != (N, N):
        img = img.resize((N, N), Image.LANCZOS)
    img.save(os.path.join(RAW, out + '.png'))
    open(os.path.join(LOG, out + '.txt'), 'w', encoding='utf8').write(prompt)
    print(out, 'raw ok'); return img


def cut(name, fill):
    """Real catalogue packshot -> RGBA cut-out (isnet mask, big components only, optional hole fill, chain trimmed)."""
    im = np.array(Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB'))
    al = np.array(Image.open(os.path.join(SRC, name + '-mask.png')).convert('L')).astype(np.float32)
    al[al < 40] = 0
    b = (al > 128).astype(np.uint8)
    if name == 'noir-eclipse':          # pendant only: drop the chain above the bail
        ys = np.where(b.any(1))[0]
        b[:int(im.shape[0] * 0.44)] = 0; al[:int(im.shape[0] * 0.44)] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(b)
    big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 0.05 * st[1:, cv2.CC_STAT_AREA].max()]
    keep = np.isin(lab, big).astype(np.uint8)
    if fill:   # stone read as background by the matte -> fill enclosed holes
        ff = keep.copy(); h, w = ff.shape
        m = np.zeros((h + 2, w + 2), np.uint8); cv2.floodFill(ff, m, (0, 0), 1)
        holes = (ff == 0)
        keep = keep | holes
        al[holes] = 255
    keep = cv2.dilate(keep.astype(np.uint8), np.ones((5, 5), np.uint8))
    al *= keep
    a = np.dstack([im, al.astype(np.uint8)])
    out = Image.fromarray(a, 'RGBA')
    return out.crop(Image.fromarray((al > 128).astype(np.uint8) * 255).getbbox())


def layer(c):
    """Jewel layer for a cover: width from the spec, resting on the snow floor of the measured sphere."""
    p = cut(c['piece'], c['fill']); s = sphere()
    h = round(p.height * c['w'] / p.width)
    surface = s['cy'] - s['r'] + c['floor'] * 2 * s['r']
    return place(p, c['w'], (s['cx'], round(surface - h / 2 + 10)))


def place(piece, width, centre):
    p = piece.resize((width, round(piece.height * width / piece.width)), Image.LANCZOS)
    lay = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    lay.paste(p, (centre[0] - p.width // 2, centre[1] - p.height // 2), p)
    return lay


def sphere():
    return json.load(open(os.path.join(HERE, 'sphere.json')))


def gen(cid):
    c = COVERS[cid]
    plate = Image.open(os.path.join(RAW, 'plate.png')).convert('RGBA')
    lay = layer(c)
    s = sphere()
    keep = np.full((N, N), 255, np.uint8)
    cv2.circle(keep, (s['cx'], s['cy']), s['r'] - 12, 0, -1)
    keep = np.maximum(keep, cv2.dilate(np.array(lay)[:, :, 3], np.ones((5, 5), np.uint8)))
    canvas = plate.copy(); canvas.alpha_composite(lay)
    return call(canvas, keep, KEEP + c['snow'] + REST + PAL, cid)


def locate(img, lay, scales=np.arange(0.86, 1.15, 0.02), pad=120):
    g = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY).astype(np.float32)
    L = np.array(lay); ys, xs = np.where(L[:, :, 3] > 0)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    piece = Image.fromarray(L[y0:y1, x0:x1]); cx0, cy0 = (x0 + x1) / 2, (y0 + y1) / 2
    best = (-2, 1.0, (cx0, cy0), piece)
    for s in scales:
        p = piece.resize((max(4, round(piece.width * s)), max(4, round(piece.height * s))), Image.LANCZOS)
        P = np.array(p); t = cv2.cvtColor(P[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
        m = (P[:, :, 3] > 128).astype(np.float32)
        sx0 = int(max(0, cx0 - p.width / 2 - pad)); sy0 = int(max(0, cy0 - p.height / 2 - pad))
        sx1 = int(min(N, cx0 + p.width / 2 + pad)); sy1 = int(min(N, cy0 + p.height / 2 + pad))
        reg = g[sy0:sy1, sx0:sx1]
        if reg.shape[0] < t.shape[0] or reg.shape[1] < t.shape[1]:
            continue
        r = cv2.matchTemplate(reg, t, cv2.TM_CCORR_NORMED, mask=m); r[~np.isfinite(r)] = -1
        _, v, _, loc = cv2.minMaxLoc(r)
        if v > best[0]:
            best = (v, s, (sx0 + loc[0] + p.width / 2, sy0 + loc[1] + p.height / 2), p)
    v, s, c, p = best
    print('  match', round(v, 3), 'scale', round(s, 2), 'at', (round(c[0]), round(c[1])))
    out = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    out.paste(p, (round(c[0] - p.width / 2), round(c[1] - p.height / 2)), p)
    return out


def unify(img):
    """Same globe in every cover: everything outside the sphere interior comes from the one plate."""
    s = sphere()
    plate = np.array(Image.open(os.path.join(RAW, 'plate.png')).convert('RGB')).astype(np.float32)
    A = np.array(img.convert('RGB')).astype(np.float32)
    m = np.zeros((N, N), np.float32); cv2.circle(m, (s['cx'], s['cy']), s['r'] - 16, 1.0, -1)
    m = cv2.GaussianBlur(m, (0, 0), 5)[..., None]
    return Image.fromarray(np.clip(A * m + plate * (1 - m), 0, 255).astype(np.uint8)).convert('RGBA')


def contact_shadow(out, lay, strength):
    """Soft shadow on the snow where the jewel's lower edge meets it (drawn under the real pixels)."""
    a = np.array(lay)[:, :, 3].astype(np.float32) / 255
    ys, xs = np.where(a > 0.5)
    y1 = ys.max(); x0, x1 = xs.min(), xs.max()
    sh = np.zeros((N, N), np.float32)
    # silhouette squashed onto the snow plane + a tight ellipse at the base
    band = a[max(0, y1 - 60):y1 + 1]
    proj = cv2.resize(band, (band.shape[1], 18))
    sh[y1 - 6:y1 + 12, :] = np.maximum(sh[y1 - 6:y1 + 12, :], proj)
    cv2.ellipse(sh, ((x0 + x1) // 2, y1 + 2), (int((x1 - x0) * 0.46), 16), 0, 0, 360, 0.8, -1)
    sh = cv2.GaussianBlur(sh, (0, 0), 9) * strength
    O = np.array(out.convert('RGB')).astype(np.float32)
    O *= (1 - sh[..., None])
    return Image.fromarray(np.clip(O, 0, 255).astype(np.uint8)).convert('RGBA')


def erase(img, box, snow_rgb=None):
    """Remove the model's own redrawn copy of the jewel (it moved it) before the real one goes in: pixels in the box
    that are not snow (dark or saturated) are inpainted from the surrounding snow and given back the snow grain."""
    A = np.array(img.convert('RGB'))
    x0, y0, x1, y1 = box
    hsv = cv2.cvtColor(A, cv2.COLOR_RGB2HSV)
    m = np.zeros(A.shape[:2], np.uint8)
    reg = (hsv[y0:y1, x0:x1, 2] < 175) | (hsv[y0:y1, x0:x1, 1] > 60)
    m[y0:y1, x0:x1] = reg.astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    out = cv2.inpaint(A, m, 9, cv2.INPAINT_TELEA).astype(np.float32)
    grain = np.random.default_rng(3).normal(0, 9, A.shape[:2])[..., None]
    out = np.where(m[..., None] > 0, out + grain, out)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')


def paste(cid, shadow=0.55):
    c = COVERS[cid]
    img = Image.open(os.path.join(RAW, cid + '.png')).convert('RGBA')
    if c.get('force'):                     # the model moved/redrew the jewel: put the real one where it put it
        (fx, fy), fs = c['force']
        p = cut(c['piece'], c['fill'])
        lay = place(p, round(c['w'] * fs), (fx, fy))
        if c.get('erase'):
            img = erase(img, c['erase'])
    else:
        lay = locate(img, layer(c), *((np.arange(0.80, 1.21, 0.02), 160) if c.get('wide') else ()))
    if c.get('grade'):   # recolour the snow only (the real jewel is pasted after): e.g. silver filings -> rose-gold filings
        sp = sphere(); A = np.array(img.convert('RGB')).astype(np.float32)
        m = np.zeros((N, N), np.float32); cv2.circle(m, (sp['cx'], sp['cy']), sp['r'] - 16, 1.0, -1)
        m = cv2.GaussianBlur(m, (0, 0), 5)[..., None]
        A = A * (1 - m) + np.clip(A * np.array(c['grade']), 0, 255) * m
        img = Image.fromarray(A.astype(np.uint8)).convert('RGBA')
    img = unify(img)
    out = contact_shadow(img, lay, c.get('shadow', shadow))
    r, g, b, a = lay.split(); lay = Image.merge('RGBA', (r, g, b, a.filter(ImageFilter.GaussianBlur(0.7))))
    out.alpha_composite(lay)
    # behind smoked glass: screen the PLATE's glass highlights (never the model's jewel) back over the real jewel
    A = np.array(Image.open(os.path.join(RAW, 'plate.png')).convert('RGB')).astype(float)
    O = np.array(out).astype(float)[:, :, :3]
    m = np.array(lay)[:, :, 3:4] / 255.0
    hi = np.clip((A - 150) / 105, 0, 1) * 0.35 * m
    O = O + (255 - O) * hi
    full = Image.fromarray(np.clip(O, 0, 255).astype(np.uint8))
    full.crop((4, 4, 1084, 1084)).save(os.path.join(RAW, cid + '-wide.png'))
    # tight crop: the globe fills the highlight circle (sphere ~80% of the frame), base clipped by the circle only
    x0, y0, side = CROP
    full.crop((x0, y0, x0 + side, y0 + side)).resize((1080, 1080), Image.LANCZOS).save(os.path.join(OUT, cid + '.png'))
    print(cid, 'final')


if __name__ == '__main__':
    mode, ids = sys.argv[1], sys.argv[2:]
    if mode == 'plate':
        canvas = Image.new('RGBA', (N, N), (12, 14, 16, 255))
        call(canvas, np.zeros((N, N), np.uint8), P_PLATE, 'plate' + (ids[0] if ids else ''))
    elif mode == 'cuts':
        S = Image.new('RGB', (7 * 320, 320), (30, 120, 60))
        for i, k in enumerate(COVERS):
            p = cut(COVERS[k]['piece'], COVERS[k]['fill']); p.thumbnail((300, 300))
            S.paste(p, (320 * i + 10, 10), p)
        S.save(os.path.join(SRC, '_cuts.jpg'))
    elif mode == 'gen':
        for c in ids:
            if gen(c) is not None:
                paste(c)
    else:
        for c in ids:
            paste(c)
