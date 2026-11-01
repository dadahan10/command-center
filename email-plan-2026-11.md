# תוכנית מייל + SMS — Diana Rafael, 2 בנובמבר – 1 בדצמבר 2026

> **גרסה 2 (1.11, אחרי ההערות של דניאל):** 5.11 היכרות מחדש עם המותג; 10.11 משחק בחירה; 12.11 תכשיטים חדשים + ביקורות; 19.11 טבעת לפי אופי/מזל; VIP + רמזי מתנות + משחקי בחירה בכל מייל עד 23.11; גישה מוקדמת מותנית במספר הנרשמים ל-VIP; בלי "נגמר הלילה" ובלי דדליין משלוח; flow "מה קורה אחרי ההזמנה"; anniversary בוטל; הפניית חבר עם מתנה אמיתית. Klaviyo-Shopify חובר מחדש, SPF+DKIM תוקנו ב-1.11.

נכתב: 1.11.2026, על נתונים חיים מקלאביו, משופיפיי ומ-DNS. שום דבר לא נוצר ולא נשלח בקלאביו.
המטרה לחודש: למכור לבסיס הקיים (קונים ומנויים), להעלות את שיעור ההמרה, ולהכין את התשתית שתקלוט את התנועה מקמפיין ה-Google Search.

---

## 1. איפה אנחנו עומדים

### המכירות (Shopify, אתר בלבד)
| תקופה | הזמנות | Net sales | AOV |
|---|---|---|---|
| 2024 | 99 | $221,411 | $2,352 |
| 2025 | 80 | $158,910 | $2,183 |
| 2026 (עד 31.10) | 38 | $80,193 | $2,110 |
| נובמבר 2024 / 2025 | 17 / 8 | $44,855 / $14,544 | — |
| ספטמבר / אוקטובר 2026 | 2 / 2 | $4,250 / $3,060 | — |

- **235 לקוחות קנו באתר אי-פעם, ורק 19 מהם קנו יותר מפעם אחת (8%).** הבסיס הקיים כמעט לא עבד עד היום, ומשם יבוא הכסף הקרוב.
- **הטבעות הן העסק:** Black_Ice Diamond Rings הביאו $341K מתוך כ-$460K מאז 2024 (163 הזמנות). הנמכרים ביותר ב-12 החודשים האחרונים: Geometric Baguette Wedding Band (4 הזמנות), Art Deco Marquise ו-Emerald Cut בזהב אדום, Pave Wedding Ring, Tennis Bracelet.
- **המשפך שבור בקופה:** באוקטובר היו 2,341 סשנים. ב-130 מהם הוסיפו לעגלה, 117 הגיעו לקופה, ו-**2 בלבד השלימו**. 115 אנשים עזבו בקופה, ואף מייל לא רדף אחריהם (פירוט בהמשך).

### קלאביו: הקהלים
| קהל | ID | גודל |
|---|---|---|
| Subscribed (רשימה, single opt-in) | XLRHrE | 1,835 |
| BUYERS ALL TIME (רשימה ידנית) | V84wEE | **96** (מול 235 קונים בשופיפיי) |
| SMS Subscribers (סגמנט) | WFxh48 | 221 |
| פתחו לפחות מייל אחד באוקטובר (ייחודיים) | — | 332 |
| Noah don't send (מוחרג) | UDGqWG | 1 |

### קלאביו: קמפיינים אחרונים (90 יום. באוגוסט ובספטמבר לא נשלח כלום)
| קמפיין | נשלח | נמענים | פתיחה | הקלקה | CTOR | המרות | Bounce | תלונות |
|---|---|---|---|---|---|---|---|---|
| Archive C "One of each, then gone" | 10.10 | 1,683 | 16.4% | 1.35% | 8.2% | 0 | 3.1% | 0 |
| REMNANT 1 Teaser | 18.10 | 1,659 | 10.8% | 0.68% | 6.3% | 0 | 2.7% | 0 |
| REMNANT 2 Launch | 25.10 | 1,656 | 10.6% | **0.31%** | 2.9% | 0 | 2.4% | 0.06% |
| REMNANT 3 Earrings | 1.11 12:54 IL | רשימה מלאה | — | — | — | — | — | — |
| REMNANT 4 Disturbed | 15.11 (Scheduled) | רשימה מלאה | | | | | | |
| Black Friday | 27.11 (טיוטה, תבנית X6KmCh) | | | | | | | |

