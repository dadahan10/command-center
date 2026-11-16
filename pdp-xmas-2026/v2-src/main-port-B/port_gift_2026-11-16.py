CR={}
def R(f):
    t=open(f, encoding="utf-8", newline="").read(); CR[f]=t.count(chr(13)+chr(10)); import re; return re.sub(chr(13)+'+'+chr(10), chr(10), t)
def W(f, s, crlf): open(f, "w", encoding="utf-8", newline="").write(s.replace(chr(10), chr(13)+chr(10)) if crlf else s)
s = R("live/snippets__product-info.liquid")
p = R("prev/new_snippet.liquid")
gs = p.index("  comment\n    Holiday gift card"); ge = p.index("-%}\n", gs)
gift_gate = p[gs:ge]
anchor = """  if dr_coll_handles contains 'featured-items' and product.tags contains 'Ready To Ship'
    assign dr_rts = true
  endif
"""
assert s.count(anchor) == 1 and "dr_gift_on" not in s
s = s.replace(anchor, anchor + gift_gate)
old_open = """          {%- when 'free_gift' -%}
            <div class="ssky-product-freegift">"""
assert s.count(old_open) == 1
bi = p.index("            {%- if dr_gift_on -%}")
be = p.index("            {%- else -%}\n            <div class=\"ssky-product-freegift\">")
block = p[bi:be].replace("xmas_gift_style | default: 'eve'", "xmas_gift_style | default: 'box'")
assert "DR-XG-DESKTOP-16-11" in block and "default: 'box'" in block
s = s.replace(old_open, "          {%- when 'free_gift' -%}\n" + block + "            {%- else -%}\n            <div class=\"ssky-product-freegift\">")
old_end = """                <div class="ssky-product-freegift__richtext">
                 {{ block.settings.freegifttext }}
                </div>
              </div>
            </div>
"""
assert s.count(old_end) == 1
s = s.replace(old_end, old_end + "            {%- endif -%}\n")
assert "DR-HOLIDAY-EYEBROW BEGIN" in s and "SALE IS NOW LIVE" in s or "DR-HOLIDAY-EYEBROW BEGIN" in s
W("new_main_snippet.liquid", s, False)
sec = R("live/sections__main-product.liquid")
ps = R("prev/sections__main-product.liquid")
a = ps.index('    {\n      "type": "text",\n      "id": "xmas_gift_start"')
e = '      "default": "eve"\n    },'
b = ps.index(e) + len(e)
settings = ps[a:b].replace('"default": "eve"', '"default": "box"')
anc = '''      "info": "PREVIEW ONLY. Keep OFF on the live theme - the elements show automatically 24 Nov - 26 Dec 2026.",
      "default": false
    },'''
assert sec.count(anc) == 1 and "xmas_gift_style" not in sec
sec = sec.replace(anc, anc + "\n" + settings)
W("new_main_section.liquid", sec, False)
print("ok")
