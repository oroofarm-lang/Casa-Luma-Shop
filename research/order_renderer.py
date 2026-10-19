"""Self-contained purchasing page; no publishing, tracking or external writes."""
import base64
import json
import html
from pathlib import Path
from urllib.parse import urlsplit

CATEGORIES={
 'צעצועי עץ':'Wooden toys','משחקים ופאזלים':'Games & puzzles','יצירה נקייה':'Quiet arts & crafts',
 'טיפוח ומשפחה':'Family care','תיקים ואביזרים':'Bags & accessories','בית ומתנות':'Home & gifts',
 'מזווה וחטיפים':'Dry food & pantry','בגדים ואביזרי ילדים':'Kids clothing','ביוטי וטיפוח לאמא':'Beauty & care for mum',
 'ים, שמש ושחייה':'Swim & sun','מוצרי תינוקות':'Baby essentials','מוצרי Casa Luma':'Casa Luma merchandise',
 'נייר, מדבקות ומתנות קטנות':'Cards, stickers & small gifts',
}

def prepare(products,suppliers):
    for p in products:
        p['category_en']=CATEGORIES[p['category']]
        p['requires_details']=bool(p.get('options_hint')) or p['category'] in ['בגדים ואביזרי ילדים','ים, שמש ושחייה','מוצרי Casa Luma'] or p.get('kind') in ['lead','collection','custom']
        p['source_url']=p.get('source_url') or p['url']
        contact=p.get('contact_info') or next((s[5] for s in suppliers if s[0]==p['primary_name'] or s[0]==p['supplier']),'')
        same=urlsplit(p['url']).netloc.replace('www.','')==urlsplit(p['primary_url']).netloc.replace('www.','')
        primary_url=p['url'] if same and p.get('kind')!='lead' else p['primary_url']
        supplier='Jarmelo / Pamatop Trading Thailand' if p['supplier']=='Jarmelo / Joan Miro Thailand' else p['primary_name']
        sources=[dict(id='primary',supplier=supplier,channel='brand / manufacturer',url=primary_url,store=p['primary_url'],price=p['price'] if same and p.get('kind')!='lead' else None,currency=p['currency'],contact=contact)]
        if not same or p.get('kind')=='lead':
            sources.append(dict(id='listing',supplier=p['seller_name']+' · listing',channel='listing / seller needs verification',url=p['url'],store=p['url'],price=p['price'],currency=p['currency'],contact=''))
        if p.get('lazada_offer'):
            o=p['lazada_offer'];sources.append(dict(id='lazada',supplier='Khun Organic Baby · Lazada',channel='Lazada shop',url=o['url'],store=p['lazada_store']['url'],price=o['price'],currency='THB',contact=p['lazada_store']['url']))
        p['sources']=p.get('order_sources') or sources
    return products

def render(products,suppliers,laz,searches,out):
    prepare(products,suppliers)
    blob=json.dumps(dict(products=products,suppliers=[dict(zip(['name','category','url','evidence','shipping','contact','next_step'],s)) for s in suppliers],lazada=laz,searches=searches),ensure_ascii=False).replace('<','\\u003c')
    logo=base64.b64encode((out/'assets/casa-luma-logo.png').read_bytes()).decode()
    template=(out/'order-page.html.in').read_text()
    # The collection must remain readable when scripts are disabled or fail.
    def e(x):return html.escape(str(x if x is not None else ''),quote=True)
    cards=[]
    for p in products:
        image=f'<img src="{e(p["image_url"])}" loading="lazy" alt="{e(p["name_en"])}">' if p['image_url'] else ''
        price='מחיר לבירור' if p['price'] is None else f'{p["price"]:g} {p["currency"]}'
        old=f'<del>{p["regular"]:g} {p["currency"]}</del><mark>−{100*(1-p["price"]/p["regular"]):.0f}%</mark>' if p['price'] is not None and p['regular'] and p['regular']>p['price'] else ''
        cards.append(f'''<article class="product-card static-card"><div class="card-main"><div class="product-head"><div class="visual"><span aria-hidden="true">◈</span>{image}</div><div><span class="tag">{e(p['category'])}</span><h3><a href="{e(p['url'])}" target="_blank" rel="noreferrer">{e(p['name'])} ↗</a></h3><p class="secondary-name" dir="ltr">{e(p['name_en'])}</p></div></div><div class="price"><strong dir="ltr">{e(price)}</strong>{old}</div><p class="price-caption">מחיר ייחוס · נצפה {e(p['checked'])}</p><div class="source"><span>מותג / ערוץ ראשי</span><a href="{e(p['primary_url'])}" target="_blank" rel="noreferrer">{e(p['primary_name'])} ↗</a></div><p class="summary">{e(p['note'])}</p><p class="small">{e(p['shipping'])}</p></div></article>''')
    template=template.replace('__STATIC_CARDS__',''.join(cards)).replace('__PRODUCT_COUNT__',str(len(products))).replace('__CATEGORY_COUNT__',str(len(CATEGORIES)))
    for key,value in [('__DATA__',blob),('__LOGO__','data:image/png;base64,'+logo),('__CSS__',(out/'order-page.css').read_text()),('__CORE__',(out/'order-core.js').read_text()),('__APP__',(out/'order-page.js').read_text())]:
        template=template.replace(key,value)
    (out/'Casa-Luma-Sourcing-Catalog.html').write_text(template)
    # Keep the already-open user URL usable; the source template has a .in suffix.
    (out/'order-page.html').write_text(template)
