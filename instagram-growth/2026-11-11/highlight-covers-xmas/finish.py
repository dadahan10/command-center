"""Finish pass: re-paste the real ring (gen.paste), then align each set and add the night star line.
- snow globe: globe+base unit shifted so the pair sits at the same height in the circle
- night: horizon of both covers moved to the same y, faint sand hairline along it + the brand star
"""
import os
import numpy as np, cv2
from PIL import Image, ImageFilter
import gen

HERE = gen.HERE
STAR = r'C:\Users\USER\Dropbox\שיווק Marketing\DUALITY REBRANDING 2025\Logos\LOGO_STAR_V1.png'
SAND = (207, 178, 136)
HORIZON = 640
SHIFT = {'globe-remnant': 118, 'globe-gifts': 68, 'night-remnant': HORIZON - 595, 'night-gifts': HORIZON - 685}
STAR_X = {'night-remnant': 300, 'night-gifts': 800}  # the star travels along the row


def shift(img, dy):
    a = np.array(img)
    if dy == 0:
        return img
    pad = abs(dy)
    a = cv2.copyMakeBorder(a, pad, pad, 0, 0, cv2.BORDER_REFLECT)
    a = a[pad - dy: pad - dy + img.height]
    return Image.fromarray(a)


def star_line(img, sx):
    img = img.convert('RGBA')
    W, H = img.size
    line = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    la = np.zeros((H, W), np.float32)
    la[HORIZON, :] = 0.42
    la[HORIZON - 1, :] = la[HORIZON + 1, :] = 0.12
    glow = cv2.GaussianBlur(la, (0, 0), 3) * 0.6
    la = np.clip(la + glow, 0, 1)
    fade = np.clip(np.minimum(np.arange(W), W - 1 - np.arange(W)) / 40.0, 0, 1)  # soft at the very edges only
    la *= np.maximum(fade, 1.0)[None, :]
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = SAND
    rgba[..., 3] = (la * 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(rgba))
    st = Image.open(STAR).convert('RGBA')
    sw = 78
    st = st.resize((sw, round(st.height * sw / st.width)), Image.LANCZOS)
    sa = np.array(st)
    sa[..., :3] = SAND
    sa[..., 3] = (sa[..., 3] * 0.9).astype(np.uint8)
    st = Image.fromarray(sa)
    g = st.filter(ImageFilter.GaussianBlur(6))
    ga = np.array(g); ga[..., 3] = (ga[..., 3] * 0.6).astype(np.uint8); g = Image.fromarray(ga)
    pos = (sx - st.width // 2, HORIZON - st.height // 2 - 8)
    img.alpha_composite(g, pos)
    img.alpha_composite(st, pos)
    return img.convert('RGB')


for cid in gen.COVERS:
    gen.paste(cid)
    p = os.path.join(HERE, gen.FOLDER[cid.split('-')[0]], f'{cid}.png')
    img = Image.open(p).convert('RGB')
    img = shift(img, SHIFT.get(cid, 0))
    if cid in STAR_X:
        img = star_line(img, STAR_X[cid])
    img.save(p)
    print('finished', cid, img.size)
