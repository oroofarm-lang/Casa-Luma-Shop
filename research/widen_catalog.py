"""Observed source rows for the larger assortment, 19 October 2026."""
import hashlib
from urllib.parse import quote

def widen(products,suppliers):
    added=[]
    def add(cat,he,en,sup,url,price=None,regular=None,sku='',image=None,options='',summary='',source=None,kind='product',market=None,contact=None):
        s=next((s for s in suppliers if s[0]==sup),None)
        primary=s[2] if s else url
        p=dict(category=cat,name=he,name_en=en,supplier=sup,url=url,price=price,regular=regular,currency='THB',checked='19.10.2026',
          evidence='פרטי רישום/קטלוג ספק נקראו ב־19.10.2026; אין אישור מחיר סיטונאי או משלוח למק״ט',quality='מפרט ספק; דגימה ותווית נדרשות.',shipping='לא אושר למשלוח 84280',decision='דגימה והצעת ספק לפני אישור',note=summary,summary_en=summary,
          primary_name=sup,primary_url=primary,primary_role='ערוץ המותג; תנאי מסחר וחשבונית דורשים אישור',seller_name=sup,lazada_store=None,lazada_offer=None,image_url=image,image_source=source or url if image else None,image_note='תמונת הספק; לאשר צבע, מק״ט ואריזה' if image else 'צילום מוצר לא אותר',sku=sku,options_hint=options,kind=kind,source_url=source or url,
          sourcing_warning_en='Sample quality and confirm exact variant, wholesale terms, invoice and shipping to 84280. Prices are observations, not guaranteed repeat-order costs.')
        if market:
            p.update(platform=market,primary_name='SHEIN brand' if sup.startswith('SHEIN brand') else 'Manufacturer / primary brand not identified',primary_role='פלטפורמה אינה יצרן. מפעל, מוכר וחשבונית דורשים אישור.',primary_url=url,seller_name='SHEIN Thailand listing — operator not independently checked',
             promotion_status='unmarked',contact_info=contact or 'https://m.shein.com/th/Customer-Service-a-743.html?lang=then',
             order_sources=[dict(id='marketplace',supplier=sup+' · '+sku+' (seller unverified)',channel='SHEIN Thailand — invoice unconfirmed',url=url,store='https://th.shein.com/',price=price,currency='THB',contact=contact or 'https://m.shein.com/th/Customer-Service-a-743.html?lang=then')])
        p['id']='cl-'+hashlib.sha256((sup+'|'+url+'|'+he).encode()).hexdigest()[:16]
        if not any(x['url']==url for x in products+added):added.append(p)
    base='https://cdn.shopify.com/s/files/1/0550/2913/7495/files/'
    games=[
      ('פאזל בולי עץ קטן','Log Puzzle - PlanMini','log-puzzle-planmini',270,450,'4651','4651_-_Main_-_sq.jpg?v=1774514117','3Yrs+'),
      ('פאזל כלב','Dog Puzzle','dog-puzzle',360,600,'4636','4636_-_Main_-_sq.jpg?v=1774514053','18M+'),
      ('ערימת בולי עץ','Stacking Logs','stacking-logs',360,600,'4638','4638_-_Main_-_sq.jpg?v=1774514070','3Yrs+'),
      ('פאזל דינוזאור','Dino Puzzle','dino-puzzle',360,600,'4642','4642_-_Main_-_sq.jpg?v=1774514071','18M+'),
      ('פאזל תרנגולת','Chicken Puzzle','chicken-puzzle',360,600,'5673','5673_-_Main_-_sq.jpg?v=1774516395','12M+'),
      ('עץ איזון','Balancing Tree','balancing-tree',405,450,'5140','5140_-_Main_-_sq.jpg?v=1774514225','3Yrs+'),
      ('משחק Shake N Flip','Shake N Flip','shake-n-flip',450,750,'4633','4633_-_Main_-_sq.jpg?v=1774514053','3Yrs+'),
      ('מנקלה מעץ','Mancala','mancala',450,750,'4623','4623_-_Main_-_sq.jpg?v=1774514034','3Yrs+'),
      ('פאזל חיות ים','Marine Puzzle','marine-puzzle',540,600,'5688','5688_-_Main_-_sq.jpg?v=1774516531','12M+'),
      ('פאזל פיל','Elephant Puzzle','elephant-puzzle',600,600,'4635','4635_-_Main_-_sq.jpg?v=1774514052','18M+'),
      ('אבנים למישוש','Tactile Stone','tactile-stone',660,1100,'5451','5451_-_Main_-_sq.jpg?v=1774515966','2Yrs+'),
      ('משחק איזון Timber Tumble','Timber Tumble','timber-tumble',675,750,'4627','4627_-_Main_-_sq.jpg?v=1774514052','3Yrs+'),
      ('משחק דיג','Fishing Game','fishing-game%E3%85%A4',675,750,'4646','4646_-_Main_-_sq.jpg?v=1774514093','3Yrs+'),
      ('סירת איזון','Balancing Boat','balancing-boat',675,750,'5136','5136_-_Main_-_sq.jpg?v=1774514225','3Yrs+'),
      ('קוביות דוגמאות גאומטריות','Geo Pattern Cubes','geo-pattern-cubes',675,750,'4648','4648_-_Main_-_sq.jpg?v=1774514093','3Yrs+'),
      ('קוביות פאזל חיות','Animal Puzzle Cubes','animal-puzzle-cubes',675,750,'4649','4649_-_Main_-_sq.jpg?v=1774514118','2Yrs+'),
      ('משחק זיכרון חיות','Animals Memo','animals-memo',675,750,'4656','4656_-_Main_-_sq.jpg?v=1774514147','2Yrs+'),
      ('מציאת הפינגווין','Finding Penguin Game','finding-penguin-game',720,1200,'4645','4645_-_Main_-_sq.jpg?v=1774514093','3Yrs+'),
      ('משחק הבונה','Beaver Tumble','beaver-tumble',720,1200,'8907','8907_-_Main_-_sq.jpg?v=1774517737','3-99Yrs+'),
      ('נחש את כוכב הלכת','Guess My Planet','guess-my-planet',720,1200,'4655','4655_-_Main_-_sq.jpg?v=1774514117','3Yrs+'),
      ('משחק זיכרון רגשות','My Mood Memo','my-mood-memo',810,900,'5656','5656_-_Main_-_sq.jpg?v=1774516375','2Yrs+'),
      ('קקטוס איזון גדול','Balancing Cactus — full size','balancing-cactus%E3%85%A4',990,1100,'4101','4101_-_Main_-_sq.jpg?v=1774513987','3-99Yrs+'),
      ('דומינו רגשות','Mood Dominos','mood-dominos',990,1100,'8905','8905_-_Main_-_sq.jpg?v=1774517596','3-99Yrs+'),
    ]
    for he,en,h,price,reg,sku,img,age in games:
        add('משחקים ופאזלים',he,en,'PlanToys','https://th.plantoys.com/en/products/'+h,price,reg,sku,base+img,summary=f'Live manufacturer price, comparison price, SKU and available flag read on 19 Oct. Supplier age tag: {age}. Sample the finish and check the age label; trade price and restock price not confirmed.')
    eb='https://cdn.shopify.com/s/files/1/2435/4547/files/'
    clothes=[
      ('בגד גוף 56888','Bodysuit 56888','bodysuit-20',189,'56888.jpg?v=1764236954','0–6m / 6–12m'),
      ('רומפר 56884','Romper 56884','romper-27',249,'56884.jpg?v=1764235866','6–12m / 12–18m / 18–24m'),
      ('רומפר 57098','Romper 57098','bodysuit-copy-1',249,'57098.jpg?v=1786174588','0–6m / 6–12m / 12–18m'),
      ('רומפר 57089','Romper 57089','bodysuit-30',259,'57089.jpg?v=1786094928','0–6m / 6–12m / 12–18m'),
      ('סט שני חלקים 57074','Two-Piece Set 57074','2-pcs-set-158',259,'57074.jpg?v=1786779715','6–9m / 9–12m / 12–18m'),
      ('סט שני חלקים 57079','Two-Piece Set 57079','2-pcs-set-159',259,'57079_f85744c6-cfe9-414b-bd13-59c5f1725f44.jpg?v=1786780099','6–9m / 9–12m / 12–18m'),
      ('סט שני חלקים 57081','Two-Piece Set 57081','2-pcs-set-160',259,'57081.jpg?v=1786780389','6–9m / 9–12m / 12–18m'),
      ('שמלה 56766','Dress 56766','2-pcs-set-93',269,'6_ELDH-56766.jpg?v=1756793482','12–18m / 18–24m / 3 years'),
      ('אוברול שינה 56886','Sleepsuit 56886','sleepsuit-3',269,'56886.jpg?v=1764236596','0–6m / 6–12m'),
      ('אוברול 56873','Sleep n Play 56873','2-pcs-set-109',269,'56873.jpg?v=1764302692','0–6m / 6–12m'),
      ('סט שני חלקים 56874','Two-Piece Set 56874','sleep-n-play',269,'56874.jpg?v=1764303044','0–6m / 6–12m'),
      ('שמלה 56768','Dress 56768','dress-3',279,'8_ELDR-56768_e9d18161-cfd5-4c84-b0cf-17ec53ed12bc.jpg?v=1756794426','12–18m / 18–24m / 3 years'),
    ]
    for he,en,h,price,img,opts in clothes:
        add('בגדים ואביזרי ילדים',he,en,'Elegant Kids','https://elegantkids.in.th/products/'+h,price,image=eb+img,options=opts,summary='Live manufacturer collection price and available flag read on 19 Oct; no comparison price returned in collection tool, so discount status is unverified. Confirm exact fabric composition for this SKU, sizes in stock, wash sample and trade invoice.',source='https://elegantkids.in.th/collections/garments')
        added[-1]['promotion_status']='unknown'
    shein=[
      ('תיק רשת כותנה','Cotton Mesh Shopping Bag','1pc-Solid-Color-Mesh-Shopping-Bag%2C-Solid-Color-Woven-Mesh-Tote-Bag%2C-Large-Capacity-Foldable-Shopping-Bag%2C-Beach-Bag%2C-Summer-Handbag%2C-Suitable-For-Women-Young-People%2C-Ideal-For-Supermarket-Shopping%2C-Beach-Trips%2C-Daily-Outings-p-14132594.html',89,'sg2303225260034774','One piece / 2 pieces / 3 pieces — confirm which pack price applies','תיקים ואביזרים','SHEIN Marketplace · seller not identified'),
      ('תיק קרושה פסים','VCAY Cotton Striped Crochet Tote','Crocheted-Colorblock-Striped-Tote-Bag%2C-Vacation-Style-p-38446254.html',289,'sg2406287433849486','One size / colour','תיקים ואביזרים','SHEIN brand · VCAY'),
      ('תיק כתף כותנה קלוע','Cotton Woven Beach Shoulder Bag','Handmade-Woven-Retro-Style-Beach-Vacation-Shoulder-Bag-p-84282302.html',329,'sg25052232412285592','Beige / brown; confirm dimensions','תיקים ואביזרים','SHEIN Marketplace · seller not identified'),
      ('מכנסי כותנה מנוקדים לילדות','Girls Cotton Polka Dot Pants','Young-Girl-100%25-Cotton-Polka-Dot-Drawstring-Elastic-Waist-Pants-Young-Girls-Squishy-Polka-p-516454502.html',201,'sk260611185361501179839','4Y / 5Y / 6Y / 7Y; colour','בגדים ואביזרי ילדים','SHEIN brand · kids'),
      ('שמלת כותנה לבנה לילדות','Girls White Cotton Sleeveless Dress','SHEIN-Girls-Collared-Sleeveless-White-Summer-Fairy-Party-Dress-100-Cotton-Young-Girls-Clothes-Simple-Countryside-Cute-Soft-Casual-Child-Young-Dresses-p-403759937.html',188,'sk260105155732583948889','4Y shown; confirm other sizes, lining and opacity','בגדים ואביזרי ילדים','SHEIN brand · kids'),
      ('זוג מכנסי כותנה לילדים','Explorewe Cotton Leisure Pants — two-piece pack','SHEIN-Explorewe-Young-Boy-2pcs-Set-Pure-Cotton-Sweat-Absorbing-Elastic-Waist-Loose-Leisure-Pants-Baby-Blue-Baby-Pink-Outdoor-Nursery-Autumn-4-7-Years-p-65821770.html',379,'sk25030765073682504','4Y / 5Y / 6Y / 7Y; two-piece pack','בגדים ואביזרי ילדים','SHEIN brand · Explorewe'),
    ]
    for he,en,path,price,sku,opts,cat,sup in shein:
        add(cat,he,en,sup,'https://th.shein.com/'+path,price,sku=sku,options=opts,market='SHEIN',kind='lead',summary='Thai SHEIN listing/index observed with 100% cotton composition and THB price. This is a sample candidate, not independently verified quality. Checkout price, seller identity, repeat availability, shipping to 84280 and invoice type remain unconfirmed. Use the Thai customer-service channel; direct manufacturer contact was not found.')
    # Additional products already visible in the official Coconut Series catalogue.
    for he,en,h,price,img in [
      ('שמן רחצה קוקוס','Organic Coconut Shower Oil','coconut-shower-oil',450,'2023/01/Coconut-Shower-Oil_front-680x680.jpg'),
      ('סקרב מלח קוקוס','Organic Coconut Salt Scrub','coconut-salt-scrub',320,'2022/08/Coconut-salt-scrub_front-680x680.jpg'),
      ('חמאת סקרב גוף קוקוס','Organic Coconut Body Scrub Butter','coconut-body-scrub-butter',320,'2022/08/Coconut-body-scrub-butter_front-680x680.jpg'),
      ('מרכך שיער קוקוס','Organic Coconut Hair Conditioner','coconut-hair-conditioner',300,'2022/08/Coconut-Hair-conditioner_front-680x680.jpg'),
      ('מסכת שיער קוקוס','Organic Coconut Hair Treatment','coconut-hair-treatment',300,'2022/08/Coconut-hair-treatment_front-680x680.jpg'),
      ('שמפו קוקוס','Organic Coconut Hair Shampoo','coconut-hair-shampoo',300,'2022/08/Coconut-Hair-shampoo_front-680x680.jpg'),
      ('סט סבוני קוקוס','Organic Coconut Soap Bar Set','coconutsoapbar-set',360,'2026/05/Coconut-Soap-Bar-Packset-680x680.jpg'),
      ('חמאת לחות קוקוס','Organic Coconut Hydrating Butter','coconut-hydrating-butter',450,'2022/08/Coconut-hydrating-butter-680x680.jpg'),
    ]:
        add('ביוטי וטיפוח לאמא',he,en,'Phutawan','https://phutawanshop.com/en/product/'+h+'/',price,image='https://phutawanshop.com/wp-content/uploads/'+img,options='Volume / scent / pack contents',source='https://phutawanshop.com/en/product-category/coconut-series/',summary='Official live category-card price and image observed on 19 Oct. No sale marked on that card; this is not a repeat-price guarantee. Adult gift candidate; confirm full ingredients, fragrance, volume, sample and wholesale quote.')
        added[-1]['promotion_status']='unmarked'
    for he,en,slug in [
      ('צבעי שעווה Silky Crayon','Silky Crayons','สีเทียนเด็กปลอดสารพิษsilkycrayon/'),
      ('מדבקות ציפורניים','Nail Stickers','nail-stickers-ชุดสติ๊กเกอร์ติดเล็บ/'),
      ('גליל נייר לציור','Drawing Roll Paper','drawing-roll-paper-ม้วนกระดาษวาดเขียน/'),
      ('קעקועים זמניים ומדבקות','Temporary Tattoos & Nail Stickers','temporary-tattoos-and-nail-stickers-for-boys-and-girls/'),
      ('כרטיסי למידה מחיקים','Wipe-Clean Learning Cards','wipe-clean-learning-cards-ของเล่นการ์ดเขียนลบ/'),
      ('חוברת Doodling','Doodling Book','doodling-for-boy-and-girl-สมุดระบายสี/'),
    ]:
        add('יצירה נקייה',he,en,'Jarmelo / Joan Miro Thailand','https://www.joanmirothailand.com/product/'+quote(slug,safe='/'),options='Exact theme / colour set / pack / age',source='https://www.joanmirothailand.com/shop/',summary='Product link observed in the official Thai distributor shop. Price and pack not verified. Choose exact theme, age and set size; request sample and test documents. Check skin-contact labels for stickers/tattoos and supervise children; no safety certification inferred from the title.',kind='lead')
    add('מזווה וחטיפים','פולי קפה צ׳יאנג מאי 250 גרם','Chiang Mai Coffee Beans — Medium Roast 250 g','Kad Kokoa','https://kadkokoa.co/products/coffee-beans-medium-roast-250g-chiang-mai',390,image='https://cdn.shopify.com/s/files/1/0529/4050/5260/products/image.jpg?v=1662797106',options='Whole beans / grind if offered / roast date',summary='Live manufacturer catalogue price and available flag, 19 Oct. Thai coffee, 250 g; confirm roast date, trade margin, invoice and delivery. No private-label Casa Luma rights assumed.')
    added[-1]['promotion_status']='unknown'
    for he,en,path in [
      ('סט עטיפות שעווה בשלוש מידות','Beeginner Beeswax Wrap Set — 3 sizes','classical-beeswax-wrap-set'),
      ('גליל עטיפת שעווה','Beeswax Wrap Roll','beeswax-wrap-roll'),
      ('עטיפת לחם XXL','Breadwrap XXL','breadwrap-xxl'),
      ('שקיות שעווה למזון','Beeswax Bags','beeswax-bags'),
      ('טבליות משחת שיניים Dentos','Dentos Toothpaste Tabs','eco-toothpaste'),
      ('סבון מוצק לכביסה','Laundry Soap Bar','laundry-soap-bar'),
      ('לופה טבעית לגוף — זוג','Eco Shower Loofah Body Scrubbers — two-pack','eco-shower-loofah-body-scrubbers'),
      ('סבון מוצק לכלים','Dishwashing Soap Bar','dishwashing-soap-bar'),
    ]:
        add('בית ומתנות',he,en,'SuperBee','https://superbee.me/s/'+path+'/',options='Size / flavour if toothpaste / number per pack',source='https://superbee.me/',summary='Manufacturer product link found. Request local THB trade price, pack size, materials/ingredients and a sample through the brand contact or LINE. No export USD price used as a Thai wholesale price. Toothpaste fluoride/age details require the exact label.')
        added[-1]['primary_url']='https://superbee.me/wholesale/'
    for he,en,sku,img in [
      ('תרסיס נגד יתושים — 15 מ״ל','Mozzie Mineral Spray — travel 15 ml','5357393867-s22773491178','e2d3cd5185d6310cb2fe76e1653f1a54'),
      ('ג׳ל לאחר עקיצות — 10 מ״ל','Mozzie Gel — travel 10 ml','5357631016-s22817366008','91ce7a7e4c76c6cd04697877b2abe3df'),
    ]:
        add('טיפוח ומשפחה',he,en,'Khun Organic','https://www.lazada.co.th/products/pdp-i'+sku+'.html?search=store',89,115,image='https://img.lazcdn.com/g/p/'+img+'.png_400x400q80.png_.webp',options='One unit / exact volume and label age',source='https://www.lazada.co.th/shop/khun-organic-baby/',summary='Lazada shop-card offer observed on 18 Oct: 89 vs 115 THB. Not refreshed on 19 Oct. Confirm the exact small bottle variant, ingredients, age label, invoice and 84280 delivery; the team must verify checkout price.')
        added[-1].update(checked='18.10.2026',primary_url='https://khunorganic.co.th/',seller_name='Khun Organic Baby · Lazada',order_sources=[dict(id='lazada',supplier='Khun Organic Baby · Lazada',channel='Lazada shop',url=added[-1]['url'],store='https://www.lazada.co.th/shop/khun-organic-baby/',price=89,currency='THB',contact='https://www.lazada.co.th/shop/khun-organic-baby/')])
    products.extend(added)
    for name,url,contact in [
       ('Kad Kokoa','https://kadkokoa.co/','contact@kadkokoa.co'),
       ('SHEIN Thailand customer service','https://th.shein.com/','https://m.shein.com/th/Customer-Service-a-743.html?lang=then'),
    ]:
        if name not in {s[0] for s in suppliers}:suppliers.append((name,'מזווה וקפה' if name=='Kad Kokoa' else 'ביגוד ואביזרים — פלטפורמה',url,'מקור פומבי נקרא; תנאי חשבונית לא אומתו','84280 לא אושר',contact,'העובד יבקש חשבונית, זהות מוכר והצעת מחיר לפני רכישה'))
    from enrich_catalog import STORES
    for p in products:
        if not p['lazada_store'] and p['supplier'] in STORES:p['lazada_store']=STORES[p['supplier']]
        s=next((s for s in suppliers if s[0] in [p['supplier'],p['primary_name']]),None)
        p['contact_info']=p.get('contact_info') or (s[5] if s else p['primary_url'])
        p['invoice_status']='Employee to request; supplier ability / invoice type not confirmed'
        p['platform']=p.get('platform') or ('Lazada' if 'lazada.' in p['url'] else 'Shopee' if 'shopee.' in p['url'] else 'LINE' if 'shop.line.me' in p['url'] else 'Thailand brand / store')
        p['promotion_status']=p.get('promotion_status') or ('sale' if p['price'] is not None and p['regular'] and p['regular']>p['price'] else 'unmarked' if p['regular'] is not None and p['price'] is not None else 'unknown')
    return added
