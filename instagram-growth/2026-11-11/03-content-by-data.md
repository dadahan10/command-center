# What to post more of, by our own data

Source: Instagram Graph API, pulled 10.11.2026 with the story-scheduler token. That covers account insights for the last 30 days, follower demographics, and per-post insights for the newest 400 posts (back to 4.2021). Snapshot without the token: `data/ig-insights-2026-11-10.json`.

## The numbers

**Followers, last 30 days (12.10 to 10.11):** 10 accounts followed and 19 unfollowed or left Instagram, so **net minus 9**. Profile visits 167, website taps 19, accounts engaged 30, views 5,126. Daily reach ran from 3 to 233, with a median of about 40.

**Who follows us** (lifetime, 2,512 with a known country):
- Israel 702 (28%), **US 651 (26%)**, India 269, Indonesia 101, Brazil 86, UK 73.
- Top cities: Tel Aviv 112, Surat 92 (a diamond-trade city), Ramat Gan 48, New York 36.
- Ages 25-34: 39%, 35-44: 31%. Women 47%, men 35%, unknown 18%.
- The store sells to the US, but three quarters of the audience is somewhere else. That's why the engagement round (file 02) targets US bridal and jewelry audiences only.

**Best hours:** no usable data. `online_followers` comes back empty for this account, and our posts are too few per hour to compare (one 10:00 ET bucket holds the viral reel and nothing else). Keep posting at 9:00-12:00 ET (16:00-19:00 Israel), when the US is awake. We'll measure again after 4 weeks of steady posting.

**Formats, 2025 to today:**

| Format | Posts | Avg reach | Avg saves | Avg shares |
|---|---|---|---|---|
| Reels | 15 | 397 (210 without the winner) | 2.3 | 4.1 |
| Single images | 82 | 128 | 0.3 | 0.1 |
| Carousels | 46 | 107 | 0.6 | 0.2 |

Reels reach about 2x more than feed posts even without the winner. The API gives follows and profile visits only for feed posts. Of those, Noir Mystique (DRhXNoHD7Ej, a single black emerald-cut ring shot big) brought the most: 16 visits and 2 follows.

**The winner:** https://www.instagram.com/reel/DGyIYlGMBq-/. Reach 3,023, 31 saves, 56 shares. Next best is 4 saves and 4 shares. It is many black diamond rings on two hands, real footage, no text, and one question in the caption: "Would you say yes to a black diamond?" The 56 shares fit the couple funnel: she sends it to him.

**The last month vs January:**

| | Posts | Median reach | Saves | Shares |
|---|---|---|---|---|
| REMNANT story posts, 20.10 to 8.11.2026 (text-led covers, ring small on a pattern) | 10 | 57 | 0 | 1 |
| January 2026 product posts (one named ring, big in frame) | 8 | 243 | 4 | 5 |

Caveat: the January posts ran during a sale, and one month is a small sample. It's still about 4x on reach, and it points the same way as Daniel's 1.11 rule: show the jewel, big.

## Hooks and formats for the next 2 weeks (11.11 to 24.11)

**Do more:**
1. **Many jewels at once, real footage, as a reel.** This is the winner pattern. Open mid-motion on the full hand, and keep text to none or one question at the end.
2. **One ring, huge in frame, named in the first line.** This is the January pattern (Lunar Cascade 411, Pera Scura 406, Noir Mystique 349). The first caption line is the ring's name plus one concrete fact, not a manifesto.
3. **A question that is meant to be forwarded.** "Would you say yes to…", "Which one would you pick for me?" The ask is "send this to…", because shares are the metric that moved.
4. **Carousels only when each slide is a different ring.** The cover is all of them together and the last slide is the question.

**Do less:**
- Slogan covers where the text is the hero and the ring is small ("Everyone breaks", "You don't have to cover it up", "Soft is not the same as weak"): 0 saves across 10 posts. The REMNANT story still belongs in the caption body and in stories, just not as the thumbnail.
- Text on every frame. Daniel's rule already says text only when needed, and the winner had none.

