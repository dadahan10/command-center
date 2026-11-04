"""Screenshot rendered email HTML files (desktop 680 wide) -> PNG. Usage: python shot.py out/render-X.html ..."""
import sys, os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sys.argv[1:]:
        for w, tag in ((680, "d"), (390, "m")):
            pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1)
            pg.goto("file:///" + os.path.abspath(f).replace("\\", "/"))
            pg.wait_for_timeout(1500)
            pg.screenshot(path=f.replace(".html", f"-{tag}.png"), full_page=True)
            pg.close()
    b.close()
