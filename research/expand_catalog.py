"""Additional sourcing observations from 19 Oct; explicit quote-only leads."""
import hashlib

OLD_EN = [
('Moving Mouse — pink','Pink SKU 1646; 40% public discount. Confirm repeat stock.'),
('Memo Game — PlanMini','Small tabletop game; discontinued line, confirm replenishment.'),
('Stegosaurus','PlanWood composite, not solid wood; manufacturer age 12m+. Discontinued line.'),
('Diplodocus','PlanWood composite; manufacturer age 12m+. Discontinued line.'),
('Tyrannosaurus Rex','Confirm SKU 6133: manufacturer text mistakenly describes a lion. Discontinued line.'),
('Triceratops','PlanWood composite; manufacturer age 12m+. Discontinued line.'),
('Sail Boat — Blue','Confirm colour and age on packaging: title/description conflict. Discontinued line.'),
('Peacock Percussion','Noisy; lower priority for indoor café play. Discontinued line.'),
('Mushroom Kaleidoscope','10% public discount; confirm colour. Manufacturer age 18m+.'),
('Whale Whistle','No discount; manufacturer age 3+. Do not share mouth-contact demos.'),
('Dolphin Whistle','No discount; manufacturer age 3+. Do not share mouth-contact demos.'),
('Mini Spinning Tops — set of 4','Price is for a four-piece set; do not assume resale as singles.'),
('Mini Balancing Cactus','13 pieces in tin; manufacturer age 3+. Confirm packaging and stock.'),
('3D Paper Model Kit','Confirm contents, age and whether scissors/glue are required.'),
('Step by Step Drawing Book','Confirm theme and instruction language; quiet table activity.'),
('My First Coloring Book','Retail price; request wholesale terms before resale purchase.'),
('Portable Watercolor Painting Book','Good fit for the brief; requires a little water and a tray.'),
('Reusable Sticker Play Set','Quiet activity; choose suitable artwork and confirm age.'),
('Transfer Stickers — Busy City','Confirm theme and age rating.'),
('Scratch Cards — Fantasy','Produces scratch debris; sample before use at café tables.'),
('Baby Roo Washable Markers','395 THB is a starting price; sets vary up to 1,185. Select exact set.'),
('Mozzie Mineral Spray 50 ml','Manufacturer and Lazada card prices are separate observations; request wholesale quote.'),
('Organic Premium Baby Lotion 50 ml','Confirm ingredients, label age and bottle size.'),
('Mozzie Gel 18 ml','Age claims conflict on supplier page (birth vs 3m+); obtain exact label.'),
('Organic Strawberry Toothpaste 40 ml','Supplier says fluoride-free; this is a specification, not an efficacy recommendation.'),
('Sól Milky SPF50 PA++++ 30 ml','825 THB indexed retail price. Obtain SPF report, ingredients and age label; reef-safe not verified.'),
('Ethnic Cotton Pouch 10 × 14 cm','USD 2 website price. Confirm MOQ, local tax, shipping, print and fabric sample.'),
('Blue Scrunchie','Confirm colour: supplier card image and Blue link differ. Request trade price.'),
('Batik Bloom Pouch','Fabric pattern varies. Retail price; request trade quote.'),
('Sunrise Blue Batik Bag','Handmade in Samui according to maker. Retail price; margin not established.'),
('Thai Fabric Keychain','Thailand/Koh Samui lettering; Koh Phangan wording not included automatically.'),
('Handmade Cotton Scrunchie','Supplier announced closure 9–20 Oct and dispatch from 21 Oct. Confirm timing.'),
('Glass Drinking Straws — set of 4','USD export price. Gift for adults; not recommended as a child-use item.'),
('Patchwork Cotton Tote','USD export price; request local THB wholesale quote.'),
('Mesh Produce Bags — set of 5','Price is per set, not per bag. Confirm retail packaging.'),
('Natural Dish Scrubber — loofah','Starting price; pack options 2/10. Do not treat as price per piece.'),
('Reusable Kitchen Cloths','Starting export price; confirm pack contents and local wholesale terms.'),
('Beeswax Food Wraps','Collection link, not a confirmed SKU. Choose size, design and pack.'),
('Bamboo Toothbrushes','Confirm adult/child size, bristle type and individual packaging.'),
('Organic Cotton Rounds','Confirm pack quantity, dimensions and washing instructions.'),
('Rakpaa Beeswax Wraps','Indexed LINE listing; size, material and current price not verified.'),
('Original Crunchy Almond Butter','295 THB indexed price; jar size unverified. 30 g trial size is a brief requirement only.'),
('Jai Jai Jam — two-jar pack','360 THB indexed pack price; confirm jar sizes, ingredients and shelf life.'),
('100% Peanut Butter — 1 kg','Indexed product link. Confirm allergens and labelling; do not repackage without supplier approval.'),
('Freeze-Dried Strawberries','Confirm full ingredient list, pack weight, humidity protection and shelf life.'),
('Roasted Almonds','Confirm pack weight, ingredients and carton price.'),
('Nut Butter Range','Shop link; choose exact flavour. Chocolate does not mean no added sugar.'),
('Begin Rice & Vegetable Spaghetti','Secondary retailer listing. Primary brand is Begin Baby Food; request exact label and quote.'),
('Begin Baby Pasta / Sauce Range','Brand channel; choose exact flavour, ingredients and pack size.'),
('Forest Honey 500 g','Honey category, not sugar-free. Wholesale margin unknown.'),
('Apple, Banana & Strawberry Purée 90 g','International manufacturer catalogue only. Thai importer and local shipping not verified.'),
('Cocoa Cereal 35 g','Indexed retail price; confirm CC-35 SKU, flavour and ingredients.'),
('Cotton Baby Set — model 92','Top stated 100% cotton, bottom cotton denim. Do not infer organic certification.'),
('Family Cotton Linen Set','Confirm exact fibre percentages, size chart and wholesale terms.'),
('Cotton Kids Shorts','Cotton/linen wording is not a fibre breakdown. Request label and sample.'),
('Anjuna Kids Clothing Range','Samui maker; cotton and rayon offered. Request specific 100% cotton styles.'),
('Cotton / Linen Top — 26106003','Supplier states 50% cotton, 50% linen. Confirm price, sizes and wash test.'),
]