**האבחנה של קלאביו:** שלושה ממצאים, לפי סדר החומרה.

1. **האינטגרציה עם שופיפיי מתה מאז מרץ 2026.** אירועי `Placed Order` (T6KBRR) ירדו ל-0 מאפריל, אחרי 9, 4, 6, 6 ו-1 בנובמבר 2025 עד מרץ 2026. מאוגוסט עד אוקטובר יש 0 אירועי `Checkout Started` ו-0 אירועי `Added to Cart`, ורק 2 אירועי `Viewed Product`. בפועל **כל 17 ה-flows ה"חיים" מורעבים**: ב-90 יום כל ה-flows יחד שלחו 58 מיילים. העגלה הנטושה, הקופה הנטושה, ה-post-purchase, בקשת הביקורת, ה-cross-sell וה-win-back לא קיבלו אף נמען. גם רשימת הקונים (96 מול 235) היא תוצאה של אותה תקלה. המשמעות היא שכל שקל שיושקע בגוגל ייפול כרגע לאתר שלא זוכר את המבקרים שלו.
2. **שם הדומיין מוגדר שבור.** ל-dianarafael.com יש 7 שרתי NS: 3 של Domain The Net ו-**4 של Klaviyo (ns1–ns4.klaviyo.com)**. בדקתי היום, ושרתי Klaviyo **מסרבים (REFUSED)** לענות על הדומיין הראשי. זו האצלה פגומה (lame delegation): בערך חצי מהשאילתות נופלות על שרת שמסרב, וזה גורם להשהיות ולכשלי SPF/DMARC לסירוגין (שאילתה אחת שלי על send.dianarafael.com נכשלה ב-timeout). בנוסף **אין רשומת SPF בדומיין הראשי בכלל**, DMARC מוגדר `p=none` בלי `rua` (אין דיווחים), ול-Google Workspace אין DKIM. ה-DKIM של קלאביו (kl/kl2 → SendGrid) תקין.
3. **המוניטין נפגע.** הרשימה שתקה כמעט שנה (מ-23.11.2025 ועד 10.10.2026), ואז קיבלה 4 שליחות בשלושה שבועות ל-1,650 איש. התוצאה בשיעורי הפתיחה לפי ספק (אוקטובר, פתיחות חלקי מיילים שהתקבלו): **Gmail 12%** (62% מהרשימה), Outlook 18%, Yahoo 27%, **Apple iCloud 6.6%**. ב-iCloud, שבו Apple MPP אמור לנפח פתיחות לכמעט 100%, מספר כזה אומר שהמייל נוחת ב-Junk. ה-Bounce עמד על 2.4–3.1% בכל שליחה (116 soft ו-19 hard באוקטובר), מעל רף ההתראה של 1%. הרשימה ישנה ולא מנוקה.

**מסקנה:** בעיית התוכן משנית. לפני שמוסיפים מיילים צריך לתקן שלושה צינורות: DNS, אינטגרציית שופיפיי וניקוי הרשימה. כל עוד אין `Placed Order`, גם הקמפיינים הטובים ביותר ימדדו 0 המרות.

---

## 2. הסגמנטציה לחודש

בונים את הסגמנטים ב-4–5.11, אחרי חיבור שופיפיי מחדש וגיבוי ההיסטוריה (Klaviyo מייבא אוטומטית את היסטוריית ההזמנות בחיבור מחדש). הגדלים הם הערכה מהנתונים של היום.

