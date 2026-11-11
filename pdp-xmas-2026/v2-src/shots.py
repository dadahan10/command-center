import asyncio, sys
from playwright.async_api import async_playwright

OUT = "C:/Users/USER/OneDrive/Desktop/CLAUDE CODE PROJECTS/command-center/pdp-xmas-2026/"
TID = "185714540713"
TAG = sys.argv[1]  # e.g. a-eve
P = {"mto": "kintsugi-natural-black-diamond-engagement-ring",
     "rts": "portal-compass-natural-black-diamond-cushion-engagement-ring"}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for dev, vp, mob in [("mobile", {"width": 390, "height": 844}, True),
                             ("desktop", {"width": 1440, "height": 900}, False)]:
            for k, h in P.items():
                ctx = await b.new_context(viewport=vp, is_mobile=mob, has_touch=mob, device_scale_factor=2)
                pg = await ctx.new_page()
                await pg.goto(f"https://dianarafael.com/products/{h}?preview_theme_id={TID}", wait_until="load", timeout=90000)
                await pg.wait_for_timeout(4500)
                await pg.keyboard.press("Escape")
                for sel in ['button:has-text("Decline")', 'button:has-text("Accept")', '[aria-label="Close dialog"]', 'button[aria-label="Close"]']:
                    try:
                        bt = pg.locator(sel).first
                        if await bt.is_visible():
                            await bt.click(); await pg.wait_for_timeout(500)
                    except Exception:
                        pass
                # hide the Shopify preview bar so it does not cover the card
                await pg.add_style_tag(content="#preview-bar-iframe,#PBarNextFrameWrapper{display:none!important}")
                info = await pg.evaluate("""()=>({theme:Shopify.theme&&Shopify.theme.id,card:(document.querySelector('.dr-xg')||{}).className||null,
                    img:(()=>{const i=document.querySelector('.dr-xg img');return i?[i.complete,i.naturalWidth]:null})(),
                    ship:(document.querySelector('.dr-xmas-ship')||{}).innerText||null})""")
                print(dev, k, info)
                await pg.evaluate("""()=>{const e=document.querySelector('.dr-xg'); if(e){e.querySelector('img').loading='eager'; e.scrollIntoView({block:'center'});}}""")
                await pg.wait_for_timeout(2500)
                await pg.add_style_tag(content="[class*=cookie],[id*=cookie],#shopify-pc__banner,.shopify-pc__banner__dialog{display:none!important}")
                for sel in ['button:has-text("Decline")']:
                    try:
                        bt = pg.locator(sel).first
                        if await bt.is_visible():
                            await bt.click(); await pg.wait_for_timeout(600)
                    except Exception:
                        pass
                await pg.evaluate("()=>{const e=document.querySelector('.dr-xg'); if(e) e.scrollIntoView({block:'center'});}")
                await pg.wait_for_timeout(800)
                await pg.screenshot(path=f"{OUT}v2-{TAG}-{dev}-{k}.png")
                await ctx.close()
        await b.close()

asyncio.run(main())
