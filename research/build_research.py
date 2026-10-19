from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit
import json, re, html

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'research'
DATE = '18.10.2026'
products = []

def add(cat, name, supplier, url, price=None, regular=None, currency='THB', evidence='דף יצרן נפתח', quality='', shipping='לא אושר ל־84280', decision='מועמד לדגימה', note=''):
    products.append(dict(category=cat, name=name, supplier=supplier, url=url, price=price, regular=regular, currency=currency, evidence=evidence, quality=quality, shipping=shipping, decision=decision, note=note, checked=DATE))

pt = 'https://th.plantoys.com/en/products/'
for name, handle, price, regular, age, note in [
 ('עכבר עץ נמשך — Moving Mouse','moving-mouse',114,190,'3+','40% הנחה; מחיר הווריאנט הוורוד אומת. כמות זמינה לא פורסמה.'),
 ('משחק זיכרון בקופסה — Memo Game','memo-game-planmini',174,290,'3+','40% הנחה; קופסה קטנה ופעילות לשולחן. מתויג בקטלוג כמוצר מופסק — לבדוק אפשרות חידוש מלאי.'),
 ('דינוזאור Stegosaurus','stegosaurus',150,250,'12 חודשים+','40% הנחה; PlanWood, חומר מעץ מעובד; אינו עץ מלא. מתויג כמוצר מופסק.'),
 ('דינוזאור Diplodocus','diplodocus',150,250,'12 חודשים+','40% הנחה; PlanWood; מתויג כמוצר מופסק.'),
 ('דינוזאור Tyrannosaurus Rex','tyrannosaurus-rex',150,250,'12 חודשים+','40% הנחה; בתיאור הספק יש טעות העתקה שמזכירה אריה. לאשר תמונה ו־SKU 6133; PlanWood.'),
 ('דינוזאור Triceratops','triceratops',150,250,'12 חודשים+','40% הנחה; PlanWood; מתויג כמוצר מופסק.'),
 ('סירת משחק — Sail Boat Blue','sail-boat-blue',180,300,'תג קטלוג: 4 חודשים+','40% הנחה; PlanWood ומפרש גומי טבעי. יש סתירה בין שם Blue לטקסט Yellow; לאשר צבע וגיל על האריזה. מתויג כמוצר מופסק.'),
 ('כלי הקשה טווס — Peacock','bird-percussion-peacock',180,300,'18 חודשים+','40% הנחה; עדיפות נמוכה לשימוש בתוך הקפה בגלל רעש; מתויג כמוצר מופסק.'),
 ('קליידוסקופ פטרייה','mushroom-kaleidoscope',171,190,'18 חודשים+','10% הנחה בלבד; מתאים למתנה קטנה.'),
 ('משרוקית לווייתן','whale-whistle',190,190,'3+','ללא הנחה. מתאים לאופי האי, אבל רועש.'),
 ('משרוקית דולפין','dolphin-whistle',190,190,'3+','ללא הנחה; לא לתצוגת התנסות בפה בין ילדים.'),
 ('סט 4 סביבונים — Mini Spinning Tops','mini-spinning-tops',324,360,'3+','המחיר הוא לסט ארבעה; לא להניח שאפשר לפצל מכירה בלי אריזה וסימון מתאימים.'),
 ('משחק שיווי משקל קקטוס קטן','mini-balancing-cactus',324,360,'3+','13 חלקים בקופסת פח; מתאים לשולחן, אך 10% הנחה בלבד.'),
]:
    add('צעצועי עץ',name,'PlanToys',pt+handle,price,regular,evidence='מחיר ומלאי אומתו בקטלוג הרשמי החי (WebMCP)',quality=f'יצרן מזוהה; לפי היצרן מיוצר בתאילנד. גיל: {age}. נדרשת דגימה.',note=note)

jm = 'https://www.joanmirothailand.com/product/'
jm_rows = [
 ('מודל קיפול נייר 3D','3d-paper-model-โมเดลกระดาษ-3-มิติ/',165,'לבדוק שזו ערכה ללא דבק/מספריים ולבחור חיות ים או מטבח.'),
 ('חוברת לימוד ציור','สมุดสอนวาดภาพชุดสัตว์โ/',165,'Step by Step Drawing Book; לבדוק שפת הוראות ותוכן לפני בחירה.'),
 ('חוברת צביעה ראשונה','my-first-coloring-book-สมุดหัดระบายสีสำหรั/',195,'פעילות נקייה; מחיר קמעונאי, נדרשת הנחת סוחר.'),
 ('חוברת צבעי מים ניידת','water-color-painting-สมุดระบายสีน้ำแบบพก/',350,'התאמה חזקה למצגת; נדרשת מעט מים ומגש קטן.'),
 ('מדבקות רב־פעמיות עם רקע','reusable-sticker-play-set-สติ๊กเกอร์ลอกใช้ซ้ำ/',390,'פעילות שקטה ומעט לכלוך; לבחור איור ללא דמויות מותג גדולות.'),
 ('מדבקות העברה — Busy City','transfer-sticker-สติ๊กเกอร์ลอกลาย/',280,'לבחור נושא מתאים; לבדוק גיל שימוש.'),
 ('כרטיסי גירוד — Fantasy','scratch-cards-fantasy-set/',195,'מופיע כהעדפה בצ׳אט, אבל יוצר פירורי גירוד — דגימה לפני שימוש בקפה.'),
 ('טושים רחיצים Baby Roo','baby-roo-washable-markers-set12-colors/',395,'מחיר החל מ־395 ועד 1,185 לפי סט; לבחור וריאנט מדויק.'),
]
for name,slug,price,note in jm_rows:
    add('יצירה נקייה',name,'Jarmelo / Joan Miro Thailand',jm+quote(slug,safe='/'),price,evidence='דף החנות הרשמית נפתח; מחיר מוצג',quality='יבואן תאילנדי מזוהה: Pamatop Trading. בקשת דוחות בדיקה למק״ט ולצבעים הספציפיים עדיין נדרשת.',shipping='מדיניות J&T בתוך תאילנד; 84280 לא אושר בנפרד',note=note)

for name,url,price,regular,note in [
 ('תרסיס נגד יתושים 50 מ״ל','mozzie-mineral-spray-50ml/',260,280,'מחיר קמעונאי; ההנחה לבדה אינה מאפשרת מרווח משמעותי.'),
 ('תחליב נגד יתושים 50 מ״ל','organic-premium-baby-lotion/',265,285,'לבדוק תווית, מרכיבים וגיל לפני בחירה.'),
 ('ג׳ל לאחר עקיצות 18 מ״ל','mozzie-gel/',275,295,'בדף היצרן יש סתירה: 3 חודשים+ לעומת מלידה. לא לקבוע גיל מתאים עד קבלת תווית/אישור.'),
 ('משחת שיניים תות 40 מ״ל','ยาสีฟันออร์แกนิค-กลิ่น-2/',175,195,'לפי היצרן ללא פלואוריד. מתועד כמפרט מוצר בלבד; לא מסקנה על יעילות או יתרון לילדים.'),
]:
    add('טיפוח ומשפחה',name,'Khun Organic','https://khunorganic.co.th/product/'+quote(url,safe='/'),price,regular,evidence='מחיר אומת באתר היצרן החי',quality='יצרן מזוהה; טענות טבעי/אורגני הן טענות הספק. אישורים ודגימות לא נבדקו.',note=note)
add('טיפוח ומשפחה','Sól Milky SPF50 PA++++ 30 מ״ל','Sollie','https://shop.line.me/@sollie/product/1005519930',825,evidence='מחיר מדף בתוצאת אתר LINE שנקראה; אינו הצעה עדכנית בקופה',quality='המותג מציין מינרלי וגיל שנה+; נדרשים INCI ודוח SPF. אין כאן אימות reef-safe.',decision='רק אם מתקבלת הנחת סוחר משמעותית',note='825 באט לצרכן — אינו מחיר רכש מומלץ. משלוח ומלאי דורשים אימות.')

