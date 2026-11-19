"""Requisition validation independent of client controls and legacy order statuses."""
import math
from fastapi import HTTPException

STATUSES={'pending_verification','ready_for_approval','approved_to_order','cancelled'}

def fail(message,code=422):
    raise HTTPException(code,message)

def amount(value):
    return type(value) in (int,float) and math.isfinite(value) and 0<=value<=1_000_000_000

def validate_verification(order,complete=False):
    v=order.get('verification')
    if not isinstance(v,dict) or not isinstance(v.get('lines'),dict):fail('Supplier verification required')
    ids=[line['row'].get('id') for line in order['lines']]
    if not ids or any(not isinstance(i,str) or not i for i in ids) or len(set(ids))!=len(ids) or set(v['lines'])!=set(ids):fail('Verification must match every frozen order line')
    for line in order['lines']:
        row=line['row'];r=v['lines'][row['id']]
        if not isinstance(r,dict):fail('Invalid verification line')
        qty=r.get('availableQty');price=r.get('finalPrice')
        if qty is not None and (type(qty)!=int or not 0<=qty<=100000):fail('Invalid available quantity')
        if price is not None and not amount(price):fail('Invalid final THB price')
        if complete and (row['qty']<1 or qty is None or qty<row['qty'] or price is None):fail('Confirm sufficient stock and final price for every line')
    for key in ['shippingCost','minimumOrder']:
        if v.get(key) is not None and not amount(v[key]):fail('Invalid '+key)
        if complete and v.get(key) is None:fail('Confirm '+key+' (zero is allowed)')
    for key in ['deliveryTime','paymentTerms','verifiedWith','notes']:
        if not isinstance(v.get(key,''),str) or len(v.get(key,''))>(500 if key in ['deliveryTime','verifiedWith'] else 2000):fail('Invalid '+key)
        if complete and key!='notes' and not v.get(key,'').strip():fail('Confirm '+key)
    for key in ['invoiceConfirmed','supplierConfirmed']:
        if type(v.get(key))!=bool:fail('Invalid supplier confirmation')
        if complete and v[key] is not True:fail('Supplier contact and invoice confirmation required')
    if v.get('invoiceType') not in ['unknown','receipt','invoice','tax_invoice']:fail('Invalid invoice type')
    if complete and v['invoiceType']=='unknown':fail('Choose confirmed invoice type')
    if complete and sum(line['row']['qty']*v['lines'][line['row']['id']]['finalPrice'] for line in order['lines'])<v['minimumOrder']:fail('Product total does not meet supplier minimum order')

def validate_changes(previous,state,role):
    old_orders={o['id']:o for o in previous.get('orders',[])}
    new_orders={o['id']:o for o in state.get('orders',[])}
    for oid,old in old_orders.items():
        newer=new_orders.get(oid)
        mutable={'status','updatedAt'}|({'verification'} if old.get('kind')=='requisition' else set())
        if not newer or {k:v for k,v in newer.items() if k not in mutable}!={k:v for k,v in old.items() if k not in mutable}:fail('Saved order contents are immutable; cancel or repeat the order instead')
        if old.get('kind')!='requisition':
            if newer.get('status') in STATUSES-{'cancelled'}:fail('Legacy orders cannot bypass the requisition workflow')
            continue
        before,after=old['status'],newer['status']
        if before!='pending_verification' and old.get('verification')!=newer.get('verification'):fail('Submitted supplier verification is locked')
        if before!=after:
            allowed={'pending_verification':{'ready_for_approval'},'ready_for_approval':set(),'approved_to_order':set(),'cancelled':set()}[before]
            if role=='owner':
                if before=='pending_verification':allowed|={'cancelled'}
                if before=='ready_for_approval':allowed|={'approved_to_order','pending_verification','cancelled'}
            if after not in allowed:fail('This role cannot perform that requisition transition',403)
        validate_verification(newer,after in ['ready_for_approval','approved_to_order'])
    for oid,new in new_orders.items():
        if oid in old_orders:continue
        if role!='owner':fail('Only the owner may transfer a shopping list',403)
        if new.get('kind')=='requisition':
            if new['status']!='pending_verification':fail('New requisitions must start pending supplier verification')
            validate_verification(new)
