
const STORE='casa-shop-solo-v1',TARGETS='casa-shop-targets-v1';
const app=document.getElementById('app');
let state=null,tab='Overview',filter='All',term='',view='Cards',modal=null,editing=null,notice='';
const categories=['Wooden toys','Quiet arts & crafts','Family care','Bags & accessories','Home & gifts','Dry food & pantry','Kids clothing','Games & puzzles','Beauty & care for mum','Baby essentials','Swim & sun','Casa Luma merchandise','Cards, stickers & small gifts','Other'];
const statuses=['Idea','Research','Supplier review','Sample review','Ready to order','Ordered','In transit','Received','On shelf','Paused'],supplierStatuses=['Not contacted','Contacted','Awaiting quote','Quoted','Approved','Inactive'],taskStatuses=['To do','In progress','Waiting','Done'];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safe=v=>{try{const u=new URL(String(v));return /^(https?:)$/.test(u.protocol)?u.href:'#'}catch{return '#'}};
const cash=v=>v===null||v===undefined||v===''?'Not set':'฿'+Number(v).toLocaleString('en-US',{maximumFractionDigits:2});
const link=(u,title='Open link')=>safe(u)==='#'?'':`<a href="${esc(safe(u))}" target="_blank" rel="noopener noreferrer">${title} ↗</a>`;
const opts=(values,chosen)=>values.map(v=>`<option value="${esc(v)}" ${String(v)===String(chosen)?'selected':''}>${esc(v)}</option>`).join('');
const counts=()=>({p:state.collection.length,s:state.suppliers.length,received:state.collection.filter(x=>['Received','On shelf'].includes(x.status)).length,ordered:state.collection.filter(x=>['Ordered','In transit'].includes(x.status)).length});
function save(){try{localStorage.setItem(STORE,JSON.stringify(state));notice='Saved in this browser';return true}catch{alert('Browser storage full. Export a backup immediately.');return false}}
function showToast(t){const d=document.createElement('div');d.className='toast';d.textContent=t;document.body.appendChild(d);setTimeout(()=>d.remove(),2600)}
function goto(t){tab=t;term='';filter='All';view='Cards';render()}
function shell(content){const n=counts();app.innerHTML=`<div class="shell"><aside class="sidebar"><div class="brand"><div class="mark">✳</div><div><strong>casa luma</strong><small>THE SHOP STUDIO</small></div></div><div class="navtitle">MY WORKSPACE</div><nav class="nav">${[['Overview','▦'],['My Collection','◇'],['Product Research','⌕'],['Suppliers','⇥'],['Orders','▤'],['Tasks','☷'],['Category goals','◎'],['Backups','⇩']].map(([t,icon])=>`<button data-tab="${t}" class="${tab===t?'active':''}"><span class="ico">${icon}</span>${t}${t==='Tasks'&&state.tasks.some(x=>x.status!=='Done')?`<span class="badge-count">${state.tasks.filter(x=>x.status!=='Done').length}</span>`:''}</button>`).join('')}</nav><div class="side-bottom"><div class="gentle"><span>✿</span><b>Curated with care</b><p>Build your shop collection at your own pace. This is your personal planning space.</p></div><div class="side-foot">LOCAL WORKSPACE · SAVE A BACKUP REGULARLY</div></div></aside><main class="main"><header class="topbar"><span>CASA LUMA / SHOP PLANNING</span><div class="topbar-right"><span class="solo-tag"><i></i> SOLO MODE</span></div></header><div class="content">${content}</div></main></div>${modal?modalHtml():''}`;document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>goto(b.dataset.tab));bind()}
const heading=(tag,title,sub,add='',type='')=>`<div class="pagehead"><div><div class="eyebrow">${tag}</div><h1>${title}</h1><p>${sub}</p></div><div class="head-actions">${add?`<button class="primary" data-add="${type}">+ ${add}</button>`:''}</div></div>`;
function overview(){const c=counts(),cats=[...new Set(state.collection.map(p=>p.category))].map(name=>({name,all:state.collection.filter(p=>p.category===name).length,received:state.collection.filter(p=>p.category===name&&['Received','On shelf'].includes(p.status)).length})).sort((a,b)=>b.all-a.all),max=Math.max(...cats.map(x=>x.all),1);return `<div class="hero"><div><div class="eyebrow">YOUR SHOP, AT A GLANCE</div><h1>Growing something <em>lovely.</em></h1><p>Your own calm space to collect ideas, compare options, and design a collection that feels like Casa.</p><button class="primary" data-add="collection">+ Add a product</button></div><div class="hero-orbit"><div class="hero-seal">CASA<br>FINDS<small>✳</small></div></div></div><div class="metric-grid">${[['MY SHOP PRODUCTS',c.p,'Your selected collection'],['IN THE SHOP',c.received,'Marked received / on shelf'],['ON ORDER',c.ordered,'Ordered / in transit'],['RESEARCH IDEAS',state.research.length,'Browse separately']].map(x=>`<div class="metric"><small>${x[0]}</small><strong>${x[1]}</strong><p>${x[2]}</p></div>`).join('')}</div><div class="dash-cols"><section class="panel"><div class="panelhead"><div><div class="eyebrow">THE BIG PICTURE</div><h2>Category balance</h2></div><button class="text-button" data-tab="Category goals">Set goals ↗</button></div><p class="muted">All ideas in light green. Confirmed received items in dark green.</p><div class="category-rows">${cats.map(c=>`<div class="category-row"><div class="category-caption"><span>${esc(c.name)}</span><small>${c.all} ideas · ${c.received} in shop</small></div><div class="bar"><i style="width:${c.all/max*100}%"></i><b style="width:${c.received/max*100}%"></b></div></div>`).join('')}</div></section><section class="panel"><div class="panelhead"><div><div class="eyebrow">FOCUS NOW</div><h2>Planning tasks</h2></div><button class="text-button" data-tab="Tasks">View all ↗</button></div><div class="tasks-brief">${state.tasks.filter(x=>x.status!=='Done').slice(0,6).map(t=>`<div class="task-brief"><button class="circle-check" title="Mark done" data-done="${esc(t.id)}"></button><div><b>${esc(t.title)}</b><small>${esc(t.assignee||'Unassigned')} · ${esc(t.status)}</small></div></div>`).join('')||'<p class="muted">No pending tasks.</p>'}</div><button class="text-button" data-add="tasks">+ Add a task</button></section></div><div class="notice">✿ &nbsp; This overview counts your collection only, not the 154 research leads. No products count as in stock until marked Received or On shelf.</div>`}
const ctrl=(p,type,options)=>`<select class="status-select" data-status="${type}" data-id="${esc(p.id)}">${opts([...new Set([...options,p.status])],p.status)}</select>`;
function productCard(p){return `<article class="product"><div class="product-cover">${safe(p.image)!=='#'?`<img loading="lazy" src="${esc(safe(p.image))}" alt="" onerror="this.style.display='none'">`:'<div class="glyph">✳</div>'}<button class="product-edit" data-edit="collection" data-id="${esc(p.id)}" aria-label="Edit product">✎</button></div><div class="product-body"><div class="category-kicker">${esc(p.category)}</div><h3>${esc(p.name)}</h3>${ctrl(p,'collection',statuses)}<div class="product-footer"><span>${cash(p.referencePrice)} reference</span>${link(p.url,'Open product')}</div></div></article>`}
function products(){const list=state.collection.filter(p=>(filter==='All'||p.category===filter)&&[p.name,p.category,p.supplier,p.status].join(' ').toLowerCase().includes(term.toLowerCase()));return heading('MY SHOP',`My Shop Collection <span class="count">${state.collection.length}</span>`,'Only items you add or select for your shop. Research ideas are kept separately.','Add product','collection')+`<div class="quick-import"><div><strong>Found something you love?</strong><p>Paste a Lazada, SHEIN or shop product URL. We will try to fill its details.</p></div><div class="quick-import-controls"><input id="quick-url" type="url" placeholder="https://..."><button id="quick-import" class="primary" type="button">Read product link →</button></div></div><div class="toolbar"><input id="search" placeholder="Search products, brands…" value="${esc(term)}"><select id="filter"><option value="All">All categories</option>${opts([...new Set(state.collection.map(p=>p.category))].sort(),filter)}</select><div class="toggle"><button data-view="Cards" class="${view==='Cards'?'chosen':''}">Cards</button><button data-view="Table" class="${view==='Table'?'chosen':''}">Table</button></div></div>${view==='Cards'?`<div class="cards">${list.map(productCard).join('')||'<div class="empty">Your collection is empty. Paste a product link above, or browse Product Research and add what you like.</div>'}</div>`:`<div class="table-wrap"><table><thead><tr><th>Product</th><th>Category</th><th>Status</th><th>Reference</th><th>Qty</th><th>Link</th><th></th></tr></thead><tbody>${list.map(p=>`<tr><td><b>${esc(p.name)}</b></td><td>${esc(p.category)}</td><td>${ctrl(p,'collection',statuses)}</td><td>${cash(p.referencePrice)}</td><td>${esc(p.quantity||0)}</td><td>${link(p.url,'Open ↗')}</td><td><button data-edit="collection" data-id="${esc(p.id)}">Edit</button></td></tr>`).join('')}</tbody></table></div>`}`}