add('תיקים ואביזרים','פאוץ׳ כותנה אתני 10×14 ס״מ','Handbag Asia / Prestige Creations','https://handbag-asia.com/product/ethnic-cotton-bags/',2,currency='USD',evidence='מחיר $2 נצפה בדף היצרן החי',quality='לפי היצרן 100% כותנה; ייצור בתאילנד. לבדוק תפירה, צבע ותחושה בדגימה.',decision='עדיפות להצעת מחיר ודגימה',note='מחיר אתר בלבד; MOQ, מחיר למשלוח מקומי, מס והדפסה לא אושרו. לא הומר לבאט.')
for name,url,price,note in [
 ('Scrunchie כחול','https://madebysora.com/scrunchie?id=scrunchie-blue',180,'מחיר לצרכן; לבדוק גוון שאינו ניאון ולבקש מחיר סוחר.'),
 ('פאוץ׳ Batik Bloom','https://madebysora.com/product?id=batik-bloom',400,'דוגמת בד משתנה; מועמד למוצר מתנה, לא מציאה במחיר לצרכן.'),
 ('תיק Sunrise Blue Batik','https://madebysora.com/product?id=sunrise-bag-blue-batik',950,'עבודת יד מקוסמוי; להשוות לדגימה ולבקש מחיר סוחר. אין הצדקה אוטומטית למחיר פי 3.'),
 ('מחזיק מפתחות מבד תאילנדי','https://madebysora.com/keychain',220,'הכיתוב הכלול הוא Thailand או Koh Samui; Koh Phangan אינו כלול אוטומטית. תוספת כיתוב באתר 240 באט.'),
]:
    add('תיקים ואביזרים',name,'Sora Studio',url,price,evidence='מחיר נצפה באתר החי',quality='לפי היצרנית עבודת יד בקוסמוי; יש הצעת סיטונאות באתר, ללא מחיר סוחר מפורסם.',shipping='האתר מציין משלוח חינם בתאילנד; 84280 לא אושר בנפרד',decision='הצעת סוחר לפני רכישה',note=note)
add('תיקים ואביזרים','גומיית כותנה בעבודת יד','IslaNatural Phuket','https://islanaturalphuket.com/products/islanatural-scrunchie',300,evidence='מחיר והודעת משלוחים נצפו באתר החי',quality='לפי המותג כותנה בעבודת יד בתאילנד; אין ביקורות מוצר באתר.',decision='עדיפות נמוכה במחיר לצרכן',note='האתר מודיע סגור 9–20 באוקטובר; משלוח הזמנות מ־8 באוקטובר מתחיל ב־21 באוקטובר. לא לבנות על הגעה לפתיחה ב־23.')

for name,path,price,note in [
 ('סט 4 קשיות זכוכית','glass-drinking-straws/',13.99,'מחיר יצוא בדולר, לא מחיר מקומי סיטונאי; מתנה למבוגרים, לא מוצר מועדף לשימוש ילדים.'),
 ('תיק כותנה Patchwork Tote','patchwork-tote-bag/',29.99,'מתאים ללוק הטבעי; לבקש מחיר סוחר בבאט.'),
 ('סט 5 שקיות רשת לתוצרת','5-mesh-produce-bags/',22.99,'המחיר לסט, לא ליחידה; לבדוק אריזת מדף.'),
 ('לופה לניקוי כלים','natural-dish-scrubber/',15.99,'מחיר החל מ־15.99 דולר, קיימות אריזות 2/10. אין לחשב ליחידה ללא בחירת אריזה.'),
 ('מטליות מטבח רב־פעמיות','reusable-kitchen-cloths/',49.99,'מחיר החל מ־49.99 דולר; פחות מתאים לקנייה אימפולסיבית במחיר הציבורי.'),
]:
    add('בית ומתנות',name,'SuperBee','https://superbee.me/s/'+path,price,currency='USD',evidence='מחיר נצפה בקטגוריית Kitchen באתר החי',quality='מותג תאילנדי מזוהה; באתר הצהרות B Corp וכותנה GOTS במוצרי הבד. לא אישור לכל מק״ט.',decision='מחיר סוחר מקומי נדרש',note=note)
for name,path,note in [
 ('עטיפות מזון משעוות דבורים','https://superbee.me/c/beeswax-wraps/','עמוד קטגוריה, לא מק״ט ולא מחיר מאומת. התאמה חזקה לסגנון החנות.'),
 ('מברשות שיניים מבמבוק','https://superbee.me/s/bamboo-toothbrushes/','קישור מתוך דף הסיטונאות החי; לבדוק האם קיים גודל ילדים ואריזה ליחידה.'),
 ('פדים רב־פעמיים מכותנה','https://superbee.me/s/organic-cotton-rounds/','קישור מתוך דף הסיטונאות; מועמד למתנה לאמא.'),
 ('עטיפות שעווה Rakpaa','https://shop.line.me/@rakpaahoney/product/1007859454','נמצא באינדקס LINE; מחיר וחומר לא אומתו ישירות.'),
]:
    add('בית ומתנות',name,'SuperBee' if 'superbee' in path else 'Rakpaa',path,evidence='קישור ספק/קטגוריה אותר; מחיר לא אומת',quality='נדרש מפרט ודגימה.',decision='בקשת הצעה',note=note)

for name,sup,url,price,note in [
 ('חמאת שקדים Original Crunchy','Adaily Factory','https://shopee.co.th/adaily.factory',295,'מחיר שמוצג באינדקס החנות; גודל הווריאנט במחיר זה לא אומת. 30 גרם מופיע רק במצגת וטרם אומת במחקר.'),
 ('ריבת Jai Jai ללא תוספת סוכר — מארז 2','Jai Jai Jam','https://shopee.co.th/jaijai_jam',360,'מחיר אינדקס לסט שתי צנצנות; גדלים לא אומתו. 180 ליחידה בחלוקה בלבד; לא מחיר סוחר.'),
 ('חמאת בוטנים 100% — אריזת 1 ק״ג','Black Bear','https://shopee.co.th/เนยถั่วลิสง-100-แบบถัง-1-กก.-Black-Bear-100-Peanut-Butter-1-Kg.-i.980711761.44307432667',None,'קישור מוצר אותר באינדקס; מתאים גם לתפריט. לא לשנות אריזה למכירה בלי בירור תנאי הספק והסימון.'),
 ('תותים מיובשים בהקפאה','Black Bear','https://shopee.co.th/สตรอเบอร์รี่ฟรีซดราย-Strawberry-Freeze-Dried-Black-Bear-Bite-i.980711761.25936147535',None,'מוצר אותר באינדקס; לאשר רכיבים מלאים, גודל, לחות ותוקף.'),
 ('שקדים קלויים','Black Bear','https://shopee.co.th/มี-อย.-อัลมอนด์อบกรอบ-Almond-Dry-Roasted-Black-Bear-Bite-i.980711761.28758998797',None,'נדרש גודל אריזה ומחיר לקרטון.'),
 ('חמאת אגוזים — מגוון','Paweenee’s','https://shopee.co.th/paweenees',None,'עמוד חנות; לבחור Original ולא להניח שכל טעמי השוקולד ללא סוכר.'),
 ('פסטה אורז וירקות','Begin','https://thelittlestore.co/products/begin-organic-rice-spaghetti',None,'דף קמעונאי מציין 65% אורז אורגני, 30% ירקות ו־5% טפיוקה; לבדוק תווית של המק״ט המסוים.'),
 ('פסטה/רוטב ילדים — קטלוג מותג','Begin Baby Food','https://shop.line.me/@beginbabyfood',None,'ערוץ מותג מתוך דפי המוצרים שנמצאו; לבקש מחיר סיטונאי ורשימת רכיבים לכל טעם.'),
 ('דבש יער 500 גרם','Rakpaa','https://shop.line.me/@rakpaahoney/product/1007952212',720,'מחיר מדף מ־LINE; מוצר דבש, לא מוצר ללא סוכר. מרווח לא ידוע.'),
 ('מחית תפוח, בננה ותות 90 גרם','FrutoNanny','https://frutonanny.com/products/in-a-soft-package/apple-banana-and-strawberry-puree/',None,'מוצר בקטלוג היצרן הבינלאומי בלבד; יבואן תאילנדי, תווית ומשלוח טרם אומתו.'),
 ('Cocoa cereal 35g','OLY','https://www.olysnacks.com/product/190776-186425/cocoa-35g',75,'מחיר מוצג בקטלוג הציבורי; קוד CC-35. בחלק מהדפים כותרת Wild Honey שגויה — לאשר טעם ורכיבים.'),
]:
    add('מזווה וחטיפים',name,sup,url,price,evidence='מקור פומבי/אינדקס נקרא; מחיר ומלאי בקופה לא אומתו',quality='מועמד בלבד: נדרשת תווית רכיבים, אלרגנים, תוקף ודגימת טעם.',decision='מחיר סיטונאי ודגימה נדרשים',note=note)

