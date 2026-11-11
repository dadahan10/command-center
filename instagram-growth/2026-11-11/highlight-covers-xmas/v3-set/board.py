"""Board for the v3 highlight set: every cover at full size, and at the real profile sizes (64px and 110px circles,
the way Instagram crops a highlight) on a light and a dark profile background, side by side.
Writes board.html (+ board.png via headless Chrome)."""
import os, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = [('gifts', 'Gifts', 'gold-leaf flakes'), ('sale', 'Sale', 'snow settled, deep white bed'),
         ('remnant', 'REMNANT', 'black-diamond shards'), ('bd', 'Black Diamonds', 'black + white snow'),
         ('reviews', 'Reviews', 'burgundy glitter + star sparkles'), ('mto', 'Made to Order', 'rose-gold bench filings'),
         ('care', 'Ring Care', 'fine white powder mist')]
SRC = json.load(open(os.path.join(HERE, 'src', 'sources.json'), encoding='utf8'))
import gen3
JEWEL = {k: SRC[gen3.COVERS[k]['piece']]['handle'] for k, _, _ in ORDER}


def row(size, bg, fg, ring):
    cells = ''.join(f'<div class="hl"><div class="ring" style="border-color:{ring}"><img src="covers/{k}.png" '
                    f'style="width:{size}px;height:{size}px"></div><span style="color:{fg};font-size:{12 if size < 100 else 13}px">'
                    f'{t}</span></div>' for k, t, _ in ORDER)
    return f'<div class="row" style="background:{bg}">{cells}</div>'


full = ''.join(f'<figure><img src="covers/{k}.png"><figcaption><b>{t}</b> &middot; {s}<br><small>{JEWEL[k]}</small>'
               f'</figcaption></figure>' for k, t, s in ORDER)
QA = {
 'gifts': 'Pass. Real pendant re-pasted where the model put it; one faint gold squiggle top-left of the bail is AI residue (invisible below 300px).',
 'sale': 'Pass with note. The model had recoloured and moved the bracelet; its copy was erased (snow inpainted) and the real yellow-gold King Cobra laid on the bed. Inside the loop the snow is slightly smoother than the rest.',
 'remnant': 'Pass. Disturbed ring 480px wide (was 330 in v2), nested in the shard heap - no floating.',
 'bd': 'Pass. Real Abyssal hoops; black pave on salt-and-pepper snow is low-contrast at 64px.',
 'reviews': 'Pass. Heart ring rests on the burgundy drift; no pink cast.',
 'mto': 'Pass. Silver filings regraded to rose-gold filings (snow only) so it does not read as Black Diamonds at 64px.',
 'care': 'Pass. Split-shank openings kept open (no marble fill); milky glow is the brightest globe in the set.',
}
qa = ''.join(f'<tr><td style="padding:4px 12px 4px 0;color:#cfb288;vertical-align:top">{t}</td><td style="padding:4px 0">{QA[k]}</td></tr>' for k, t, _ in ORDER)
html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Highlight covers v3</title>
<style>
body{{margin:0;background:#141414;color:#e9e4da;font:14px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;padding:28px}}
h1{{font-weight:500;font-size:20px;margin:0 0 4px}} p.sub{{margin:0 0 22px;color:#a9a294}}
h2{{font-weight:500;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:#cfb288;margin:26px 0 10px}}
.pair{{display:flex;gap:18px;flex-wrap:wrap}}
.row{{display:flex;gap:16px;padding:18px 20px;border-radius:10px;align-items:flex-start}}
.hl{{display:flex;flex-direction:column;align-items:center;gap:6px;width:max-content}}
.ring{{border:1px solid;border-radius:50%;padding:3px}} .ring img{{display:block;border-radius:50%;object-fit:cover}}
.full{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
figure{{margin:0}} figure img{{width:100%;display:block;border-radius:6px}}
figcaption{{padding:6px 2px;color:#d8d2c6}} small{{color:#8d877b}}
</style></head><body>
<h1>Instagram highlight covers &mdash; Christmas, set v3</h1>
<p class="sub">One smoked-glass globe on a gold base in all seven; the snow, the fill and the real catalogue jewel change.
The rows below are the true on-profile sizes (64px phone, 110px desktop), cropped to the circle exactly as Instagram does.</p>
<h2>At 64px &mdash; the real phone size</h2>
<div class="pair">{row(64, '#ffffff', '#262626', '#dbdbdb')}{row(64, '#000000', '#f5f5f5', '#363636')}</div>
<h2>At 110px</h2>
<div class="pair">{row(110, '#ffffff', '#262626', '#dbdbdb')}{row(110, '#000000', '#f5f5f5', '#363636')}</div>
<h2>REMNANT motion (3 s) &mdash; black-diamond shards falling</h2>
<video src="covers/remnant-shards.mp4" autoplay loop muted playsinline style="width:360px;border-radius:6px"></video>
<h2>Full size (1080 &times; 1080)</h2>
<div class="full">{full}</div>
<h2>QA (ai-image-qa)</h2><table style="border-collapse:collapse;max-width:1100px">{qa}</table>
</body></html>"""
open(os.path.join(HERE, 'board.html'), 'w', encoding='utf8').write(html)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if os.path.exists(chrome):
    subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1500,2400',
                    '--screenshot=' + os.path.join(HERE, 'board.png'), 'file:///' + os.path.join(HERE, 'board.html').replace('\\', '/')],
                   check=False, capture_output=True)
print('board written')
