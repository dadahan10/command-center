import requests,base64,io,sys,json
from PIL import Image, ImageFilter
key=[l.split("=",1)[1].strip().strip('"') for l in open("C:/Users/USER/.claude-secrets/customizeai/api/.env",encoding="utf-8") if l.startswith("OPENAI_API_KEY")][0]
cut=Image.open("img/cut_clean.png").convert("RGBA")
a=cut.split()[-1].point(lambda v:0 if v<40 else v); cut.putalpha(a); bb=a.getbbox(); cut=cut.crop(bb)
name,W,H,sw,cx,cy,prompt=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),sys.argv[7]
s=sw/cut.width; c=cut.resize((sw,round(cut.height*s)),Image.LANCZOS)
x,y=cx-c.width//2,cy-c.height//2
canvas=Image.new("RGBA",(W,H),(22,20,20,255)); canvas.alpha_composite(c,(x,y)); canvas.convert("RGB").save(f"v2/{name}_in.png")
mask=Image.new("RGBA",(W,H),(0,0,0,0)); m=Image.new("RGBA",c.size,(0,0,0,255)); mask.paste(m,(x,y),c.split()[-1].filter(ImageFilter.MaxFilter(5))); mask.save(f"v2/{name}_mask.png")
c.save(f"v2/{name}_studs.png"); json.dump({"x":x,"y":y,"w":c.width,"h":c.height},open(f"v2/{name}_pos.json","w"))
r=requests.post("https://api.openai.com/v1/images/edits",headers={"Authorization":"Bearer "+key},
  files={"image":("in.png",open(f"v2/{name}_in.png","rb"),"image/png"),"mask":("mask.png",open(f"v2/{name}_mask.png","rb"),"image/png")},
  data={"model":"gpt-image-2","prompt":prompt,"size":f"{W}x{H}","quality":"high","n":"1",**({"input_fidelity":"high"} if __import__("os").environ.get("HF") else {})},timeout=400)
if r.status_code!=200: print(r.status_code,r.text[:600]); raise SystemExit(1)
open(f"v2/{name}_raw.png","wb").write(base64.b64decode(r.json()["data"][0]["b64_json"])); print("ok",name)