for name,sup,url,note in [
 ('סט כותנה לתינוק','Elegant Kids','https://elegantkids.in.th/products/2-pcs-set-92','דף מוצר מציין טופ 100% כותנה ומכנס כותנת דנים. אין להניח שדגם זה אורגני רק כי המותג משתמש גם בבד אורגני.'),
 ('סט משפחתי Cotton Linen','Bloomingcub','https://shop.line.me/@bloomingcub/product/1004312334','נמצא ב־LINE; לבקש אחוזי הרכב מדויקים, מחיר סוחר וטבלת מידות.'),
 ('מכנס קצר Cotton Kids','Cottonica','https://shop.line.me/@cottonica/product/1001926642','נמצא ב־LINE; תיאור cotton linen אינו מפרט אחוזים; דגימה נדרשת.'),
 ('בגדי ילדים מתוצרת תאילנד','Anjuna Kids, Samui','https://anjunakids.com/','ספק סמוך גאוגרפית; האתר מציין כותנה וריון. לבקש דגמי 100% כותנה והצעת סוחר; אין אישור משלוח לקופנגן.'),
 ('גופייה/בגד כותנה ופשתן','Minene Thailand','https://minenethailand.com/products/26106003','דף מציין 50% כותנה/50% פשתן; לא נבדק מחיר או מרווח.'),
]:
    add('בגדים ואביזרי ילדים',name,sup,url,evidence='דף ספק/מוצר אותר במקור פומבי; רכש לא אומת',quality='מפרט הוא הצהרת מוכר; נדרשות בדיקת כביסה, התכווצות ותפירה.',decision='הצעה ודגימה לפני קנייה',note=note)

