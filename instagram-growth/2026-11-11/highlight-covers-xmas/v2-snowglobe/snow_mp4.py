"""3 s motion version of cover A-bd: the real ring and the globe stay perfectly still, only the snow moves.
Snow = programmatic particles (white flakes + black diamond dust grains) inside the glass sphere, falling with a slow
sway, settling into the mound; the real ring layer is re-drawn on top so flakes pass behind it. ffmpeg -> H.264."""
import os, subprocess
import numpy as np, cv2
from PIL import Image
import gen2

FPS, SEC = 30, 3
W, H = 1080, 1920
CX, CY, R = 541, 836, 430          # glass sphere (measured on A-bd)
MOUND = lambda x: 1030 + 0.00042 * (x - CX) ** 2   # mound surface (approx)

base = np.array(Image.open(os.path.join(gen2.OUT, 'A-bd.png')).convert('RGB')).astype(np.float32)
raw = Image.open(os.path.join(gen2.RAW, 'A-bd.png')).convert('RGBA')
ring = np.array(gen2.locate(raw, gen2.layers_for('A-bd')[0][0]))[:, 4:4 + W]
ring_a = cv2.GaussianBlur(ring[:, :, 3].astype(np.float32) / 255, (0, 0), 0.7)[..., None]
ring_rgb = base.copy()   # the final cover already holds the real ring; re-use its pixels as the top layer

rng = np.random.default_rng(11)
N_W, N_B = 260, 90
def spawn(n, black):
    x = rng.uniform(CX - R, CX + R, n); y = rng.uniform(CY - R, MOUND(x))
    return dict(x=x, y=y, v=rng.uniform(28, 85, n), ph=rng.uniform(0, 6.28, n), amp=rng.uniform(4, 16, n),
                s=rng.uniform(1.2, 3.6, n) if not black else rng.uniform(1.0, 2.4, n),
                a=rng.uniform(0.45, 0.95, n), black=black)
parts = [spawn(N_W, False), spawn(N_B, True)]

yy, xx = np.mgrid[0:H, 0:W]
inside = (((xx - CX) ** 2 + (yy - CY) ** 2) < (R - 18) ** 2).astype(np.float32)
inside = cv2.GaussianBlur(inside, (0, 0), 6)

out = os.path.join(gen2.HERE, 'covers', 'A-bd-snow.mp4')
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
                       '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for f in range(FPS * SEC):
    t = f / FPS
    lw = np.zeros((H, W), np.float32); lb = np.zeros((H, W), np.float32)
    for p in parts:
        y = p['y'] + p['v'] * t
        top = CY - R
        span = MOUND(p['x']) - top
        y = top + np.mod(y - top, span)              # flakes that settle re-enter at the top of the sphere
        x = p['x'] + p['amp'] * np.sin(p['ph'] + 1.3 * t + y * 0.004)
        L = lb if p['black'] else lw
        for xi, yi, si, ai in zip(x, y, p['s'], p['a']):
            fade = min(1.0, (MOUND(xi) - yi) / 40.0)  # melt into the mound
            cv2.circle(L, (int(xi * 4), int(yi * 4)), max(1, int(si * 4)), float(ai * fade), -1, cv2.LINE_AA, 2)
    lw = cv2.GaussianBlur(lw, (0, 0), 0.8) * inside
    lb = cv2.GaussianBlur(lb, (0, 0), 0.6) * inside
    fr = base.copy()
    fr = fr * (1 - lb[..., None] * 0.85) + 18 * lb[..., None] * 0.85        # black dust grains
    fr = fr + (246 - fr) * lw[..., None]                                    # white flakes
    fr = fr * (1 - ring_a) + ring_rgb * ring_a                              # the real ring stays on top, untouched
    ff.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
print('wrote', out)
