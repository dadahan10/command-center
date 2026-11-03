# ניתוח פלואים קיימים ב-Klaviyo + מבנה מוצע לבנייה מחדש — 3.11.2026

> ניתוח קריאה-בלבד. לא נוצר, נערך, הושהה או נמחק שום דבר ב-Klaviyo.
> מקורות: `get_flow` (definition מלא), `get_flow_report`, `get_campaigns`, `get_campaign_report`, `render_email_template` (התוכן של כל מייל).
> מבוסס על האפיון של דניאל מ-3.11 (`memory/feedback_klaviyo_flows_spec.md`).

---

## 0. ממצאי-על (לקרוא קודם)

1. **ה-Browse וה-Cart לא תלויים באינטגרציית Shopify.** הטריגרים `Viewed Product` (RdGtZY) ו-`Added to Cart` (RjxRum) הם מטריקות **API / onsite** (Klaviyo.js), לא Shopify. רק `Checkout Started`, `Placed Order`, `Fulfilled Order`, `Ordered Product` ו-`Delivered Shipment` מגיעים מ-Shopify. כלומר החזרת האינטגרציה ב-3.11 מחיה את ה-checkout ואת הפוסט-פרצ'ס, אבל **לא בהכרח את ה-Browse וה-Cart**.
   - Y6Zunh שלח בסך הכול ל-**4** אנשים ב-12 החודשים האחרונים (ול-89 בשנה שלפניהם).
   - Y3ZV7x ו-UrfQ29 שלחו ל-**0**.
   - קיימת גם מטריקת Shopify בשם `Added to Cart` (WT7SJV). כדאי לבדוק איזו מהשתיים באמת יורה, ולבנות עליה.
2. **באג חשוד ב-Y6Zunh:** פילטר הפרופיל כולל `Viewed Page = 0 since flow start`. כל גולש שממשיך לדפדף באתר אחרי שצפה במוצר יוצא מהפלואו לפני שהמייל הראשון יוצא (מייל ראשון אחרי 2 שעות). זו כנראה הסיבה העיקרית לנפח האפסי. (השערה — לאמת מול מספר האירועים ב-RdGtZY.)
3. **ה-Welcome הנוכחי (WPeiJQ) כמעט לא קיים לרוב המנויים.** המייל השני מתפצל לפי `chosen_diamond / shopping_for = white`:
   - **מסלול Black** (כ-1,500 מקבלים בשנה הקודמת, כ-92%): מקבל **4 מיילים בלבד** ונגמר אחרי כ-6 ימים.
   - **מסלול White** (כ-120 מקבלים): מקבל סדרה של 13 מיילים, רובה חינוך על יהלומים **לבנים** (Clarity Enhanced, Light Performance ×3, Certificates, Golden, Geometric Albedo).
   - בנוסף, פילטר הפרופיל מוציא מה-Welcome כל מי שעשה Add to Cart או Checkout. זה סותר את העיקרון "Welcome שלא נגמר".
4. **מסירות (deliverability):** פלואי ה-checkout קיבלו **4.5% open** (VB4v4q, 1,084 מקבלים) ו-**9% open** (XW6UqR, 1,756 מקבלים) בשנה הקודמת. בפוסט-פרצ'ס, באותה תקופה, ה-open היה 58%–71%. גם הקמפיינים ירדו מכ-22% open (2024–2025) לכ-10% (2025–2026).
   - הסבר אפשרי 1: הרבה פרופילי checkout הם בוטים או כתובות זבל.
   - הסבר אפשרי 2: המיילים נוחתים בספאם.
   - לפני שמאריכים את הפלואים, צריך לבדוק Google Postmaster, DMARC ואת שיעור ה-spam. פלואים ארוכים לנמענים קרים מעלים תלונות.
5. **הפרות של כללי הבית ובאגים בתוכן הקיים** (פירוט מלא בסעיף 3):
   - **מספר ביקורות ישן:** "400" ו-"450+" (הנכון: 530+).
   - **מילות dark:** "Dark Side", "shine darkly", ובקמפיין "When Darkness Meets Light".
   - **דדליינים מזויפים:** "cart about to expire", "24 hours", "48 hours", "Last chance", "going fast", "will disappear".
   - **הנחה בנושא שלא קיימת בגוף המייל:** 5% / 15% / "exclusive offer".
   - **קוד אחד, שני ערכים:** `DIAMOND` הוא 10% במייל אחד ו-5% במייל אחר.
   - **סף עגילים חינם לא עקבי:** Free studs ב-$2000 במקום אחד וב-$3000 במקום אחר.
   - **לינקים שבורים:** לינק פגישה בפורמט `http://#https://…`, ו-`http://customercare@` במקום mailto.
   - **לינקים שמוציאים מהאתר:** לינקי ביקורות שמובילים ל-**Etsy**.
   - **דומיין שגוי:** כרטיסי מוצר מקושרים ל-**diana-rafael.myshopify.com** במקום לדומיין האתר.
   - **זמן ייצור:** במייל האישור כתוב "7-10 business days". הכלל הוא "ships within 10 business days".
   - **שליחה מוקדמת:** "on its way" נשלח לפני שהפריט נשלח בפועל.
   - **ציטוט ביקורת:** ציטוט חתום "-Daniel-" שמודה ל-Daniel חוזר ב-8 תבניות.
   - **כתובת שולח שגויה:** `cutomercare@dianarafael.com` בכל מיילי UrfQ29.
   - **פגישה:** הלינקים בתבניות הם ל-Calendly של 30 דק'. הכלל הוא 15 דק'.
   - **WhatsApp:** לא מופיע באף מייל.

### מילון מטריקות (לקריאת התנאים)

| ID | שם | מקור |
|---|---|---|
| RdGtZY | Viewed Product | API (onsite) |
| RjxRum | Added to Cart | API (onsite) |
| WT7SJV | Added to Cart | Shopify |
| UgasKH | Checkout Started | Shopify |
| T6KBRR | Placed Order | Shopify |
| Yu3gpi | Fulfilled Order | Shopify |
| RijJmn | Ordered Product | Shopify |
| Uin4Gb | Delivered Shipment | Shopify |
| R6e7eC | Package delivered | Klaviyo shipping |
| Tt7p6A | Viewed Page | API |
| XdZba4 | Clicked Email | Klaviyo |
| Ypq23U | Opened Email | Klaviyo |
| Xtibzp | Subscribed to SMS | Klaviyo |
| SSDYK7 | Ready to review | Klaviyo Reviews |
| UF5SfA | Submitted review | Klaviyo Reviews |
| list VS2G3K | SMS Subscribers | — |
| list XLRHrE | Subscribed (single opt-in) | — |

### ביצועים: שתי תקופות
עמודת "12ח' אחרונים" מכסה 3.11.25–3.11.26. אירועי Shopify מתים ממרץ 2026, לכן **אפסים ב-2026 לא אומרים כלום**. עמודת "שנה קודמת" מכסה 3.11.24–2.11.25 ומשמשת כבנצ'מרק. ההמרות הן Placed Order מיוחס.

