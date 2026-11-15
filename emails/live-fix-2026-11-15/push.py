"""Push out/<tid>.html into the live flow templates. DnD templates get one full-width HTML block (definition replaced);
SIMPLE/CODE templates get html. Usage: python push.py test | python push.py <tid> [<tid>...]"""
import json, re, sys, copy, kl
base = json.load(open("backup/base_clean.json", encoding="utf-8"))

def body_inner(html):
    # keep <style> (mobile rules) + the <body> content; the DnD shell supplies html/head/body
    styles = "".join(re.findall(r"<style.*?</style>", html, flags=re.S))
    b = re.search(r"<body[^>]*>(.*)</body>", html, flags=re.S).group(1)
    return styles + b

def definition(html):
    d = {"body": {"properties": base["body"]["properties"], "styles": {"background_color": "#e9e4da", "width": 600},
                  "sections": [{"content_type": "section", "type": "section",
                                "data": {"properties": {}, "display_options": {}, "styles": {"inner_padding_top": 0, "inner_padding_bottom": 0, "inner_padding_left": 0, "inner_padding_right": 0}},
                                "rows": [{"data": {"styles": {"column_layout": "1-column-full-width"}},
                                          "columns": [{"blocks": [{"content_type": "block", "type": "html",
                                                                   "data": {"content": body_inner(html), "display_options": {}}}]}]}]}]},
         "styles": base["styles"]}
    return d

def push(tid, html, editor):
    if editor == "SYSTEM_DRAGGABLE":
        attrs = {"definition": definition(html)}
    else:
        attrs = {"html": html}
    return kl.call("PATCH", f"templates/{tid}", {"data": {"type": "template", "id": tid, "attributes": attrs}})

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["test"]:
        html = open("out/RGSj5h.html", encoding="utf-8").read()
        s, d = kl.call("POST", "templates", {"data": {"type": "template", "attributes": {"name": "TEST dnd html block (delete)", "editor_type": "SYSTEM_DRAGGABLE", "definition": definition(html)}}})
        print("create", s, str(d)[:400]);
        if s in (200, 201):
            tmp = d["data"]["id"]; print("TMP", tmp)
            s2, r = push(tmp, html, "SYSTEM_DRAGGABLE"); print("patch", s2, str(r)[:300])
            s3, g = kl.call("GET", f"templates/{tmp}?fields[template]=html"); h = g["data"]["attributes"]["html"]
            open("preview/dnd-test.html", "w", encoding="utf-8").write(h); print("html len", len(h), "has CART5", "CART5" in h, "has for-loop", "{% for item" in h, "has style @media", "@media only screen and (max-width:620px)" in h)
            kl.call("DELETE", f"templates/{tmp}")
    else:
        ed = {"Re9UiL": "SIMPLE"}
        for tid in args:
            html = open(f"out/{tid}.html", encoding="utf-8").read()
            s, r = push(tid, html, ed.get(tid, "SYSTEM_DRAGGABLE"))
            print(tid, s, "" if s == 200 else str(r)[:400])
