"""Source attribution and observed images; no guessed marketplace shop URLs."""
from pathlib import Path
import shutil

STORES = {
    'Khun Organic': dict(url='https://www.lazada.co.th/shop/khun-organic-baby/',
        status='חנות פעילה; כותרת Lazada מציגה חנות רשמית. בעלות מול היצרן טרם הוצלבה.',
        evidence='https://www.lazada.co.th/shop/khun-organic-baby/'),
    'SuperBee': dict(url='https://www.lazada.co.th/shop/superbee-wax-wraps-official-store',
        status='ערוץ Lazada מקושר מעמוד הקישורים של המותג; קטלוג החנות לא נטען לבדיקה.',
        evidence='https://linktr.ee/superbeewaxwraps'),
}

PRIMARY = {
    'PlanToys': ('PlanToys', 'https://th.plantoys.com/en/', 'אתר היצרן בתאילנד'),
    'Jarmelo / Joan Miro Thailand': ('Jarmelo / Joan Miro', 'https://www.joanmirothailand.com/', 'ערוץ תאילנד: Pamatop Trading, יבואן; מפעל הייצור לא אומת'),
    'Khun Organic': ('Khun Organic', 'https://khunorganic.co.th/', 'אתר המותג; זהות מפעל הייצור לא נבדקה'),
    'SuperBee': ('SuperBee', 'https://superbee.me/wholesale/', 'סיטונאות ישירות מהמותג'),
    'Handbag Asia / Prestige Creations': ('Handbag Asia / Prestige Creations', 'https://handbag-asia.com/', 'יצרן/ספק התאמה אישית לפי האתר'),
    'Sora Studio': ('Sora Studio, Koh Samui', 'https://madebysora.com/', 'היוצרת והמותג; עבודת יד לפי האתר'),
    'IslaNatural Phuket': ('IslaNatural Phuket', 'https://islanaturalphuket.com/', 'מותג ומסלול סיטונאות ישיר'),
    'Sollie': ('Sollie Skin', 'https://www.instagram.com/sollieskin/', 'קישור המותג; מפעל ייצור לא אומת'),
    'Adaily Factory': ('Adaily Factory', 'https://shopee.co.th/adaily.factory', 'חנות מזוהה בשם המותג; זהות משפטית טרם אומתה'),
    'Jai Jai Jam': ('Jai Jai Jam', 'https://www.instagram.com/jaijai_jam/', 'קישור המותג מהחומרים; תנאי יצרן לא אומתו'),
    'Black Bear': ('Black Bear Superfood', 'https://www.instagram.com/blackbear.superfood/', 'קישור המותג מהחומרים; מפעל הייצור לא אומת'),
    'Paweenee’s': ('Paweenee’s', 'https://linktr.ee/paweenees', 'ערוצי המותג; תנאי סיטונאות לא אומתו'),
    'Begin': ('Begin Baby Food', 'https://shop.line.me/@beginbabyfood', 'ערוץ המותג ב־LINE; מחיר המוצר מגיע מקמעונאי משני'),
    'Begin Baby Food': ('Begin Baby Food', 'https://shop.line.me/@beginbabyfood', 'ערוץ המותג; מפעל הייצור לא אומת'),
    'Rakpaa': ('Rakpaa Honey', 'https://shop.line.me/@rakpaahoney', 'ערוץ המותג ב־LINE'),
    'FrutoNanny': ('FrutoNanny', 'https://frutonanny.com/products/', 'קטלוג היצרן הבינלאומי; יבואן תאילנדי לא אומת'),
    'OLY': ('OLY Snacks', 'https://www.olysnacks.com/th/brand/671/oly', 'אתר המותג; מחיר סוחר לא אומת'),
    'Elegant Kids': ('Elegant Kids', 'https://elegantkids.in.th/', 'אתר היצרן התאילנדי ומסלול סיטונאות'),
    'Bloomingcub': ('Bloomingcub', 'https://shop.line.me/@bloomingcub', 'ערוץ בשם המותג; זהות יצרן לא אומתה'),
    'Cottonica': ('Cottonica', 'https://shop.line.me/@cottonica', 'ערוץ בשם המותג; זהות יצרן לא אומתה'),
    'Anjuna Kids, Samui': ('Anjuna Kids, Samui', 'https://anjunakids.com/', 'אתר המותג המקומי; תנאי ייצור לא אומתו'),
    'Minene Thailand': ('Minene Thailand', 'https://minenethailand.com/', 'ערוץ המותג בתאילנד; זהות המפעל לא אומתה'),
}