| Flow | 12ח' אחרונים: נמענים / open / click / conv / $ | שנה קודמת: נמענים / open / click / conv / $ |
|---|---|---|
| WPeiJQ Welcome | 158 / 28% / 1.4% / 0 / 0 | 8,494 / 11.8% / 0.61% / 3 / $9,110 |
| WbFMJh Custom design | 12 / 42% / 0 / 0 / 0 | 55 / 21% / 0 / 1 / $5,500 |
| Y6Zunh Browse | 4 / 0 / 0 / 0 | 89 / 31% / 2.3% / 0 |
| Y3ZV7x Cart BI | 0 | 246 / 30% / 2.4% / 0 |
| UrfQ29 Cart non-BI | 0 | 83 / 27% / 0% / 0 |
| VB4v4q Checkout non-BI | 135 / 12% / 0% / 0 (1 unsub) | 1,084 / 4.5% / 0.19% / 0 |
| XW6UqR Checkout BI | 109 / 17% / 1% / 0 | 1,756 / 9% / 1.2% / 1 / $1,350 |
| WvEmp7 Order Placed | 101 / 52% / 6.9% / 1 / $592 | 314 / 58% / 9.9% / 0 |
| W6eUNC Order Fulfilled | 67 / 48% / 25% / 0 | 223 / 71% / 42% / 0 |
| WTfhxp Review request | 64 / 52% / 9.4% / 0 | 152 / 54% / 5.3% / 0 |
| Tc6EaJ Cross-sell BI | 0 | 15 / 53% / 13% / 0 |
| Ye7y3T Cross-sell White | 1 | 1 |
| VtbjEg Winback | 50 / 45% / 2.1% / 0 | 161 / 37% / 3.1% / 0 |

**קריאה:** אף פלואו נטישה לא הביא הכנסה מיוחסת אמיתית בשנתיים האחרונות (מלבד $1,350 אחד). ההכנסה המיוחסת הגיעה מה-Welcome (3 הזמנות, $9.1K) ומה-Custom design (1 הזמנה, $5.5K). בפוסט-פרצ'ס, מייל ה-tracking (RSn7b3) עם 55% click ומייל ה-Form 5106 (VQTTX3) עם 76% click הם הכי "נקראים" בחשבון: לקוחות קוראים מיילים תפעוליים.

---

## 1. פירוט כל פלואו קיים

סטטוס בפלואו: **live** = נשלח, **manual** = וריאציית A/B שלא רצה, **draft** = טיוטה (לא נשלח).

### 1.1 WPeiJQ — "Welcome Flow Pop Up subscribers (clone)" (live)

**טריגר:** Added to List `Subscribed` (XLRHrE, single opt-in).

**פילטר:** Added to Cart = 0, Checkout Started = 0 ו-Placed Order = 0 since flow start. כלומר יוצאים מהפלואו בכל פעולת עגלה.

| # | זמן | שלב / תנאי | Subject / Preview | סטטוס | תוכן / התנגדות |
|---|---|---|---|---|---|
| — | +10h | Split: country = United Kingdom | | | |
| 1 UK | | A/B (draft experiment) | "Dive into Diana Rafael's Celestial world 🖤💍" (XLniKA) + 2 וריאציות "Welcome to Diana Rafael's universe" / "Welcome to Diana Rafael!" (Vogue UK, 19.4.25) | live | כמו #1 הכללי. אין שום תוכן ספציפי ל-UK. **הפיצול מיותר.** |
| 1 | | | "Welcome to Diana Rafael- Let's Make Your Style Shine ✨" (QNVBAL) | live | Since 2014, "1000 customized pieces", 5-star. בחירה בין "Shop White Side" ל-"Shop **Dark Side**" (redirect שקובע את הענף). פתק CEO + Book Design Meeting. **אמון + זהות.** |
| — | +2d | Split: chosen_diamond=white AND shopping_for=White Diamond | | | |
| 2W | | white | "{{first_name}}, exclusive Offer Inside!" (TLLjZ7) | live | 4 מוצרים לבנים עם מחירים קשיחים + באנר "Free Black Diamond Studs $2000+". **אין offer בטקסט.** |
| 2B | | black | אותו subject (VeFc82) | live | סיפור Black Ice ("night skies, nebulas… shine **darkly**"), באנר studs. **אין offer.** |
| — | +1d | Split: viewed "Book Online Appointment" ב-30 ימים (ב-B גם: opened email ב-30 ימים) | | | |
| 3 | | true | "Book Your Online Appointment Now!💍💎" (XmC725 / R2Nnur) + SMS "it's Daniel" (Calendly 30min) | live | פגישה עם דניאל. **צורך באדם.** |
| 4 | +1d | | "Enhance Your Experience: Complete Your Customer Profile" (WJB4ps / Wq62ZS) | live | טופס KYC → /pages/get-to-know-you-better… |
| — | +1d | Split: SMS Subscribers → SMS welcome | | | |
| 5 | | | "Your Personal Design Meeting Awaits" (Uja8gk / TYD6SL "+10%") | live | פגישה. **ה-10% מהשם לא מופיע בטקסט.** |
| 6B | +1d | black | "Black Ice Magic" (XzuRTJ) | live | 4 מוצרי Black Ice + פגישה. **סוף מסלול Black.** |
| 6W | +2d | white | "Your Sparkle Matters ✨" (RTHc9e) | live | בחירה בין Black ל-White. |
| 7W | +2d | A/B draft | "About Diana Rafael" (XgYQEF + 2 וריאציות live) | live | סיפור מותג (כולו תמונות). |
| 8W | +3d | | "Your custom design ✨💍" (W2WKrr) | live | תהליך עיצוב אישי (תמונות). |
| 9W | +4d | | "Why Diana Rafael?" (VpVGNN) | live | USPs (תמונות). |
| 10W | +7d | | "Diamond Knowledge - Why Clarity Enhanced Diamonds are the Answer" (Rc4Tbd) | live | חינוך יהלום לבן. **Off-brand.** |
| 11W | +14d | | "What is Diamond Light Performance?" (ULUEcb) | live | לבן. |
| 12W | +14d | | "Diamond Knowledge - Light Performance - Terms, Science…" (YmLrd9) | live | לבן. |
| 13W | +14d | | "Light Performance in Elongated Shaped Diamonds…" (VWjv63) | live | לבן. |
| 14W | +14d | | "The Truth About Diamond Certificates" (Vjistq) | live | לבן, מחירים מחוקים ישנים. |
| 15W | +14d | | "Clarity Enhanced Diamonds vs. Non Enhanced" (R7rCPP) | live | לבן. |
| 16W | +14d | | "Indroduction: Golden Diamond Collection" (UGhpQM) | live | טבעות חותם זהב, $900. ייתכן שקולקציה ישנה. |
| 17W | +14d | | "Intuducrtion: Geometric Albedo" (SgQtHF) | live | לבן. |
| 18W | +14d | | "Why People Are Buying Black Diamond Rings" (VRGeJD) | live | **המייל היחיד באורך on-brand.** |

**לוגיקה:** בחירת צבע → הצעה → פגישה → KYC → פגישה → (Black: מוצרים וסוף) / (White: סדרת חינוך ארוכה). הפיצולים בנויים על תכונת ה-redirect, ועל SMS שכמעט לא בשימוש (1 SMS בשנה).

