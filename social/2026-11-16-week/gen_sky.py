"""15.11 fix (Daniel): no flat black backgrounds -> one night-sky world behind the real jewel (AI world, real jewel always).
Generates the sky plates only (no jewelry, no text). export PYTHONUTF8=1 && python gen_sky.py"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "remnant-launch", "pipeline"))
from gemini_image import generate  # noqa: E402

COMMON = ("Photorealistic long-exposure astrophotography plate used as a luxury jewelry campaign backdrop. "
          "Palette strictly: deep blue-black ink night (#0F1418), soft champagne-sand gold (#CFB288) star dust, "
          "a few cool silver-white stars. Fine natural film grain, real camera, no CGI look. Calm, premium, cinematic. "
          "No people, no objects, no jewelry, no planets, no moon, no text, no logo, no watermark, no lens flare. ")
SKIES = {
    "sky-story-a": ("9:16", COMMON + "Vertical frame. The faint band of the Milky Way crosses diagonally from upper left to lower right, "
                    "dense with tiny stars and warm gold dust, with soft dark dust lanes. The centre of the frame is calmer and darker "
                    "(a jewel will be placed there). Tiny pinpoint stars, varied sizes, no big glowing orbs."),
    "sky-story-b": ("9:16", COMMON + "Vertical frame. A deep open star field with a soft warm gold nebula haze glowing low in the frame, "
                    "fading to pure deep ink at the top. The very bottom 15% is the soft black silhouette of a distant low desert ridge "
                    "under the stars. Pinpoint stars, varied sizes."),
    "sky-feed": ("4:5", COMMON + "Portrait frame. An even deep star field with a soft champagne-gold glow of the Milky Way core "
                 "behind the centre, darker towards the edges, very fine pinpoint stars."),
}


def one(k):
    asp, p = SKIES[k]
    out = os.path.join(HERE, "src", "sky", k + ".jpg")
    try:
        generate(p, refs=[], aspect=asp, size="2K", out=out)
        return k, "ok"
    except Exception as e:  # noqa: BLE001
        return k, f"FAIL {type(e).__name__}: {str(e)[:200]}"


if __name__ == "__main__":
    ks = sys.argv[1:] or list(SKIES)
    with ThreadPoolExecutor(3) as ex:
        for k, r in ex.map(one, ks):
            print(k, r, flush=True)