| # | שם הסגמנט | הגדרה | גודל משוער | שימוש |
|---|---|---|---|---|
| S1 | **Buyers — all time** | Placed Order ≥1 over all time (מחליף את הרשימה הידנית V84wEE) | ~235 | בסיס הכסף. מקבלים הכול לפני כולם |
| S2 | **Buyers — engagement ring, no band** | S1 + Ordered Product שבו product type/title מכיל "Engagement" + אין Ordered Product עם "Band"/"Wedding" | ~120 | upsell לטבעת נישואין תואמת |
| S3 | ~~Anniversary Nov–Dec~~ | בוטל (דניאל 1.11: אין מספיק נתונים) | — | — |
| S4 | **VIP repeat** | Placed Order ≥2 או סך קנייה ≥$4,000 | ~25 | WhatsApp אישי מדניאל + גישה מוקדמת |
| S5 | **Engaged 90d** | Opened OR Clicked Email ≥1 ב-90 יום, OR Active on Site ב-30 יום, AND לא ב-S1 | ~330 | הקהל הראשי לשבועות 1–3 |
| S6 | **Clickers 90d** | Clicked Email ≥1 ב-90 יום | ~40 | resend וקהל חם ל-SMS |
| S7 | **Cold** | Subscribed, אין פתיחה/הקלקה ב-180 יום, לא ב-S1, נוצר לפני יותר מ-180 יום | ~1,250 | **מייל אחד בלבד** החודש: BF ב-27.11. אחר כך sunset |
| S8 | **Dead** | אין פתיחה/הקלקה ב-365 יום, OR ≥3 soft bounces, OR bounced hard | ~300 | Suppress מיד (4.11). לא נשלח אליהם שוב |
| S9 | **SMS** | WFxh48, מנויי SMS | 221 | 4 הודעות בחודש, רק סביב BF |
| S10 | **BF clicked, no order** | Clicked Email 27–30.11 AND אין Placed Order מאז 27.11 | יחושב | 1.12 |

החרגה קבועה בכל קמפיין: UDGqWG, S8, ומי שקנה ב-72 השעות האחרונות (חוץ ממיילים ל-S1 בלבד).

**אטסי:** אין לנו רשות להכניס קונים של אטסי לקלאביו. מדיניות אטסי אוסרת שיווק לקונים שלא נתנו הסכמה. הקונים מאטסי מקבלים פנייה רק דרך הכלים של אטסי עצמו (ראו סעיף 3ב).

---

## 3. לוח השליחה

שעת שליחה ברירת מחדל: **10:00 לפי השעון המקומי של הנמען** (Klaviyo local time). ב-BF השעה היא 07:00. Smart Sending פעיל בכל השליחות, ו-UTM בכל קישור (`utm_source=klaviyo&utm_medium=email&utm_campaign=<slug>`).
**חוקי תוכן שחלים על כל מייל:** אף פעם לא תאריך הגעה, וגם לא דדליין משלוח (אנשים מזמינים ברגע האחרון). שפה מרוממת בלי "dark/darkness". התכשיט מוצג גדול ודרמטי בראש המייל. קישורים רק לאתר שלנו. 200–300 מילה לכל היותר.
**החוט שעובר בכל המיילים בתקופה (דניאל 1.11):** להזכיר שאנחנו חברה טובה, שכל תכשיט נעשה בהזמנה אישית (custom made), ושיש התאמות אישיות (סרטון קצר של CustomizeAI). ובכל מייל עד 23.11:
- **כפתור "Join the VIP list"** (רשימת קלאביו חדשה `VIP Early Access`): "VIPs get every Black Friday offer days before everyone else." דחיפות ו-FOMO, בלי לחשוף את גובה ההנחה.
- **רמז למתנות:** "Gifts with every order above certain amounts are coming." (מדרגות המתנה עצמן נחשפות ב-VIP).
- **משחק בחירה (engagement):** שני תכשיטים זה מול זה, "Which one is more you?". כל לחיצה מתייגת את הפרופיל (property `style_pick`) ומובילה לעמוד המוצר. הקליקים מחממים את הדומיין ומלמדים אותנו מה כל לקוחה אוהבת.

**ההצעות בחודש:**
- **2–23.11:** אין הנחה. מוכרים דרך ערך, ביקורות ומתנה, ובונים את רשימת ה-VIP.
- **24–26.11, גישה מוקדמת, מותנה:** אם רשימת ה-VIP הגיעה ל-**60 נרשמים לפחות עד 22.11** → הגישה המוקדמת (30% עם קוד `CIRCLE30`) רק לנרשמים ל-VIP. אם לא → לכל הקונים והמנויים הפעילים (S1+S5). ההחלטה ב-22.11 לפי המספר.
- **27.11 עד 31.1.2027:** 30% site-wide אוטומטי (קיים ומתוזמן). Archive עד 70% בנפרד, בלי stacking.
- **מתנות לפי סכום, לכל אורך המבצע ולא "נגמרות הלילה":** חריטה מתנה מעל $2,000 (לא הנחה בשופיפיי, ולכן אין התנגשות עם ה-30%). ממתין לאישור דניאל על המדרגה.

### 3א. מייל