### 1.2 WbFMJh — "Welcome Series - custom design questionnaire" (live)
- **טריגר:** Added to list RbxaPN (שאלון עיצוב). **פילטר:** Placed Order = 0.
- **+2d:** "Let's craft magic together 🌟" / "Book Your Personal Design Consultation" (VyEK7E). מכתב אישי מדניאל ("Your requests have reached me directly") + Book a meeting + Lifetime warranty.
- **+1d:** אם נרשם ל-SMS → SMS עם Calendly.
- **ביצועים:** הזמנה אחת של $5.5K מ-55 נמענים. **שומרים** (מעדכנים ל-15 דק' + WhatsApp).

### 1.3 Y6Zunh — "Viewed product (Browse Abandonment)" (live)

**טריגר:** Viewed Product (API).

**פילטרים:**
- Placed Order = 0, Checkout Started = 0 ו-Added to Cart = 0 since start
- **Viewed Page = 0 since start** (ראו §0.2)
- לא היה בפלואו ב-30 הימים האחרונים. Re-entry: 30 יום.

| # | זמן | Split | Subject / Preview | תוכן / התנגדות |
|---|---|---|---|---|
| — | 0 | **Split A:** Clicked Email ב-10 ימים | | |
| 1 | +2h | true | "Did you see something you like?" / "Ready to make it yours? 🛍️" (S6GMed, A/B completed) | "Had your eyes on this item? Need help… Want to personalize?" בלוק מוצר, "Free Expedited & Insured Shipping Worldwide", פס אמון, פגישה. **צורך בעזרה + משלוח.** |
| 1' | +2h | false | אותו subject (WG6TBv) | **טקסט זהה.** ההבדל הוא רק בעיצוב הפוטר. |
| — | | **Split B** (רק במסלול A): ב-SMS Subscribers? → +1d SMS "We love that you love the {{product}}" | | |
| 2 | +1d | | "Why You Should Count on Us? 💍" / "Over **400** 5-star reviews!" (VFyyfb) | "This item is going fast" (**דחיפות מזויפת**), ציטוט ביקורת, לינק ל-**Etsy**, פגישה. **אמון.** |
| 3 | +2d | A/B draft | "Enjoy Flexible Layaway Options with Affirm at Diana Rafael!" (SQtzKD) | Affirm. לינק פגישה שבור. **מחיר.** |
| 4 | +1d | | "✨ Last Chance for 10% Off - Claim Now!" (RtFJBA) | 10% עם קוד `DianaRafael`. "Last chance" בלי דדליין. **מחיר.** |

**מה הפיצולים עושים והאם צריך אותם:**
- **Split A (Clicked Email ב-10 ימים):** מפריד בין שתי גרסאות עם **אותו טקסט**. אין לו ערך → **להוריד.**
- **Split B (SMS list):** שולח SMS רק במסלול A. היה SMS אחד בשנה → **להוריד**, אלא אם דניאל מתכנן להחיות SMS.
- **פילטר Viewed Page:** **להוריד** (הורג את הפלואו).
- **פילטרי Placed Order / Checkout / Added to Cart:** **לשמור.** הם מעבירים את האחריות לפלואו המתקדם יותר.

### 1.4 Y3ZV7x — "Add to Cart - (Black Ice)" (live)

**טריגר:** Added to Cart (API) כש-`Categories contains "Black Ice"`.

**פילטר:** Checkout Started = 0 ו-Placed Order = 0 since start, ולא היה בפלואו ב-30 יום. Re-entry: 30 יום.

| # | זמן | Split | Subject / Preview | תוכן / התנגדות |
|---|---|---|---|---|
| — | +2h | Placed Order = 0 ב-30 יום (אחרת יציאה) → SMS consent? | | |
| 1 | | SMS: "Love it? Need it? Gotta have it?…" ואחרי +5h מייל (UypUrF) / בלי SMS: מייל (S3HdXt) | "Will You Leave All That Black Ice Beauty In Your Cart?" (בלי preview) | באנר "Free Black Diamond Studs $2000+", "YOU HAVE A GREAT TASTE… make it yours", Return to cart, פס אמון (Insured express, 30-day returns, certificate), באנר Affirm, "CHAT WITH OUR EXPERT". **תזכורת + אמון + אדם.** |
| 2 | +22h | A/B completed | "Extra 5% Inside Just For you!" / "Your cart is about to expire- Shop it Now" (RqGbkQ) | "Don't Forget Your Sparkle" + "The Power of Black Diamonds" + "Over **450+** 5-star reviews". **ה-5% לא קיים בגוף המייל.** **איכות/אותנטיות של black diamond + הוכחה חברתית.** |
| 3 | +1d | A/B draft | "Enjoy Flexible Layaway Options with Affirm" (YApHnL) | Affirm. לינק פגישה שבור. נחתם "valued customer… serving you again". **מחיר.** |
| 4 | +2d | | "Exclusive Offer: Shop Now with Affirm & Save 15%!" (UnwTKb) | **בגוף: 10% עם AFFIRM10** (לא 15%). Studs $2000+, ביקורת. **מחיר.** |

### 1.5 UrfQ29 — "Add to Cart- (Not Black Ice)" (live)

**טריגר:** Added to Cart (API) כש-Categories not-contains "Black Ice". **פילטר:** Placed Order = 0 ו-Checkout = 0. **שולח:** `cutomercare@` (שגיאת כתיב).

| # | זמן | Subject | תוכן / התנגדות |
|---|---|---|---|
| 1 | +2h (SMS או מייל; למנויי SMS המייל אחרי +4h) | "Will You Leave All That Sparkle In Your Cart?" / "Leaving all this BLING behind?" (WdFHwC) | "This item is going fast" (**מזויף**), פס אמון, ביקורת ארוכה, פגישה. **אמון + דחיפות.** |
| 2 | +1d | "Leaving all this SPARKLE 💎?" (Tgp4Lf) | אותו תוכן. לינק ביקורות ל-**Etsy**, תמונת מוצר ריקה. |
| — | +2d | Split: נרשם ל-SMS ב-30 יום → SMS "Still thinking about that SPARKLE?" | |
| 3 | +1d | "Enjoy Flexible Layaway Options with Affirm" (VnYnGP) | זהה ל-SA72eG. "Start shopping" מוביל ל-**Black Ice** (בפלואו של non-BI). **מחיר.** |
| 4 | +3d | "Exclusive Offer: Shop Now with Affirm & Save 10%!" (UHAzSf) | AFFIRM10 10%. Studs **$3000+** (סותר את ה-$2000 במקום אחר). "Shop Black Ice Shop Engagement Rings" (כפילות בכפתור). **מחיר.** |

### 1.6 VB4v4q — "Abandoned Checkout - NOT Black Ice" (live)

**טריגר:** Checkout Started כש-Collections not-contains "Black Ice". **פילטר:** Placed Order = 0, ולא היה בפלואו 7 ימים. Re-entry: 7 ימים.

| # | זמן | Split | Subject / Preview | תוכן / התנגדות |
|---|---|---|---|---|
| 1 | +2h | | "Is This the One? 💍" / "Save 10% OFF on your first order!" (StMn7j) | "Your Love Story Deserves This One-Of-A-Kind Ring", **10% קוד DIAMOND**, פס אמון, פגישה. **מחיר + אמון.** |
| — | +20h | **Opened Email = 0 alltime?** | | |
| 2 | | true (מעולם לא פתח) | "Your cart is about to expire." (THZmcx) | **5% קוד DIAMOND** (סותר את #1), 4 מוצרים קשיחים על myshopify, ביקורת, פגישה, עיצוב אישי. **דדליין מזויף.** |
| 2' | | false | SMS: "complete your cart… or secure a 1-on-1 online appointment" (Calendly) | **אדם.** |
| 3 | +16h | | "Why DIana Rafael?" / "You should only choose your jewelrt once…" (R4hG8Q) | כולו תמונות (USPs) + פגישה. **אמון/לגיטימיות.** |
| 4 | +2d | | "Your Sparkle is About to Fade Away 💫💎" (TExD4m), from "Daniel of Diana Rafael" | "Here is a little treat" (ההטבה בתוך תמונה; לא ידוע מה היא). אין כפתור טקסט. **מחיר.** |
| 5 | **0 (מיד אחרי #4)** | | "Have Any Questions? Let's Meet!" (SP9bMD) | "Crafting Brilliance: Your Personal Design Meeting", warranty. **אדם + עיצוב אישי.** ⚠️ **נשלח באותה דקה כמו #4 (באג).** |
| 6 | +16h+1d | | "Enjoy Flexible Layaway Options with Affirm" (TxkYX7) | Affirm, לינק שבור. "shopping" מוביל ל-Black Ice. **מחיר.** |
| — | +1d | Split: Opened Email ב-2 ימים | | |
| 7 | | true | "Exclusive Offer: Shop Now with Affirm & Save 10%!" (Rru67M) | AFFIRM10 + "**valid for 48 hours**" (**מזויף**), לינק ל-Etsy. **מחיר + דחיפות.** |

### 1.7 XW6UqR — "Checkout started (Abandoned Cart - Black Ice)" (live)

**טריגר:** Checkout Started כש-Collections contains "Black Ice". **פילטר:** Placed Order = 0.

| # | זמן | Subject / Preview | תוכן / התנגדות |
|---|---|---|---|
| 1 | +2h (A/B completed) | "Is This the One? 💍" / "Complete your purchase now to make it yours!" (TJe6Mg) | Studs $2000+, "Your Love Story Deserves This One-Of-A-Kind Ring", טבלת עגלה, פגישה. **תזכורת + אדם.** |
| — | +20h | Split SMS → SMS "…enjoy **15% OFF**" (אין קוד) / אחרת +1d | |
| 2 | +1d (A/B completed) | "Extra 5% Off Inside—Just for You!" / "Your Cart Is About To Expire..." (T7d4aD) | "YOUR CART IS ABOUT TO EXPIRE… sell out quickly… next 24 hours" (**מזויף**). **ה-5% לא קיים בגוף.** פגישה, פס אמון. **דחיפות + אדם.** ההמרה היחידה ($1,350) יוחסה למייל הזה. |
| 3 | +1d | "Last Chance to Save on Your Favorite Items! Find" (RRaWVp) | "SOON, YOUR BELOVED PIECE… WILL DISAPPEAR" (**מזויף**), ביקורת "-Daniel-", Affirm. **אמון + מחיר.** |
| 4 | +2d (A/B draft) | "Enjoy Flexible Layaway Options with Affirm" (XesBsQ) | Affirm, לינק שבור. **מחיר.** |
| 5 | +1d | "Unlock 10% Off – Shop Now & Pay Over Time!" / "Your exclusive code is inside!" (T2zMPf) | AFFIRM10 10% sitewide, studs, פס אמון. **מחיר.** |

### 1.8 WvEmp7 — "Post Purchase - Order Placed | A" (live)
**טריגר:** Placed Order. **אין פילטר.**

| # | זמן | Split | Subject / Preview | סטטוס | תוכן |
|---|---|---|---|---|---|
| 0 | +5m | | SMS אישור הזמנה | live | |
| 1 | +5m | | "Sparkle in style - Order confirmed! ✨🤩" / "Thank You For Your Order" (R4RTxX) | live | אישור; Form 5106 מעל $2500; "Most items will be manufactured and ship within a **7-10** business days"; FedEx/DHL, insured, חתימה. **אין מילה על מכס.** |
| — | +1d | Placed Order count = 1 / = 2 / יותר | | | |
| 2a | | קונה ראשון | "Thank you! Your Choice Is Top-Notch." (WinQxN) | live | Light Performance (לבן), Read our story, ביקורת "-Daniel-". |
| 2b | | קונה שני | "Thank You Again! You Taste Is Still Excellent." (SygyQ4) | live | Jewelry Care Program, best sellers ריקים. |
| 2c | | 3+ | אותו subject (RmCHNM) | live | ← **סוף.** |
| 3 | +4d | | "We'd Love to Get to Know You Better 💍" (Y6Wbph / S5te7Y) | live | סקר VIP buyers (`/pages/diana-rafael-vip-buyers`). |
| 4 | +2d / +1d | | "Discover Your Unique Sparkle🌟" / "While you're waiting…" (WyBKHd / Su9J5c) | live | היסטוריית black diamonds + cross-sell עם מחירים קשיחים. **"on its way" בזמן שהפריט עוד בייצור.** ההמרה היחידה ($592). |
| — | +8d | Fulfilled ב-12 / 30 יום? | | | |
| 5 | +2d | fulfilled | "How do you like the item?" (QTy5Yx live; VXfHec draft) | live/draft | בקשת ביקורת. **לינק שבור ("/products/").** |
| 5' | | not fulfilled | "Email #3 Sorry for the delay" (SZqYPR, ULTSey) | **draft, בלי תבנית** | — |
| 6 | +4d | | "Email #9 Our Latest Collections" (WX4hmQ) | **draft, בלי תבנית** | — |

### 1.9 W6eUNC — "Order Fulfilled (Post Purchase Flow)" (live)
**טריגר:** Fulfilled Order. **אין פילטר.**

| # | זמן | Split | Subject | תוכן |
|---|---|---|---|---|
| 1 | 0 | | "Your Order Is On The Move!" / "We're So Excited" (RSn7b3) | "IT'S HEADING YOUR WAY!", מספר מעקב + "CLICK HERE TO TRACK YOUR ORDER", פס אמון, cross-sell של wedding bands (myshopify). **55% click.** אין מכס, אין "שילמנו את המשלוח". ברכה עם משתנה ריק ("Hi . 💎"). |
| — | +1d | Ordered Product sum > $2499 ב-30 יום | | |
| 2 | | true | "Important Update About Your Order" (VQTTX3) | Form 5106 (Importer ID) ל-US Customs, הורדה מ-Google Drive, שליחה לנו או ל-FedEx. **76% click.** הטקסט אומר "over $2500" אבל התנאי הוא > 2499. |
| — | +10d (רק במסלול true) → Split: Subscribed to SMS ב-30 יום | | | |
| 3 | | SMS | SMS Google review ואחרי +1d מייל "Your Feedback Matters to Us! 🖤" (UzxBue) | Google review (maps link). |
| 3' | | no SMS | "Your Feedback Matters to Us! 🖤" (Y4kn3D) | Google review. ⚠️ **במסלול שמתחת ל-$2499 אין המתנה של 10 ימים.** בקשת הביקורת יוצאת **יום אחרי שליחה**, לפני שהפריט הגיע. |

### 1.10 WTfhxp — "Review request" (live)
- **טריגר:** Ready to review (Klaviyo Reviews).
- **פילטר:** אין ביקורת 1★ או 2★ ב-90 יום, ואין ביקורת since start.
- **SMS או מייל:** "What did you think of {{product}}?" (UtNmqh). דירוג 1–5 כוכבים (ביקורת מוצר באתר). לינק REVIEWS מוביל ל-Etsy.
- **+7d:** "Thoughts on {{product}}?" (Upb74T).
- **הערה:** זו בקשת ביקורת **מוצר** (Klaviyo Reviews), בנוסף לבקשת ה-**Google** ב-W6eUNC. לקוח עלול לקבל 3–4 בקשות ביקורת.

### 1.11 Tc6EaJ — "Cross-Sell Flow - Black Ice" (live)
- **טריגר:** Placed Order כש-Collections contains "Black Ice" **וגם** "Engagement Rings".
- **+5 ימים (10:00):** שרשרת של כ-10 conditional splits לפי **שם מוצר מדויק** ב-Items: Black Magic, Black Scorpio, Night Crawler, Gravastar, Pale Darkness, Kamari, Noir Romance, Noir Desir, Noir Mystique. כל ענף שולח "Complete Your Love Story❤️" / "Discover the Perfect Match for Your Engagement Ring" עם טבעת נישואין תואמת (למשל Monoceros / Malagasy).
- **ברירת מחדל:** "Email #11" / "Wedding Rings for Him & Her!" (T8Efmm). 8 להקות Black Ice (Callisto, Voidfire Star…) + Affirm.
- **בעיות:**
  - נשלח 5 ימים אחרי ההזמנה, כשהפריט עוד בייצור.
  - התאמה לפי שמות מוצרים שבירה. שמות שהשתנו או מוצרים שירדו לא יתאימו.
  - חלק מהענפים מכילים כפילויות ו-additional_filters סותרים (למשל ענף Pale Darkness שולח תבנית עם פילטר Kamari).

### 1.12 Ye7y3T — "Cross-sell Flow - White" (live)
- **טריגר:** Placed Order (כל הזמנה).
- **+5 ימים:** שרשרת של כ-12 splits לפי שם מוצר לבן ("These Two Were Made For Each Other", להקה תואמת).
- **אם אין התאמה:** trigger-split. Engagement Rings → **סוף**. Necklaces → "We Saved This Coupon Just For You!" (VQ88Xa). אחרת → "Your Secret Coupon Inside" (WqR6TE).
- **⚠️ הקופונים הפוכים:**
  - VQ88Xa (אחרי **שרשרת**) מדבר על "your stunning earrings" ומציע שרשרת (5OFFNECKLACE).
  - WqR6TE (ברירת מחדל) מדבר על "your fabulous necklace" ומציע עגילים (5OFFEARRINGS).
- **נפח:** כמעט אפס (נמען 1 בשנתיים). **לכבות.**

### 1.13 VtbjEg — "Customer Winback - Junaid" (live)
- **טריגר:** Placed Order. **פילטר:** Placed Order = 0 since start (כלומר לא קנה שוב).
- **+100 ימים (12:00):** "Because We Miss You…" / "A Lot Has Changed And You've GOT To See What's New ✨" (XfBdaK). "WE MISS YOU… let's not lose touch", best sellers, Black Ice, ביקורת ל-Etsy.
- **+2d:** "Ready To Get Back Together?🤍" (XH6ETy). **15% קוד WINBACK.**
- **לפי האפיון:** יוחלף ב-JEWELVERSARY (שנה, בלי הנחה ובלי בקשת הפניה).

---

## 2. הלוגיקה של דניאל (מה שעובד בבסיס, ומה לשמור)

### 2.1 רצף ההתנגדויות בעגלה ובצ'קאאוט (כפי שמשתקף בפועל)
1. **תזכורת עדינה + שכבת אמון קבועה** (בכל מייל): Fully Insured Express Shipping · 30 Days Returns & Exchanges · Diamond & Jewelry Certificate · "Chat with our expert" (פגישה). **ההתנגדויות: סיכון והחזרות.**
2. **דחיפות או הנחה קטנה** ביום 1 (5%/10%, "about to expire"). **ההתנגדות: דחיינות.** ← הרכיב שמפר את כללי הבית.
3. **"למה אנחנו" + הוכחה חברתית** (Why Diana Rafael, ביקורות, The Power of Black Diamonds). **ההתנגדויות: לגיטימיות של מותג מחו"ל ואיכות black diamond.**
4. **אדם:** פגישה אישית עם דניאל / עיצוב אישי / warranty. **ההתנגדויות: "יש לי שאלות" ו"אני רוצה להתאים".**
5. **מחיר:** Affirm (תשלומים).
6. **מנוף מחיר אחרון:** Affirm + 10% (AFFIRM10) + עגילים חינם מעל $2000.

**המסקנה:** הרצף נכון כשלד, אבל הוא **קצר מדי** (4–7 מיילים ב-4–7 ימים). הוא **מדלג על ההתנגדויות הכבדות** של מוצר יקר מחו"ל:
- משלוח, מכס, מי משלם
- ייצור לפי הזמנה וכמה זמן זה לוקח
- מידה, resizing ו-warranty
- "האם זה באמת natural black diamond"

הוא גם **נשען על דדליינים מזויפים והנחות סותרות** במקום על הסרת התנגדויות.

### 2.2 Black Ice מול לא-Black Ice — מה שונה באמת
| | Black Ice (Y3ZV7x / XW6UqR) | לא-Black Ice (UrfQ29 / VB4v4q) |
|---|---|---|
| קצב | מהיר (5% כבר ביום 1, הכול נגמר בכ-4–7 ימים) | איטי יותר (עד 7 מיילים) |
| נרטיב | סיפור black diamond / Black Ice, 450+ ביקורות, studs חינם מעל $2000 | ביקורות טקסט, "Why Diana Rafael", פגישה ועיצוב אישי, מוצרים לבנים |
| הנחות | "5%" (לא קיים בגוף), AFFIRM10 (הנושא אומר 15%) | DIAMOND 10%, ואז 5%, ואז AFFIRM10 + "48 hours" |
| פיצול נוסף | Placed Order ב-30 יום, SMS | Opened Email (מי שלא פתח מקבל מייל; מי שפתח מקבל SMS) |

**ההבדל הוא בתוכן ובקולקציה, לא בלוגיקה.** אותו שלד מתאים לשניהם. מה שמשתנה: בלוק "מה זה natural black diamond" (חשוב ל-BI ול-REMNANT), התמונות והלינק לקולקציה.

### 2.3 פוסט-פרצ'ס
דניאל כבר הבין שהמיילים התפעוליים הם הנקראים ביותר: tracking עם 55% click, Form 5106 עם 76% click. **חסרים:**
- הסבר על מכס, ו-"Diana Rafael covered and paid all shipping costs"
- הזמנה לאינסטגרם
- "what happens now" (ייצור)
- תזמון הביקורת לפי **מסירה** ולא לפי fulfilled (היום הבקשה יוצאת יום אחרי שליחה)

---

## 3. רשימת תיקוני תוכן שחייבים לעבור לכל מייל שמשתמשים בו מחדש
- [ ] מספר ביקורות: **530+** (לא 400 ולא 450+). להסיר את הציטוט החתום "-Daniel-".
- [ ] להסיר "Dark Side" / "shine darkly" / כל "dark/darkness". הנושא של REMNANT 4 "Disturbed" תקין.
- [ ] בלי דדליינים מזויפים: "about to expire", "24 hours", "48 hours", "Last chance", "going fast", "will disappear", "about to fade".
- [ ] אף נושא לא מבטיח הנחה שלא קיימת בגוף. מדיניות קודים אחת (ראו שאלה 2).
- [ ] זמנים: "ships within 10 business days" בלבד. לא "7-10", לא "on its way" לפני שליחה, ובלי תאריך הגעה.
- [ ] לינקים: `dianarafael.com` בלבד (לא myshopify). ביקורות ל-`/pages/our-customers-reviews` (לא Etsy). לתקן את `http://#https://…` ואת `http://customercare@`.
- [ ] פגישה: 15 דק' עם דניאל + WhatsApp **+972-3-575-5066** בכל מייל (פוטר אחיד).
- [ ] כתובת שולח אחידה (`daniel@` לטון אישי, `customercare@` לתפעול). לתקן את `cutomercare@`.
- [ ] לשכתב את סגירת ה-Affirm "valued customer… serving you again" (לא מתאימה ללקוח שעוד לא קנה).
- [ ] מחירים קשיחים ומחירים מחוקים להחליף בבלוקי מוצר דינמיים או בקטלוג.
- [ ] Free studs: סף אחד ($2000 או $3000), או להסיר. **שאלה לדניאל.**

---

## 4. המבנה המוצע (לפי האפיון)

עקרונות רוחביים:
- **פוטר אחיד** בכל פלואי המכירה: פס אמון (Insured shipping paid by us · 30-day returns · Certificate · 530+ reviews) + "15 min with Daniel" + WhatsApp.
- **מקור אמת אחד לכל פלואו.** במקום שני פלואים נפרדים ל-BI ול-non-BI: **פלואו אחד** עם בלוקי show/hide לפי `event.Collections` (Black Ice / REMNANT / אחר), או conditional split רק במיילים שהתוכן בהם באמת שונה. זה חוסך לדניאל לתחזק כל שינוי פעמיים (עיקרון 1). אם דניאל מעדיף שני פלואים: לשכפל מתבנית-אם אחת.
- **יציאות (exit) בכל פלואו מכירה:** Placed Order (מאז הכניסה), unsubscribe/bounce (אוטומטי). בעגלה: גם Checkout Started. ב-Browse: גם Added to Cart ו-Checkout Started.
- **Smart Sending פעיל** בפלואים הארוכים, כדי שלקוח לא יקבל 2 מיילים מפלואים שונים באותו יום.

### 4.1 Welcome — Evergreen ("לא נגמר")

**טריגר:** Added to list `Subscribed` (XLRHrE). **פילטר:** רק unsubscribe.

**הצעה:**
- **לא** להוציא בגלל cart/checkout. הפלואים האלה רצים במקביל, ו-Smart Sending מונע התנגשות.
- לקונים: split אחד אחרי מייל 6. אחרי רכישה הם ממשיכים רק במיילי התוכן (צוות, היסטוריה, השראה, מאמרים) ומדלגים על מיילי ה-"Book / Affirm". **שאלה לדניאל.**

**אין פיצול White/Black ואין פיצול UK.** אם רוצים, בלוק דינמי אחד במייל 1.

**קצב:**
- 14 הימים הראשונים צפופים: 0, 2, 4, 7, 10, 14.
- אחר כך כל 7–10 ימים.
- מעבר לכך: **מוסיפים בסוף** כל קמפיין evergreen חדש, 10–14 ימים אחרי האחרון.

| # | יום | נושא / מטרה | מקור (reuse / rewrite) |
|---|---|---|---|
| 1 | 0 | Welcome: מי אנחנו, since 2014, 530+ ביקורות, 15 דק' עם דניאל, WhatsApp | rewrite של VqXACw (QNVBAL): להסיר "Dark Side" ו-"exclusive offer" |
| 2 | 2 | מה זה natural black diamond (מקור, אותנטיות, תעודה) | rewrite: הקטע "The Power of Black Diamonds" מ-VQ7Smu + בלוג black-diamond-history |
| 3 | 4 | הצוות והסטודיו בישראל, איך אנחנו עובדים (ייצור לפי הזמנה, ships within 10 business days, משלוח מבוטח על חשבוננו) | **חדש** (מבוסס על התמונות של RgG9wB "About Diana Rafael") |
| 4 | 7 | ביקורות: 530+, 3 סיפורי לקוחות | rewrite של הקמפיינים "Nov 16- Reviews" / "Jan 11- Reviews" |
| 5 | 10 | קולקציית Black Ice | rewrite של RzcaKE "Black Ice Magic" + X375Cv (בלי "darkly") |
| 6 | 14 | REMNANT (הסיפור + ההשקה) | קמפיין "REMNANT — 2 Launch (25.10)" (+ Teaser 18.10 כפתיח) |
| 7 | 21 | עיצוב אישי: המסע מסקיצה לטבעת | קמפיין "Dec 9- Custom Design Journey" (הביא הזמנה של $1,700) + XPnCVU |
| 8 | 28 | "15 דקות עם דניאל" / WhatsApp: שאלות שאנשים שואלים | rewrite של RmjpRZ |
| 9 | 35 | השראה: Shop the Look, להקות תואמות | קמפיינים "Dec 12- Shop the Look black" (CTR 1.74%) + "Feb 18- matching rings Black" |
| 10 | 42 | Why people are buying black diamond rings | XE88f8 (VRGeJD), למחוק את המחירים הקשיחים |
| 11 | 49 | צורות: Oval / Emerald / Cushion בשחור | קמפיינים "March 22- black OVAL" (CTR 1.43%) + "Feb 26- Emerald Black" + "Feb 20- Cushion Black", **בלי ה-10%** |
| 12 | 56 | סיפור שמיימי: Eclipse / Equinox / Portal (ההשראה לשמות) | קמפיינים "April 8- Solar Eclipse B&W" (1.37%), "March 20- the Equinox", "Dec 10- Portal". לשכתב ל-evergreen בלי תאריכים |
| 13 | 63 | Breaking Tradition: למה לא יהלום לבן | קמפיין "Jan 22- Breaking Tradition" |
| 14 | 70 | REMNANT Earrings | קמפיין "REMNANT — 3 Earrings (1.11)" |
| 15 | 77 | REMNANT Disturbed | קמפיין "REMNANT — 4 Disturbed (15.11)", אחרי שיישלח |
| 16 | 84 | איך משלמים: Affirm (בלי דחיפות) | rewrite של SA72eG |
| 17 | 91 | For Him: להקות גברים | קמפיין "Jan 30- Gift for Him" (בלי הקשר ה-Valentine's) |
| 18 | 98 | "Reintro" (מה השתנה אצלנו) | קמפיין "2026-11-05 Reintro" |
| 19+ | +10–14 | **כל מאמר בלוג או קמפיין evergreen חדש מצטרף כאן** | — |

**לא מצרפים:**
- מכירות ועונתיים: Black Friday, 11/11, Valentine's, "Sale ends", Archive Sale, Christmas/NY, "10% OFF", "ready to ship 15%".
- חינוך יהלום לבן: Clarity Enhanced, Light Performance ×4, Certificates, Geometric Albedo, Emerald White, White rings. **שאלה לדניאל:** האם הם עוד חלק מהמותג.
- Golden: לבדוק אם הקולקציה עוד חיה.

**KYC / Customer Profile form (Wq62ZS):** להעביר לפוסט-פרצ'ס (כבר קיים שם כ-"buyers form"), או להשאיר כמייל 9 אופציונלי. **שאלה לדניאל.**

> הערה: לא קראתי את תוכן הקמפיינים עצמם (רק שמות, תאריכים וביצועים). לפני שמצרפים כל קמפיין, צריך לעבור עליו לפי רשימת התיקונים בסעיף 3. רובם מכילים מחירים או אזכורי עונה.

### 4.2 Browse Abandonment ("להתחיל למכור") — מבוסס Y6Zunh

**טריגר:** Viewed Product. אם ה-API metric לא יורה אחרי ההחזרה, לבדוק את ה-onsite tracking של Klaviyo.

**פילטרים:**
- Placed Order = 0, Checkout = 0, Added to Cart = 0 since start
- לא היה בפלואו ב-14 יום (במקום 30)
- **להסיר:** Viewed Page

**פיצולים:**
- Split A (Clicked Email): **להוריד.** הטקסט זהה בשני הענפים.
- Split B (SMS): **להוריד**, אלא אם מחזירים SMS.

| # | זמן | Subject (רעיון) | מטרה / התנגדות | מקור |
|---|---|---|---|---|
| 1 | +2h | "Still thinking about the {{ event.Name }}?" | תזכורת + המוצר + פס אמון + "ask Daniel" | reuse RsYy37: להסיר את Split A ולתקן את הלינק הריק |
| 2 | +1d | "Why 530+ customers trusted a studio in Israel" | לגיטימיות + ביקורות | rewrite של T69UQN: בלי "going fast", בלי Etsy, 530+ |
| 3 | +3d | "Every piece is made for you — here's how" | ייצור לפי הזמנה, תעודה, natural black diamond, ships within 10 business days | **חדש** (משותף לעגלה) |
| 4 | +5d | "Questions? 15 minutes with Daniel" | אדם / התאמה אישית + Affirm בשורה אחת | rewrite של XWZA4z + SQtzKD |

"Last Chance 10%" (RtFJBA) **יוצא**. אם דניאל רוצה הנחה, היא עוברת למייל האחרון בעגלה ובצ'קאאוט בלבד.

### 4.3 Abandoned Cart — ארוך, הסרת התנגדויות

**טריגר:** Added to Cart. להחליט בין API (RjxRum) ל-Shopify (WT7SJV), לפי מה שבאמת יורה.

**פילטרים:** Checkout Started = 0 ו-Placed Order = 0 since start. Re-entry: 30 יום.

**מבנה:** פלואו **אחד**, עם בלוקי show/hide לפי Categories (Black Ice / REMNANT / אחר). זה מחליף את Y3ZV7x ואת UrfQ29.

| # | זמן | Subject (רעיון) | התנגדות | מקור |
|---|---|---|---|---|
| 1 | +1h | "Your {{ item }} is saved in your cart" | תזכורת + פס אמון | reuse S3HdXt (TQ97tW) / XJ7Ydx: להסיר "going fast" ולתקן את Return to cart |
| 2 | +1d | "Is it really a natural black diamond?" | אותנטיות ואיכות. תעודה, מה ההבדל מ-treated/lab | rewrite של "Power of Black Diamonds" מ-VQ7Smu |
| 3 | +3d | "530+ reviews from people who were exactly where you are" | אמון במותג מחו"ל | rewrite של QNZb92 "Why Diana Rafael" (שכרגע כולו תמונות) |
| 4 | +5d | "Made to order, shipped insured — on us" | ייצור, ships within 10 business days, משלוח מבוטח על חשבוננו, מכס אפשרי (לבדוק בעצמך) | **חדש** |
| 5 | +7d | "What if it doesn't fit?" | מידה, resizing, 30-day returns, lifetime warranty / Jewelry Care | **חדש** (לינק `/pages/lifetime-manufacturer-warranty`) |
| 6 | +9d | "Pay over time with Affirm" | מחיר | reuse SA72eG: לתקן את הלינק ואת הסגירה |
| 7 | +11d | "Want to change something? 15 minutes with Daniel" | התאמה אישית / אדם, WhatsApp | rewrite של XWZA4z |
| 8 | +14d | "A note from Daniel" (טקסט אישי, plain text) | סגירה אנושית, בלי דדליין. הנחה רק אם דניאל מחליט (שאלה 2) | **חדש** |

### 4.4 Abandoned Checkout — אותו עיקרון

**טריגר:** Checkout Started. **פילטר:** Placed Order = 0. Re-entry: 7 ימים.

**מבנה:** פלואו אחד עם show/hide לפי Collections. מחליף את VB4v4q ואת XW6UqR.

**הבדלים מהעגלה:**
- התחלה מהירה יותר.
- מייל מוקדם שמתייחס ישירות **לחסם בקופה**: עלויות משלוח (הכול עלינו), מכס, תשלום, Affirm.

| # | זמן | Subject (רעיון) | התנגדות | מקור |
|---|---|---|---|---|
| 1 | +1h | "Is this the one? 💍" (שומרים, ה-A/B ניצח) | תזכורת + פס אמון | reuse RGSj5h / UqT2bc: להסיר את ה-10% DIAMOND או ליישר (שאלה 2) |
| 2 | +1d | "Anything stop you at checkout?" | משלוח בחינם ומבוטח, מכס אפשרי, Affirm, WhatsApp. **שאלה פתוחה, תשובה ישירה לדניאל** | **חדש** (במקום THZmcx "about to expire") |
| 3 | +2d | "Is it really a natural black diamond?" | אותנטיות | משותף לעגלה #2 |
| 4 | +4d | "530+ reviews" | אמון | משותף לעגלה #3 |
| 5 | +6d | "What if it doesn't fit?" | מידה / החזרה / warranty | משותף לעגלה #5 |
| 6 | +8d | "Pay over time with Affirm" | מחיר | משותף לעגלה #6 |
| 7 | +10d | "15 minutes with Daniel" | אדם | rewrite של XWZA4z: **לתקן את שליחת #4 ו-#5 באותה דקה** |
| 8 | +13d | "A note from Daniel" | סגירה | משותף לעגלה #8 |

**פיצולים:**
- **"Opened Email = 0 alltime" (VB4v4q):** להוריד. הוא מבוסס opens, שאינם אמינים אחרי Apple MPP.
- **"Placed Order ב-30 יום" (Y3ZV7x):** מיותר, כי יש פילטר Placed Order.
- **פיצולי SMS:** להוריד, אלא אם מחזירים SMS.

### 4.5 Post-purchase — "חשוב מאוד"

**A. Order Placed** (טריגר Placed Order). מחליף את WvEmp7.

| # | זמן | Subject | תוכן | מקור |
|---|---|---|---|---|
| 1 | 0 | "Your order is confirmed — here's what happens now" | אישור. ייצור לפי הזמנה, **ships within 10 business days**, נשלח מייל עם מספר מעקב. מעל $2,500: טופס 5106 בהמשך. **הזמנה לאינסטגרם** (@dianarafaeljewelry: "follow your piece being made") | rewrite של XNADM8 ("7-10" → "within 10 business days") |
| 2 | +2d | "Meet the hands making your piece" | הצוות והסטודיו + אינסטגרם | rewrite של ULX2Q3: בלי "on its way" ובלי cross-sell עם מחירים |
| 3 | +5d | "Help us get to know you" | סקר VIP buyers | reuse Y6Wbph (URcFNf) |
| — | split | count = 1 מול repeat | מייל תודה לקונה חוזר + Jewelry Care | reuse SygyQ4 (XhjyNZ): לתקן את בלוק ה-best sellers הריק |

**B. Shipped** (טריגר Fulfilled Order). מחליף את W6eUNC.

| # | זמן | Subject | תוכן | מקור |
|---|---|---|---|---|
| 1 | 0 | "Your piece has shipped — tracking inside" | לינק מעקב. **"Diana Rafael covered and paid all shipping costs."** הסבר קצר על מכס: "Depending on your state and the order value, US customs duties may apply — please check for yourself." Fully insured, חתימה. **בלי תאריך הגעה.** אינסטגרם. **בלי cross-sell.** | rewrite של TEMYFw: לתקן את משתנה השם הריק |
| 2 | +1d, רק מעל $2,500 | "Important: US customs form for your order" | Form 5106 | reuse VQTTX3 (RwnPPx): ליישר סף 2500 ולהעביר את הטופס מ-Drive לקובץ באתר |

**C. Delivered → Google review.**
- **טריגר:** Delivered Shipment (Uin4Gb, Shopify) או Package delivered (R6e7eC). לבדוק איזה מהם באמת מתמלא.
- **Fallback אם אף אחד:** Fulfilled + 10 ימים.
- **+3 ימים:** "How does it feel to wear it?" עם לינק Google review (reuse Y4kn3D / S43ETz, בלי ציטוט "-Daniel-").
- **+5 ימים:** תזכורת אחת. אחר כך יציאה.

**WTfhxp (ביקורת מוצר ב-Klaviyo Reviews):** להחליט בין Google לביקורת מוצר באתר. לא שתיהן במקביל באותו שבוע (שאלה 4).

### 4.6 Cross-sell — חודשיים אחרי קבלת הפריט

**טריגר:** Delivered Shipment, או Fulfilled Order + 10 ימים כ-proxy. **השהיה:** +60 יום.

**פילטר:** Placed Order = 0 since start, ואין ביקורת 1–2★.

**פיצול לפי סוג מוצר** (trigger split על `Collections` / `Categories` של ההזמנה המקורית, **לא** לפי שם מוצר):

| קנה | מציעים |
|---|---|
| Engagement ring | Wedding bands שעובדות איתה (דינמי, Black Wedding Bands) |
| Bracelet | טבעות או עגילים |
| Necklace | עגילים |
| Earrings | שרשרת |

**רצף:** 3 מיילים — יום 0 ("Made to go with your {{type}}"), יום 4 (השראה/stack), יום 9 ("Want it designed to match? 15 min with Daniel").

**"קליק או צפייה במוצר אחר מתחילים מחדש את Browse":** זה קורה אוטומטית, כי Browse מופעל על Viewed Product. צריך רק לוודא שפילטר "לא היה בפלואו" ב-Browse לא חוסם (14 יום מספיק).

**מקור:** תבניות ה-"Complete Your Love Story" של Tc6EaJ (T8Efmm / Rzb3hs) כבסיס לעיצוב. התאמה מדויקת של "הלהקה של הטבעת הזו" מתבצעת דרך metafield `matching_band` בקטלוג ובלוק דינמי, לא דרך 20 splits.

### 4.7 JEWELVERSARY — שנה מהרכישה
- **טריגר:** Placed Order. **השהיה:** +365 ימים. **פילטר:** בלי Refunded/Cancelled Order להזמנה הזו.
- **בלי** פילטר "לא קנה שוב": גם קונה חוזר מקבל ברכה.
- **אלטרנטיבה:** פלואו date-based על תכונת פרופיל `first_order_date`, שחוזר כל שנה. **שאלה 6.**
- **מייל 1 (יום השנה):** "Happy JEWELVERSARY, {{first_name}} 🖤". שנה מאז שה-{{product}} הגיע. touching base: איך היא נראית היום, טיפ טיפול, הזמנה לניקוי/בדיקה (Jewelry Care).
- **מייל 2 (+7d):** "What's new at the studio" — מה חדש (REMNANT ודומיו).
- **בלי הנחה ובלי בקשת הפניה.**
- **מקור:** חדש. VtbjEg לא ממוחזר, כי הוא בנוי על "We miss you" + 15% WINBACK.

### 4.8 פלואים לכיבוי (רק אחרי שהחדשים live ונבדקו)

| פלואו | פעולה |
|---|---|
| WPeiJQ | להחליף ב-Welcome evergreen. לשכפל את המיילים הטובים לפני הכיבוי |
| Y6Zunh | לערוך במקום (להסיר split ופילטר), או לשכפל ולכבות |
| Y3ZV7x + UrfQ29 | להחליף בפלואו Cart אחד |
| VB4v4q + XW6UqR | להחליף בפלואו Checkout אחד |
| WvEmp7 | להחליף ב-Order Placed. **למחוק את ה-drafts הריקים** (SZqYPR, ULTSey, WX4hmQ) |
| W6eUNC | להחליף ב-Shipped + Delivered |
| Tc6EaJ + Ye7y3T | להחליף ב-Cross-sell אחד לפי סוג מוצר |
| VtbjEg | להחליף ב-JEWELVERSARY |
| WbFMJh | **להשאיר** ולעדכן (15 דק', WhatsApp) |
| WTfhxp | לפי ההחלטה בשאלה 4 |

---

## 5. שאלות פתוחות לדניאל
1. **SMS:** משתמשים בו עוד? (נשלחו כ-1–3 SMS בשנה.) אם לא, מורידים את כל פיצולי ה-SMS.
2. **הנחות בפלואי נטישה:** לשמור הנחה אחת אמיתית במייל האחרון (איזה קוד, כמה, בלי דדליין), או בלי הנחות בכלל? והאם Free studs ממשיך, ובאיזה סף ($2000 או $3000)?
3. **BI ו-non-BI:** פלואו אחד עם בלוקים לפי קולקציה (ההמלצה), או להשאיר שני פלואים נפרדים כמו היום?
4. **ביקורות:** Google בלבד, Klaviyo product reviews בלבד, או שתיהן בהפרש (למשל Google ביום 3 אחרי מסירה, product review ביום 14)?
5. **Welcome לקונים:** ממשיכים לקבל את מיילי התוכן אחרי רכישה (עם דילוג על מיילי המכירה), או יוצאים?
6. **JEWELVERSARY:** פעם אחת (Placed Order + 365d) או כל שנה (date-based)?
7. **תוכן לבן:** קולקציות לבנות (Geometric Albedo, Golden, Emerald White) עדיין נמכרות? אם לא, הן לא נכנסות לשום פלואו.
8. **פגישה:** הלינק יהיה Calendly 15 דק' (איזה URL?) או `/pages/book-online-appointment`? היום יש שלושה לינקים שונים (calendly 30min, calendly d/crf7-…, ודף האתר).
9. **Form 5106:** לשים את הטופס כקובץ באתר במקום Google Drive?

## 6. מה לא הצלחתי לקרוא
- **טקסט שנמצא בתוך תמונות:** RgG9wB "About", XcmAjh "Why DR", XPnCVU "custom design", QNZb92 "Why Diana Rafael?", ה"treat" ב-USZ7dd, וכל ה-hero banners. ייתכן שה-5% / 10% / 15% שבנושאים נמצאים שם.
- **בלוקים דינמיים** (עגלה, מוצר, tracking, "Return to cart") שמתרנדרים ריקים בלי event אמיתי. צריך שליחת preview עם event אמיתי כדי לאמת.
- **תוכן הקמפיינים:** קראתי רק שמות, תאריכים וביצועים, לא את גוף המייל.
- **וריאציות A/B שהושלמו** (winning variation של TJe6Mg, T7d4aD, S6GMed): קראתי את ה-main action בלבד.
- **ביצועי SMS:** נבדקו רק ב-12 החודשים האחרונים (כמעט אפס).