function research(){
const cats=[...new Set(state.research.map(p=>p.category))].sort();
const list=state.research.filter(p=>(filter==='All'||filter===p.category)&&[p.name,p.category,p.supplier].join(' ').toLowerCase().includes(term.toLowerCase()));
return heading('INSPIRATION LIBRARY','Product Research <span class="count">'+state.research.length+'</span>','Ideas gathered from sourcing research. Not part of your shop unless you add them.')
+'<div class="notice">✿ &nbsp; Nothing in Product Research counts toward your shop mix, ordering or inventory. Select only what you love.</div>'
+'<div class="toolbar"><input id="search" placeholder="Search research by name or brand…" value="'+esc(term)+'"><select id="filter"><option value="All">All categories</option>'+opts(cats,filter)+'</select></div>'
+'<div class="cards">'+(list.map(p=>{
 const selected=state.collection.some(x=>x.sourceResearchId===p.id);
 return '<article class="product"><div class="product-cover">'+(safe(p.image)!=='#'?'<img loading="lazy" src="'+esc(safe(p.image))+'" alt="">':'<div class="glyph">✳</div>')+'</div><div class="product-body"><div class="category-kicker">'+esc(p.category)+'</div><h3>'+esc(p.name)+'</h3><div class="muted">'+esc(p.supplier||'Supplier to verify')+' · '+cash(p.referencePrice)+' (reference)</div><div class="product-footer">'+link(p.url,'View product')+'<button class="text-button" '+(selected?'disabled aria-label="Already added"':'data-promote="'+esc(p.id)+'"')+'>'+(selected?'✓ Added':'+ Add to my shop')+'</button></div></div></article>'
}).join('')||'<div class="empty">Nothing matches these filters.</div>')+'</div>';
}
function promote(id){
 const p=state.research.find(x=>x.id===id);if(!p)return;
 if(state.collection.some(x=>x.sourceResearchId===id)){showToast('Already in your shop');return}
 state.collection.unshift({...p,id:'collection-'+crypto.randomUUID(),sourceResearchId:id,status:'Idea',quantity:0,cost:null,retail:null,priority:'Normal',origin:'research'});
 save();goto('My Collection');showToast('Added to My Shop Collection');
}
function suppliers(){let list=state.suppliers.filter(s=>[s.name,s.status,s.notes].join(' ').toLowerCase().includes(term.toLowerCase()));return heading('PEOPLE & PARTNERS',`Suppliers <span class="count">${state.suppliers.length}</span>`,'Every contact, social account and wholesale conversation in one place.','Add supplier','suppliers')+`<div class="toolbar"><input id="search" placeholder="Search suppliers…" value="${esc(term)}"></div><div class="supplier-cards">${list.map((s,i)=>`<article class="supplier"><small>${String(i+1).padStart(2,'0')}</small><h3>${esc(s.name)}</h3>${ctrl(s,'suppliers',supplierStatuses)}<p>${esc(s.notes||'Research wholesale pricing, shipping, and invoice terms.')}</p><div class="supplier-footer">${link(s.url,'Visit supplier')}<button class="text-button" data-edit="suppliers" data-id="${esc(s.id)}">Edit ✎</button></div></article>`).join('')||'<div class="empty">No supplier matches.</div>'}</div>`}
function orders(){const stages=['Ready to order','Ordered','In transit','Received'];return heading('MAKE IT REAL','Ordering desk','Move items along the ordering journey. Nothing gets purchased automatically.')+`<div class="kanban">${stages.map(stage=>`<section class="lane"><h3>${stage}<span>${state.collection.filter(p=>p.status===stage).length}</span></h3>${state.collection.filter(p=>p.status===stage).map(p=>`<div class="ordercard"><strong>${esc(p.name)}</strong><small>${esc(p.category)}</small>${ctrl(p,'collection',statuses)}${link(p.url,'Product link')}</div>`).join('')||'<p class="muted">No items yet.</p>'}</section>`).join('')}</div>`}
function tasks(){return heading('ONE STEP AT A TIME','Planning tasks','Your private checklist while you build your store.','Add task','tasks')+`<div class="task-table">${state.tasks.map(t=>`<div class="task-item"><input type="checkbox" data-taskcheck="${esc(t.id)}" ${t.status==='Done'?'checked':''}><div class="task-main"><strong style="${t.status==='Done'?'text-decoration:line-through':''}">${esc(t.title)}</strong><small>${esc(t.notes||'No notes yet')}</small></div><small class="muted">${esc(t.assignee)}</small>${ctrl(t,'tasks',taskStatuses)}<button data-edit="tasks" data-id="${esc(t.id)}">✎</button></div>`).join('')||'<div class="empty">No tasks yet.</div>'}</div>`}
function goals(){let custom={};try{custom=JSON.parse(localStorage.getItem(TARGETS)||'{}')}catch{}const names=[...new Set([...categories,...state.collection.map(p=>p.category)])];return heading('A BETTER BALANCE','Category goals','Set your ideal number of different products per category. Targets are for planning, not purchase commitments.')+`<div class="target-grid">${names.map(name=>{const all=state.collection.filter(p=>p.category===name).length,stock=state.collection.filter(p=>p.category===name&&['Received','On shelf'].includes(p.status)).length,target=Number(custom[name]||0),need=Math.max(0,target-all);return `<div class="target-card"><div class="eyebrow">PRODUCT MIX</div><h3>${esc(name)}</h3><div class="countline"><strong>${all}</strong><small>ideas so far</small></div><div class="numbers"><div>Already in shop: <b>${stock}</b></div><div>Ideas needed to target: <b>${need}</b></div></div><label>Your idea target<input class="minitarget" type="number" min="0" max="1000" value="${target}" data-target="${esc(name)}"></label><div style="margin-top:14px"><span class="target-status ${target===0?'none':need>0?'under':''}">${target===0?'No target yet':need>0?'Explore '+need+' more':'Target met for ideas'}</span></div></div>`}).join('')}</div>`}
function backup(){return heading('KEEP YOUR WORK SAFE','Backups & privacy','Your progress stays in this browser until you export it. Nobody is invited or notified.')+`<div class="backup-grid"><div class="backup-section"><div class="eyebrow">RECOMMENDED</div><h2>Download a full backup</h2><p>Export both My Shop Collection and Product Research, plus suppliers, tasks and category targets, to one JSON file. Keep it somewhere safe. Use it later to move to the shared system.</p><div class="buttonrow"><button id="export" class="primary">↓ Download backup</button></div></div><div class="backup-section"><div class="eyebrow">RESTORE</div><h2>Import a previous backup</h2><p>Restore your work from a JSON file saved by this studio. The import replaces the current browser draft after confirmation.</p><input id="import" type="file" accept=".json,application/json"></div><div class="backup-section"><div class="eyebrow">SHARE WITH YOURSELF</div><h2>Export CSV product list</h2><p>Download an easy-to-review copy of My Shop Collection only. CSV exports do not include all workspace settings.</p><button id="csv" class="secondary">Download CSV</button></div><div class="backup-section"><div class="eyebrow">ABOUT SOLO MODE</div><h2>Private draft workflow</h2><p>This prototype has no team accounts, no invitations and no live collaboration. Your edits save in the browser you use. Clearing browser storage could delete them.</p><div class="note-privacy"><b>Privacy note:</b> This preview is hosted on a public GitHub Pages address. It is not password-protected. Your edits stay on your own device, but do not put confidential information in the page or link until private hosting is configured.</div></div></div>`}
const config={collection:[['name','Product name'],['category','Category'],['supplier','Supplier / store'],['url','Product or order link'],['image','Image URL'],['referencePrice','Reference price (THB)'],['cost','Confirmed cost (THB)'],['retail','Retail price (THB)'],['quantity','Quantity received'],['status','Status'],['priority','Priority'],['notes','Research notes']],suppliers:[['name','Supplier name'],['url','Website / Instagram link'],['contact','Contact details'],['status','Status'],['notes','Wholesale / MOQ / shipment notes']],tasks:[['title','Task'],['assignee','Assignee'],['status','Status'],['notes','Notes']]};
function modalHtml(){const f=config[modal]||[],obj=editing||{};return `<div class="dialog-backdrop" id="backdrop"><form class="dialog" id="editor"><div class="dialog-header"><div><div class="eyebrow">CASA SHOP PLANNING</div><h2>${editing?'Edit':'Add'} ${modal==='collection'?'product':modal==='suppliers'?'supplier':'task'}</h2></div><button type="button" class="dialog-close" id="close">×</button></div>${modal==="collection"?"<div class=\"link-import\"><div class=\"eyebrow\">QUICK PRODUCT IMPORT</div><label class=\"muted\" for=\"import-link\">Paste any product URL. We will try to read its title, photo, store and price.</label><div class=\"quick-import-controls\"><input id=\"import-link\" type=\"url\" placeholder=\"https://www.lazada.co.th/... or SHEIN / store URL\"><button type=\"button\" id=\"extract-product\" class=\"primary\">Auto-fill from link</button></div><p class=\"muted\" id=\"extract-note\">Links are sent to Jina Reader for page extraction. Some shops block access, so please verify before saving.</p></div>":""}<div class="fields">${f.map(([k,label])=>`<label class="field ${k==='notes'?'full':''}">${label}${k==='category'? `<select name="${k}">${opts([...new Set([...categories,...state.collection.map(p=>p.category)])],obj[k]||'Other')}</select>`:k==='status'? `<select name="${k}">${opts(modal==='collection'?statuses:modal==='suppliers'?supplierStatuses:taskStatuses,obj[k]||(modal==='collection'?'Idea':modal==='suppliers'?'Not contacted':'To do'))}</select>`:k==='priority'? `<select name="${k}">${opts(['Low','Normal','High'],obj[k]||'Normal')}</select>`:k==='notes'?`<textarea name="${k}" rows="4">${esc(obj[k]||'')}</textarea>`:`<input name="${k}" ${['referencePrice','cost','retail','quantity'].includes(k)?'type="number" min="0" step="any"':''} value="${esc(obj[k]??'')}">`}</label>`).join('')}</div><div class="dialog-actions">${editing?'<button class="danger" id="delete" type="button">Delete item</button>':''}<button class="secondary" type="button" id="cancel">Cancel</button><button class="primary">Save changes</button></div></form></div>`}

