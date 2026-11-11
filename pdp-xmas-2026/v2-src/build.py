import sys
sys.path.insert(0, '.')
from hdr import R, W

s = R("a/prev/snippets__product-info.liquid")
gate_end = """  if dr_coll_handles contains 'featured-items' and product.tags contains 'Ready To Ship'
    assign dr_rts = true
  endif
-%}
"""
assert s.count(gate_end) == 1
gift_gate = """  comment
    Holiday gift card: own window, section settings xmas_gift_start / xmas_gift_end (YYYY-MM-DD, default 2026-12-01..2026-12-25)
  endcomment
  assign dr_gift_from = section.settings.xmas_gift_start | default: '2026-12-01' | remove: '-' | plus: 0
  assign dr_gift_to = section.settings.xmas_gift_end | default: '2026-12-25' | remove: '-' | plus: 0
  assign dr_gift_on = false
  if dr_xmas_today >= dr_gift_from and dr_xmas_today <= dr_gift_to
    assign dr_gift_on = true
  endif
  if section.settings.xmas_force_show
    assign dr_gift_on = true
  endif
-%}
"""
s = s.replace(gate_end, gate_end[:-len("-%}\n")] + gift_gate)
i = s.index("            {%- if dr_xmas_on -%}\n            <div class=\"dr-xmas-gift\">")
j = s.index("            {%- else -%}\n            <div class=\"ssky-product-freegift\">")
NEW = open("v2/gift.liquid", encoding="utf-8").read().replace("\r\n", "\n")
s = s[:i] + NEW + s[j:]
W("v2/new_prev_snippet.liquid", s)

sec = R("a/prev/sections__main-product.liquid")
anc = '''      "info": "PREVIEW ONLY. Keep OFF on the live theme - the elements show automatically 24 Nov - 26 Dec 2026.",
      "default": false
    },'''
assert sec.count(anc) == 1
sec = sec.replace(anc, anc + '''
    {
      "type": "text",
      "id": "xmas_gift_start",
      "label": "Holiday gift card: first day (YYYY-MM-DD)",
      "default": "2026-12-01"
    },
    {
      "type": "text",
      "id": "xmas_gift_end",
      "label": "Holiday gift card: last day (YYYY-MM-DD)",
      "default": "2026-12-25"
    },
    {
      "type": "select",
      "id": "xmas_gift_style",
      "label": "Holiday gift card: design",
      "options": [
        {"value": "eve", "label": "A - Christmas Eve (full-bleed)"},
        {"value": "box", "label": "B - The opened gift (split, burgundy)"}
      ],
      "default": "eve"
    },''')
W("v2/new_prev_section.liquid", sec)

for f in ["templates__product.json", "templates__product.remnant-constellation.json"]:
    t = R("a/prev/" + f)
    for style in ["eve", "box"]:
        u = t.replace('"xmas_force_show": true,', '"xmas_force_show": true,\n        "xmas_gift_style": "%s",' % style, 1)
        assert u != t
        W(f"v2/{style}__{f}", u)
print("ok")
