import sys
sys.path.insert(0, '.')
from hdr import R, W

s = R("g/main/snippets__product-info.liquid")
p = R("v2/new_prev_snippet.liquid")
# 1. gift gate: take it verbatim from the preview
gs = p.index("  comment\n    Holiday gift card")
ge = p.index("-%}\n", gs)
gift_gate = p[gs:ge]
anchor = """  if dr_coll_handles contains 'featured-items' and product.tags contains 'Ready To Ship'
    assign dr_rts = true
  endif
"""
assert s.count(anchor) == 1 and "dr_gift_on" not in s
s = s.replace(anchor, anchor + gift_gate)
# 2. gift block: new card while dr_gift_on, otherwise the original free-gift block (no double-up)
old_open = """          {%- when 'free_gift' -%}
            <div class="ssky-product-freegift">"""
assert s.count(old_open) == 1
bi = p.index("            {%- if dr_gift_on -%}")
be = p.index("            {%- else -%}\n            <div class=\"ssky-product-freegift\">")
block = p[bi:be]
s = s.replace(old_open, """          {%- when 'free_gift' -%}
""" + block + """            {%- else -%}
            <div class="ssky-product-freegift">""")
old_end = """                <div class="ssky-product-freegift__richtext">
                 {{ block.settings.freegifttext }}
                </div>
              </div>
            </div>
"""
assert s.count(old_end) == 1
s = s.replace(old_end, old_end + "            {%- endif -%}\n")
W("g/new_main_snippet.liquid", s)

sec = R("g/main/sections__main-product.liquid")
ps = R("v2/new_prev_section.liquid")
a = ps.index('''    {
      "type": "text",
      "id": "xmas_gift_start"''')
b = ps.index('''      "default": "eve"
    },''') + len('''      "default": "eve"
    },''')
settings = ps[a:b].replace('"default": "eve"', '"default": "box"')
anc = '''      "info": "PREVIEW ONLY. Keep OFF on the live theme - the elements show automatically 24 Nov - 26 Dec 2026.",
      "default": false
    },'''
assert sec.count(anc) == 1 and "xmas_gift_style" not in sec
sec = sec.replace(anc, anc + "\n" + settings)
W("g/new_main_section.liquid", sec)
print("ok")