function slugName(url){
 try{const u=new URL(url),parts=u.pathname.split('/').filter(Boolean),s=parts.filter(x=>!/^\d+$/.test(x)).pop()||'';
 const decoded=decodeURIComponent(s).replace(/\.(html?|php)$/i,'').replace(/[-_]+/g,' ').replace(/\b(?:item|product)\b/gi,' ').trim();
 return decoded.length>4&&/[a-zA-Z\u0E00-\u0E7F\u0590-\u05FF]/.test(decoded)?decoded.slice(0,140):'';
 }catch{return ''}
}
function hostName(url){
 try{let h=new URL(url).hostname.replace(/^www\./,'');if(h.includes('lazada'))return 'Lazada';if(h.includes('shein'))return 'SHEIN';return h.split('.')[0].replace(/[-_]/g,' ').replace(/^./,c=>c.toUpperCase())}catch{return ''}
}
function firstImage(markdown){
 const all=[...String(markdown).matchAll(/!\[[^\]]{0,100}\]\((https?:\/\/[^\s)]+)\)/g)];
 return all.map(m=>m[1]).find(u=>!/(logo|icon|avatar|tracking|pixel|banner|favicon)/i.test(u))||'';
}
function parsePrice(text){
 const m=String(text).slice(0,8500).match(/(?:\bprice\s*[:：]\s*)?(?:฿|THB\s*|\bBaht\s*)([0-9][0-9,]*(?:\.[0-9]{1,2})?)/i);
 if(!m)return null;const v=Number(m[1].replace(/,/g,''));return Number.isFinite(v)&&v>0&&v<300000?v:null;
}
function fallbackFromUrl(url){
 const supplier=hostName(url);
 return {name:slugName(url),supplier,url,image:'',referencePrice:null,status:'Idea',quantity:0,priority:'Normal',notes:'Product link saved. Automatic page data could not be verified; please complete and review details.'};
}
async function lookupProduct(url){
 const u=new URL(url);if(!/^https?:$/.test(u.protocol)||u.username||u.password)throw Error('Please enter a normal http(s) product URL without login credentials.');
 const result=fallbackFromUrl(u.href);
 // Reader runs only when the user clicks auto-fill. It is independent of the future private hosting.
 const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),18000);
 try{
 const response=await fetch('https://r.jina.ai/'+u.href,{method:'GET',headers:{Accept:'application/json'},signal:controller.signal});
 if(!response.ok)throw Error('Reader returned '+response.status);
 const envelope=await response.json();
 const d=(envelope&&typeof envelope.data==='object')?envelope.data:(typeof envelope?.data==='string'?{content:envelope.data,title:envelope.title||''}:envelope);
 const title=String(d?.title||'').trim();
 const content=String(d?.content||'').slice(0,45000);
 if(!title&&!content)throw Error('No readable product data was found.');
 if(/just a moment|access denied|robot check|captcha/i.test(title))throw Error('Store blocks page extraction.');
 if(title.length>3){
 const cleaned=title.replace(/\s*[|\u2013\u2014]\s*(?:Lazada|SHEIN|Shopee|Official Store).*$/i,'').trim();
 if(cleaned.length>3&&!/home page|log in|sign in|cookie policy/i.test(cleaned))result.name=cleaned.slice(0,180);
 }
 if(d?.images){const imgs=Array.isArray(d.images)?d.images:Object.values(d.images);for(const img of imgs){const candidate=typeof img==='string'?img:(img?.url||img?.src||'');if(safe(candidate)!=='#'&&!/(logo|icon|avatar)/i.test(candidate)){result.image=candidate;break}}}
 if(!result.image)result.image=firstImage(content);
 const price=parsePrice(content);if(price!==null)result.referencePrice=price;
 const detail=content.replace(/\s+/g,' ').slice(0,200);
 result.notes='Auto-filled from public product page. Verify photo, variant, price, currency and supplier before ordering. '+detail;
 return {values:result,success:true,message:'Product details suggested. Review every field, especially the price and variant, before saving.'};
 }catch(e){
 return {values:result,success:false,message:'This site could not be read automatically ('+(e.name==='AbortError'?'request timed out':e.message)+'). The link is kept; complete the missing details manually.'};
 }finally{clearTimeout(timeout)}
}
async function autoFillModal(){
 if(modal!=='collection')return;
 const urlInput=document.getElementById('import-link'),note=document.getElementById('extract-note'),btn=document.getElementById('extract-product');
 const raw=urlInput?.value?.trim()||'';
 if(safe(raw)==='#'){if(note)note.textContent='Enter a valid product link starting with https://';return}
 btn.disabled=true;btn.textContent='Reading product…';note.textContent='Trying to read public product details…';
 try{
 const r=await lookupProduct(raw);
 if(modal!=='collection'||!document.getElementById('editor'))return;
 const form=document.getElementById('editor');
 for(const [k,v] of Object.entries(r.values)){
 const field=form.elements.namedItem(k);
 if(!field||v===null||v===undefined||v==='')continue;
 if(editing&&k!=='url'&&field.value.trim())continue;
 field.value=String(v);
 }
 note.textContent=r.message;note.style.color=r.success?'#3a7652':'#a46a42';
 }catch(e){note.textContent=e.message;note.style.color='#a46a42'}
 finally{if(document.getElementById('extract-product')){btn.disabled=false;btn.textContent='Auto-fill from link'}}
}
function normalizeWorkspace(w){
 if(!w||typeof w!=='object')throw Error('Invalid backup data');
 if(!Array.isArray(w.suppliers)||!Array.isArray(w.tasks))throw Error('Invalid workspace lists');
 if(!Array.isArray(w.collection)||!Array.isArray(w.research)){
  if(!Array.isArray(w.products))throw Error('No product catalog found in backup');
  w.collection=w.products.filter(p=>p.origin==='shop'||String(p.id||'').startsWith('manual-'));
  w.research=w.products.filter(p=>!w.collection.includes(p));
 }
 if(!Array.isArray(w.collection)||!Array.isArray(w.research))throw Error('Missing lists');
 delete w.products;
 return w;
}
function openModal(type,id){modal=type;editing=id?state[type].find(x=>String(x.id)===id):null;render()}
function updateStatus(type,id,value){const item=state[type].find(x=>String(x.id)===id);if(item){item.status=value;save();render();showToast('Status updated')}}
function closeModal(){modal=null;editing=null;render()}
function download(name,contents,mime){const blob=new Blob([contents],{type:mime}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000)}
function bind(){
document.querySelectorAll('[data-tab]').forEach(el=>el.onclick=()=>goto(el.dataset.tab));
document.querySelectorAll('[data-add]').forEach(el=>el.onclick=()=>openModal(el.dataset.add));
document.querySelectorAll('[data-promote]').forEach(el=>el.onclick=()=>promote(el.dataset.promote));
const quick=document.getElementById('quick-import');if(quick)quick.onclick=async()=>{const raw=document.getElementById('quick-url')?.value?.trim();if(safe(raw)==='#'){alert('Please paste a valid product URL');return}openModal('collection');const target=document.getElementById('import-link');if(target)target.value=raw;await autoFillModal()};
document.querySelectorAll('[data-edit]').forEach(el=>el.onclick=()=>openModal(el.dataset.edit,el.dataset.id));
document.querySelectorAll('[data-view]').forEach(el=>el.onclick=()=>{view=el.dataset.view;render()});
document.querySelectorAll('[data-status]').forEach(el=>el.onchange=()=>updateStatus(el.dataset.status,el.dataset.id,el.value));
document.querySelectorAll('[data-done]').forEach(el=>el.onclick=()=>updateStatus('tasks',el.dataset.done,'Done'));
document.querySelectorAll('[data-taskcheck]').forEach(el=>el.onchange=()=>updateStatus('tasks',el.dataset.taskcheck,el.checked?'Done':'To do'));
document.querySelectorAll('[data-target]').forEach(el=>el.onchange=()=>{let x={};try{x=JSON.parse(localStorage.getItem(TARGETS)||'{}')}catch{}x[el.dataset.target]=Number(el.value)||0;localStorage.setItem(TARGETS,JSON.stringify(x));render();showToast('Category target saved')});
const search=document.getElementById('search');if(search)search.oninput=e=>{const n=e.target.selectionStart;term=e.target.value;render();let z=document.getElementById('search');z.focus();z.setSelectionRange(n,n)};
const select=document.getElementById('filter');if(select)select.onchange=e=>{filter=e.target.value;render()};
const exp=document.getElementById('export');if(exp)exp.onclick=()=>{download('casa-shop-backup-'+new Date().toISOString().slice(0,10)+'.json',JSON.stringify({schema:2,date:new Date().toISOString(),workspace:state,targets:JSON.parse(localStorage.getItem(TARGETS)||'{}')},null,2),'application/json');showToast('Backup downloaded')};
const csv=document.getElementById('csv');if(csv)csv.onclick=()=>{const keys=['name','category','supplier','status','priority','referencePrice','cost','retail','quantity','url','notes'];const q=v=>'"'+String(v??'').replace(/"/g,'""')+'"';download('casa-shop-products.csv',[keys.map(q).join(','),...state.collection.map(p=>keys.map(k=>q(p[k])).join(','))].join('\r\n'),'text/csv;charset=utf-8')};
const imp=document.getElementById('import');if(imp)imp.onchange=async()=>{const file=imp.files[0];if(!file)return;try{const d=JSON.parse(await file.text());if(![1,2].includes(d.schema)||!d.workspace||!Array.isArray(d.workspace.suppliers)||!Array.isArray(d.workspace.tasks))throw Error('File is not a valid Casa Studio backup');if(!confirm('Replace the current browser draft with this backup?'))return;state=normalizeWorkspace(d.workspace);localStorage.setItem(TARGETS,JSON.stringify(d.targets||{}));save();goto('Overview');showToast('Backup restored')}catch(e){alert(e.message)}};
const edit=document.getElementById('editor');if(edit){const extract=document.getElementById('extract-product');if(extract)extract.onclick=autoFillModal;document.getElementById('cancel').onclick=closeModal;document.getElementById('close').onclick=closeModal;document.getElementById('backdrop').onclick=e=>{if(e.target.id==='backdrop')closeModal()};edit.onsubmit=e=>{e.preventDefault();const d=Object.fromEntries(new FormData(edit));if(!(d.name||d.title)?.trim()){alert('Please enter a name or task title');return}for(let k of ['referencePrice','cost','retail','quantity'])if(k in d)d[k]=d[k]===''?null:Number(d[k]);if(editing){Object.assign(editing,d)}else{state[modal].unshift({id:'manual-'+crypto.randomUUID(),...(modal==='collection'?{status:'Idea',priority:'Normal',quantity:0}:modal==='suppliers'?{status:'Not contacted'}:{status:'To do'}),...d})}save();closeModal();showToast('Saved')};const del=document.getElementById('delete');if(del)del.onclick=()=>{if(confirm('Remove this record from your draft?')){state[modal]=state[modal].filter(x=>x!==editing);save();closeModal()}}}
}
function render(){if(!state)return;const screens={Overview:overview,'My Collection':products,'Product Research':research,Suppliers:suppliers,Orders:orders,Tasks:tasks,'Category goals':goals,Backups:backup};shell(screens[tab]())}
async function start(){try{let saved=localStorage.getItem(STORE);if(saved){state=normalizeWorkspace(JSON.parse(saved))}else{const r=await fetch('./solo-seed.json');if(!r.ok)throw Error('Could not load initial catalog');state=normalizeWorkspace(await r.json())}save();render()}catch(e){app.innerHTML='<div class="boot">Unable to open the studio. '+esc(e.message)+'</div>'}}
start();
