"""SALE cover rework (Daniel: from a distance it read as a black globe). OpenAI credit was exhausted, so this is done
in code from our own assets: the snow texture is the model's own settled bed (raw/sale-ai.png), raised to ~58% of the
globe; the interior gets a cool silver glow (Ring Care is warm); the real King Cobra goes on top, larger, via
gen3.paste. Writes raw/sale.png (scene without jewel) -> then `python gen3.py paste sale`."""
import os
import numpy as np, cv2
from PIL import Image
import gen3

N = gen3.N
sp = gen3.sphere(); CX, CY, R = sp['cx'], sp['cy'], sp['r']
SURF = int(CY - R + 0.60 * 2 * R)
rng = np.random.default_rng(5)

ai = cv2.cvtColor(cv2.imread(os.path.join(gen3.RAW, 'sale-ai.png')), cv2.COLOR_BGR2RGB).astype(np.float32)
# 1. snow texture: procedural powder grain (fine + medium) on cool white, with soft low-frequency drifts
def noise(sig, amp):
    n = cv2.GaussianBlur(rng.normal(0, 1, (N, N)).astype(np.float32), (0, 0), sig)
    return n / (n.std() + 1e-6) * amp
g = noise(0.6, 7) + noise(1.6, 5) + noise(45, 5)
sparkle = (rng.random((N, N)) > 0.9965).astype(np.float32)
sparkle = cv2.GaussianBlur(sparkle, (0, 0), 0.7) * 60
tex = (232 + g + sparkle)[..., None] * np.ones(3)

yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
d = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
inside = cv2.GaussianBlur((d < R - 16).astype(np.float32), (0, 0), 5)

# 2. the bed: a softly undulating lip seen slightly from above (an ellipse of the sphere's chord at SURF)
half = np.sqrt(max(R ** 2 - (SURF - CY) ** 2, 1))
lip = SURF + 26 * (1 - np.clip(((xx - CX) / half) ** 2, 0, 1)) ** 0.5 * 0 + 6 * np.sin(xx / 61.0) + 4 * np.sin(xx / 23.0 + 1)
bed = np.clip((yy - lip) / 3.0, 0, 1)
shade = 1 - 0.20 * np.clip((yy - SURF) / (CY + R - SURF), 0, 1)          # deeper snow a touch darker
rim = 1 - 0.30 * np.clip((d - (R - 70)) / 60, 0, 1)                      # snow darkens against the curved glass
lipglow = 1 + 0.07 * np.exp(-((yy - lip - 30) / 34) ** 2) - 0.05 * np.exp(-((yy - lip - 2) / 3) ** 2)                # light catching the top of the bed
bed_rgb = tex * (shade * rim * lipglow)[..., None] * np.array([0.97, 0.99, 1.02])

# 3. the liquid above: cool silver glow, brightest just above the bed, plus a few settling flakes
glow = np.exp(-(((xx - CX) / 330) ** 2 + ((yy - (SURF - 40)) / 260) ** 2))
liquid = 22 + 150 * glow
liquid = liquid[..., None] * np.array([0.90, 0.95, 1.05])[None, None, :]
liquid = liquid * (1 - 0.35 * np.clip((d - (R - 90)) / 80, 0, 1))[..., None]
fl = np.zeros((N, N), np.float32)
for _ in range(70):
    x, y = rng.uniform(CX - R * .8, CX + R * .8), rng.uniform(CY - R * .85, SURF - 20)
    cv2.circle(fl, (int(x * 4), int(y * 4)), int(rng.uniform(1.0, 2.6) * 4), float(rng.uniform(.4, .95)), -1, cv2.LINE_AA, 2)
fl = cv2.GaussianBlur(fl, (0, 0), .8)
liquid = liquid + (250 - liquid) * fl[..., None] + noise(0.8, 2.5)[..., None]

scene = liquid * (1 - bed[..., None]) + bed_rgb * bed[..., None]
# 4. keep the model's glass reflections: screen the plate's highlights back over the new interior
plate = cv2.cvtColor(cv2.imread(os.path.join(gen3.RAW, 'plate.png')), cv2.COLOR_BGR2RGB).astype(np.float32)
hi = np.clip((plate - 120) / 135, 0, 1) * (yy < SURF - 20)[..., None]
scene = scene + (255 - scene) * hi * 0.8
out = ai * (1 - inside[..., None]) + scene * inside[..., None]
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(gen3.RAW, 'sale.png'))
print('sale scene, bed lip at y', SURF)
