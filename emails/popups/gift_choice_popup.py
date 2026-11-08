"""Create the 'Gift choice — black or white studs' Klaviyo popup (draft) via the Forms API.
Publishing is done in the Klaviyo UI (the API only creates drafts). Daniel 5.11.2026."""
import json, os, sys, urllib.request, glob

BLACK = "https://cdn.klaviyomail.com/company/UEHusj/images/d40d6d65-4a9c-4977-ad32-43b1fcbc87b2.jpeg"
WHITE = "https://cdn.klaviyomail.com/company/UEHusj/images/66a849f8-e6f6-4cd4-8415-36c8f1ef8dd1.jpeg"
LIST = "XLRHrE"  # Subscribed -> welcome flow WPeiJQ
BG, TXT, MUTED, GOLD = "#0E0E0E", "#F4EFE6", "#A9A39A", "#C9A96E"
SERIF = "'Cormorant Garamond', Georgia, serif"

def html(s, pad=(0, 24, 0, 24)):
    return {"type": "html_text", "properties": {"content": s},
            "styles": {"padding": {"top": pad[0], "right": pad[1], "bottom": pad[2], "left": pad[3]}}}

def p(text, size=15, color=TXT, serif=False, bold=False, ls=None, upper=False):
    st = f"text-align:center;font-size:{size}px;color:{color};line-height:1.35;"
    if serif: st += f"font-family:{SERIF};"
    if bold: st += "font-weight:700;"
    if ls: st += f"letter-spacing:{ls};"
    if upper: st += "text-transform:uppercase;"
    return f'<p style="{st}">{text}</p>'

def button(label, action, extra=None, filled=True):
    b = {"type": "button", "properties": {"label": label}, "action": action,
         "styles": {"background_color": BG, "color": GOLD if filled else BG, "width": "fill", "height": 48,
                    "alignment": "center", "padding": {"top": 6, "right": 20, "bottom": 6, "left": 20},
                    "hover_background_color": "#B8975C" if filled else "#1C1C1C",
                    "border_styles": {"radius": 2, "style": "solid", "color": GOLD, "thickness": 1},
                    "text_styles": {"font_size": 14, "font_weight": 700, "character_spacing": 2,
                                    "text_color": BG if filled else TXT}}}
    if extra: b["properties"]["additional_fields"] = extra
    return b

def choice_image(src, alt, value):
    return {"type": "image", "properties": {"image": {"src": src, "alt_text": alt}},
            "styles": {"horizontal_alignment": "center", "width": 230, "padding": {"top": 10, "right": 8, "bottom": 6, "left": 8}}}

def nxt(): return {"type": "next_step", "submit": False}

def submit(): return {"type": "next_step", "submit": True, "properties": {"list_id": LIST}}

step1 = {"name": "Choose", "columns": [{"rows": [
    {"blocks": [html(p("A gift with your first order", 11, GOLD, bold=True, ls="3px", upper=True), (26, 24, 0, 24))]},
    {"blocks": [html(p("Black or white?", 34, TXT, serif=True), (4, 24, 0, 24))]},
    {"blocks": [html(p("Free natural diamond studs with orders from $2,000.<br>Which pair would you choose?", 15, MUTED), (2, 28, 4, 28))]},
    {"blocks": [choice_image(BLACK, "Black diamond studs", "black"), choice_image(WHITE, "White diamond studs", "white")]},
    {"blocks": [{"type": "email", "properties": {"placeholder": "Your email, to reserve them", "required": True,
                 "property_name": "$email", "show_label": False}}]},
    {"blocks": [button("I'D CHOOSE BLACK", submit(), [{"name": "gift_preference", "value": "black"}]),
                button("I'D CHOOSE WHITE", submit(), [{"name": "gift_preference", "value": "white"}], filled=False)]},
    {"blocks": [html(p("Reserved for your first order from $2,000. No spam, unsubscribe anytime.", 11, MUTED), (4, 24, 22, 24))]},
]}]}

step2 = {"name": "Success", "columns": [{"rows": [
    {"blocks": [html(p("You're in", 11, GOLD, bold=True, ls="3px", upper=True), (34, 24, 0, 24))]},
    {"blocks": [html(p("Your studs are reserved.", 30, TXT, serif=True), (4, 24, 0, 24))]},
    {"blocks": [html(p("Great choice. Watch your inbox, Daniel will write to you personally.", 15, MUTED), (2, 28, 8, 28))]},
    {"blocks": [button("CONTINUE BROWSING", {"type": "close", "submit": False})]},
    {"blocks": [html("", (0, 0, 24, 0))]},
]}]}

version = {
    "name": "Gift choice v1", "type": "popup", "status": "draft", "ab_test": False, "channel": "WEB",
    "steps": [step1, step2],
    "properties": {"show_close_button": True, "click_outside_to_close": ["both"], "record_utm_params_on_submit": True,
                   "accessible_name": "Choose your free diamond studs"},
    "styles": {"width": "medium", "background_color": BG,
               "input_styles": {"background_color": "#1A1A1A", "text_color": TXT, "placeholder_color": MUTED, "border_color": "#3A3A3A", "border_focus_color": GOLD, "corner_radius": 2, "field_height": 46}, "overlay_color": "rgba(0,0,0,0.6)",
               "border_styles": {"radius": 4, "style": "solid", "color": "#2A2A2A", "thickness": 1}},
    "triggers": [
        {"type": "delay", "properties": {"seconds": 20}},
        {"type": "page_visits", "properties": {"pages": 2}},  # UI: "Only display if all selected conditions are met" ON (8.11, Daniel)
        {"type": "url_patterns", "properties": {"allow_list": ["*/products/*"], "deny_list": ["*vip=join*", "*/checkout*", "*/checkouts/*", "*/cart*"]}},
        {"type": "unidentified_profiles"},
        {"type": "previously_submitted"},
        {"type": "after_close_or_submit_timeout", "properties": {"timeout_days": 5}},
    ],
}
body = {"data": {"type": "form", "attributes": {"name": "Gift choice — black or white studs", "status": "draft",
                                                 "ab_test": False, "definition": {"versions": [version]}}}}

if __name__ == "__main__":
    out = json.dumps(body, ensure_ascii=False)
    if "--dry" in sys.argv: print(out); sys.exit()
    envp = glob.glob(os.path.expanduser("~/OneDrive/Desktop/CLAUDE CODE PROJECTS/diana-rafael-marketing/connectors/klaviyo/.env"))[0]
    key = [l.split("=", 1)[1].strip().strip('"') for l in open(envp) if l.startswith("KLAVIYO") and "KEY=" in l][0]
    req = urllib.request.Request("https://a.klaviyo.com/api/forms", data=out.encode(), method="POST",
                                 headers={"Authorization": f"Klaviyo-API-Key {key}", "revision": "2026-10-15",
                                          "content-type": "application/vnd.api+json", "accept": "application/vnd.api+json"})
    try:
        r = urllib.request.urlopen(req); d = json.load(r); print("created", d["data"]["id"])
    except urllib.error.HTTPError as e:
        print(e.code, e.read().decode()[:3000])
