"""Concept B finish: the brand star engraved into the front of each gold base (real logo file, not AI), then split
the one wide shelf plate into the two covers so the row reads as one continuous shelf."""
import os
import numpy as np, cv2
from PIL import Image
import gen2

STAR = r'C:\Users\USER\Dropbox\שיווק Marketing\DUALITY REBRANDING 2025\Logos\LOGO_STAR_V1.png'
BASES = [((578, 1092), 54), ((1556, 1096), 70)]   # (centre on the wide plate, star width)


def engrave(img, centre, w):
    st = Image.open(STAR).convert('RGBA')
    st = st.resize((w, round(st.height * w / st.width)), Image.LANCZOS)
    a = np.array(st)[:, :, 3].astype(np.float32) / 255
    A = np.array(img).astype(np.float32)
    x0, y0 = centre[0] - st.width // 2, centre[1] - st.height // 2
    reg = A[y0:y0 + st.height, x0:x0 + st.width]
    # recessed cut: darker inside, a thin shadow on the upper-left lip and a highlight on the lower-right lip
    dark = a * 0.42
    sh = np.clip(np.roll(np.roll(a, 1, 0), 1, 1) - a, 0, 1)   # lip catching shadow
    hi = np.clip(a - np.roll(np.roll(a, -1, 0), -1, 1), 0, 1)  # lip catching the spot light
    reg = reg * (1 - dark[..., None]) * (1 - 0.35 * sh[..., None])
    reg = reg + (255 - reg) * (0.45 * hi[..., None])
    A[y0:y0 + st.height, x0:x0 + st.width] = reg
    return Image.fromarray(np.clip(A, 0, 255).astype(np.uint8))


img = Image.open(os.path.join(gen2.RAW, 'B-pasted.png')).convert('RGB')
for c, w in BASES:
    img = engrave(img, c, w)
img.save(os.path.join(gen2.RAW, 'B-final-wide.png'))
img.crop((4, 0, 1084, 1920)).save(os.path.join(gen2.OUT, 'B-gifts.png'))
img.crop((1092, 0, 2172, 1920)).save(os.path.join(gen2.OUT, 'B-bd.png'))
print('B finished')

# Concept C: centre globe + hand in the Instagram circle (the model put the globe high) - shift down, reflect-fill the top
SHIFT_C = {'C-gifts': (0, 130), 'C-reviews': (40, 110)}
for cid, (dx, dy) in SHIFT_C.items():
    gen2.paste(cid)
    p = os.path.join(gen2.OUT, cid + '.png')
    a = np.array(Image.open(p).convert('RGB'))
    a = cv2.copyMakeBorder(a, dy, 0, dx, 0, cv2.BORDER_REPLICATE)[:1920, :1080]
    # the filled band (outside the Instagram circle) becomes a soft out-of-focus extension, no mirrored content
    blur = cv2.GaussianBlur(a, (0, 0), 25)
    w = np.clip((dy + 60 - np.arange(1920)) / 60.0, 0, 1)[:, None, None]
    wx = np.clip((dx + 40 - np.arange(1080)) / 40.0, 0, 1)[None, :, None] if dx else 0
    w = np.maximum(w, wx)
    a = (a * (1 - w) + blur * w).astype(np.uint8)
    Image.fromarray(a).save(p)
    print(cid, 'centred')
