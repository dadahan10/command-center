import cv2,json,sys,numpy as np
from PIL import Image
for n in sys.argv[1:]:
    raw=Image.open(f"v2/{n}_raw.png").convert("RGB"); st=Image.open(f"v2/{n}_studs.png").convert("RGBA"); p=json.load(open(f"v2/{n}_pos.json"))
    R=cv2.cvtColor(np.array(raw),cv2.COLOR_RGB2GRAY).astype(np.float32)
    best=None
    for s in np.arange(float(__import__("os").environ.get("S0","0.94")),1.061,0.01):
        t=st.resize((round(st.width*s),round(st.height*s)),Image.LANCZOS); a=np.array(t)
        T=cv2.cvtColor(a[:,:,:3],cv2.COLOR_RGB2GRAY).astype(np.float32); M=(a[:,:,3]>128).astype(np.float32)
        x0,y0=max(0,p["x"]-160),max(0,p["y"]-160); sub=R[y0:y0+t.height+320,x0:x0+t.width+320]
        res=cv2.matchTemplate(sub,T,cv2.TM_CCORR_NORMED,mask=M); _,v,_,loc=cv2.minMaxLoc(res)
        if best is None or v>best[0]: best=(v,s,x0+loc[0],y0+loc[1],t)
    v,s,x,y,t=best; print(n,"score %.4f scale %.2f dx %d dy %d"%(v,s,x-p["x"],y-p["y"]))
    out=raw.convert("RGBA"); out.alpha_composite(t,(x,y)); out.convert("RGB").save(f"v2/{n}_final.png")
    # diff check: how much the model changed the studs region
    d=np.abs(np.array(raw.crop((x,y,x+t.width,y+t.height))).astype(int)-np.array(t)[:,:,:3].astype(int))[np.array(t)[:,:,3]>128].mean()
    print(n,"mean abs diff in stud pixels before repaste: %.1f"%d)
