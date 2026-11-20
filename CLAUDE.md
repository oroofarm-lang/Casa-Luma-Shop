# Casa Luma Shop

סביבת עבודה לאיתור ספקים והזמנות של Casa Luma (קו פנגן, תאילנד). שלושה חלקים באותו ריפו:
קטלוג סטטי ציבורי (`docs/`), מקורות המחקר והבנייה שלו (`research/`), ואפליקציית רכש פרטית (`studio/`, Node + PostgreSQL).

## פקודות
- בדיקת הלוגיקה של דף ההזמנות: `node research/test-order-core.cjs`
- בדיקת סקריפט הקטלוג: `node research/catalog-script-check.js`
- בניית הקטלוג: סקריפטי Python ב-`research/` (`build_research.py`, `enrich_catalog.py`, `expand_catalog.py`, `widen_catalog.py`, `render_catalog.py`, `order_renderer.py`). אין קובץ שמפעיל את כולם בסדר; בודקים בקוד לפני הרצה.
- פרסום האתר: מעתיקים `research/order-page.html` ל-`docs/index.html`, עושים commit ו-push. GitHub Pages מפרסם `main` מתוך `/docs`.
- אפליקציית Studio: `cd studio && npm install && npm start` (Node 20+, דורש PostgreSQL ומשתני סביבה, ראו `studio/.env.example` (קיים ב-repo; PGSSL אופציונלי ולא מופיע בו)).
- בדיקות CI של Studio (כמו ב-`.github/workflows/casa-shop-studio-check.yml`): `node --check server.js`, `node --check public/app.js`, ובדיקה ש-`data/catalog-seed.json` מכיל 154 מוצרים ולפחות 13 ספקים.
- Health של Studio: `GET /health`.

## מבנה
- `docs/` - האתר הציבורי (GitHub Pages): `index.html` הוא הקטלוג, בנוסף `solo-studio.html` ו-`solo-*.js/css/json`.
- `research/` - נתוני הקטלוג (`catalog-data.json`), `order-page.html(.in)`, `order-core.js`, סקריפטי Python, מדריך הזמנה ומחקר.
- `studio/` - `server.js` (Express + pg), `public/` (ממשק), `data/catalog-seed.json`, `railway.json` (פריסה ל-Railway, שורש `/studio`).
- `vault/` - ידע הפרויקט בפורמט Markdown (Home, Decisions, Requirements, Backup-and-Publishing).
- `.github/workflows/` - בדיקת syntax ל-Studio.

## כללים חשובים
- הריפו ציבורי. לא מכניסים לריפו סודות, סיסמאות, גיבויים או קבצי מקור פרטיים. מוחרגים ב-`.gitignore`: `backups/`, `Store Management (CL)/`, `*.pdf`, `*.pptx`, `research/*-extracted.txt`, `.env`, `.env.*`.
- מחירים ומבצעים בקטלוג הם תצפיות, לא הצעות מחיר. משלוח לקוד 84280 ותנאי חשבונית דורשים אישור ספק.
- שום הזמנה לא נשלחת אוטומטית. הודעות לספקים באנגלית או בתאילנדית; העברת עבודה לעובד באנגלית.
- בחירות המשתמש נשמרות בדפדפן בלבד (לא בגיט, לא מסונכרן). לגיבוי מייצאים JSON מהקטלוג.
- `studio/` מנותק מהקטלוג הציבורי. כל הממשק שלו באנגלית. סיסמאות נשמרות כ-hash. לא מכניסים סיסמאות לקוד.
- הוספת משתמש בעל הרשאות: רק דרך `OWNER_NAME`/`OWNER_PASSWORD` בהרצה ראשונה על DB ריק; אחרי כניסה ראשונה מסירים את `OWNER_PASSWORD`.
- לא משנים את מספר 154 המוצרים ב-`studio/data/catalog-seed.json` בלי לעדכן את בדיקת ה-CI.
- המדיה הכבדה: אין. הגיבוי המלא (ZIP) נשמר מקומית בלבד ב-`backups/` ולא בגיט.