| תאריך | סגמנט | מטרה | Subject + Preview | תוכן ליבה / הצעה | CTA | יעד KPI |
|---|---|---|---|---|---|---|
| **ה' 5.11** | S1 Buyers + S5 Engaged (~550) | **היכרות מחדש עם Diana Rafael:** המיתוג החדש, הקולקציות, מה אנחנו יכולים להכין | **"A lot has changed since you last heard from us"** / *"New look, new collections, same hands making every piece."* | מכתב קצר מדניאל + המיתוג החדש. 3 בלוקים גדולים: REMNANT, טבעות אירוסין, להקות. "Every piece is made to order, and we can change almost anything" + סרטון CustomizeAI קצר. בסוף: "Reply and tell me what you're wearing today, I read every one." + VIP + משחק בחירה. | Explore the collections | CTR ≥3%, replies ≥5 |
| **ג' 10.11** | S1+S5 | **Engagement: משחק בחירה** (במקום מייל יום הנישואין, שאין לו מספיק נתונים) | **"Which ring is her?"** / *"Pick one. We'll tell you what it says about her."* | 4 זוגות של טבעות (מוארכת מול סימטרית, קלאסית מול אוונגרד...). כל לחיצה מובילה לעמוד שמסביר את האופי + המוצר. VIP. | Pick yours | CTR ≥4% |
| **ה' 12.11** | S5 Engaged (~330) + S1 | **תכשיטים חדשים**, מתואם לנחיתות של קמפיין גוגל | **"New this season"** / *"The newest pieces from our studio, and what customers wrote this month."* | Hero: התכשיט החדש הכי מרשים, גדול. גריד של 4–6 תכשיטים חדשים. **סקשן "New reviews"**: 3 ביקורות אחרונות (Etsy/Google, 530+ בסך הכול). VIP. | Shop new arrivals | CTR ≥2%, הזמנה אחת |
| **א' 15.11** | **שינוי קהל:** S1+S5 במקום הרשימה המלאה | REMNANT Disturbed (מתוזמן) | כמו שמתוזמן ("It passes") | ללא שינוי בתוכן | — | CTR ≥1.5% |
| **ג' 17.11** | S2 Engagement-ring buyers w/o band (~120) | **upsell: הלהקה התואמת** | **"The band that completes your ring"** / *"Designed to sit flush with the ring you already love."* | גריד 6 להקות. "Tell us your ring and we'll match the curve." VIP. | Shop wedding bands / Reply with your ring | CTR ≥4%, 2 הזמנות |
| **ה' 19.11** | S1+S5 | **עונת ההצעות:** איזו טבעת מתאימה לאופי שלה / למזל שלה | **"The ring that matches her sign"** / *"Fire, earth, air or water: which stone is hers?"* | 4 יסודות (אש/אדמה/אוויר/מים), לכל אחד מזלות + טבעת מומלצת + שורה על האופי. "Not sure? Book 15 minutes with Daniel." VIP + רמז למתנות. | Find her ring | CTR ≥2.5%, הזמנה אחת |
| **א' 22.11** | S1+S5 שלא נרשמו ל-VIP | **הזדמנות אחרונה להצטרף ל-VIP** | **"VIP list closes tomorrow"** / *"Black Friday starts early for the people on it."* | קצר. מה מקבלים ב-VIP (גישה מוקדמת + מדרגות מתנה). | Join the VIP list | הרשמות ≥60 בסך הכול |
| **ב' 23.11** | VIP (או S1+S5 אם <60) | ציפייה לגישה המוקדמת | **"Tomorrow, Black Friday starts for you"** / *"30% off everything, days before everyone else."* | הכרזה על CIRCLE30 + מדרגות המתנה. Hero: הנמכרת ביותר, גדולה. | Save my favorites | CTR ≥2.5% |
| **ג' 24.11** | VIP (או S1+S5) | **פתיחת הגישה המוקדמת** | **"You're in: 30% off, starting now"** / *"Your code CIRCLE30 works until Thursday."* | קוד, 6 מוצרים, מתנה מעל $2,000, custom made. | Shop with my code | CTR ≥4%, 3 הזמנות |
| **ד' 26.11 (Thanksgiving)** | VIP שלא קנו | הקוד נסגר היום (אמיתי: ב-27.11 נפתח לכולם) | **"Thank you. Your head start ends tonight"** / *"Tomorrow it opens to everyone."* | קצר, תודה של חג + 3 מוצרים. | Use CIRCLE30 | הזמנה אחת |
| **ה' 27.11 (BF) 07:00** | S1+S5+**S7 Cold (פעם אחת)** | הכנסה + ניסיון אחרון להחיות את הקרים | הקמפיין הקיים (X6KmCh) | כמו שבנוי + שורת מתנה מעל $2,000 + custom made. | Shop Black Friday | CTR ≥1.5%, 3 הזמנות |
| **ש' 28.11** | S5+S1 שלא פתחו את 27.11 | resend | **"30% off, everything (yes, even engagement rings)"** / *"Every piece still made to order, just for you."* | אותו תוכן, Hero מחודש (טבעת אירוסין) | Shop now | CTR ≥1.5% |
| **ב' 30.11 (Cyber Monday)** | S1+S5+S6 | זווית חדשה: התאמה אישית | **"Make it yours, 30% off"** / *"Change the stone, the gold, the band. We make it for you."* | CustomizeAI + 3 דוגמאות של שינוי (אבן/צבע זהב/חריטה). בלי "נגמר הלילה". | Customize mine | CTR ≥2.5%, 2 הזמנות |
| **ג' 1.12** | S10 BF clicked, no order | המרת מתלבטים | **"Still thinking about it?"** / *"Ask me anything, I'll answer myself. Daniel"* | המוצר שהקליקו עליו + "Talk to Daniel" (Calendly) + ביקורות. בלי דדליין. | Complete my order / Book a call | CTR ≥6%, הזמנה אחת |

