import json,sys,statistics,csv
h=sys.argv[1]; d=json.load(open(f"{h}-posts.json",encoding="utf-8")); M=d["media"]
for m in M: m["eng"]=(m.get("like_count") or 0)+(m.get("comments_count") or 0)
med=statistics.median([m["eng"] for m in M])
for m in M: m["x"]=round(m["eng"]/med,2) if med else 0
fmt=lambda m: "REEL" if m.get("media_product_type")=="REELS" else m["media_type"]
with open(f"{h}-ranked.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["rank","x_median","likes","comments","format","date","permalink","caption"])
    for i,m in enumerate(sorted(M,key=lambda m:-m["eng"]),1):
        w.writerow([i,m["x"],m.get("like_count"),m.get("comments_count"),fmt(m),m["timestamp"][:10],m["permalink"],(m.get("caption") or "").replace("\n"," / ")])
print(h,"n",len(M),"median",med,"range",M[-1]["timestamp"][:10],"->",M[0]["timestamp"][:10])
from collections import Counter
for k in ["REEL","CAROUSEL_ALBUM","IMAGE","VIDEO"]:
    s=[m["x"] for m in M if fmt(m)==k]
    if s: print(k,len(s),"median x",statistics.median(s))
print("--- TOP 15")
for m in sorted(M,key=lambda m:-m["eng"])[:15]:
    print(m["x"],m.get("like_count"),m.get("comments_count"),fmt(m),m["timestamp"][:10],m["permalink"],"|",(m.get("caption") or "")[:300].replace("\n"," / "))
print("--- BOTTOM 8")
for m in sorted(M,key=lambda m:m["eng"])[:8]:
    print(m["x"],m.get("like_count"),m.get("comments_count"),fmt(m),m["timestamp"][:10],m["permalink"],"|",(m.get("caption") or "")[:150].replace("\n"," / "))