suppliers = [
 ('Samui Health Shop by Lamphu','מזווה, טיפוח ומוצרי אקו','https://www.samuihealthshop.com/wholesale/','עמוד חי נפתח; ספק עוגן','האתר מציין במפורש משלוח בסירה לקופנגן; מחיר, מסירה לנמל/לחנות וזמן טרם אושרו','LINE https://lin.ee/QrqcmxM ; WhatsApp https://wa.me/66966348752','מחירון, MOQ, חשבונית מס, מותגים שאפשר לרכז באותה הזמנה'),
 ('PlanToys','צעצועי עץ','https://th.plantoys.com/en/collections/planmini','מחירים ומלאי נבדקו בקטלוג חי','לא אושר למיקוד. מדיניות כללית מציינת עד 5 ימי עבודה, בכפוף למוביל','shopify-th@plantoys.com ; 02-237-9070','מחיר סוחר, אישור מכירה חוזרת, משלוח 84280 והמשכיות דגמי מבצע'),
 ('SuperBee','עטיפות שעווה, בד, במבוק וקשיות','https://superbee.me/wholesale/','עמוד סיטונאות חי; מחיר סוחר מאחורי הרשמה','לא אושר ל־84280. קיים מחסן בתאילנד לפי FAQ','https://shop.line.me/@superbeewaxwraps','MOQ ציבורי $200; עד 64% מרווח לפי הספק בהזמנות גדולות, לא הבטחה להזמנה ראשונה; לבקש מחיר מקומי בבאט'),
 ('Jarmelo / Joan Miro Thailand','יצירה','https://www.joanmirothailand.com/shop/','חנות חיה ומחירי מדף נקראו','J&T שני–שישי, חיתוך 11:00, זמן כללי 1–3 ימי עבודה. אין התחייבות ייעודית לאי','https://page.line.me/dro1878x','מחיר סוחר, חבילות קטנות, תעודות בדיקה למוצרים הנבחרים'),
 ('Handbag Asia / Prestige Creations','פאוצ׳ים, תיקי בד ומיתוג','https://handbag-asia.com/new-products/','דף מוצר חי; פאוץ׳ $2','לא אושר לקופנגן','https://handbag-asia.com/index.php/contact-us/','MOQ לכל דגם, כמות ניסיון מעורבת, מס, מחיר מקומי, דגימת תפירה'),
 ('Sora Studio, Koh Samui','תיקי בד ואביזרים','https://madebysora.com/','מחירי מדף חיים; מציעים wholesale','משלוח חינם בתאילנד לפי האתר; 84280 לא אושר','himadebysora@gmail.com ; https://wa.me/66610496855','מחיר סוחר/קונסיגנציה; ליין צבעים רגוע. אין הנחה סיטונאית מפורסמת'),
 ('Khun Organic','טיפוח ילדים','https://khunorganic.co.th/our-product/','אתר חי; מחירים אומתו','לא אושר ל־84280','https://line.me/R/ti/p/@exb8924u ; 094-545-6041','מחיר סוחר, INCI, תווית גיל מדויקת, קרטון מעורב'),
 ('Conscious Living Care','טיפוח טבעי','https://consciouslivingthailand.com/for-businesses/','אתר מותג ועמוד B2B נקראו','האתר מציין חינם מעל 2,000 באט בתוך תאילנד; האי לא אושר בנפרד','contact@consciouslivingthailand.com ; +66 89 156 9556','מחירון לעסקים, מוצרים קטנים, תוקף וחשבונית'),
 ('Jai Jai Jam','ריבות','https://shopee.co.th/jaijai_jam','נמצא באינדקס; אין מחיר סוחר','לא אושר','https://www.instagram.com/jaijai_jam/','רכיבים ותוקף לאחר פתיחה, גדלי צנצנות, מחיר קרטון, דגימה'),
 ('Adaily Factory','חמאות אגוזים','https://shopee.co.th/adaily.factory','חנות אותרה; מחיר אינדקס בלבד','לא אושר','LINE @adaily.factory — מהמצגת, לא אומת מחדש','לאמת שקיימים גדלי 30 גרם; Original ללא תוספות; מחיר סוחר'),
 ('Black Bear Superfood','חמאות אגוזים, פירות מיובשים','https://shopee.co.th/blackbear.superfood','לפי צ׳אט 17.10 נענו; אין הצעת מחיר כתובה בקבצים','לא אושר','https://www.instagram.com/blackbear.superfood/','מחיר סוחר, גדלים קטנים, תוויות אלרגנים והנחת קרטון'),
 ('BeALLA Organic Beauty','טיפוח','https://www.instagram.com/bealla_organicbeauty/','לפי צ׳אט 17.10 נענו; Instagram לא נגיש במחקר','לא אושר','קישור Instagram משמאל','לקבל קטלוג ותוויות; אין בקבצים מחירון מזוהה או דוחות איכות'),
 ('OLY Snacks','דגני בוקר וחטיפים','https://www.olysnacks.com/th/brand/671/oly','אתר וקטלוג ציבורי נקראו','לא אושר','https://www.olysnacks.com/th/contactus ; hello@olysnacks.com','להבחין בין no added sugar לבין המתקה בדבש; לקבל רשימת רכיבים'),
 ('Nature’s Delight','אגוזים ופירות יבשים','https://www.instagram.com/naturesdelightbrand/','קישור מהחומרים; נמצאו מוצרים בשם זה ב־Makro','לא אושר','https://shop.line.me/@naturesdelight','לאמת זהות מול המותג שב־Makro; אם זה אותו מוצר נפוץ — עדיפות לחומרי גלם לקפה ולא למדף הבוטיק'),
 ('Avocado Chiang Mai','טרם אומתה קטגוריית מוצרים','https://www.instagram.com/avocadochiangmai/','מסומן ❌ בצ׳אט; אין הסבר שמאפשר להסיק שלא שולחים','לא ידוע','Instagram משמאל','זהות, קטלוג, זמינות, שרשרת קירור לפי מוצר'),
 ('Rakpaa Honey','דבש ועטיפות שעווה','https://shop.line.me/@rakpaahoney','מותג ומוצרים אותרו','לא אושר','https://www.instagram.com/rakpaa.honey/','מחיר סוחר, מידות עטיפות, מחיר מתנות, משלוח 84280'),
 ('Phutawan','סבון, באלם ומוצרי ריח','https://phutawanshop.com/?lang=en','לפי צ׳אט 17.10 יש מדרגות הנחה; אתר רשמי אותר','לא אושר','https://www.instagram.com/phutawan_official/','מתחיל 5,000 באט ב־15%; לא להגדיל הזמנה רק בשביל הנחה; לבדוק חשבונית ודוגמאות'),
 ('Plas Tao Koh Tao','קטלוג לא זמין בקבצים','https://www.instagram.com/plastao_kohtao/','לפי צ׳אט 18.10: רכישה בחנות בלבד','אין משלוח לפי העדכון בקבצים','Instagram משמאל','להוציא מרשימת ספקים למשלוח ישיר; איסוף עצמי הוא מסלול נפרד'),
 ('Paweenee’s','חמאות אגוזים','https://linktr.ee/paweenees','חנות Shopee נמצאה; מחיר סוחר לא נמצא','לא אושר','https://shopee.co.th/paweenees','לבחור טעמים לפי תווית מלאה; הנחת כמות ומינימום'),
 ('Sollie Skin','הגנה מהשמש','https://shop.line.me/@sollie/product/1005519930','דף מוצר נקרא; מחיר מדף 825 באט','לא אושר','https://www.instagram.com/sollieskin/','מחיר סוחר, נפח, INCI, SPF וגיל; לא להסתפק בכיתוב organic'),
 ('Coco Paradise Life BKK','חטיפי קוקוס ואגוזים','https://www.instagram.com/cocoparadiselife.bkk/','לפי צ׳אט 18.10: תכנון 30 יחידות והנחה צפויה 12%; לא אישור הזמנה','לא אושר','https://linktr.ee/cocoparadise','אין מחיר בסיס בקבצים; לבדוק דבש/סירופים, מחירון סוחר וחשבון תאילנדי ולא הונג־קונג'),
 ('FrutoNanny Thailand','מחיות לילדים','https://www.instagram.com/frutonanny.th/','לפי הצ׳אט ללא מענה; אתר יצרן בינלאומי נמצא','לא אושר','https://frutonanny.com/products/','יבואן תאילנדי מזוהה, תוויות, מחיר סוחר. אין אימות למשלוח מהאתר הבינלאומי'),
 ('IslaNatural Phuket','אביזרי כותנה','https://islanaturalphuket.com/products/islanatural-scrunchie','עמוד מוצר חי ומסלול wholesale','משלוח מחושב בקופה; מתחילים לשלוח 21.10 לפי הודעת האתר','contact@islanaturalphuket.com','מרווח במחיר סוחר, זמינות למשלוח בזמן'),
 ('Elegant Kids','בגדי תינוקות ומוסלין','https://elegantkids.in.th/','יצרן תאילנדי עם ערוץ wholesale לפי האתר','לא אושר','https://elegantkids.in.th/th/pages/about-us','ליין רגוע, הרכב ואישור לכל בד, MOQ ומידות'),
 ('Anjuna Kids, Samui','בגדי ילדים','https://anjunakids.com/','אתר עסק מקומי נקרא באינדקס','לא אושר','אתר משמאל','סיטונאות או קונסיגנציה; כותנה לעומת ריון, זמני מילוי מלאי'),
 ('LittleNovaBangkok','אביזרי שיער בעבודת יד','https://www.instagram.com/littlenovabangkok/','מהצ׳אט; נמצאו מוצרי מוכר בשם זה ב־Etsy','לא אושר','https://www.etsy.com/listing/1710316038/sun-cloud-and-rainbow-hair-clips-felt','לקבל מחיר מקומי; Etsy אינו מחיר סיטונאי ולא אישור זהות סופי'),
 ('I Found Something Good','מדבקות וגלויות מאיירים','https://shopee.co.th/ifoundsthgood','חנות באינדקס; במצגת מופיע כליד','לא אושר','Shopee משמאל','מחיר סוחר או חיבור ישיר למאיירים; מדבקות טקסט תאילנדי אינן בהכרח מתאימות לקהל'),
 ('141 Social Enterprise','צעצועי עץ מקומיים','https://en.pinkoi.com/product/CbfAvitW','מוצר סביבון אותר ב־Pinkoi','לא אושר','https://en.pinkoi.com/product/Qr6xdvmp','מחיר מקומי סיטונאי, גיל, בדיקות גימור וצבע'),
 ('Oinic Life','סבון טבעי בסיטונאות','https://www.oiniclife.com/','אתר ספק סיטונאי אותר','לא אושר','אתר משמאל','MOQ, מחיר ליחידה, INCI ודגימות; טענת cold process אינה הוכחת איכות לבדה'),
 ('Command+P Studio','מדבקות וגלויות Casa Luma','https://www.commandpstudio.com/en','בית דפוס תאילנדי; עמוד שירותים נקרא','לא אושר','LINE @commandpstudio','מחיר 50/100 גיליונות, עמידות במים ודוגמת הדפסה'),
]

LAZ = [
 ('צעצועי עץ','Mini Balancing Cactus','https://www.lazada.co.th/products/plantoys-mini-balancing-cactus-3y-i2944165651.html','קישור אינדקס בלבד; מחיר/מוכר/מלאי לא אומתו'),
 ('צעצועי עץ','PlanToys — עמוד מותג','https://www.lazada.co.th/plantoys/','נפתח, אך קטלוג ומחירים לא נטענו; עמוד מותג אינו אישור לחנות רשמית'),
 ('יצירה נקייה','Melissa & Doug Water Wow','https://www.lazada.co.th/products/melissa-and-doug-reusable-water-wow-7-i4712254480.html','קישור אינדקס בלבד; לאמת מוכר מורשה ומקוריות'),
 ('יצירה נקייה','Water Wow Under the Sea','https://www.lazada.co.th/products/melissa--doug----water-wow-under--the-sea-i5996262689.html','קישור אינדקס בלבד; מתאים רעיונית, אין אישור איכות לפריט'),
 ('יצירה נקייה','Jarmelo Dot Painting','https://h5.lazada.co.th/products/joan-miro-dot-painting-set-non-toxic-dot-painting-set-educational-toy-for-kids-big-and-round-easy-grip-for-little-kids-i2690023247.html','קישור אינדקס בלבד; צבעי דוט אינם נטולי לכלוך'),
 ('טיפוח ומשפחה','Khun Organic — ביקורות מוצר','https://www.lazada.co.th/product-reviews/?item_id=4321544353','זה קישור ביקורות, לא עמוד רכישה ולא הוכחת דירוג'),
 ('טיפוח ומשפחה','Khun ג׳ל עקיצות — ביקורות','https://www.lazada.co.th/product-reviews/?item_id=5385392701','זה קישור ביקורות; מחיר וספק לא אומתו'),
 ('טיפוח ומשפחה','Baybee Organic 40g','https://www.lazada.co.th/products/baybee-40g-i5121665334.html','זוהה לפי קישור אינדקס; סוג המוצר/וריאנט דורשים אישור'),
 ('מזווה וחטיפים','Adaily Crunchy Chocolate Salted Almond','https://www.lazada.co.th/products/adaily-factory-crunchy-chocolate-salted-almond-butter-i2590354049.html','קישור אינדקס; רכיבים ותוספת סוכר לא אומתו'),
 ('מזווה וחטיפים','Adaily Crunchy Matcha Almond','https://www.lazada.co.th/products/adaily-factory-matcha-almond-butter-smooth-i2589522176.html','קישור URL מציין smooth — לאשר וריאנט; אין מחיר מאומת'),
 ('מזווה וחטיפים','Adaily Keto Chocolate Almond','https://www.lazada.co.th/products/adaily-factory-keto-chocolate-almond-butter-i2684915185.html','קישור אינדקס; keto אינו בהכרח ללא ממתיקים'),
 ('מזווה וחטיפים','Xongdur Organic Instant Congee','https://www.lazada.co.th/products/xongdur-organic-instant-congee-i4132780758.html','קישור אינדקס; עדיפות נמוכה, לבדוק התאמה למזווה'),
 ('בית ומתנות','SuperBee Beeginner Wrap Set','https://www.lazada.co.th/products/superbee-wax-wraps-beeginner-set-hipster-100-g-i1690922934.html','קישור אינדקס; לאמת מוכר ואריזת סט'),
 ('בית ומתנות','SuperBee Five Mesh Produce Bags','https://www.lazada.co.th/products/superbee-5-five-mesh-produce-bags-i2693473029.html','קישור אינדקס; להשוות מחיר לסט של 5'),
 ('טיפוח ומשפחה','DODOLOVE מגבונים — קרטון 16×80','https://www.lazada.co.th/products/whole-box-of-16-packs-80-sheets-of-dodolove-organic-baby-wipes-cleaning-wipes-for-children-dodolove-organic-wet-wipes-i5003449160-s21131629219.html','היעד שנחשף בהפניית הקישור המקורי; נחסם באימות גישה. אינו קישור לחיתולי שחייה'),
]

