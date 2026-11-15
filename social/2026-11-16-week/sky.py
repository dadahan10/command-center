"""15.11 fix (Daniel): no flat black backgrounds. One night-sky world (DUALITY: the longing for the cosmos) behind the real jewel.
Procedural astrophotography plate (no AI credits left on 15.11: Gemini 402, Higgsfield free plan) in the brand palette:
ink #0F1418 night, sand #CFB288 star dust, a few cool silver stars, a soft Milky Way band with dark dust lanes, film grain.
The world moves (slow drift + twinkle) while the jewel stays still (Aluna principle 1).

  plate(kind, w, h)        -> float RGB array (cached to src/sky/<kind>-<w>x<h>.npy)
  Sky(kind).frame(t)       -> 1080x1920 float RGB frame at time t (slow drift/zoom over a 1.18x plate)
"""
import os
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "src", "sky")
INK = np.array((15, 20, 24), float)
NAVY = np.array((12, 20, 34), float)
SAND = np.array((207, 178, 136), float)
SILVER = np.array((214, 224, 240), float)


def _noise(h, w, scale, rng):
    """smooth value noise: blurred white noise at a given feature scale, normalised to 0..1."""
    sh, sw = max(4, int(h / scale)), max(4, int(w / scale))
    n = rng.standard_normal((sh, sw))
    n = ndimage.gaussian_filter(n, 1.0)
    n = ndimage.zoom(n, (h / sh, w / sw), order=3)[:h, :w]
    n -= n.min(); n /= n.max() + 1e-9
    return n


def _fbm(h, w, base, rng, octaves=5):
    out = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        out += amp * _noise(h, w, base / (2 ** o), rng); tot += amp; amp *= .5
    return out / tot


def plate(kind="story", w=1280, h=2260, seed=7):
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, f"{kind}-{w}x{h}-{seed}.npy")
    if os.path.exists(cp):
        return np.load(cp)
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    # band geometry: diagonal from upper-left to lower-right (story) / soft core behind centre (feed)
    if kind == "feed":
        d = np.hypot((xx - w * .5) / w, (yy - h * .5) / h * 1.1)
        band = np.exp(-(d / .34) ** 2)
    else:
        # distance to the line through (0.05w, 0.12h) -> (0.95w, 0.88h)
        x0, y0, x1, y1 = .02 * w, .10 * h, .98 * w, .90 * h
        dx, dy = x1 - x0, y1 - y0
        dist = np.abs(dy * (xx - x0) - dx * (yy - y0)) / np.hypot(dx, dy)
        band = np.exp(-(dist / (.20 * w)) ** 2)
    band *= .75 + .25 * _fbm(h, w, 420, rng, 3)
    # sky base: ink to a faint navy towards the top, slightly lifted inside the band
    vert = (1 - yy / h)[..., None]
    sky = INK * (1 - .35 * vert) + NAVY * (.35 * vert)
    # Milky Way glow: warm dust, broken by dark dust lanes
    neb = _fbm(h, w, 260, rng, 6)
    lanes = _fbm(h, w, 160, rng, 5)
    lane_mask = np.clip((lanes - .48) / .14, 0, 1) ** 1.5
    glow = band * (.15 + .85 * neb ** 1.8) * (1 - .85 * lane_mask)
    glow = ndimage.gaussian_filter(glow, 2)
    sky = sky + (np.array((215, 172, 112.)) * .62)[None, None] * glow[..., None] + (SILVER * .03)[None, None] * (band * neb)[..., None]
    # stars: power-law brightness, density higher inside the band
    img = np.zeros((h, w))
    col = np.zeros((h, w, 3))
    n_faint = int(w * h * .010)
    dens = .35 + 1.9 * band
    ys = rng.integers(0, h, n_faint * 2); xs = rng.integers(0, w, n_faint * 2)
    keep = rng.random(n_faint * 2) < dens[ys, xs] / dens.max()
    ys, xs = ys[keep][:n_faint], xs[keep][:n_faint]
    br = (rng.pareto(2.2, len(ys)) + .35) * .085
    br = np.clip(br, 0, 1.6)
    temp = rng.random(len(ys))
    np.add.at(img, (ys, xs), br)
    tint = np.where(temp[:, None] < .22, SAND / 255, np.where(temp[:, None] > .85, np.array((.80, .88, 1.0)), np.array((1, 1, .97))))
    np.add.at(col, (ys, xs), tint * br[:, None])
    # small PSF so stars are round points, not single hard pixels
    star = np.stack([ndimage.gaussian_filter(col[..., k], .75) for k in range(3)], -1) * 6.5
    # a few brighter stars with a soft halo (no spikes, no orbs)
    nb = int(w * h * 2.2e-5)
    by = rng.integers(0, h, nb); bx = rng.integers(0, w, nb)
    halo = np.zeros((h, w)); np.add.at(halo, (by, bx), np.clip(rng.pareto(3, nb) * .35 + .15, 0, 1))
    halo_img = ndimage.gaussian_filter(halo, 1.1) * 40 + ndimage.gaussian_filter(halo, 5) * 55
    sky = sky + star * 255 + halo_img[..., None] * np.array((1, .97, .92)) * 255 * .9
    # film grain + gentle vignette
    sky = sky + rng.normal(0, 2.2, (h, w))[..., None]
    v = np.clip(1 - (np.hypot((xx - w / 2) / w, (yy - h / 2) / h) / .75) ** 2.2 * .55, 0, 1)
    sky = np.clip(sky * v[..., None], 0, 255).astype(np.float32)
    np.save(cp, sky)
    return sky


class Sky:
    """1080x1920 (or W x H) window that drifts slowly over the plate; brighter stars twinkle."""

    def __init__(self, kind="story", W=1080, H=1920, drift=(-40, -70), zoom=.035, seed=7, dim=1.0):
        self.W, self.H = W, H
        pw, ph = int(W * 1.18), int(H * 1.18)
        self.p = plate(kind, pw, ph, seed) * dim
        self.drift, self.zoom = drift, zoom

    def frame(self, t, T=8.0):
        import cv2
        k = min(max(t / T, 0), 1)
        s = 1.0 + self.zoom * k
        ph, pw = self.p.shape[:2]
        cw, ch = self.W * (1.10 / s), self.H * (1.10 / s)
        cx = pw / 2 + self.drift[0] * (k - .5); cy = ph / 2 + self.drift[1] * (k - .5)
        M = np.float32([[cw / self.W, 0, cx - cw / 2], [0, ch / self.H, cy - ch / 2]])
        out = cv2.warpAffine(self.p, M, (self.W, self.H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
        return out.astype(float)


if __name__ == "__main__":
    from PIL import Image
    for kind, (w, h) in (("story", (1280, 2260)), ("feed", (1280, 1600))):
        p = plate(kind, w, h)
        Image.fromarray(p.astype(np.uint8)).save(os.path.join(CACHE, f"preview-{kind}.jpg"), quality=92)
        print(kind, p.shape, p.mean())