**סך הכול:** S1 מקבלים 9–11 מיילים בחודש, S5 מקבלים 8, S7 מקבלים 1. **יעד החודש:** 12+ הזמנות שמיוחסות למייל ול-SMS, ≈$22K נטו (נובמבר 2024 הגיע ל-$44.9K מכל הערוצים, נובמבר 2025 ל-$14.5K).

### 3ב. SMS (221 מנויים, רק סביב BF. 4 הודעות, לא יותר)
| תאריך ושעה (מקומי) | טקסט (≤160 תווים, כולל opt-out שקלאביו מוסיף) | KPI |
|---|---|---|
| ג' 24.11 11:00 | `Diana Rafael: Your Black Friday starts now. 30% off everything with CIRCLE30, 3 days early. dianarafael.com/collections/black-friday-30` | CTR ≥8% |
| ד' 26.11 12:00 | `Diana Rafael: Happy Thanksgiving. Early access code CIRCLE30 ends 5pm ET today.` | CTR ≥5% |
| ה' 27.11 09:00 | `Diana Rafael: Black Friday is live. 30% off everything + a gift on orders over $2,000.` | CTR ≥6% |
| ב' 30.11 12:00 | `Diana Rafael: Make it yours. Change the stone, the gold, the band, 30% off.` | CTR ≥5%, unsub <2% |

**WhatsApp:** אין שליחה המונית. השולח על Twilio Sandbox ונופל כל 72 שעות, ואסור לבנות עליו מול לקוחות. במקום זה דניאל שולח **הודעה אישית מהטלפון שלו ל-S4 (כ-25 לקוחות VIP)** ב-ג' 24.11, ב-15 דקות עם טקסט מוכן:
> *"Hi {name}, it's Daniel from Diana Rafael. You were one of the first to trust us, so you get Black Friday first: 30% off everything with code CIRCLE30, until Thursday. If you're thinking about a band or a gift, send me a photo of your ring and I'll match it myself."*

**אטסי (שתי החנויות), דרך כלי אטסי בלבד:** Sale ב-27–30.11 על כל החנות (30%, מיושר לאתר). Targeted offers פעילים: Thank-you coupon לקונים, Abandoned cart, Favorited item (15%) מ-2.11. אין מייל לקונים של אטסי מחוץ לאטסי.

### 3ג. תמיכה בקמפיין Google Search
- כל קישור במייל מקבל UTM כדי ש-GA4 יפריד בין מייל לגוגל.
- סנכרון סגמנטים מקלאביו ל-Google Ads Customer Match: S1 כרשימת **החרגה** מקמפייני prospecting (לא משלמים על מי שכבר קנה), S5 כקהל observation עם bid +20%.
- אחרי שהאינטגרציה מתוקנת, כל מבקר מגוגל שמשאיר מייל נכנס ל-browse/cart/checkout flows. זה מכפיל ההחזר על כל קליק ששולם.
- נושא המייל של 12.11 משקף את מילות המפתח של הקמפיין (black diamond engagement ring), ונחיתות המייל וגוגל זהות.

---

