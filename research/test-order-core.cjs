const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const C=require('./order-core.js'),data=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog-data.json'),'utf8')),ps=data.products;
const find=s=>ps.find(p=>p.name_en.includes(s));
let state=C.defaultState();
assert.equal(C.group(state,ps).length,0,'no selections preloaded');
const mouse=find('Moving Mouse'),clothes=find('Cotton Waffle'),lotion=find('Baby Lotion'),sb=find('Patchwork Cotton Tote');
const mouseLine=C.addLine(state,mouse);mouseLine.qty=3;C.setStatus(state,mouse,'approved');
const shirtA=C.addLine(state,clothes);assert.equal(C.setStatus(state,clothes,'approved'),false,'size details required');
C.editLine(state,clothes,shirtA.id,'size','6–12m');C.editLine(state,clothes,shirtA.id,'qty','2');assert(C.setStatus(state,clothes,'approved'));
const shirtB=C.addLine(state,clothes,shirtA);shirtB.size='18–24m';shirtB.qty=4;assert.equal(state.items[clothes.id].status,'shortlist','duplicate requires reapproval');C.setStatus(state,clothes,'approved');
let groups=C.group(state,ps);assert.equal(groups.length,2);assert.equal(groups.find(x=>x.supplier==='Elegant Kids').lines.length,2);
assert.equal(C.totals(groups.find(x=>x.supplier==='PlanToys').lines).amounts.THB,342);
assert(C.editLine(state,mouse,mouseLine.id,'qty','5'));assert.equal(C.group(state,ps).some(g=>g.supplier==='PlanToys'),false,'edited approved line excluded');C.setStatus(state,mouse,'approved');
C.hide(state,mouse);assert.equal(state.items[mouse.id].status,'skip');assert(!C.group(state,ps).some(g=>g.supplier==='PlanToys'));state.items[mouse.id].hidden=false;assert(!C.group(state,ps).some(g=>g.supplier==='PlanToys'),'restoring visibility does not reapprove');
const l=C.addLine(state,lotion);C.editLine(state,lotion,l.id,'source','lazada');assert.equal(l.unitPrice,229);assert(C.setStatus(state,lotion,'approved'));assert(C.group(state,ps).some(g=>g.supplier==='Khun Organic Baby · Lazada'));
const usd=C.addLine(state,sb);C.setStatus(state,sb,'approved');const mixed=C.totals([{row:l},{row:usd}]);assert.equal(mixed.amounts.THB,229);assert.equal(mixed.amounts.USD,undefined);assert.equal(mixed.unknown.THB,1);
C.editLine(state,lotion,l.id,'unit','carton');assert.equal(l.unitPrice,null,'unit change must clear incompatible reference price');assert.equal(C.setStatus(state,lotion,'approved'),true);assert.equal(C.totals(C.group(state,ps).find(g=>g.supplier==='Khun Organic Baby · Lazada').lines).unknown.THB,1);
C.editLine(state,lotion,l.id,'unitPrice','100');C.editLine(state,lotion,l.id,'priceKind','quote');assert.equal(l.priceKind,'quote');C.editLine(state,lotion,l.id,'colour','blue');assert.equal(l.priceKind,'reference','old quote not treated as quote for new variant');C.setStatus(state,lotion,'approved');
groups=C.group(state,ps);const eg=groups.find(x=>x.supplier==='Elegant Kids');const en=C.message(eg,state.settings,'en'),th=C.message(eg,state.settings,'th');assert(en.includes('6–12m')&&en.includes('18–24m')&&en.includes('84280'));assert(th.includes('จำนวน:')&&th.includes(clothes.name_en)&&th.includes('84280'));assert(!en.includes(mouse.name_en));
const inMemory=new Map(),storage={getItem:k=>inMemory.get(k)??null,setItem:(k,v)=>inMemory.set(k,v)};
const rounds=[];for(let run=1;run<=3;run++){assert(C.save(storage,state));state=C.load(storage,ps);const g=C.group(state,ps);rounds.push({run,products:Object.keys(state.items).length,groups:g.length,approvedLines:g.reduce((n,x)=>n+x.lines.length,0),shirtQuantities:state.items[clothes.id].lines.map(r=>r.qty)});assert.deepEqual(state.items[clothes.id].lines.map(r=>r.qty),[2,4]);assert.equal(g.length,3);}
const clone=JSON.parse(JSON.stringify(state));clone.items[clothes.id].lines[0].qty=0;assert.throws(()=>C.normalize(clone,ps));clone.items[clothes.id].lines[0].qty=2;clone.items[clothes.id].lines[0].source='invented-channel';assert.throws(()=>C.normalize(clone,ps));
const copy=JSON.parse(JSON.stringify(state));copy.items.unknown={status:'approved',lines:[]};assert.equal(C.normalize(copy,ps).omitted,1);
const draft=structuredClone(state);draft.items[clothes.id].lines[0].qty=0;draft.items[clothes.id].status='shortlist';C.save(storage,draft);const recovered=C.load(storage,ps);assert.equal(recovered.items[clothes.id].lines[0].qty,0);assert.equal(Object.keys(recovered.items).length,4,'unfinished draft survives reload without losing other choices');
assert(!C.save({setItem(){throw Error('unavailable');}},state));assert(!C.safeUrl('javascript:alert(1)'));
const c=state.items[clothes.id].lines[0];c.note='=HYPERLINK("x")';const csv=C.csv(state,ps);assert(csv.includes("'=HYPERLINK"));assert(!csv.includes(mouse.name_en),'skip items absent from CSV');
// Shopping architecture: visible product price drafts are independent of the basket.
let shopping=C.defaultState();const d=C.productDraft(shopping,mouse);assert.equal(d.unitPrice,114);
C.editDraft(shopping,mouse,'unitPrice','199');C.editDraft(shopping,mouse,'qty','2');assert.equal(C.cartLines(shopping,ps).length,0,'editing price does not add unwanted cart rows');
let cartRow=C.addToCart(shopping,mouse);assert.equal(cartRow.unitPrice,199);assert.equal(cartRow.qty,2);
C.addToCart(shopping,mouse);assert.equal(C.cartLines(shopping,ps).length,1,'identical variants merge');assert.equal(cartRow.qty,4);
C.editDraft(shopping,mouse,'unitPrice','210');assert.equal(cartRow.unitPrice,199,'product draft changes do not alter existing basket price');
C.editDraft(shopping,mouse,'colour','blue');C.addToCart(shopping,mouse);assert.equal(C.cartLines(shopping,ps).length,2,'different variants remain separate');
C.editCartLine(shopping,mouse,cartRow.id,'selected',false);assert.equal(C.cartLines(shopping,ps,true).length,1);
const before=structuredClone(shopping);const made=C.checkout(shopping,ps,'order');assert.equal(made.length,1);assert.equal(made[0].lines.length,1);assert.equal(C.cartLines(shopping,ps).length,1,'checkout leaves excluded rows in basket');
const historicalPrice=made[0].lines[0].row.unitPrice;C.editDraft(shopping,mouse,'unitPrice','1');assert.equal(made[0].lines[0].row.unitPrice,historicalPrice,'saved order is immutable snapshot');
assert(C.orderMessage(made[0],'en').includes(made[0].number));assert(C.updateOrder(shopping,made[0].id,'received'));assert(!C.updateOrder(shopping,made[0].id,'invalid'));
const savedOrderRoundTrips=[];for(let n=1;n<=3;n++){C.save(storage,shopping);shopping=C.load(storage,ps);assert.equal(shopping.orders.length,1);assert.equal(shopping.orders[0].status,'received');assert.equal(shopping.orders[0].lines[0].row.unitPrice,historicalPrice);savedOrderRoundTrips.push({run:n,orders:shopping.orders.length,status:shopping.orders[0].status,cartLines:C.cartLines(shopping,ps).length});}
const quoteWork=C.defaultState();C.editDraft(quoteWork,mouse,'unitPrice','');C.addToCart(quoteWork,mouse);assert.throws(()=>C.checkout(quoteWork,ps,'order'),/incomplete/);const inquiries=C.checkout(quoteWork,ps,'quote');assert.equal(inquiries.length,1);assert.equal(C.cartLines(quoteWork,ps).length,1);assert(C.orderMessage(inquiries[0],'en').includes('not a confirmed purchase order'));assert(C.orderMessage(inquiries[0],'th').includes('ยังไม่ใช่คำสั่งซื้อ'));
const mixedSources=C.defaultState();C.addToCart(mixedSources,mouse);C.editDraft(mixedSources,lotion,'source','lazada');C.addToCart(mixedSources,lotion);assert.equal(C.checkout(mixedSources,ps).length,2,'checkout splits real supplier/channel recipients');
const missingVariant=C.defaultState();C.addToCart(missingVariant,clothes);assert.throws(()=>C.checkout(missingVariant,ps),/incomplete/);C.editCartLine(missingVariant,clothes,missingVariant.items[clothes.id].lines[0].id,'size','12m');C.editCartLine(missingVariant,clothes,missingVariant.items[clothes.id].lines[0].id,'unitPrice','200');assert.equal(C.checkout(missingVariant,ps).length,1);
const clothingInquiry=C.defaultState();C.addToCart(clothingInquiry,clothes);const clothingQuotes=C.checkout(clothingInquiry,ps,'quote');assert.equal(clothingQuotes.length,1);assert(C.orderMessage(clothingQuotes[0],'en').includes('confirm the required clothing size'));const importedClothing=C.normalizeOrder(clothingQuotes[0]);assert.doesNotThrow(()=>C.orderMessage(importedClothing,'th'));
const outStock=C.defaultState();C.addToCart(outStock,mouse);C.updateInfo(outStock,mouse,'stock','out_of_stock');assert.throws(()=>C.checkout(outStock,ps),/incomplete/);assert.equal(C.checkout(outStock,ps,'quote').length,1);
const req=C.defaultState(),rr=C.addLine(req,mouse);for(const [value,expected] of [['250','within'],['250.01','over'],['','unknown']]){C.editLine(req,mouse,rr.id,'unitPrice',value);assert.equal(C.budget(mouse,req.items[mouse.id]),expected);}
C.updateInfo(req,mouse,'stock','in_stock');C.updateInfo(req,mouse,'invoiceStatus','received');C.updateInfo(req,mouse,'invoiceType','tax_invoice');C.save(storage,req);assert.equal(C.load(storage,ps).items[mouse.id].invoiceStatus,'received');
const legacy=structuredClone(req);legacy.items[mouse.id].lines[0].currency='USD';legacy.items[mouse.id].lines[0].unitPrice=29.99;legacy.items[mouse.id].status='approved';const migrated=C.normalize(legacy,ps).state;assert.equal(migrated.items[mouse.id].lines[0].unitPrice,null);assert.equal(migrated.items[mouse.id].status,'shortlist');
assert(C.updateInfo(req,mouse,'lazadaUrl','https://www.lazada.co.th/shop/example/'));assert(!C.updateInfo(req,mouse,'lazadaUrl','https://lazada.co.th.example.com/'));C.deleteProduct(req,mouse);assert.equal(C.cartLines(req,ps).length,0);C.save(storage,req);assert(C.load(storage,ps).items[mouse.id].deleted);
assert(ps.every(p=>p.currency==='THB'&&p.sources.every(s=>s.currency==='THB')));
// Execute the new storefront and real event handlers against a minimal DOM fixture.
const template=fs.readFileSync(path.join(__dirname,'order-page.html.in'),'utf8'),ids=[...template.matchAll(/id="([^"]+)"/g)].map(x=>x[1]);
class Element{constructor(id){this.id=id;this.value='';this.textContent='';this.innerHTML='';this.hidden=false;this.checked=false;this.dataset={};this.events={};this.tagName='DIV';this.classList={toggle(){},add(){},remove(){}};}addEventListener(k,f){const previous=this.events[k];this.events[k]=previous?(e=>{previous(e);return f(e);}):f;}setAttribute(k,v){this[k]=v;}querySelectorAll(){return [];}querySelector(){return null;}focus(){}select(){}showModal(){this.open=true;}close(){this.open=false;}}
const elements=Object.fromEntries(ids.map(id=>[id,new Element(id)]));elements['catalog-data'].textContent=JSON.stringify(data);elements['initial-state'].textContent='null';const documentEvents={},browserStorage=new Map(),ctx=vm.createContext({document:{getElementById:id=>elements[id],documentElement:{},addEventListener:(key,fn)=>documentEvents[key]=fn},window:{},URL,crypto:globalThis.crypto,structuredClone,Blob,console,setTimeout:()=>0,clearTimeout(){},localStorage:{getItem:k=>browserStorage.get(k)||null,setItem:(k,v)=>browserStorage.set(k,v)},navigator:{},confirm:()=>false});
vm.runInContext(fs.readFileSync(path.join(__dirname,'order-core.js'),'utf8'),ctx);ctx.CasaOrder=ctx.window.CasaOrder;vm.runInContext(fs.readFileSync(path.join(__dirname,'order-page.js'),'utf8'),ctx);
assert.equal((elements['catalog-grid'].innerHTML.match(/class="product-card /g)||[]).length,ps.length);
assert.equal((elements['catalog-grid'].innerHTML.match(/data-field="unitPrice"/g)||[]).length,ps.length,'every product shows its estimate before adding');
assert(elements['catalog-grid'].innerHTML.includes('readonly aria-readonly="true"'));
elements.language.events.change({target:{value:'en'}});assert.equal(elements['catalog-title'].textContent,'Build your next collection.');
elements['catalog-grid'].events.click({target:{closest:()=>({dataset:{action:'unlock-price',pid:mouse.id,scope:'draft'}})}});
elements['catalog-grid'].events.input({target:{dataset:{scope:'draft',pid:mouse.id,field:'unitPrice'},value:'225',tagName:'INPUT',closest:()=>null}});
assert.equal(JSON.parse([...browserStorage.values()][0]).items[mouse.id].draft.unitPrice,225);
elements['catalog-grid'].events.click({target:{closest:()=>({dataset:{action:'add',pid:mouse.id}})}});
assert(elements['cart-link'].textContent.includes('1'));documentEvents.click({target:{closest:()=>({dataset:{view:'cart'}})}});assert(elements['cart-items'].innerHTML.includes(mouse.name_en));
assert(elements['cart-items'].innerHTML.includes('value="225"'));elements.checkout.events.click();assert(elements['order-history'].innerHTML.includes(mouse.name_en));assert(elements['verification-queue'].innerHTML.includes('Submit for final approval'));assert.equal(JSON.parse([...browserStorage.values()][0]).orders[0].status,'pending_verification');assert.equal(JSON.parse([...browserStorage.values()][0]).orders.length,1);
elements['search'].value='No match at all xyz';elements['search'].events.input();assert.equal(elements['catalog-empty'].hidden,false);
assert(elements['supplier-directory'].innerHTML.includes('https://line.me/R/ti/p/@adaily.factory'));
assert(elements['supplier-directory'].innerHTML.includes('https://line.me/R/ti/p/@commandpstudio'));
console.log(JSON.stringify({core:'passed',legacyPersistenceRounds:rounds,shoppingOrderPersistence:savedOrderRoundTrips,visiblePriceInputs:ps.length,cartMergeAndVariants:'passed',supplierChannelCheckout:'passed',quoteVsOrderValidation:'passed',historicalSnapshot:'passed',storefrontEventFlow:'passed',products:ps.length},null,2));

// Requisitions freeze the estimate and require a complete, separate supplier checklist.
let rq=C.defaultState();C.editDraft(rq,mouse,'unitPrice','');C.addToCart(rq,mouse);C.editDraft(rq,lotion,'source','lazada');C.addToCart(rq,lotion);
assert.throws(()=>C.submitRequisition(rq,ps,'employee'),/owner-required/);
const rqs=C.submitRequisition(rq,ps);assert.equal(rqs.length,2);assert.equal(C.cartLines(rq,ps).length,0);
const ro=rqs[0],rid=ro.lines[0].row.id;assert.equal(ro.status,'pending_verification');assert.equal(ro.lines[0].row.unitPrice,null);
assert(!C.updateOrder(rq,ro.id,'received'));assert(!C.transitionRequisition(rq,ro.id,'approved_to_order','owner'));
assert(!C.transitionRequisition(rq,ro.id,'ready_for_approval'));
for(const [key,value] of Object.entries({availableQty:ro.lines[0].row.qty,finalPrice:180}))C.editVerification(rq,ro.id,key,value,rid);
for(const [key,value] of Object.entries({shippingCost:0,deliveryTime:'2 days',minimumOrder:0,invoiceConfirmed:true,invoiceType:'receipt',paymentTerms:'COD',supplierConfirmed:true,verifiedWith:'Test supplier call',notes:'Synthetic'}))C.editVerification(rq,ro.id,key,value);
assert.deepEqual(C.verificationIssues(ro),[]);assert.equal(C.verifiedTotal(ro).total,180);
C.editVerification(rq,ro.id,'minimumOrder',9999);assert(C.verificationIssues(ro).includes('minimumNotMet'));C.editVerification(rq,ro.id,'minimumOrder',0);
assert(C.transitionRequisition(rq,ro.id,'ready_for_approval','employee'));assert(!C.editVerification(rq,ro.id,'shippingCost',30));
assert(!C.transitionRequisition(rq,ro.id,'approved_to_order','employee'));assert(C.transitionRequisition(rq,ro.id,'pending_verification','owner'));
assert(C.editVerification(rq,ro.id,'notes','Checked again'));assert(C.transitionRequisition(rq,ro.id,'ready_for_approval','employee'));assert(C.transitionRequisition(rq,ro.id,'approved_to_order','owner'));
for(let run=1;run<=3;run++){C.save(storage,rq);rq=C.load(storage,ps);const restored=rq.orders.find(o=>o.id===ro.id);assert.equal(restored.status,'approved_to_order');assert.equal(restored.lines[0].row.unitPrice,null);assert.equal(restored.verification.lines[rid].finalPrice,180);assert.equal(rq.orders.length,2);console.log(JSON.stringify({requisitionPersistenceRound:run,status:restored.status,estimate:restored.lines[0].row.unitPrice,finalPrice:restored.verification.lines[rid].finalPrice,orders:rq.orders.length}));}
console.log('Requisition gates, supplier checklist, owner permissions and persistence passed');

const pending=structuredClone(rq.orders[0]);pending.status='pending_verification';
const returned=structuredClone(pending);returned.verification.notes='Employee return file';returned.status='ready_for_approval';
const merged=C.mergeSharedOrders([pending],[returned]);assert.equal(merged.length,1);assert.equal(merged[0].verification.notes,'Employee return file');assert.equal(merged[0].status,'ready_for_approval');
const changed=structuredClone(returned);changed.lines[0].row.qty=999;assert.throws(()=>C.mergeSharedOrders([pending],[changed]),/frozen shopping list/);
assert.throws(()=>C.mergeSharedOrders([],[returned]),/pending requisitions only/);
console.log('Shared employee-return import preserves checklist updates and rejects changed snapshots');
// Drive the employee UI handlers through completion, not only the pure model.
const uiOrder=JSON.parse([...browserStorage.values()][0]).orders[0],uiLine=uiOrder.lines[0].row.id;
assert(elements['verification-queue'].innerHTML.includes('disabled>Submit for final approval'));
function verifyField(key,value,lineId=''){
 const el={dataset:{verify:key,oid:uiOrder.id,...(lineId?{verifyLine:lineId}:{})},type:typeof value==='boolean'?'checkbox':'text',tagName:'INPUT',value:String(value),checked:value===true};
 elements['verification-queue'].events.change({target:el});
}
verifyField('availableQty',uiOrder.lines[0].row.qty,uiLine);verifyField('finalPrice',180,uiLine);
for(const [key,value] of Object.entries({shippingCost:0,deliveryTime:'Synthetic QA delivery',minimumOrder:0,invoiceType:'receipt',invoiceConfirmed:true,paymentTerms:'QA COD',verifiedWith:'Synthetic QA, no supplier contacted',supplierConfirmed:true}))verifyField(key,value);
assert(!elements['verification-queue'].innerHTML.includes('disabled>Submit for final approval'));
assert(elements['verification-queue'].innerHTML.includes('Confirmed total incl. shipping: 180 THB'));
function requisitionButton(status){return {target:{closest:selector=>selector==='[data-requisition-status]'?{dataset:{oid:uiOrder.id,requisitionStatus:status}}:null}};}
elements['verification-queue'].events.click(requisitionButton('ready_for_approval'));
assert.equal(JSON.parse([...browserStorage.values()][0]).orders[0].status,'ready_for_approval');
assert(elements['verification-queue'].innerHTML.includes('Final owner approval'));
assert(elements['verification-queue'].innerHTML.includes('fieldset disabled'));
elements['verification-queue'].events.click(requisitionButton('approved_to_order'));
assert.equal(JSON.parse([...browserStorage.values()][0]).orders[0].status,'approved_to_order');
assert(elements['verification-queue'].innerHTML.includes('No requisitions awaiting'));
assert.equal(JSON.parse([...browserStorage.values()][0]).orders[0].lines[0].row.unitPrice,225);
console.log('Employee UI change/click events: mandatory checks, final total, submission, field locking, owner approval passed');
