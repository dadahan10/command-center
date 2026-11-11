"""3 s loop of the REMNANT cover: the real ring, the globe and the heap stay still; black-diamond shards fall.
Shards are programmatic: small irregular dark polygons that tumble, each with a bright facet edge that flashes as it
turns (that flash is what makes black dust visible on a dark globe). The real ring is re-drawn on top. ffmpeg H.264."""
import os, subprocess
import numpy as np, cv2
from PIL import Image
import gen3

FPS, SEC, W = 30, 3, 1080
x0, y0, side = gen3.CROP
k = W / side
sp = gen3.sphere()
CX, CY, R = (sp['cx'] - x0) * k, (sp['cy'] - y0) * k, sp['r'] * k
HEAP = lambda x: 640 + 0.00055 * (x - CX) ** 2          # top of the shard heap (final px)

base = np.array(Image.open(os.path.join(gen3.OUT, 'remnant.png')).convert('RGB')).astype(np.float32)
raw = Image.open(os.path.join(gen3.RAW, 'remnant.png')).convert('RGBA')
lay = gen3.locate(raw, gen3.layer(gen3.COVERS['remnant']), np.arange(0.80, 1.21, 0.02), 160)
ring_a = np.array(lay.crop((x0, y0, x0 + side, y0 + side)).resize((W, W), Image.LANCZOS))[:, :, 3].astype(np.float32) / 255
ring_a = cv2.GaussianBlur(ring_a, (0, 0), 0.7)[..., None]

rng = np.random.default_rng(7)
n = 150
P = dict(x=rng.uniform(CX - R * 0.85, CX + R * 0.85, n), y=rng.uniform(CY - R, 660, n), v=rng.uniform(40, 110, n),
         s=rng.uniform(4, 13, n), rot=rng.uniform(0, 6.28, n), w=rng.uniform(-3, 3, n), ph=rng.uniform(0, 6.28, n),
         amp=rng.uniform(3, 12, n), verts=[rng.uniform(0.55, 1.0, 5) for _ in range(n)])
yy, xx = np.mgrid[0:W, 0:W]
inside = cv2.GaussianBlur((((xx - CX) ** 2 + (yy - CY) ** 2) < (R - 20) ** 2).astype(np.float32), (0, 0), 6)

out = os.path.join(gen3.OUT, 'remnant-shards.mp4')
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{W}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
                       '-movflags', '+faststart', out], stdin=subprocess.PIPE)
SS = 4  # subpixel
for f in range(FPS * SEC):
    t = f / FPS
    dark = np.zeros((W, W), np.float32); glint = np.zeros((W, W), np.float32)
    top = CY - R
    for i in range(n):
        span = HEAP(P['x'][i]) - top
        y = top + np.mod(P['y'][i] - top + P['v'][i] * t * (span / (span + 1)), span)
        x = P['x'][i] + P['amp'][i] * np.sin(P['ph'][i] + 1.4 * t + y * 0.004)
        fade = min(1.0, (HEAP(x) - y) / 30.0, (y - top) / 40.0)
        if fade <= 0:
            continue
        a = P['rot'][i] + P['w'][i] * t
        ang = a + np.arange(5) * 2 * np.pi / 5
        pts = np.stack([x + np.cos(ang) * P['s'][i] * P['verts'][i], y + np.sin(ang) * P['s'][i] * 0.7 * P['verts'][i]], 1)
        cv2.fillPoly(dark, [(pts * SS).astype(np.int32)], float(fade), cv2.LINE_AA, 2)
        flash = max(0.0, np.cos(a * 2 + P['ph'][i])) ** 6          # the facet catches the key light as it turns
        e = (pts[0], pts[1]) if flash > 0.05 else None
        cv2.line(glint, tuple((pts[0] * SS).astype(int)), tuple((pts[1] * SS).astype(int)), float(fade * (0.35 + 0.65 * flash)), 2, cv2.LINE_AA, 2)
        if flash > 0.6:
            cv2.circle(glint, tuple((pts[0] * SS).astype(int)), 2 * SS, float(fade * flash), -1, cv2.LINE_AA, 2)
    dark = cv2.GaussianBlur(dark, (0, 0), 0.6) * inside
    glint = cv2.GaussianBlur(glint, (0, 0), 0.8) * inside
    fr = base * (1 - dark[..., None] * 0.92) + 14 * dark[..., None] * 0.92      # opaque black shard bodies
    fr = fr + (250 - fr) * np.clip(glint, 0, 1)[..., None] * 0.9              # bright facet edges
    fr = fr * (1 - ring_a) + base * ring_a                                        # the real ring stays untouched on top
    ff.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
print('wrote', out)