## 4. Flows לתיקון ולבנייה החודש, לפי סדר עדיפות

**סדר 0, תנאי לכל השאר:** חיבור מחדש של Shopify ↔ Klaviyo (Integrations → Shopify → Reconnect, לסמן Onsite tracking + Sync historical data + Subscribe customers who accept marketing). אימות: `Viewed Product`, `Added to Cart`, `Checkout Started` ו-`Placed Order` מופיעים ב-Activity feed תוך 24 שעות מצפייה והזמנת-מבחן. עד שזה ירוק, שום flow לא נבדק.

| עדיפות | Flow | הפער שנמצא | מה עושים (עד תאריך) |
|---|---|---|---|
| **1** | **Abandoned Checkout** | 115 קופות נטושות באוקטובר ו-0 נמענים. יש שני flows חיים מקבילים (VB4v4q "NOT Black Ice" + XW6UqR "Black Ice"), ושניהם מורעבים. | **עד 6.11:** ממזגים לאחד (משאירים את VB4v4q ומכבים את XW6UqR ואת הטיוטה Rs2Fcr). 3 מיילים: שעה, 24 שעות, 72 שעות. מייל 1: "Your ring is waiting" + תמונת המוצר גדולה. מייל 2: ביקורות + "Questions? Reply or book 15 min with Daniel". מייל 3: "ships within 10 business days" + חריטה מתנה מעל $2,000. בלי קוד הנחה, כי ה-30% האוטומטי מכסה מ-27.11. יציאה כשיש Placed Order. **יעד: 5% recovery = כ-2 הזמנות בחודש.** |
| **2** | **Browse + Cart abandonment** | 7 flows חיים חופפים (Y6Zunh, Y9u9DF Viewed Page, YqVvEY Active on site, UrfQ29, Y3ZV7x, R8UpBY, V3x2q7), שכולם שלחו 4 מיילים ב-90 יום. | **עד 9.11:** משאירים 2 בלבד. **Added to Cart** (UrfQ29): 2 מיילים, 4 שעות ו-48 שעות. **Viewed Product** (Y6Zunh): מייל אחד אחרי 24 שעות, רק ל-≥2 צפיות באותו מוצר. מכבים את Y9u9DF, YqVvEY, Y3ZV7x, R8UpBY ו-V3x2q7. הם יוצרים רעש וסיכון תלונות ברגע שהאירועים יחזרו לזרום. |
| **3** | **Post-purchase: "מה קורה עכשיו" + upsell + ביקורת** | W6eUNC, WvEmp7, WTfhxp, Tc6EaJ/Ye7y3T: כולם live, כולם עם 0 נמענים. | **עד 12.11:** (א) רצף "What happens after you order": מייל 1 מיד, תודה + הצעדים (אישור פרטים/מידה, ייצור ידני בסטודיו, בדיקת איכות, משלוח עם מעקב) + "עונה לך אדם, לא AI"; מייל 2 בזמן הייצור, מאחורי הקלעים מהסטודיו; מייל 3 כשנשלח, מעקב + טיפול בתכשיט. בלי תאריך הגעה. (ב) "matching band" אחרי 21 יום, רק לטבעת אירוסין. (ג) בקשת ביקורת 10 ימים אחרי Delivered Shipment (Google Reviews). |
| **4** | ~~Anniversary~~ | בוטל לבינתיים (דניאל 1.11: אין מספיק נתונים). | — |
| **5** | **Win-back + הפניית חבר** | VtbjEg live, מורעב, תוכן מ-2021. | **עד 20.11:** טריגר 365 יום מאז Placed Order. מייל 1: What's new since you bought. מייל 2 אחרי 14 יום, הפניית חבר עם מתנה אמיתית: "If your friend orders over $2,000, you get 1 ct black diamond studs, made for you." (עלות ייצור משוערת $200–260). קישור הפניה אישי (UTM + property referred_by). |
| **6** | **Welcome** | WPeiJQ live, אבל 5 נמענים ב-90 יום (ה-onsite לא נטען עד 25.10). הטיוטות SsZMSX, YqP3sD ו-Ud7bZG מבלבלות. | **עד 23.11:** מוודאים שהטריגר של WPeiJQ = הרשימה שאליה כותבים הפופאפים החדשים (ATC/known lead). 4 מיילים ב-10 ימים: Story (2014, טבעי, לא מטופל) ← Bestsellers + ביקורות ← "How to choose" ← Book a call. מוחקים את 3 הטיוטות הכפולות. |
| **7** | **Sunset** | לא קיים. 1,835 מנויים single opt-in ו-332 פתחו. | **4.11:** suppress חד-פעמי ל-S8. אחרי 1.12, מי שב-S7 ולא פתח או הקליק על BF עובר ל-suppression. Flow קבוע: 120 יום בלי מעורבות → מייל "Still want to hear from us?" → suppress אחרי 14 יום. |