**Cadence:** 3 feed items a week. At least 2 are reels, posted as Trial Reels per the reels plan (they reach non-followers first), and the winner gets shared to followers after 48 hours. Everything still goes through the Wednesday approval board. Nothing here gets queued on its own.

## Three concepts built on "many jewels together" (approved assets only)

No AI imagery in any of the three, so ai-image-qa doesn't apply. If a background is swapped (bg_swap.py) or a frame is retouched, it goes through ai-image-qa before Daniel sees it.

### Concept 1. Reel: "Would you say yes?" (the winner, re-shot from the same world)
- **Assets:** `Dropbox\שיווק Marketing\Images & Videos\Photoshoots - 14.3\Katya videos\187A8165-187A8178` (the pro shoot, all one world: same light, same lens). Use only the black-ring takes. The files are online-only in Dropbox, 1-4 GB each, so download first. Grade them to match the 14.3 EDITED stills.
- **Edit (7-9 s, ig-reel):** open on the frame where both hands are fullest (the hook comes from the middle). Then cut back to one hand with one ring, and add a ring on every beat until both hands are full again. Loop point = the opening frame.
- **Text:** none in the video. Caption first line: "Would you say yes to a black diamond?" Ask: "Send this to the person who'd be asking." (caption below, linted)
- **Why:** it repeats the only post that ever got 56 shares, but with new frames. Reposting the old reel would count as unoriginal content.
- **Overlap:** storyboard A ("Black or white?") uses the same footage. If A runs the week of 15.11, this runs the week of 22.11 with the remaining takes.

### Concept 2. Carousel: "Pick one for me" (10 slides, 1080x1350, ig-carousel)
- **Assets:** cover = a 14.3 EDITED frame with at least 3 rings in it (`Photoshoots - 14.3\EDITED`, Dmitriy Green). Slides 2-9 = one black diamond ring per slide from `14.3\EDITED`, `Photoshoots - Batch 4 - 22.10.24\Edited` and `Black Ice session - 28.2.24\Edited`. Vary the type of shot (on-hand, macro, flat) and never put two identical hand poses back to back (28.10 rule). Slide 10 = all of them again.
- **Copy:** each slide carries a small number and the ring's name (Champie Light/Bold), placed on clear ground, never over the hand or the stone. The cover has one line: "Pick one for me."
- **Caption ask:** "Send this to the person who'd have to choose." Search phrase in line 2: "black diamond engagement rings".
- **Why:** "many jewels together" combined with the share-to-partner mechanic. After it's posted it takes pinned slot 2.

### Concept 3. Reel: "The stack builds" (stop-motion from stills, one shoot)
- **Assets:** `Photoshoots - Batch 4 - 22.10.24\Edited` (105 edited frames). Pick 6-8 frames with the same hand position and light, and sequence them from 1 ring to full stack at 0.3-0.4 s per frame. If fewer than 6 frames match, this becomes a carousel. Never mix shoots in one reel ("one visual world").
- **Text:** none until the last frame; one word at most. The removal test decides.
- **Caption first line:** "How many is too many?" Ask: comment the number you'd stop at. That's a comment prompt, not a keyword DM, because DM automation isn't live.
- **Why:** many jewels plus a loop that rewards a second watch. It needs no new shoot.

## Sample caption, Concept 1 (linted with ig-caption/caption.py)
```
Would you say yes to a black diamond?

Natural black diamond engagement rings, every one made to order in solid gold. Light and dark in one ring.

Some people want the classic. Some people want the ring nobody else at the table is wearing.

Send this to the person who'd be asking.

#blackdiamondring #uniqueengagementring #alternativebride
```
Linter: first line 37 characters and fits whole, 3 hashtags, both search terms in the visible window, no links, no emoji. One WARN on "one ask": the linter doesn't recognise "Send this…" as an ask. Kept on purpose, because sharing is the action the data rewards.
