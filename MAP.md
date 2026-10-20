# Casa Luma — מפת ניווט

עודכן: 20.10.2026. המצפן מתייחס לפרויקט הזה בלבד; אין צורך לסרוק פרויקטים מקבילים או לקרוא את כל המפה בכל משימה.

## איך מתחילים

- כשקיים `handoff.md`, מתחילים ממנו וממשיכים רק לקבצים הקשורים למשימה. הקובץ טרם נוצר במסגרת התהליך הנוכחי.
- בוחרים מסלול מהטבלה ופותחים רק את הקבצים הנחוצים. אין לטעון את היסטוריית השיחות כברירת מחדל.
- ההחלטה העדכנית: חנות רכש עם **מחיר ידני גלוי, סל והזמנות משותפים וכניסה למערכת**. קוד השרת נמצא בבנייה; פריסת המערכת המשותפת טרם הושלמה.
- התהליך נעצר אחרי כל שלב לאישור הבעלים. שלבים 1–3 הושלמו; השלב הבא הוא מסמך ניווט גלובלי, לאחר אישור.

## לאן הולכים לפי המשימה

| הקשר | נקודת כניסה | קבצים נוספים רק לפי הצורך |
|---|---|---|
| הקשר העסק, עובדות ומשימות | [תיקיית הישות](entities/casa-luma/context.md) | [עובדות](entities/casa-luma/memory.md), [משימות](entities/casa-luma/tasks.md), [מפתח קבצים](entities/casa-luma/files/README.md) |
| מסכים, כרטיס מוצר, מחיר גלוי וסל | [ממשק החנות](research/order-page.js) | [תבנית HTML](research/order-page.html.in), [עיצוב](research/order-page.css) |
| כמויות, וריאנטים, חישובים ופיצול הזמנות | [לוגיקת הרכש](research/order-core.js) | [בדיקות רכש וחנות](research/test-order-core.cjs) |
| מוצרים, מחירי מקור וערוצי ספקים | [נתוני הקטלוג](research/catalog-data.json) | [דוח המחקר](research/Casa-Luma-Sourcing-Research-2026-10-18.md), [קישורי המקור הציבוריים](research/Original-Sourcing-Links.md) |
| הוספת נתוני מחקר ובניית הקטלוג | [תהליך הבנייה](research/build_research.py) | `research/enrich_catalog.py`, `research/expand_catalog.py`, `research/widen_catalog.py` — רק המודול הרלוונטי |
| הפקת קובצי HTML | [מחולל הדף](research/order_renderer.py) | תבנית, עיצוב וממשק מהשורה הראשונה |
| התחברות, צוות, שמירה משותפת והתנגשויות | [שרת המערכת](server/app.py) | [מסך התחברות](server/auth.html), [בדיקות HTTP](server/test_app.py), [תלויות](requirements.txt) |
| שימוש של הבעלים והעובד | [מדריך ההזמנות](research/Ordering-Guide.md) | [החלטות](vault/Decisions.md), [דרישות הרכש](vault/Requirements-2026-10-20.md) |
| ארכיטקטורה וידע מסכם | [ארכיטקטורת החנות](vault/Internal-Shop-Architecture.md) | [כניסה ל־Vault](vault/Home.md), [גיבוי ופרסום](vault/Backup-and-Publishing.md) |

## מקור מול תוצר

- עורכים את קוד המקור ב־`research/` ואת השרת ב־`server/`.
- `research/order-page.html` ו־`research/Casa-Luma-Sourcing-Catalog.html` הם תוצרי בנייה, לא תבניות לעריכה ידנית.
- `docs/` מכילה את עותק הפרסום ל־GitHub Pages. שינוי מקומי אינו הוכחה שהאתר הפעיל עודכן.
- `research/render_catalog.py` ו־`research/catalog-script-check.js` הם קבצים ותיקים; הם אינם נקודת הכניסה הנוכחית לבנייה ולבדיקות.
- המיתוג: [הלוגו המקומי](research/assets/casa-luma-logo.png); הצבעים מוגדרים בקובץ העיצוב.

## חומרים פרטיים וגיבויים

- מסמכי מקור מקומיים: `Casa Luma Shop · Vision Guide for Pearl.pptx`, `Suppliers.pdf` ותיקיית `Store Management (CL)/`. פותחים רק כשנדרשת ראיה נקודתית; אין להעלותם למאגר הציבורי.
- `backups/` מכילה גיבוי ZIP מקומי. `vault/.obsidian/` מכילה הגדרות מקומיות, ואינה תוכן ידע לפרסום.
- הגיבוי המלא שלפני שינוי המבנה: `../_backup-Casa-Luma-Shop-2026-10-20/`. קובץ `BACKUP-MANIFEST.json` בתוכו מתעד את בדיקת ההעתקה.
- [מאגר GitHub](https://github.com/oroofarm-lang/Casa-Luma-Shop) ציבורי. ענף גיבוי שלב 1: `backup/casa-luma-2026-10-20-step1`; תמונת המצב המאומתת שלו: `b478c1a356a2246c9ba938984a7b271f203f1df9`.
- אין לכלול סיסמאות, טוקנים, קובצי סביבה או מסדי נתונים מקומיים ב־Git. אין לפרסם גרסת ביניים של המערכת המשותפת.

## מבנה שטרם הוקם

תיקיית `entities/casa-luma/` הוקמה בשלב 3. קובצי `AGENTS.md`, `handoff.md` ו־`lessons.md` ועדכון ה־Vault יטופלו בשלבים הבאים, כל אחד לאחר אישור. קובצי המקור נשארו במקומם; לא אוחדו או נמחקו כפילויות.