---

## 5. תיקוני Deliverability (לפי סדר, הכול עד 9.11)

1. **להסיר את 4 רשומות ה-NS של Klaviyo מהדומיין הראשי** (ns1–ns4.klaviyo.com, אצל Domain The Net). הן מחזירות REFUSED. ה-sending domain של קלאביו כבר עובד דרך `send.dianarafael.com` (CNAME ל-SendGrid) ו-`kl/kl2._domainkey` (CNAME), כך שה-NS האלה מיותרים ומזיקים. **ביום ההסרה מוודאים שלא נשארה ב-Klaviyo הגדרת "Branded sending domain via NS".** אם יש כזו, מעבירים אותה ל-CNAME.
2. **SPF בדומיין הראשי:** `v=spf1 include:_spf.google.com ~all` (מכסה את Google Workspace. קלאביו מאומת דרך send.dianarafael.com).
3. **DKIM ל-Google Workspace:** Admin → Apps → Gmail → Authenticate email → רשומת `google._domainkey`.
4. **DMARC:** `v=DMARC1; p=none; rua=mailto:dmarc@dianarafael.com; fo=1`. אחרי 30 יום נקיים (7.12) עוברים ל-`p=quarantine`, וזה גם הבסיס ל-BIMI בהמשך.
5. **Google Postmaster Tools** לדומיין (Gmail = 62% מהרשימה). מעקב שבועי אחרי domain reputation ו-spam rate.
6. **היגיינה:** suppress ל-S8 ב-4.11. כל profile עם ≥3 soft bounces מסומן suppress. **יעד bounce <1%** (מול 2.4–3.1% היום).
7. **Warm-up לפי מעורבות:** בשבועות 2–23.11 שולחים רק ל-S1+S5 (כ-550 איש). הקרים מקבלים מייל אחד בלבד, ב-27.11, כשההצעה הכי חזקה.
8. **שולח אחיד:** From = "Daniel from Diana Rafael" `<daniel@dianarafael.com>`, Reply-to לאותה כתובת, בכל קמפיין. מייל הטקסט מ-5.11 נועד לייצר תשובות, שהן האות החיובי החזק ביותר ל-Gmail.
9. **מדידה:** הצלחה נמדדת ב-CTR, ב-CTOR ובהזמנות, לא בפתיחות (MPP). **סף עצירה:** תלונות >0.10% או bounce >2% בשליחה כלשהי = עוצרים את השליחה הבאה ובודקים.

---

## 6. מה דניאל צריך לספק (מינימום)

1. **DNS אצל Domain The Net (15 דקות):** הסרת 4 ה-NS של Klaviyo + SPF + DMARC (הטקסטים מוכנים בסעיף 5). DKIM של Google מתוך ה-Admin. **עד 4.11.**
2. **לחיצה אחת בקלאביו:** Integrations → Shopify → Reconnect, עם שלוש תיבות סימון (סעיף 4, סדר 0). **עד 4.11.** אני מאמת את האירועים אחריה.
3. **Schedule** לכל קמפיין כשהוא מוכן (המחבר חסום לשליחה). בנוסף: **לשנות את הקהל של Disturbed 15.11** ל-S1+S5 (הוא מתוזמן כרגע לרשימה המלאה).
4. **15 דקות ב-24.11:** הודעות WhatsApp אישיות ל-~25 לקוחות VIP (רשימה + טקסט אכין).
5. **תמונה אחת:** הידיים שלך על שולחן העבודה, או טבעת על יד ליד להקה תואמת, למיילים של 10.11 ו-17.11. אם אין, אשתמש ברינדור/On-body קיים.
6. **אישור חד-משמעי אחד:** חריטה מתנה מעל $2,000 בכל הטבעות, 24–30.11 (כן/לא). יצירת קוד `CIRCLE30` (30%, קולקציה Black Friday 30, 24.11 05:00 UTC עד 26.11 22:00 UTC, פעם אחת ללקוח) נעשית אחרי ה"כן".
