/* Pure ordering model, shared by the page and local regression checks. */
(function(root){
'use strict';
const VERSION=2,KEY='casa-luma-purchasing-v2';
const statuses=['review','shortlist','approved','skip'];
const text=(x,n=2000)=>typeof x==='string'?x.slice(0,n):'';
const safeUrl=x=>{try{const u=new URL(x);return ['https:','http:'].includes(u.protocol)?u.href:'';}catch{return '';}};
const uid=()=>typeof crypto!=='undefined'&&crypto.randomUUID?crypto.randomUUID():'line-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
const defaultState=()=>({version:VERSION,updatedAt:'',settings:{lang:'he',messageLang:'en',buyer:'Casa Luma Shop',address:'Koh Phangan, Surat Thani 84280, Thailand',contact:'',neededBy:'',notes:''},items:{}});
function promotion(p){return p.promotion_status||((p.price!==null&&p.regular>p.price)||p.lazada_offer?'sale':'unknown');}
function discount(p){return Math.max(p.price!==null&&p.regular>p.price?1-p.price/p.regular:0,p.lazada_offer?1-p.lazada_offer.price/p.lazada_offer.regular:0);}
function matchesSource(p,value){return !value||(value==='Lazada'?p.platform==='Lazada'||!!p.lazada_store:p.platform===value);}
function sortProducts(products,mode){const list=[...products];const cost=p=>p.price??Infinity;return list.sort((a,b)=>mode==='discount'?discount(b)-discount(a):mode==='supplier'?a.primary_name.localeCompare(b.primary_name,'en'):mode==='price'?((a.currency==='THB'?0:1)-(b.currency==='THB'?0:1)||a.currency.localeCompare(b.currency)||cost(a)-cost(b)):0);}
function normalize(raw,catalog,strict=true){
 if(!raw||raw.version!==VERSION||!raw.items||typeof raw.items!=='object'||Array.isArray(raw.items))throw Error('Invalid Casa Luma work file / version');
 const s=defaultState(),known=new Map(catalog.map(p=>[p.id,p]));let omitted=0;
 for(const k of Object.keys(s.settings)){const v=raw.settings&&raw.settings[k];if(typeof v==='string')s.settings[k]=text(v);}
 if(!['he','en'].includes(s.settings.lang))s.settings.lang='en';if(!['en','th'].includes(s.settings.messageLang))s.settings.messageLang='en';
 for(const [id,item] of Object.entries(raw.items)){
  const p=known.get(id);if(!p){omitted++;continue;}if(!item||typeof item!=='object')continue;
  const lines=[];
  for(const r of Array.isArray(item.lines)?item.lines.slice(0,200):[]){
   if(!r||typeof r!=='object')continue;
   const qty=Number(r.qty),v=r.unitPrice,price=v===null||v===''||v===undefined?null:Number(v);
   const validQty=Number.isSafeInteger(qty)&&qty>0&&qty<=100000;
   if(!validQty&&strict)throw Error('Invalid quantity in imported line');
   if(!p.sources.some(x=>x.id===r.source)&&strict)throw Error('Unknown purchasing channel in imported line');
   lines.push({id:uid(),source:text(r.source,100),qty:validQty?qty:0,
    model:text(r.model,300),size:text(r.size,100),colour:text(r.colour,100),pack:text(r.pack,200),unit:['piece','set','pack','box','carton','kg'].includes(r.unit)?r.unit:'piece',
    unitPrice:Number.isFinite(price)&&price>=0?price:null,currency:['THB','USD','EUR','GBP'].includes(r.currency)?r.currency:'THB',priceKind:r.priceKind==='quote'?'quote':'reference',note:text(r.note)});
  }
  s.items[id]={status:statuses.includes(item.status)?item.status:'review',hidden:!!item.hidden,lines};
  if(s.items[id].status==='approved'&&issues(p,s.items[id]).length)s.items[id].status='shortlist';
 }
 s.updatedAt=text(raw.updatedAt,100);return {state:s,omitted};
}
function itemFor(s,p){return s.items[p.id]||(s.items[p.id]={status:'review',hidden:false,lines:[]});}
function addLine(s,p,from){const i=itemFor(s,p),src=p.sources[0];const r=from?{...from,id:uid()}:{id:uid(),source:src.id,qty:1,model:'',size:'',colour:'',pack:'',unit:/set|kit/i.test(p.name_en)?'set':'piece',unitPrice:src.price??null,currency:src.currency||'THB',priceKind:'reference',note:''};i.lines.push(r);if(i.status!=='shortlist')i.status='shortlist';i.hidden=false;return r;}
function issues(p,item){
 const out=[];if(item.hidden)out.push('hidden');if(!item.lines.length)out.push('no-lines');
 for(const r of item.lines){if(!Number.isSafeInteger(r.qty)||r.qty<1||r.qty>100000)out.push('quantity');if(!p.sources.some(s=>s.id===r.source))out.push('source');if(r.unitPrice!==null&&(!Number.isFinite(r.unitPrice)||r.unitPrice<0))out.push('price');if(p.requires_details&&![r.model,r.size,r.colour,r.pack].some(v=>v.trim()))out.push('details');}
 return [...new Set(out)];
}
function setStatus(s,p,status){if(!statuses.includes(status))return false;const i=itemFor(s,p);if(['shortlist','approved'].includes(status)&&!i.lines.length)addLine(s,p);if(status==='approved'&&issues(p,i).length)return false;i.status=status;return true;}
function editLine(s,p,lineId,field,value){const i=itemFor(s,p),r=i.lines.find(x=>x.id===lineId);if(!r)return false;if(!['source','qty','model','size','colour','pack','unit','unitPrice','currency','priceKind','note'].includes(field))return false;
 if(field==='qty'){const n=Number(value);r.qty=value===''?0:n;}else if(field==='unitPrice')r.unitPrice=value===''?null:Number(value);else r[field]=text(value);
 if(field==='source'){const src=p.sources.find(x=>x.id===value);if(!src)return false;r.unitPrice=src.price??null;r.currency=src.currency||'THB';r.priceKind='reference';}
 if(['unit','pack'].includes(field)){r.unitPrice=null;r.priceKind='reference';}
 if(['model','size','colour','currency','unitPrice'].includes(field))r.priceKind='reference';
 const invalidated=i.status==='approved';if(invalidated)i.status='shortlist';return invalidated;
}
function hide(s,p){const i=itemFor(s,p);i.hidden=true;i.status='skip';}
function removeLine(s,p,id){const i=itemFor(s,p);i.lines=i.lines.filter(r=>r.id!==id);i.status=i.lines.length?'shortlist':'review';}
function group(s,catalog,status='approved'){
 const groups=new Map();
 for(const p of catalog){const i=s.items[p.id];if(!i||i.hidden||i.status!==status||issues(p,i).length)continue;for(const r of i.lines){const src=p.sources.find(x=>x.id===r.source);const key=src.supplier+'|'+(src.channel||'direct');if(!groups.has(key))groups.set(key,{key,supplier:src.supplier,channel:src.channel||'direct',contact:src.contact||'',url:src.store||src.url,lines:[]});groups.get(key).lines.push({product:p,row:r,source:src});}}
 return [...groups.values()].sort((a,b)=>a.supplier.localeCompare(b.supplier,'en'));
}
function totals(lines){const amounts={},unknown={};for(const {row:r} of lines){if(r.unitPrice===null){unknown[r.currency]=(unknown[r.currency]||0)+1;continue;}amounts[r.currency]=(amounts[r.currency]||0)+r.qty*r.unitPrice;}return {amounts,unknown};}
function message(g,settings,lang='en'){
 const th=lang==='th',lines=[];const buyer=settings.buyer||'Casa Luma Shop';
 lines.push(th?'สวัสดี '+g.supplier:'Hello '+g.supplier+',');
 lines.push(th?'เราคือ '+buyer+' ต้องการสั่งสินค้าตามรายการด้านล่าง กรุณายืนยันราคาและรายละเอียดก่อนยืนยันคำสั่งซื้อ':'We are '+buyer+'. We would like to order the items below, subject to your confirmation of price, availability and delivery.');
 for(const {product:p,row:r,source:src} of g.lines){
  lines.push('');lines.push((lines.filter(x=>/^\d+\./.test(x)).length+1)+'. '+p.name_en);
  if(p.sku)lines.push('SKU: '+p.sku);
  lines.push((th?'จำนวน: ':'Quantity: ')+r.qty+' '+r.unit);
  for(const [key,en,thai] of [['model','Model / flavour','รุ่น / รสชาติ'],['size','Size','ขนาด'],['colour','Colour','สี'],['pack','Pack contents / weight','จำนวนต่อแพ็ก / น้ำหนัก']])if(r[key])lines.push((th?thai:en)+': '+r[key]);
  if(p.requires_details&&![r.model,r.size,r.colour,r.pack].some(x=>x.trim()))lines.push(th?'กรุณายืนยันรุ่นและขนาดที่แน่นอน':'Please confirm exact model/size.');
  lines.push((th?'ลิงก์สินค้า / อ้างอิง: ':'Product / reference link: ')+src.url);
  lines.push((th?'ผู้ผลิต / แบรนด์: ':'Primary brand: ')+p.primary_name+' — '+p.primary_url);
  lines.push(r.unitPrice===null?(th?'ราคาต่อหน่วย: กรุณาเสนอราคา':'Unit price: please quote'):(th?'ราคาต่อหน่วยเพื่ออ้างอิง: ':'Unit price for reference: ')+r.unitPrice.toFixed(2)+' '+r.currency+' / '+r.unit+' ('+(r.priceKind==='quote'?(th?'ผู้ใช้ระบุว่าได้รับใบเสนอราคาแล้ว':'marked as supplier quote by our team'):(th?'ราคาอ้างอิง ยังไม่ยืนยัน':'reference only, not confirmed'))+')');
  if(r.note)lines.push((th?'หมายเหตุ: ':'Notes: ')+r.note);
 }
 lines.push('');lines.push(th?'จัดส่งไปยัง: '+settings.address:'Delivery destination: '+settings.address);
 if(settings.contact)lines.push((th?'ติดต่อ: ':'Contact: ')+settings.contact);
 if(settings.neededBy)lines.push((th?'วันที่ต้องการรับสินค้า: ':'Requested arrival date: ')+settings.neededBy);
 if(settings.notes)lines.push((th?'หมายเหตุเพิ่มเติม: ':'Additional notes: ')+settings.notes);
 lines.push(th?'กรุณายืนยันสินค้าคงเหลือ รุ่น ขนาด สี จำนวนต่อแพ็ก ราคาขายส่ง ภาษีมูลค่าเพิ่ม ยอดรวม ค่าขนส่งและค่าพื้นที่เกาะ ระยะเวลาจัดส่งถึงรหัสไปรษณีย์ 84280 การส่งถึงหน้าร้านหรือรับที่ท่าเรือ จำนวนขั้นต่ำ ใบกำกับภาษี และเงื่อนไขสินค้าชำรุด พร้อมฉลากส่วนผสม/วัสดุและเอกสารทดสอบที่เกี่ยวข้อง':'Please confirm exact stock/variants and pack contents, wholesale unit prices, VAT basis, total, shipping and island surcharge, delivery date to postcode 84280, door delivery vs pier collection, mixed-order MOQ, tax invoice and damaged-item terms. Please provide ingredient/material labels and relevant test documents.');
 lines.push(th?'กรุณาอย่าเปลี่ยนรุ่น ขนาด สี หรือรสชาติโดยไม่ได้รับความยินยอม เรายังไม่ยืนยันยอดชำระเงินจนกว่าจะได้รับและตรวจสอบรายละเอียดทั้งหมด ขอบคุณ':'Please do not substitute models, sizes, colours or flavours without approval. We will confirm the final order and payment after reviewing your quotation. Thank you.');
 lines.push(th?'พนักงานของเราจะติดต่อเพื่อขอใบเสร็จ/ใบแจ้งหนี้ หรือใบกำกับภาษีเต็มรูป กรุณายืนยันว่าท่านออกเอกสารประเภทใดได้ และต้องใช้ข้อมูลผู้ซื้ออะไรบ้าง ยังไม่ได้ยืนยันความสามารถในการออกใบกำกับภาษี':'Our employee will request the invoice directly. Please confirm whether you can issue an ordinary invoice/receipt or a full Thai tax invoice, and which buyer details you require. Your ability to issue a tax invoice has not yet been confirmed.');
 return lines.join('\n');
}
function csv(s,catalog){const cols=['status','supplier','channel','product','sku','quantity','order_unit','model_flavour','size','colour','pack_contents','unit_price','currency','price_basis','source_url','primary_brand','primary_url','notes','promotion_status','observed_price','comparison_price','observed_date','public_contact','invoice_status'];const rows=[cols];for(const status of ['approved','shortlist'])for(const g of group(s,catalog,status))for(const {product:p,row:r,source:src} of g.lines)rows.push([status,g.supplier,g.channel,p.name_en,p.sku,r.qty,r.unit,r.model,r.size,r.colour,r.pack,r.unitPrice??'',r.currency,r.priceKind,src.url,p.primary_name,p.primary_url,r.note,promotion(p),src.price??'',src.id==='lazada'&&p.lazada_offer?p.lazada_offer.regular:(p.regular??''),p.checked,p.contact_info||src.contact||'',p.invoice_status||'Employee to request']);return '\ufeff'+rows.map(row=>row.map(v=>'"'+String(v??'').replace(/^[=+@-]/,"'$&").replace(/"/g,'""')+'"').join(',')).join('\r\n');}
function save(storage,s){s.updatedAt=new Date().toISOString();try{storage.setItem(KEY,JSON.stringify(s));return true;}catch{return false;}}
function load(storage,catalog){try{const raw=storage.getItem(KEY);return raw?normalize(JSON.parse(raw),catalog,false).state:defaultState();}catch{return defaultState();}}
root.CasaOrder={VERSION,KEY,defaultState,normalize,itemFor,addLine,issues,setStatus,editLine,hide,removeLine,group,totals,message,csv,save,load,safeUrl,promotion,discount,matchesSource,sortProducts};
if(typeof module!=='undefined'&&module.exports)module.exports=root.CasaOrder;
})(typeof window!=='undefined'?window:globalThis);