# Each URL was read from the manufacturer's product tool or a rendered product card.
PT_IMAGES = [
 ('moving-mouse','1646_-_Main_-_sq.jpg?v=1774509855'),
 ('memo-game-planmini','4128_-_Main_-_sq.jpg?v=1774513987'),
 ('stegosaurus','6131_-_Main_-_sq.jpg?v=1774517246'),
 ('diplodocus','6130_-_Main_-_sq.jpg?v=1774517245'),
 ('tyrannosaurus-rex','6133_-_Main_-_sq.jpg?v=1774517244'),
 ('triceratops','6132_-_Main_-_sq.jpg?v=1774517245'),
 ('sail-boat-blue','5813_-_Main.jpg?v=1774517051'),
 ('bird-percussion-peacock','6432_-_Main_-_sq.jpg?v=1774517369'),
 ('mushroom-kaleidoscope','4317_MushroomKaleidoscope_PS.jpg?v=1775795455'),
 ('whale-whistle','4606_-_Main.jpg?v=1774514034'),
 ('dolphin-whistle','4605_-_Main.jpg?v=1774514034'),
 ('mini-spinning-tops','4132_-_Main_-_sq.jpg?v=1774514010'),
 ('mini-balancing-cactus','4130_-_Main_-_sq.jpg?v=1774514007'),
]
JM_IMAGES = [
 ('3d-paper-model-', '2017/10/3D-Paper-Model-016-800-x-800px.png'),
 ('%E0%B8%AA%E0%B8%A1%E0%B8%B8%E0%B8%94%E0%B8%AA%E0%B8%AD%E0%B8%99', '2020/08/STEP-BY-STEP.jpg'),
 ('my-first-coloring-book-', '2021/07/My-First-Coloring-Book-023-1000-x-1000px.png'),
 ('water-color-painting-', '2022/12/Watercolor-Painting-19-1000-x-1000px.png'),
 ('reusable-sticker-play-set-', '2020/02/Reusable-Sticker-Play-Set-018-1000-x-1000px.jpg'),
 ('transfer-sticker-', '2017/12/Transfer-Sticker-Busy-City-001-800-x-800px.jpg'),
 ('scratch-cards-fantasy-set', '2018/09/Scratch-Card-009-800-x-800px.png'),
 ('baby-roo-washable-markers-', '2017/10/Washable-Makers-56-1000-x-1000px.png'),
]
KHUN_OFFERS = [
 ('mozzie-mineral-spray-50ml', '3354530591-s12446178441',229,280,'9c8ed1d10849abe6f6a004cf469378b5'),
 ('organic-premium-baby-lotion', '3354438747-s12445945909',229,285,'8e2ad1b90cf18eeceeac7a78b39607a4'),
 ('mozzie-gel', '3354610751-s12446509815',229,295,'883c3879189405e3589c67a5b8e02aa3'),
 ('%E0%B8%A2%E0%B8%B2%E0%B8%AA%E0%B8%B5', '3354700304-s12446691453',139,195,'749b6040654fccc6073a2ca85ae875d8'),
]
SORA_IMAGES = {
 'scrunchie?id=scrunchie-blue':'scred.webp',
 'product?id=batik-bloom':'pouchbatik1.webp',
 'product?id=sunrise-bag-blue-batik':'thaiblue.webp',
 'keychain':'llaveros.webp',
}
SB_IMAGES = {
 'glass-drinking-straws':'glass-drinking-straws-glass-straw-in-smoothie-portrait-560w.avif',
 'natural-dish-scrubber':'natural-dish-scrubber-with-fresh-vegetables-560w.avif',
 'reusable-kitchen-cloths':'reusable-kitchen-cloths-wiping-a-spill-560w.avif',
 'patchwork-tote-bag':'patchwork-tote-bag-tote-bag-over-the-shoulder-portrait-560w.avif',
 '5-mesh-produce-bags':'5-mesh-produce-bags-filled-at-the-market-square-560w.avif',
}

def enrich(products, out):
    for p in products:
        name,url,role=PRIMARY[p['supplier']]
        p.update(primary_name=name,primary_url=url,primary_role=role,
                 seller_name='The Little Store — קמעונאי משני' if p['supplier']=='Begin' else p['supplier'],
                 lazada_store=STORES.get(p['supplier']),image_url=None,image_source=None,lazada_offer=None)
        for handle,image in PT_IMAGES:
            if p['url'].endswith('/'+handle):
                p['image_url']='https://cdn.shopify.com/s/files/1/0550/2913/7495/files/'+image
        if p['supplier']=='Jarmelo / Joan Miro Thailand':
            p['seller_name']='Joan Miro Thailand / Pamatop Trading — יבואן תאילנדי'
            for slug,image in JM_IMAGES:
                if slug.lower() in p['url'].lower():
                    p['image_url']='https://i0.wp.com/www.joanmirothailand.com/wp-content/uploads/'+image+'?resize=600%2C600&ssl=1'
        for slug,sku,price,regular,image in KHUN_OFFERS:
            if slug.lower() in p['url'].lower():
                p['lazada_offer']=dict(url='https://www.lazada.co.th/products/pdp-i'+sku+'.html?search=store',price=price,regular=regular,currency='THB',evidence='כרטיס מוצר בחנות Khun Organic Baby; לא מחיר קופה. לאשר יחידה, טעם ווריאנט.',checked='18.10.2026')
                p['image_url']='https://img.lazcdn.com/g/p/'+image+'.png_400x400q80.png_.webp'
                p['image_source']=p['lazada_store']['url']
        for slug,image in SORA_IMAGES.items():
            if p['url']=='https://madebysora.com/'+slug:
                p['image_url']='https://madebysora.com/assets/'+image
        for slug,image in SB_IMAGES.items():
            if p['url']=='https://superbee.me/s/'+slug+'/':
                p['image_url']='https://superbee.me/img/'+image
        if p['image_url'] and not p['image_source']:
            p['image_source']=p['url']
        p['image_note']='תמונת קטלוג הספק; יש לאשר צבע/אריזה/וריאנט' if p['image_url'] else 'סמל קטגוריה בלבד — צילום מוצר לא אותר'
        if p['supplier']=='Sora Studio' and 'scrunchie-blue' in p['url']:
            p['image_note']='תמונת הספק בקישור Blue מציגה גוון שונה; לאשר צבע לפני בחירה'
    assets=out/'assets'
    assets.mkdir(exist_ok=True)
    shutil.copy2('/Users/ohadfait/Desktop/casa /CASA Breand/Logo-01 (1).png',assets/'casa-luma-logo.png')