def expand(products, suppliers):
    assert len(products)==len(OLD_EN), 'Original product order changed; review English names.'
    for p,(name,summary) in zip(products,OLD_EN):
        p.update(name_en=name,summary_en=summary,sku='',options_hint='',kind='product')
    new=[]
    def add(cat,he,en,supplier,url,price=None,regular=None,sku='',options='',image=None,summary='',note='',kind='product',evidence='מקור ספק פומבי נקרא ב־19.10.2026; מחיר קופה ומשלוח לא אומתו',source=None,role='ערוץ המותג; זהות מפעל ותנאי סחר דורשים אישור'):
        primary=next((s[2] for s in suppliers if s[0]==supplier),url)
        p=dict(category=cat,name=he,name_en=en,supplier=supplier,url=url,price=price,regular=regular,currency='THB',
            evidence=evidence,quality='מפרט ספק בלבד; נדרשים תווית/מסמכים ודגימה.',shipping='לא אושר ל־84280',decision='הצעת סוחר ודגימה לפני אישור',note=note or summary,checked='19.10.2026',
            primary_name=supplier,primary_url=primary,primary_role=role,seller_name=supplier,lazada_store=None,lazada_offer=None,
            image_url=image,image_source=source or url if image else None,image_note='תמונת קטלוג; לאשר וריאנט ואריזה' if image else 'צילום מוצר לא אותר',
            summary_en=summary,sku=sku,options_hint=options,kind=kind,source_url=source or url)
        new.append(p)
    for he,en,handle,price,regular,sku,img in [
        ('לוחות השחלה מעץ','Lacing Boards','lacing-boards',765,850,'5923','5923_-_Packshot_-_01.jpg?v=1774517165'),
        ('פאזל מלבנים PlanMini','Rectangular Puzzle — PlanMini','rectangular-puzzle-planmini',270,450,'4652','4652_-_Main_-_sq.jpg?v=1774514117'),
        ('סט 5 מכוניות עץ קטנות','Mini Car Set — 5 vehicles','mini-car-set',360,600,'6286','6286_-_Main_-_sq.jpg?v=1774517287'),
        ('כבשת השחלה','Lacing Sheep','lacing-sheep',675,750,'5150','5150_-_Main_-_sq.jpg?v=1774514245'),
    ]:
        add('משחקים ופאזלים',he,en,'PlanToys','https://th.plantoys.com/en/products/'+handle,price,regular,sku,image='https://cdn.shopify.com/s/files/1/0550/2913/7495/files/'+img,summary='Manufacturer price and available flag read live on 19 Oct. Confirm packaging, age label and repeat stock; retail discount is not a wholesale quote.',evidence='מחיר, מק״ט וזמינות סומנו בקטלוג היצרן החי (WebMCP), 19.10.2026')
    for he,en,handle,price,sku,img,opts in [
        ('סט כותנה Waffle דגם 56587','Cotton Waffle Two-Piece Set 56587','2-pcs-set-86',339,'PR 339-24 ELDR-56587','56587.jpg?v=1752917930','6–12m / 12–18m / 18–24m'),
        ('סט כותנה דגם 56762','Cotton Two-Piece Set 56762','2-pcs-set-89',289,'PR342-ELCS-56762','2_ELCS-56762.jpg?v=1756787229','12–18m / 18–24m / 3 years'),
        ('סט כותנה דגם 56769','Cotton Two-Piece Set 56769','dress-1',289,'PR342-ELCK-56769','9_ELCK-56769.jpg?v=1756794049','12–18m / 18–24m / 3 years'),
    ]:
        add('בגדים ואביזרי ילדים',he,en,'Elegant Kids','https://elegantkids.in.th/products/'+handle,price,sku=sku,options=opts,image='https://cdn.shopify.com/s/files/1/2435/4547/files/'+img,summary='Manufacturer states 100% cotton. Live price for the returned variant; other sizes need stock confirmation. Request trade price and wash sample.',evidence='מחיר, מק״ט, אפשרויות מידה והרכב נקראו בקטלוג היצרן החי, 19.10.2026')
    for he,en,path,price,img in [
        ('ליפ באלם קוקוס','Organic Coconut Lip Balm','organic-coconut-lipbalm',120,'2026/03/Coconut-Lip-Balm-White-BG_Coconut_BoxTube-680x680.jpg'),
        ('סבון קוקוס מוצק','Organic Coconut Soap Bar','organic-coconut-soap-bar',150,'2022/08/CoconutSoap-Original-front-680x680.jpg'),
        ('קרם גוף קוקוס','Organic Coconut Body Lotion','coconut-body-lotion',350,'2022/08/Coconut-Body-lotion_front-680x680.jpg'),
        ('סרום שמן לשיער','Organic Coconut Hair Oil Serum','coconut-hair-serum',450,'2022/08/Coconut-hair-oil-serum_Box-680x680.jpg'),
        ('ג׳ל רחצה קוקוס','Organic Coconut Shower Gel','coconut-shower-gel',300,'2022/08/Coconut-Shower-gel_front.jpg'),
    ]:
        add('ביוטי וטיפוח לאמא',he,en,'Phutawan','https://phutawanshop.com/en/product/'+path+'/',price,image='https://phutawanshop.com/wp-content/uploads/'+img,options='Choose scent / volume / pack',source='https://phutawanshop.com/en/product-category/coconut-series/',summary='Live category-card retail price, 19 Oct; exact volume/scent and wholesale price need confirmation. Organic is supplier wording; check full ingredients. For adult gift assortment.',evidence='מחיר ותמונה בכרטיס קטגוריה חי, 19.10.2026; דף סבון מאונדקס הציג בעבר מחיר שונה — לאשר בקופה')
    for he,en,url,size in [
        ('תחליב רחצה צמחי לאמא','Plant-Based Body Wash 300 ml','https://consciouslivingthailand.com/product/100-natural-pro-biotic-body-wash/','300 ml'),
        ('שמפו צמחי לאמא','Plant-Based Shampoo 300 ml','https://consciouslivingthailand.com/product/100-natural-pro-biotic-shampoo/','300 ml'),
        ('סבון רחצה לתינוק','Head to Toe Baby Wash 250 ml','https://consciouslivingthailand.com/product/100-natural-plants-fruits-head-to-toe-baby-wash-250-ml/','250 ml'),
    ]:
        add('מוצרי תינוקות' if 'Baby' in en else 'ביוטי וטיפוח לאמא',he,en,'Conscious Living Care',url,options=size,summary='Official brand listing found. Request current trade price, full ingredient label and sample; supplier probiotic/health claims are not independently verified.',kind='product',source='https://consciouslivingthailand.com/shop/')
    for he,en,url in [
        ('סט שחייה ארוך לילדים','Long-Sleeve Swim Shirt & Bottom Set','https://minenethailand.com/products/long-sleeves-shirt-pantie-s'),
        ('כובע שמש לשחייה — קטלוג','Kids Sun Hat — choose SKU','https://minenethailand.com/collections/swimwear/swimwear'),
    ]:
        add('ים, שמש ושחייה',he,en,'Minene Thailand',url,options='Size / print / colour',summary='Brand catalogue found. UPF50+ is a supplier claim; request a report covering the exact fabric/SKU, sizing, stock and wholesale quote.',kind='collection' if 'Hat' in en else 'product')
    add('מוצרי תינוקות','חיתולים — אריזה קטנה','Standard Soft Diapers — small pack','DODOLOVE','https://shop.line.me/@dodolove/product/1007511146',options='S–4XL; weight range / pieces per pack',summary='Official-name LINE listing indexed. Confirm exact size, pack count, price and whether this commonplace brand fits the shop brief; no wholesale offer verified.')
    add('ים, שמש ושחייה','חיתול שחייה — ליד לבירור','Swim Diaper — confirm official Thai SKU','DODOLOVE','https://shop-th.tiktok.com/pdp/1729550491245709888',options='Size / baby weight / print / pack',summary='Marketplace product lead only; seller identity, current stock and authenticity not verified. Ask DODOLOVE brand channel for the correct current Thai SKU. Not approved for purchase.',kind='lead',role='מותג: https://www.dodolove.com/ ; מוכר הליד טרם זוהה')
    for he,en in [
        ('Coco Cinnamon Almond','Coco Cinnamon Almond'),('Coco Honey Cashew Bite','Coco Honey Cashew Bite'),
        ('Coco Toasted Caramel Bite','Coco Toasted Caramel Bite'),('Coco Brownie Protein Brittle','Coco Brownie Protein Brittle'),
    ]:
        add('מזווה וחטיפים',he,en,'Coco Paradise Life BKK','https://www.instagram.com/cocoparadiselife.bkk/',options='Exact Thai pack / net weight / flavour',summary='Named in the 18 Oct team chat. Proposed 30-pack mixed order and 12% discount were not a confirmed order or price quote. Honey/caramel/cinnamon/brownie recipes must be checked for added sweeteners and allergens. Thai channel only; no Hong Kong price reused.',kind='lead',evidence='שם המוצר וכיוון ההזמנה מתוך הצ׳אט 18.10; אין מחיר בסיס, תווית או אישור הזמנה')
    add('מזווה וחטיפים','OLY מארז קקאו ותות','Cocoa 35 g & Strawberry 45 g Mix Pack','OLY Snacks','https://www.olysnacks.com/product/224583-221248/cocoa-strawberry-mix-pack',options='Pack count / flavour split',summary='Official product listing indexed. Request current carton price, full ingredients, allergens and shelf life; no no-added-sugar conclusion from marketing copy.')
    for he,en,url,sku in [
        ('חטיף אורז אצות','Organic Jasmine Rice Puffs — Seaweed','https://www.xongdur.com/en/product/25091-29379/409-001','409-001'),
        ('ארוחת אורז מונבט, תרד ודלעת','Sprouted Brown Rice Baby Meal — Spinach & Pumpkin','https://www.xongdur.com/en/product/25087-29375/405-005','405-005'),
    ]:
        add('מזווה וחטיפים',he,en,'Xongdur',url,sku=sku,options='Net weight / sachets per box / age label',summary='Official product and ingredients found. Contains seasoning/soy-sauce powder depending on SKU; request complete sub-ingredients, allergens and age label. Brand reports broad distribution, so check Koh Phangan availability before adding to boutique range. Current price not verified.')
    for cat,he,en,sup,url,summary in [
        ('מוצרי Casa Luma','חולצות עם איור הבית','Casa Luma Cotton T-Shirts — custom print','Thai T-Shirt Studio','https://www.thaitshirtstudio.com/en/tshirt.html','Custom production enquiry, not a ready SKU. Request adult/child size chart, cotton fabric weight, print proof, washing sample, mixed-size MOQ and shipping quote. Artwork is not uploaded by this tool.'),
        ('מוצרי Casa Luma','פאוץ׳ כותנה ממותג','Casa Luma Cotton Drawstring Pouch — custom logo','Handbag Asia / Prestige Creations','https://handbag-asia.com/product/plain-natural-cotton-custom-size-drawstring-bag/','Custom cotton bag production lead. Choose tote/pouch construction, dimensions, fabric weight, handle, logo print, MOQ and sample before approving.'),
        ('מוצרי Casa Luma','מדבקות קופנגן','Koh Phangan Sticker Sheet — custom print','Command+P Studio','https://www.commandpstudio.com/en','Print-service enquiry from the brief. Confirm sheet dimensions, number of designs, material/water resistance, print proof and run quantity; no finished artwork or SKU yet.'),
        ('נייר, מדבקות ומתנות קטנות','גלויות ומדבקות מאיירים','Thai Artist Cards & Stickers — choose design','I Found Something Good','https://shopee.co.th/ifoundsthgood','Shop-level lead from the brief. Select exact illustrator/design, language and SKU; confirm rights for resale, wholesale price and pack quantity.'),
        ('מוצרי Casa Luma','עטיפות מזון במיתוג','Casa Luma Beeswax Wraps — private label','SuperBee','https://wholesale.superbee.me/private-label-and-customisation/','Custom/private-label enquiry only. Confirm print/design permissions, dimensions, minimum order and sampling; no brand artwork uploaded.'),
    ]:
        add(cat,he,en,sup,url,summary=summary,kind='custom' if cat=='מוצרי Casa Luma' else 'collection')
    products.extend(new)
    extra_suppliers=[
        ('DODOLOVE','חיתולים ומוצרי תינוקות','https://www.dodolove.com/','אתר מותג נקרא; מק״טי רכש דורשים אישור','לא אושר ל־84280','https://shop.line.me/@dodolove','גודל אריזה, מחיר סוחר וזמינות; להבחין ממוצר נפוץ באי'),
        ('Minene Thailand','בגדי ילדים ושחייה','https://minenethailand.com/','אתר מותג/דף שחייה אותרו','לא אושר ל־84280','אתר המותג','מק״ט, מידות, מחיר סוחר ודוח UPF'),
        ('Xongdur','מזון יבש וחטיפי אורז','https://www.xongdur.com/en/','קטלוג ורכיבים נקראו; תפוצה רחבה מצוינת באתר','לא אושר ל־84280','https://www.xongdur.com/en/','בדיקת בידול באי, תווית מלאה, אריזות ומחיר סוחר'),
        ('Thai T-Shirt Studio','חולצות Casa Luma בהדפסה','https://www.thaitshirtstudio.com/en/tshirt.html','עמוד ספק הדפסה אותר','לא אושר ל־84280','אתר הספק','בד כותנה, מידות ילדים/מבוגרים, דוגמה, MOQ מעורב והצעת מחיר'),
    ]
    suppliers.extend(s for s in extra_suppliers if s[0] not in {x[0] for x in suppliers})
    for p in products:
        p['id']='cl-'+hashlib.sha256((p['supplier']+'|'+p['url']+'|'+p['name']).encode()).hexdigest()[:16]
        if p['supplier']=='DODOLOVE':p['primary_url']='https://www.dodolove.com/'
        if p['supplier']=='Minene Thailand':p['primary_url']='https://minenethailand.com/'
        if p['supplier']=='Xongdur':p['primary_url']='https://www.xongdur.com/en/'
        p['sourcing_warning_en']='Quality and delivery to 84280 require confirmation. Reference price excludes unconfirmed freight/taxes.'
    return new
