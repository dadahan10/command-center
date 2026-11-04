"""VIP confirmation (flow RRcbwY, message V5gEYq, template TLp5wQ) - layout 'Sealed invitation' (noir).
Image job: make the reader feel chosen / inside -> a sealed black envelope with a gold wax seal and a brass key
under one spotlight at the studio after hours (new image, no jewelry drawn by AI)."""
from rd import *

T = "noir"
th = THEMES[T]


def build():
    card_p = f'style="margin:0 0 14px;font-family:{SANS};font-size:16px;line-height:1.65;color:#2a241d;"'
    card = f"""<tr><td class="pad" style="padding:0 32px;">
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#f3ead9" style="background:#f3ead9;border:1px solid {GOLD};">
<tr><td style="padding:6px;"><table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="border:1px solid #d9c79c;">
<tr><td align="center" style="padding:34px 30px 6px;font-family:{SANS};font-size:11px;letter-spacing:.3em;text-transform:uppercase;font-weight:700;color:#7a5d1e;">Black Friday 2026 · Private list</td></tr>
<tr><td align="center" style="padding:10px 30px 8px;"><h1 class="h1" style="margin:0;font-family:{SERIF};font-size:42px;line-height:1.08;font-weight:500;color:#1f1b16;">You're on the list,<br/><i>{{{{ first_name|default:'friend' }}}}.</i></h1></td></tr>
<tr><td align="center" style="padding:6px 30px 22px;"><div style="width:40px;height:1px;line-height:1px;font-size:1px;background:{GOLD};">&nbsp;</div></td></tr>
<tr><td class="pad" style="padding:0 38px 18px;">
<p {card_p}>Thank you for joining. Here's what being on the VIP list means:</p>
<p {card_p}>&#8212; <b>Every Black Friday offer reaches you days before everyone else</b>, straight to this inbox.<br/>&#8212; <b>Gifts with orders above certain amounts are coming</b>, and you'll hear about them first.</p>
<p {card_p}>There's nothing else you need to do. Keep an eye on emails from us over the next few weeks. That's where your early access will arrive.</p>
<p {card_p} >In the meantime, if there's a piece you've had your eye on, tell me which one. Reply to this email or <a href="https://wa.me/97235755066" target="_blank" style="color:#7a5d1e;text-decoration:underline;">message me on WhatsApp</a>, and I'll make sure you have everything you need to decide before the offers open.</p>
</td></tr>
<tr><td class="pad" style="padding:0 38px 30px;"><p style="margin:0 0 4px;font-family:{SERIF};font-style:italic;font-size:22px;color:#1f1b16;">Glad to have you close,</p>
<p style="margin:0;font-family:{SANS};font-size:14px;color:#7a5d1e;">Daniel, Diana Rafael</p></td></tr>
</table></td></tr></table></td></tr>"""
    html = (head(T, "Black Friday offers reach you days before everyone else.")
            + logo(T, pad="26px 40px 20px", width=190)
            + hero(IMG["vip"], "A sealed black envelope with a gold wax seal and a brass key on black slate", href="https://dianarafael.com/collections/new-arrivals")
            + spacer(30) + card + spacer(10)
            + button(T, "See what's new", "https://dianarafael.com/collections/new-arrivals", pad="22px 40px 18px")
            + trust(T) + foot(T))
    return html


if __name__ == "__main__":
    import sys
    open(sys.argv[1] if len(sys.argv) > 1 else "vip.html", "w", encoding="utf-8").write(build())
