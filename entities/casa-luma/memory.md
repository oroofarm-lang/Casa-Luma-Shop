# Casa Luma — עובדות קבועות וניווט טכני

עודכן: 20.10.2026. מחירים, מבצעים, מלאי ומשלוח דורשים בדיקה מחדש ואינם עובדות קבועות.

| נושא | ערך |
|---|---|
| יעד משלוח | Koh Phangan, Thailand; מיקוד 84280 |
| מטבע | THB בלבד בכל המחירים והחישובים |
| מגבלת מחיר | התרעה וסינון מעל 250 THB ליחידת הזמנה; אין פסילה אוטומטית |
| שפות | עובד: אנגלית; טיוטות ספק: אנגלית ותאית |
| GitHub | https://github.com/oroofarm-lang/Casa-Luma-Shop |
| אתר סטטי קיים | https://oroofarm-lang.github.io/Casa-Luma-Shop/ |
| ענף העבודה הנוכחי | backup/casa-luma-2026-10-20-step1 |

## מיתוג

Cream `#F9EDE8`, Golden Sand `#dfbc69`, Sage `#A8C3A0`, Terracotta `#E07A5F`, Charcoal `#333333`. הלוגו הקנוני: `research/assets/casa-luma-logo.png`.

## מבנה טכני

- קוד החנות: `research/order-page.js`, `order-page.css`, `order-page.html.in`.
- לוגיקת סל והזמנות: `research/order-core.js`; נתונים: `research/catalog-data.json`.
- בנייה: `research/build_research.py`, `research/order_renderer.py`; `docs/` הוא עותק הפרסום הסטטי.
- שרת בפיתוח: `server/app.py`, מסך כניסה `server/auth.html`; FastAPI, סשנים ו-CSRF. PostgreSQL נדרש לפריסה משותפת; SQLite משמש לבדיקות.
- בדיקות ממוקדות: `research/test-order-core.cjs`, `server/test_app.py`. מעבר בדיקות מקומי אינו הוכחה לפריסה מוצלחת.
- קובצי HTML שנוצרו אינם המקור לעריכה. מפתח קבצים: [files](files/README.md).

## תמונת מצב שאינה אימות מסחרי

במיפוי הנוכחי 154 מוצרים ולידים, 13 קטגוריות ו-36 רשומות ספקים. איכות, זמינות ומשלוח למיקוד 84280 לא אושרו לכל מוצר. שדה מחיר ידני אינו מאמת מחיר ספק. קישור חיפוש אינו חנות רשמית מאומתת.

המאגר ציבורי: אין להעלות סודות, קובצי סביבה, מסדי נתונים או מסמכי המקור הפרטיים. הגיבוי המלא המקורי נמצא בתיקייה המקבילה `_backup-Casa-Luma-Shop-2026-10-20`, עם `BACKUP-MANIFEST.json`; הוא נפרד מהגיבוי הציבורי ב-GitHub.
