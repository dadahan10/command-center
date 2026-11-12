"""Prep for the 3 sample stories (12.11.2026): real-photo cutouts + crops. Sources = Dropbox 2026 drop."""
import subprocess, os
from PIL import Image
from rembg import remove, new_session
D = r"C:\Users\USER\Dropbox\שיווק Marketing\Images & Videos\2026 drop"
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sess = new_session("isnet-general-use")
def frame(vid, t, out):
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",os.path.join(D,vid),"-frames:v","1","-q:v","1",out],check=True)
# earrings in palm -> cutout (try 3 timestamps, keep all for picking)
for t in (2.0, 5.0, 9.6):
    p = os.path.join(O, f"ear-{t}.jpg"); frame("VID20260830141602.mp4", t, p)
    remove(Image.open(p), session=sess).save(os.path.join(O, f"ear-{t}-cut.png"))
# starburst in blue box: crop around piece then cut
im = Image.open(os.path.join(D,"IMG20260531150148.jpg")); im.save(os.path.join(O,"blue.jpg"))
# emerald ring full + cutout
em = Image.open(os.path.join(D,"IMG20260701115142.jpg")); em.save(os.path.join(O,"emerald.jpg"))
remove(em, session=sess).save(os.path.join(O,"emerald-cut.png"))
print("ok")
