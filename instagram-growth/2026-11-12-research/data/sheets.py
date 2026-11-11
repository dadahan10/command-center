"""Build contact sheets from already-collected media URLs (read-only download of public media).
python sheets.py <handle> <mode> <shortcode,...>   mode: reel (frames at fixed seconds) | car (all slides) | grid (thumbnails of all posts)"""
import json, sys, pathlib, urllib.request, subprocess, os
from PIL import Image, ImageDraw
H, mode, codes = sys.argv[1], sys.argv[2], (sys.argv[3].split(",") if len(sys.argv) > 3 else [])
base = pathlib.Path(__file__).parent; tmp = pathlib.Path(os.environ["TMPDL"]); tmp.mkdir(parents=True, exist_ok=True)
M = json.load(open(base / f"{H}-posts.json", encoding="utf-8"))["media"]
by = {m["permalink"].rstrip("/").split("/")[-1]: m for m in M}
def get(url, p):
    if not p.exists(): urllib.request.urlretrieve(url, p)
    return p
def sheet(imgs, labels, out, w=270, cols=6):
    ims = [Image.open(i).convert("RGB") for i in imgs]
    hs = [int(w * im.height / im.width) for im in ims]; h = max(hs)
    rows = (len(ims) + cols - 1) // cols; S = Image.new("RGB", (cols * w, rows * (h + 18)), "white"); d = ImageDraw.Draw(S)
    for k, im in enumerate(ims):
        x, y = (k % cols) * w, (k // cols) * (h + 18); S.paste(im.resize((w, hs[k])), (x, y)); d.text((x + 3, y + h + 2), labels[k], fill="black")
    S.save(out, quality=82)
out = base / "screens"; out.mkdir(exist_ok=True)
if mode == "grid":
    imgs, labs = [], []
    for i, m in enumerate(M):
        u = m.get("thumbnail_url") or m.get("media_url")
        if not u: continue
        try: imgs.append(get(u, tmp / f"{H}-t{i}.jpg")); labs.append(f"{m['timestamp'][2:10]} {m.get('like_count')}")
        except Exception as e: print("skip", i, e)
    for c in range(0, len(imgs), 48): sheet(imgs[c:c+48], labs[c:c+48], out / f"{H}-grid-{c//48+1}.jpg", w=180, cols=8)
for c in codes:
    m = by[c]
    if mode == "reel" and not m.get("media_url"):
        print("NO VIDEO URL", c); continue
    if mode == "reel":
        v = get(m["media_url"], tmp / f"{c}.mp4")
        dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(v)],capture_output=True,text=True).stdout.strip() or 0)
        ts = [0,0.5,1,1.5,2,3] + [round(dur*f,1) for f in (0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.97)]
        fr = []
        for t in ts:
            f = tmp / f"{c}-{t}.jpg"; subprocess.run(["ffmpeg","-y","-v","error","-ss",str(t),"-i",str(v),"-frames:v","1",str(f)])
            if f.exists(): fr.append((f, f"{t}s/{dur:.0f}s"))
        sheet([a for a,_ in fr], [b for _,b in fr], out / f"{H}-{c}.jpg", w=220, cols=8)
    else:
        ch = m.get("children", {}).get("data", []) or [m]
        fs = []
        for i, x in enumerate(ch):
            if not x.get("media_url"): continue
            if x.get("media_type") != "VIDEO": fs.append(get(x["media_url"], tmp / f"{c}-{i}.jpg")); continue
            v = get(x["media_url"], tmp / f"{c}-{i}.mp4"); f = tmp / f"{c}-{i}-f.jpg"
            dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(v)],capture_output=True,text=True).stdout.strip() or 0)
            subprocess.run(["ffmpeg","-y","-v","error","-ss",str(round(dur*0.6,1)),"-i",str(v),"-frames:v","1",str(f)])
            if f.exists(): fs.append(f)
        sheet(fs, [str(i+1) for i in range(len(fs))], out / f"{H}-{c}.jpg", w=300, cols=5)
    print("ok", c)
