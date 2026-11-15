"""Week 16-22.11 prep: download real catalog renders (Shopify CDN) + cut them out (rembg). No AI imagery."""
import os, urllib.request
from PIL import Image
from rembg import remove, new_session
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
C = "https://cdn.shopify.com/s/files/1/2469/5441/files/"
SRC = {
 "centauri-y": "R513-01-R513-Y.jpg", "centauri-r34": "R513-07-R513-R-34.jpg",
 "algol-y": "R541-01-R541-Y.jpg", "algol-r34": "R541-09-R541-R-34.jpg",
 "selkie-y": "R516-01-R516-Y.jpg", "selkie-w": "R516-04-R516-W.jpg",
 "corcaroli-y": "R491-01-R491-Y.jpg", "corcaroli-r34": "R491-06-R491-R-34.jpg",
 "pleiades-y": "R481-01-R481-Y.jpg", "polaris-y": "R505-01-R505-Y-front-src.jpg",
 "hyades-y": "R520-01-R520-Y.jpg", "hyades-r34": "R520-07-R520-R-34.jpg",
 "noireclipse": "3d4b5d5d-9e31-5eb7-a4e3-817e1790d05c.jpg",
 "spindle-y": "E019-YG_1.jpg", "umbra": "cd2d7ff7-6996-5672-8fb7-f9f858119f59.jpg",
}
sess = new_session("isnet-general-use")
for k, f in SRC.items():
    p = os.path.join(O, k + ".jpg")
    if not os.path.exists(p):
        req = urllib.request.Request(C + f, headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req, timeout=60).read())
    cp = os.path.join(O, k + "-cut.png")
    if not os.path.exists(cp):
        im = Image.open(p).convert("RGB")
        cut = remove(im, session=sess)
        cut.crop(cut.getbbox()).save(cp)
    print(k, Image.open(p).size)
