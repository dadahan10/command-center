"""Build board.html (covers large + profile highlight rows at 64px / 2x on light & dark) and render board.png headless."""
import os, pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = [
 ('A', 'THE SNOW IS OUR MATERIAL', 'same globe, the snow changes per highlight',
  'One smoked-glass globe on a brushed sand-gold base, the same plate for every highlight. Only the snow changes: for '
  'REMNANT it is raw black-diamond shards (the collection = fragments made whole); for Black Diamonds it is white snow '
  'mixed with black-diamond dust.',
  [('A-remnant', 'REMNANT', 'REMNANT · Disturbed (catalogue render, front)'),
   ('A-bd', 'Black Diamonds', 'Black Diamonds · Pera Scura pear (catalogue, front)')], True),
 ('B', 'NIGHT WINDOW', 'one shelf across the row',
  'A boutique window on a winter night. One wide plate was generated and then cut into the two covers, so the '
  'black-marble shelf runs on from one highlight to the next. The brand star is engraved into each gold base, using the '
  'real logo file.',
  [('B-gifts', 'Gifts', 'Gifts · Kintsugi huggie earrings (catalogue pair)'),
   ('B-bd', 'Black Diamonds', 'Black Diamonds · Black Magic three-sided (catalogue, side angle)')], False),
 ('C', 'GLOBE IN HAND', 'two real jewels per cover',
  'A real Diana Rafael on-hand catalogue photo. The cup she was holding became a snow globe, with a second real piece '
  'floating inside it. The hand, the nails and the tattoos come from the catalogue photo, and the worn ring is re-pasted '
  'from the original.',
  [('C-gifts', 'Gifts', 'Gifts · worn: Accretion shard band · inside: Triangulum'),
   ('C-reviews', 'Reviews', 'Reviews · worn: Gravitational Wave · inside: Mystery Soirée')], False),
]


def row(items, cls, mode):
    hl = ''.join(f'<div class="hl"><div class="c" style="background-image:url(covers/{f}.png)"></div>{lab}</div>'
                 for f, lab, _ in items)
    empty = '<div class="hl empty"><div class="c"></div>&nbsp;</div>' if cls == 's1' else ''
    return f'<div class="row {mode} {cls}">{hl}{empty}</div>'


secs = ''
for n, name, sub, note, items, mp4 in SEC:
    covers = ''.join(f'<div class="cover"><img src="covers/{f}.png"><div class="ring"></div><p>{cap}</p></div>'
                     for f, _, cap in items)
    if mp4:
        covers += ('<div class="cover"><video src="covers/A-bd-snow.mp4" autoplay loop muted playsinline></video>'
                   '<div class="ring"></div><p>Motion, 3 s MP4: the ring stays still, the snow moves</p></div>')
    secs += (f'<section><h2><i class="n">{n}</i> · {name} <span>{sub}</span></h2><p class="note">{note}</p>'
             f'<div class="wrap"><div class="covers">{covers}</div><div class="rows"><div class="tag">real size 64px</div>'
             f'{row(items, "s1", "light")}{row(items, "s1", "dark")}<div class="tag">2x</div>'
             f'{row(items, "s2", "light")}{row(items, "s2", "dark")}</div></div></section>\n')

CSS = '''
@font-face{font-family:Champie;src:url(../../highlight-covers/fonts/CHAMPIE-LIGHT.ttf);font-weight:300}
@font-face{font-family:Champie;src:url(../../highlight-covers/fonts/CHAMPIE-BOLD.ttf);font-weight:700}
:root{--ink:#0F1418;--sand:#CFB288;--sand-d:#B09266;--snow:#F4F2EE}
*{box-sizing:border-box}
body{margin:0;background:var(--snow);color:var(--ink);font:15px/1.5 "Segoe UI",system-ui,sans-serif}
header{padding:40px 48px 8px}
h1{font-family:Champie,serif;font-weight:300;font-size:40px;margin:0;letter-spacing:.02em} h1 b{font-weight:700}
.sub{color:#555;max-width:980px}
section{padding:28px 48px 36px;border-top:1px solid #ddd6cb}
h2{font-family:Champie,serif;font-weight:700;font-size:26px;margin:0 0 4px;letter-spacing:.04em}
h2 .n{font-family:"Segoe UI",sans-serif;font-style:normal;font-weight:300} h2 span{font-weight:300;color:var(--sand-d)}
.note{color:#555;margin:0 0 18px;max-width:980px}
.wrap{display:flex;gap:36px;align-items:flex-start;flex-wrap:wrap}
.covers{display:flex;gap:18px;flex-wrap:wrap}
.cover{position:relative;width:270px}
.cover img,.cover video{width:270px;height:480px;display:block;border-radius:6px;object-fit:cover}
.cover .ring{position:absolute;left:0;top:105px;width:270px;height:270px;border-radius:50%;
  box-shadow:0 0 0 1px rgba(207,178,136,.85);pointer-events:none}
.cover p{margin:6px 0 0;font-size:13px;color:#444}
.rows{display:flex;flex-direction:column;gap:14px}
.row{display:flex;gap:22px;padding:18px 22px;border-radius:10px;align-items:flex-start}
.row.light{background:#fff;color:#000} .row.dark{background:#000;color:#f5f5f5}
.hl{display:flex;flex-direction:column;align-items:center;gap:6px;font:12px -apple-system,"Segoe UI",sans-serif}
.hl .c{border-radius:50%;background-size:100% auto;background-position:center}
.row.light .hl .c{box-shadow:0 0 0 1px #fff,0 0 0 2.5px #dbdbdb} .row.dark .hl .c{box-shadow:0 0 0 1px #000,0 0 0 2.5px #363636}
.s1 .c{width:64px;height:64px} .s2 .c{width:128px;height:128px} .s2 .hl{font-size:15px;gap:9px}
.tag{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#888;margin:0 0 2px}
.empty .c{background:#efefef} .row.dark .empty .c{background:#262626}
footer{padding:20px 48px 48px;color:#666;font-size:13px}
'''
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Snow globe covers v2</title><style>{CSS}</style></head><body>
<header><h1><b>SNOW GLOBE</b> highlight covers <span style="font:300 30px Segoe UI,sans-serif">· v2</span></h1>
<p class="sub">Three upgraded snow-globe concepts with 2 covers each (1080x1920, no text). Every jewel is a real catalogue
image, placed back over the generated scene after generation. No piece from v1 is reused (no standing Kintsugi, no Portal).
The gold circle on each large cover shows what Instagram crops. Each concept is also shown as a profile highlight row at
real size (64px) and at 2x, on light and on dark.</p></header>
{secs}<footer>Generated 11.11.2026 · gpt-image-2 (edit, mask) + real catalogue pixels re-pasted · gen2.py / finish2.py /
snow_mp4.py in this folder · samples only, nothing uploaded to Instagram.</footer>
</body></html>'''
path = os.path.join(HERE, 'board.html')
open(path, 'w', encoding='utf8').write(html)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1500, 'height': 1000})
    pg.goto(pathlib.Path(path).as_uri())
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(HERE, 'board.png'), full_page=True)
    b.close()
print('board ok')