SEARCHES = [
 ('תיקים ואביזרים','פאוצ׳ים מכותנה','กระเป๋าผ้า cotton pouch handmade'),
 ('תיקים ואביזרים','גומיות פשתן','linen cotton scrunchie handmade'),
 ('טיפוח ומשפחה','חיתולי שחייה DODOLOVE','DODOLOVE กางเกงว่ายน้ำ'),
 ('טיפוח ומשפחה','Khun נגד יתושים','Khun Organic กันยุง'),
 ('טיפוח ומשפחה','משחת שיניים Lamoon','Lamoon toothpaste'),
 ('בית ומתנות','SuperBee','SuperBee'),
 ('יצירה נקייה','ספר מים של מותג מזוהה','Melissa Doug Water Wow'),
 ('יצירה נקייה','Jarmelo קיפול נייר','Jarmelo 3D Paper Model'),
 ('מזווה וחטיפים','Adaily Original','Adaily Factory original almond butter'),
 ('בגדים ואביזרי ילדים','Elegant Kids כותנה','Elegant Kids cotton'),
 ('בגדים ואביזרי ילדים','כובעי שמש UV','kids sun hat UPF50'),
 ('בגדים ואביזרי ילדים','חולצות שחייה UV','kids rash guard UPF50'),
]

def link(label,url):
    return f'[{label}]({url})'

def table(headers, rows):
    clean=lambda x:str(x if x is not None else 'לא פורסם').replace('|',' / ').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(map(clean,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(clean,r))+' |' for r in rows])

intro = '''# Casa Luma — מחקר מוצרים וספקים לחנות

תאריך מחקר: 18 באוקטובר 2026 · יעד משלוח: Koh Phangan 84280 · כל המחירים לפני עלות משלוח אלא אם צוין אחרת.

## מה אפשר להסיק כבר עכשיו

המועמדים המיידיים הטובים ביותר שנמצאו במחיר ציבורי הם עכבר PlanToys ב־114 באט, משחק זיכרון ב־174, ארבעת דגמי הדינוזאורים ב־150 וסירת המשחק ב־180. דגמים אלה הוצגו בהנחה של 40% מהמחיר הרגיל של אותו יצרן; זו אינה הוכחה למחיר נמוך ב־40% מכל השוק. הקליידוסקופ ב־171 מוצג בנפרד בהנחה של 10% בלבד. עבור מרווח גבוה יותר כדאי לרכז הצעת סוחר מ־SuperBee, פאוצ׳ים/אביזרי בד ומוצרי יצירה, ולא לבסס את הקנייה על מחירי מדף של מותגי טיפוח.

**המחקר לא מאשר עדיין סל רכישה שכל מוצריו איכותיים ושכולם נשלחים ל־84280.** יש רשימת מועמדים מסוננת, מחירים שאומתו בחלק מהערוצים, והפרדה מפורשת בין מה שנבדק לבין מה שעוד דורש אישור. לא נשלחו הודעות לספקים ולא בוצעו הזמנות.

פי 3 הוא שאיפה, לא תנאי סף — בהתאם להבהרת אוהד בשיחה. מוצר איכותי ומבודל עם מרווח קטן יותר נשאר מועמד. אין כאן מחיר מכירה מקומי מאומת ואין המלצה להעלות אוטומטית מחיר פי 3.

## רמות האימות

- **חי:** נפתח אתר או קטלוג יצרן במהלך המחקר; צוין בדיוק מה נצפה.
- **מקור פומבי/אינדקס:** נמצא דף או רישום בחיפוש; המחיר יכול להיות צילום מצב ישן, ולא מחיר קופה נוכחי.
- **מהחומרים:** מידע מהמצגת, PDF או הצ׳אט, עם תאריך כשקיים. זו אינה תשובה חדשה מהספק.
- **חיפוש מוכן:** קישור חיפוש שנוצר עבורך; הוא אינו דף מוצר מאומת.

מבחינת משלוח: **אזכור מפורש של Phangan**, **מדיניות כללית לתאילנד**, **לא אושר**, או **לא שולחים לפי הצ׳אט**. גם אזכור Phangan אינו קובע מחיר משלוח, זמינות למק״ט או מסירה לדלת החנות.

## הכיוון שנלקח מהחומרים

חנות קטנה למשפחות באי: חומרים טבעיים, צבעים רגועים, מתנות לאמא, ציוד שימושי למשפחה, יצירה נקייה, מוצרי מזווה ובגדי ילדים. המצגת מעדיפה 2–3 ספקי עוגן ועוד יצרנים קטנים, חשבונית מס, כמויות ניסיון והחלפת מוצרים שלא נמכרים. בקבצים אין תמונות WhatsApp עצמן — רק סימוני Image; לכן אי אפשר לזהות בדיעבד אילו מוצרים מצולמים אושרו או נפסלו.

הסינון במחקר נשען על יצרן מזוהה, חומר ומפרט, התאמה לחנות ודגימה נדרשת. מדינת הייצור, המחיר והמילים natural/organic לבדם אינם אימות איכות. לא הוכנסה המלצת קנייה למוצר גנרי רק משום שהוא זול.

## סדר עדיפויות מעשי

1. **Samui Health Shop:** לקבל הצעה מרוכזת למזווה ולטיפוח, עם משלוח בסירה לקופנגן. זה הספק היחיד במחקר שנצפתה אצלו הצהרה מפורשת על המסלול לאי.
2. **PlanToys:** לבדוק דגימה קטנה של עכבר, משחק זיכרון ו־2 דינוזאורים. במבצע הציבורי המרווח במחיר הרגיל הוא 40% לפני משלוח; דגמים רבים מתויגים כמופסקים, ולכן זו הזדמנות נקודתית ולא בהכרח קו קבוע.
3. **Handbag Asia / SuperBee:** לבקש מחיר מקומי לסוחר ולבחור 2–4 דגמים. יש פוטנציאל לבידול, אך טרם חושבה רווחיות מאומתת.
4. **Jarmelo:** מודל נייר, חוברת ציור/צביעה ומדבקות רב־פעמיות. המחירים שנמצאו הם לצרכן; דרושה הנחה לפני רכש למכירה חוזרת.
5. **Black Bear / Adaily / Jai Jai:** דגימות טעם, תוויות ותוקף לפני החלטה על כמות. לא הוצגה הנחה סיטונאית מאומתת.

## 1. צעצועי עץ — מחירים חיים ומלאי מסומן זמין

מחיר רגיל הוא מחיר ההשוואה של היצרן, לא סקר שוק. מחירי קטלוג PlanToys נמסרים בבאט; המלאי סומן זמין בזמן הבדיקה, ללא התחייבות לכמות. שינוע ל־84280 לא אושר.
'''

