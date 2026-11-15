"""15.11 fix (Daniel): the Algol story kept a leftover of the floor reflection under the bezel. Clean re-cut of R541-Y:
rembg isnet on the full frame -> drop the floor -> the bezel's lower outline on the right is replaced by the mirror of the
clean left outline (the bezel is symmetric) -> 1px antialiased edge. Output src/algol-y-cut-clean.png. Checked at 200%."""
import os, sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
o = Image.open(os.path.join(SRC, "algol-y.jpg")).convert("RGB")
a = np.asarray(remove(o, session=new_session("isnet-general-use"))).copy()
al = a[..., 3].astype(float)
al[1640:] = 0
lab, n = ndimage.label(al > 40)
sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
al *= ndimage.binary_dilation(lab == (np.argmax(sizes) + 1), iterations=3)
H, W = al.shape
bot = np.array([(np.where(al[:, x] > 128)[0].max() if (al[:, x] > 128).any() else -1) for x in range(W)], float)
cx = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
fixed = bot.copy()
for x in range(cx, cx + 330):
    m = 2 * cx - x
    if bot[m] > 0:
        fixed[x] = min(bot[x], bot[m])
yy = np.arange(H)[:, None]
edge = np.clip(fixed[None, :] + 1.0 - yy, 0, 1)
cols = (np.arange(W) >= cx) & (np.arange(W) < cx + 330)
al[:, cols] *= edge[:, cols]
al[al < 24] = 0
a[..., 3] = al.astype(np.uint8)
im = Image.fromarray(a)
im = im.crop(Image.fromarray((al > 30).astype(np.uint8) * 255).getbbox())
im.save(os.path.join(SRC, "algol-y-cut-clean.png"))
print("saved", im.size, "bottom profile right of centre:", [int(fixed[x]) for x in range(cx, cx + 330, 30)])
