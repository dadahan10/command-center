import sys
p = sys.argv[1]; out = sys.argv[2]
s = open(p, encoding="utf-8", newline="").read()
anchor = """                .dr-xg--box .dr-xg__ribbon{left:0;right:0;top:0;bottom:auto;width:auto;height:5px;background:linear-gradient(180deg,#0b0b0b 0 1px,#CFB288 1px 2px,#0b0b0b 2px 3px,#CFB288 3px 4px,transparent 4px)}
              }
"""
assert s.count(anchor) == 1, s.count(anchor)
assert "DR-XG-DESKTOP-16-11" not in s
add = """              /* DR-XG-DESKTOP-16-11: desktop only - narrower card, studs zoomed (Daniel 16.11) */
              @media (min-width:700px){
                .dr-xg--box{max-width:380px;margin-left:auto;margin-right:auto;grid-template-columns:50% 1fr;min-height:236px}
                .dr-xg--box .dr-xg__media{overflow:hidden}
                .dr-xg--box .dr-xg__media img{object-position:56% 51%;transform:scale(1.6);transform-origin:57% 52%}
                .dr-xg--box .dr-xg__panel{padding:20px 16px 18px 20px}
                .dr-xg--box .dr-xg__title{font-size:19px}
                .dr-xg--box .dr-xg__sub{font-size:12px}
                .dr-xg--box .dr-xg__eyebrow{letter-spacing:.2em;white-space:nowrap}
              }
"""
s = s.replace(anchor, anchor + add)
open(out, "w", encoding="utf-8", newline="").write(s)
print("ok")