from enrich_catalog import enrich, STORES
enrich(products, OUT)
from expand_catalog import expand
new_products = expand(products, suppliers)
from widen_catalog import widen
new_products += widen(products, suppliers)
from order_renderer import prepare
prepare(products, suppliers)
parts=[intro, '\nעדכון 19.10.2026: נוספו '+str(len(new_products))+' מוצרים ולידים וקובץ הקטלוג הורחב לכלי בחירה והזמנות. מחירים קודמים נושאים את תאריך התצפית המקורי. דף העובד מופק באנגלית, והודעות הספק באנגלית או בתאית. ראו Ordering-Guide.md.\n']
for cat_index, cat in enumerate(dict.fromkeys(p['category'] for p in products), 1):
    if cat != 'צעצועי עץ': parts.append('\n## '+str(cat_index)+'. '+cat+'\n')
    rows=[]
    for p in products:
        if p['category']!=cat:continue
        price='לא פורסם' if p['price'] is None else f"{p['price']:g} {p['currency']}"
        if p['regular'] and p['regular']!=p['price']:price+=f" במקום {p['regular']:g}"
        rows.append([link(p['name'],p['url']),p['supplier'],price,p['evidence'],p['note'],p['shipping']])
    parts.append(table(['מוצר וקישור','ספק','מחיר ציבורי','מה אומת','התאמה / מגבלה','משלוח לקופנגן'],rows))
    if cat=='יצירה נקייה':parts.append('\nהאתר הרשמי נפתח ונקראו מחירי המדף. מקוריות ואישורי חומרים לכל מק״ט עדיין דורשים מסמך מהיבואן. גירוד ודוט יוצרים לכלוך מסוים; ספרי נייר ומדבקות עדיפים לניסוי הראשון. [מדיניות משלוח Jarmelo](https://www.joanmirothailand.com/deliverymethod/).')
    if cat=='טיפוח ומשפחה':parts.append('\nיש מחירי השוואה ציבוריים טובים לדיון עם הספקים, אך אין כאן מציאת רכש מוכחת. אין להשתמש בטענות טבעי, מינרלי או reef-safe כהוכחה ליעילות, בטיחות או התאמה לגיל. במקרה Khun ג׳ל יש סתירת גיל בדף עצמו; אין המלצת שימוש עד הבהרה.')
    if cat=='בית ומתנות':parts.append('\nבאתר SuperBee בורר המטבע הראה THB אך מחירי המוצרים הוצגו ב־USD; נשמרו הסכומים כפי שנראו, ללא המרה וללא הנחה שהם המחירים המקומיים. לא הסתמכתי על מבצעי 50% שהופיעו בגרסת חיפוש ישנה אך לא הופיעו בדף החי. קישורים אלה מיועדים לבחירת דגמים ולבקשת הצעת סוחר.')
    if cat=='מזווה וחטיפים':parts.append('\n[קטלוג OLY](https://www.olysnacks.com/th/brand/671/oly): Wild Honey ו־Cocoa 210 גרם הוצגו ב־365 במקום 385; 35 גרם ב־75 במקום 85. אלו הנחות קמעונאיות בלבד. במוצר עם דבש היצרן משתמש בניסוח no added sugar, אך דבש הוא רכיב ממתיק — אין לסווג אוטומטית כמתאים לכלל המזווה המחמיר של המצגת. ב־Coco Paradise הטעמים Honey ו־Caramel דורשים אותה בדיקת רכיבים. דבש טהור הוא קטגוריה בפני עצמה, לא מוצר נטול סוכר.')
    if cat=='בגדים ואביזרי ילדים':parts.append('\nלא נמצא במחקר ספק תאילנדי זול לבגדי UV עם אימות גם לדוח UPF וגם למשלוח 84280. הקטגוריה נשארת פתוחה; אין המלצת קנייה של חולצת UV גנרית רק על בסיס הכיתוב UPF50. ליין מידות קטן ודגימות כביסה יקטינו סיכון מלאי.')

parts.append('''
## 8. Lazada תאילנד — חנויות, הצעות חיות ולידים נוספים

עדכון: חנות Khun Organic Baby נטענה עם תמונות ומחירי כרטיסי מוצר, המתועדים בנפרד להלן. בחלק מהעמודים האחרים נטענו רק כותרות/וריאנטים, בלי מחיר ומשלוח. לכן **הלידים בטבלה הבאה אינם מוכרזים כאיכותיים, זולים או זמינים למשלוח ל־84280**. אלו מועמדים להשוואה מול החנות הרשמית, ולא רשימת הזמנה מאושרת. URL שנמצא בחיפוש אינו מבטיח שעמוד הרכישה עדיין פעיל.
''')
parts.append(table(['קטגוריה','קישור','מצב בדיקה'],[[c,link(n,u),s] for c,n,u,s in LAZ]))
parts.append('\n### חיפושים מוכנים ב־Lazada\n\nאלה קישורי חיפוש בלבד. אין להם מחיר, ספק או מוצר מאומת מראש.\n')
parts.append(table(['קטגוריה','חיפוש','מילים להעתקה'],[[c,link(n,'https://www.lazada.co.th/catalog/?q='+quote(q)),q] for c,n,q in SEARCHES]))
parts.append('''
## 9. ספר ספקים — כל 13 הספקים מה־PDF וספקים נוספים

סטטוס מענה מהצ׳אט אינו אישור לתנאים מסחריים. חשבונית מס, MOQ, החלפת סחורה ומחיר סיטונאי לא הונחו כקיימים כשלא נמצאה ראיה.
''')
parts.append(table(['ספק וקישור','קטגוריה','מקור / סטטוס','משלוח','ערוץ קשר ציבורי','מה חסר להצעת רכש'],[[link(n,u),c,s,ship,contact,ask] for n,c,u,s,ship,contact,ask in suppliers]))
parts.append('''
## 10. מה כבר ידוע מהצ׳אט — ולא צריך להתחיל מאפס

| ספק | הנתון בקבצים | המשמעות לרכש |
| --- | --- | --- |
| DODOLOVE חיתולי שחייה | ב־2.9 נכתב שהוזמנו 200 יחידות ב־3,000 באט כולל משלוח | 15 באט ליחידה, היסטורי. זו ראיה לעסקה קודמת, לא להצעת מחיר חדשה. לבדוק את אותו ספק לפני מעבר לחנות אקראית |
| DODOLOVE ישיר | ב־30.9 נכתב שהמחיר הטוב דורש 10,000 יחידות | לא לבחור כמות כזו בשביל הנחה. מדובר בעדכון היסטורי; לא MOQ שאומת היום |
| Mama Tales | ב־31.8 הוצגו 20 יחידות בסה״כ 3,569.5 באט, אחרי 45%, משלוח חינם | 178.475 באט ליחידה בחישוב, בכפוף לאימות. אין יתרון ברור למחיר פי 3 מעל מחיר המדף המקורי |
| Kindee | באוגוסט הוצעו 30% מעל 3,000 ו־35% מעל 10,000 באט | המצגת מציינת שחלק מהמוצרים נמכרים ב־7-Eleven. להשאיר רק מק״ט מבודל לאחר בדיקה מקומית |
| Phutawan | 17.10: 5,000 / 15,000 / 25,000 / 50,000 / 100,000 / 200,000 באט נותנים 15% / 20% / 25% / 30% / 35% / 40% | במחיר המכירה הרגיל אלו בקירוב מרווחים לפני משלוח והוצאות, לא יעד פי 3. מפיצי ריח נפרדים ויש חריג לקמפור |
| Phutawan diffuser | 50 מ״ל: 50 קופסאות ב־150 ליחידה; 100/200/300 ב־145/140/130. 100 מ״ל: 230/215/205/190 | יש חוסר בהירות בשיחה לגבי "קופסה". לא לפרש כקרטון מלא או כמארז רב־יחידות בלי אישור בכתב |
| Coco Paradise | 18.10: הוצעו 8 Cinnamon Almond, ‏8 Honey Cashew, ‏7 Toasted Caramel, ‏7 Brownie Protein Brittle; צפי ל־12% הנחה | 30 אריזות בסה״כ. אין בקבצים מחיר בסיס או אישור שההזמנה בוצעה; אי אפשר לחשב רווח |
| Plas Tao | 18.10: רכישה בחנות בלבד, ללא משלוח | לא ספק למשלוח ישיר לקופנגן לפי המידע הקיים |
| ריבות More Please | ב־28.9 הוזכר 200 לשתיים; ב־16.10 Pearl כתבה שלא רכשה בגלל המחיר | לא לטעון שנוסו/נטעמו. ה־0 באט בטקסט השיתוף אינו מחיר אמיתי מאומת |
| Cacao King / Satimi | קיים קשר מקומי בקופנגן ושיחה על אספקה | אין בקבצים קישור עסק ציבורי מאומת או מחירון מתאים. להשלים דרך הקשר שכבר קיים; לא לייחס את 95 באט לכוס למחיר אריזת קקאו |

## 11. מרווח — מה המספרים אומרים

מרווח גולמי = (מחיר מכירה פחות עלות כוללת ליחידה) / מחיר מכירה. הוא אינו תוספת המחיר על העלות. פי 3 על העלות נותן 66.7% מרווח לפני הוצאות החנות; פי 2 נותן 50%; פי 1.67 בערך 40%.

במחקר לא נמדדו מחירי מדף בחנויות בקופנגן. המחירים הרגילים של היצרן הם נקודת ייחוס בלבד, והנחות לחבר חדש/קופונים אישיים לא נחשבו למחיר רכש שניתן לשכפל.

| דוגמה | קנייה ציבורית | מחיר השוואה רגיל של היצרן | הפרש לפני משלוח | מרווח במחיר ההשוואה | עלות כוללת מרבית כדי להגיע לפי 3 באותו מחיר |
| --- | --- | --- | --- | --- | --- |
| PlanToys Moving Mouse | 114 | 190 | 76 | 40% | 63.33 |
| PlanToys Memo Game | 174 | 290 | 116 | 40% | 96.67 |
| PlanToys דינוזאור | 150 | 250 | 100 | 40% | 83.33 |
| PlanToys Sail Boat | 180 | 300 | 120 | 40% | 100 |
| Khun תרסיס 50 מ״ל | 260 | 280 | 20 | 7.1% | 93.33 |

כל הסכומים בטבלה בבאט. אם למשל מוקצים לעכבר 10 באט משלוח ו־5 באט אריזה/פחת, זו הנחת תרחיש בלבד: העלות 129, ובמכירה ב־190 המרווח 32.1%. לא התקבלה הצעת משלוח של 10 באט.

**איפה סביר לחפש מרווח גבוה:** פריטים קטנים מיוצר מקומי, מחיר סוחר ישיר, מותג Casa Luma או קונסיגנציה. זו השערה מסחרית לבדיקה, לא רווח מוכח. מוצרי מותג עם מחיר שקוף ברשת מתאימים לעיתים למרווח נמוך יותר ולשירות למשפחה.

## 12. ניסוי קנייה מצומצם — תרחיש, לא הזמנה

לצורך דגימה אפשר לשקול 3 עכברים, 3 משחקי זיכרון, 3 Stegosaurus ו־3 Triceratops. עלות מוצרים לפי המחיר שנצפה: **1,764 באט**. מחיר ההשוואה המצטבר של היצרן: **2,940 באט**. ההפרש: **1,176 באט / 40%**, לפני משלוח, אריזה, מסים לפי חשבונית והוצאות. המשלוח והיתר מכירה חוזרת לא אושרו, והמחיר יכול להשתנות. אם רוצים לבדוק איכות בלבד, אפשר להתחיל ביחידה אחת מכל דגם — 588 באט למוצרים.

במקביל, לפני קניית מלאי בד/יצירה: יחידת דגימה מכל אחד מהדגמים הרלוונטיים ובקשת מחיר סוחר. אין מספיק נתונים לבנות תקציב כולל אמין לשאר הקטגוריות.

## 13. איכות: מה צריך לקבל לפני אישור מק״ט

לא סומנו מוצרים כ״סופר איכותיים״ על סמך תמונות או מחיר. המוצרים לעיל מחולקים למועמדים עם מפרט יצרן ולידים שחסרים להם מסמכים.

| סוג מוצר | הראיה שצריך לפני אישור |
| --- | --- |
| צעצוע/יצירה לילדים | גיל על האריזה, יצרן/יבואן מזוהה, דוח בדיקת חומרים וצבעים למק״ט, דגימה לבדיקת קצוות/חלקים/ריח. לוגו מותג אינו דוח מעבדה |
| בדים | הרכב מדויק, תפירה, בדיקת כביסה/צבע/התכווצות. GOTS/OEKO-TEX רק אם התעודה מכסה את המוצר/בד שנבחר |
| מוצר מזון | תמונת רכיבים ואלרגנים באנגלית, תווית/יבואן מקומי, תוקף שנותר, הוראות אחסון ודגימת טעם. טעם שוקולד/דבש אינו אוטומטית ללא תוספת סוכר |
| טיפוח/הגנה מהשמש | INCI, מספר מוצר/יצרן, גיל לפי תווית ודוחות התומכים בטענות SPF/UPF לפי הצורך. מחקר זה אינו בדיקת יעילות רפואית |
| כלי אוכל/זכוכית | מפרט מגע במזון, חומר, גימור, אריזה נגד שבירה. קשיות זכוכית לא קיבלו המלצת שימוש לילדים |

## 14. משלוח 84280 — מצב אמיתי והפעולה שנותרה

- **Samui Health Shop:** הצהרה מפורשת על שינוע בסירה לפנגן נצפתה באתר חי. עדיין צריך תמחור, תאריך ומשלוח עד הדלת לעומת איסוף מהנמל.
- **Sora / Conscious Living / Jarmelo:** מדיניות משלוח בתוך תאילנד נמצאה; אין אישור ספציפי להזמנה ול־84280.
- **PlanToys ושאר הספקים:** אין אישור פרטני למיקוד; לא להסיק משלוח מעצם היות החנות תאילנדית.
- **Plas Tao:** אין משלוח לפי הצ׳אט.
- **Lazada:** חנות Khun נטענה עם מחירים; חנויות ודפי מוצר אחרים נטענו באופן חלקי. לא נבדק שדה משלוח תקין ל־84280 עבור אף מק״ט. נדרש להשלים באפליקציה או בדפדפן עם גישה תקינה ולבדוק מוצר+וריאנט+מוכר+כמות. לא בוצע ניסיון לעקוף אימות גישה.

המחקר מתקדם עד הנקודה שניתנת לבדיקה פומבית. אישור שכל המוצרים מגיעים לקופנגן מחייב אישורי ספקים/קופה; אין להציג אותו כאילו כבר התקבל.

### נוסח קצר לצוות לבקשת הצעה — לא נשלח

Hello, we are sourcing a small first order for a lifestyle and family shop in Koh Phangan, postcode 84280. Please quote the exact products and quantities listed below, including: wholesale unit price and VAT basis; mixed-order MOQ; availability and repeat-order prices; full Thai tax invoice; samples and product specifications/testing documents; shipping cost, island surcharge and expected delivery date; delivery to our shop versus pier collection; and damaged-item/return terms. Please specify each product size, variant and pack quantity. Thank you.

## 15. עוד קישורי פיתוח למותג Casa Luma

- [פאוצ׳ים טבעיים במידה ובהדפסה מותאמים](https://handbag-asia.com/product/plain-natural-cotton-custom-size-drawstring-bag/) — לבדוק MOQ והדפסה.
- [תיקי כותנה עם לוגו](https://denniswisser.com/product/custom-logo-eco-cotton-shopping-bag/) — ספק ייצור בתאילנד, מחיר וכמות לא אומתו.
- [SuperBee private label](https://wholesale.superbee.me/private-label-and-customisation/) — כיוון להמשך, לא MOQ מאומת להזמנה ראשונה.
- [Command+P — מדבקות, גלויות והדפסה](https://www.commandpstudio.com/en) — אפשר להשתמש באיור הבית/האי כדי לבדל; נדרש תמחור ודוגמה.
- [Zongggd — קטלוג דפוס](https://www.zongggd.com/en/products) — מחירי ״החל מ־״ לא הועתקו למחיר מק״ט, כי הם תלויים בכמות ובחומר.
- [141 — צעצוע אייל מעץ](https://en.pinkoi.com/product/Qr6xdvmp) ו־[חיפושית עץ](https://en.pinkoi.com/product/zt8NQUV8) — דגמים מסיפור יצרן מקומי, לא מחירי סיטונאות מאומתים.

## 16. מקורות מקומיים וגבולות המחקר

נקראו טקסט המצגת, PDF הספקים וייצוא השיחה ב־Markdown; קובץ txt זוהה כגרסה נוספת ולא שימש מקור נפרד. רשימת קישורי הספקים הציבוריים מהשיחה נשמרה בנפרד. תמונות/קטלוגים שמופיעים בצ׳אט כ־Image אינם כלולים בייצוא ואינם נגישים כאן. קישורי Google Drive/WPS נמצאים בקבצי המקור; תוכנם לא שימש כראיה. חלק מקישורי Instagram/Facebook ו־Heyzine לא נפתחו בכלי החיפוש; לא הוסקו מהם מחירים או איכות.

המקורות המסחריים מקושרים ליד כל פריט. מידע שסותר בין אינדקס ישן לדף חי נלקח מהדף החי; בפרט מחירי PlanToys, קטלוג SuperBee והודעת IslaNatural. מלאי, קופונים ומבצעים עשויים להשתנות. אין במחקר התחייבות מצד ספק או בדיקת מעבדה עצמאית.
''')


parts.append('''
## 17. ספק ראשי, מוכר בפועל וחנויות Lazada — עדכון תצוגה

״ספק ראשי״ להלן הוא היצרן או ערוץ המותג המזוהה, לפי רמת האימות הכתובה. אין בכך אישור שהחנות מפעילה את מפעל הייצור. כשנמצא יבואן או קמעונאי, תפקידו מפורש. חנות Lazada שלא אותרה אינה מוחלפת בקישור חיפוש המתחזה לחנות.
''')
parts.append(table(['מוצר','מותג / ספק ראשי','סוג המקור הראשי','המוכר / מקור המחיר','חנות Lazada'],[[link(p['name'],p['url']),link(p['primary_name'],p['primary_url']),p['primary_role'],p['seller_name'],link('חנות',p['lazada_store']['url']) if p['lazada_store'] else 'חנות ישירה טרם אותרה ואומתה'] for p in products]))
parts.append('''
### חנויות שאותרו
''')
parts.append(table(['מותג','חנות Lazada','רמת אימות','ראיה'],[[n,link('חנות המותג',v['url']),v['status'],link('מקור',v['evidence'])] for n,v in STORES.items()]))
parts.append('''
### הצעות חיות בחנות Khun Organic Baby

המחירים נצפו בכרטיסי החנות ב־18.10.2026. מחיר השוואה הוא המחיר המחוק בכרטיס, לא מחיר שוק. המחירים באתר היצרן בטבלאות הקודמות נשמרים בנפרד, עם מקור שונה. יש לאשר את הווריאנט, גודל היחידה והכמות בדף המוצר; מחיר קופה ומשלוח ל־84280 לא אומתו.
''')
parts.append(table(['מוצר','קישור מוצר ווריאנט','מחיר Lazada THB','מחיר השוואה THB','הנחה מחושבת'],[[p['name'],link('כרטיס החנות',p['lazada_offer']['url']),p['lazada_offer']['price'],p['lazada_offer']['regular'],f"{100*(1-p['lazada_offer']['price']/p['lazada_offer']['regular']):.1f}%"] for p in products if p['lazada_offer']]))
parts.append('''
### תמונות ועיצוב

צבעי ספר המותג: Cream #F9EDE8, Golden Sand #dfbc69, Sage #A8C3A0, Terracotta #E07A5F, Charcoal #333333. הלוגו המקורי הועתק ללא שינוי. תמונות מוצרים נטענות ישירות מאתרי המקור, לא נשמרו תמונות מרוחקות מקומית ולא נוצרו הדמיות מוצר. תמונת קטלוג יכולה להראות צבע/אריזה אחרים; יש לאשר וריאנט. במוצרים ללא צילום מופיע סמל קטגוריה עם תווית מפורשת.
''')
parts.append(table(['מוצר','מקור התמונה','תיאור'],[[p['name'],link('מקור',p['image_source']) if p['image_source'] else 'צילום לא אותר',p['image_note']] for p in products]))

report='\n\n'.join(parts)+'\n'
(OUT/'Casa-Luma-Sourcing-Research-2026-10-18.md').write_text(report)
(OUT/'catalog-data.json').write_text(json.dumps({'date':DATE,'updated':'19.10.2026','postcode':'84280','products':products,'suppliers':[dict(zip(['name','category','url','evidence','shipping','contact','next_step'],s)) for s in suppliers],'lazada_candidates':[dict(zip(['category','name','url','evidence'],r)) for r in LAZ]},ensure_ascii=False,indent=2))

# Preserve original public sourcing links; remove social share tracking, and do not
# copy chat messages, meeting links, or private document-share parameters.
chat=(ROOT/'Store Management (CL)'/'chat.md').read_text()
original=[]
for u in re.findall(r'https?://[^\s<>]+',chat):
    u=u.rstrip('_.,)')
    host=urlsplit(u).netloc.lower()
    if host not in {'www.instagram.com','www.facebook.com','onelink.shein.com','s.lazada.co.th','th.shp.ee','heyzine.com','khunorganic.co.th','share.google'}:continue
    if 'instagram.com' in host:
        x=urlsplit(u);u=urlunsplit((x.scheme,x.netloc,x.path.rstrip('/')+'/', '', ''))
    if u not in original: original.append(u)
archive=['# קישורי המקור מהחומרים','חולצו מייצוא השיחה; אלה אינם ספקים מאומתים. קישורי SHEIN הם היסטוריית רעיונות בלבד ואינם המלצות רכש. קישורי פגישות וקבצים פרטיים אינם מועתקים לכאן.','']
for i,u in enumerate(original,1):
    group='היסטוריית השראה — לא המלצה' if 'shein' in u else 'קישור מקור — זהות/תוכן דורשים בדיקה'
    if 'instagram' in u:group='ספק/מותג — קישור מקור, תנאים לא אומתו'
    archive.append(f'{i}. [{group}]({u})')
(OUT/'Original-Sourcing-Links.md').write_text('\n\n'.join(archive)+'\n')

# Local reader; product images load from the cited public supplier hosts.
from order_renderer import render
render(products, suppliers, LAZ, SEARCHES, OUT)
urls=set(re.findall(r'https?://[^\s<>"\)]+',report))
print(json.dumps({'products':len(products),'suppliers':len(suppliers),'lazada_links':len(LAZ),'lazada_searches':len(SEARCHES),'original_public_links':len(original),'distinct_report_urls':len(urls)},ensure_ascii=False))
