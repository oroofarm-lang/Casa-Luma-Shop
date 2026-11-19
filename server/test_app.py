"""HTTP integration checks with synthetic users and isolated SQLite. No real credentials."""
import copy, importlib, json, os, secrets, tempfile, unittest, uuid
from pathlib import Path
from fastapi.testclient import TestClient

_tmp=tempfile.TemporaryDirectory(prefix='casa-server-test-')
os.environ['SQLITE_PATH']=str(Path(_tmp.name)/'shared.sqlite3')
os.environ['APP_ENV']='test'
os.environ['APP_ORIGIN']='http://localhost:8000'
os.environ['SETUP_TOKEN']=secrets.token_urlsafe(32)
os.environ.pop('DATABASE_URL',None)
mod=importlib.import_module('server.app')
ORIGIN={'Origin':'http://localhost:8000'}

class SharedWorkspaceTests(unittest.TestCase):
    def setUp(self):
        mod.initialize()
        with mod.DB() as db:
            for table in ['sessions','invitations','users','workspace_revisions','workspace_requests','audit_events','rate_limits']:db.execute('DELETE FROM '+table)
            db.execute('UPDATE workspace SET version=0,data=? WHERE id=1',(json.dumps(mod.default_state()),))
        self.owner=TestClient(mod.app,base_url='http://localhost:8000')
        self.employee=TestClient(mod.app,base_url='http://localhost:8000')
        self.password=secrets.token_urlsafe(24)
    def setup_owner(self):
        r=self.owner.post('/api/setup',json=dict(setupToken=os.environ['SETUP_TOKEN'],email='owner@example.test',name='Test owner',password=self.password),headers=ORIGIN)
        self.assertEqual(r.status_code,200,r.text)
        session=self.owner.get('/api/session').json();self.csrf={**ORIGIN,'X-CSRF-Token':session['csrf']}
    def add_employee(self):
        invite=self.owner.post('/api/admin/invitations',json={'email':'employee@example.test','role':'owner'},headers=self.csrf)
        self.assertEqual(invite.status_code,200,invite.text)
        token=invite.json()['url'].split('#')[1]
        r=self.employee.post('/api/join',json={'token':token,'name':'Employee','password':self.password,'role':'owner'},headers=ORIGIN)
        self.assertEqual(r.status_code,200,r.text)
        session=self.employee.get('/api/session').json();self.assertEqual(session['role'],'employee')
        self.employee_csrf={**ORIGIN,'X-CSRF-Token':session['csrf']}
        return token
    def put(self,client,state,version,headers,request_id=None):
        return client.put('/api/workspace',json={'state':state,'version':version,'requestId':request_id or uuid.uuid4().hex},headers=headers)
    def test_private_routes_setup_and_csrf(self):
        self.assertEqual(self.owner.get('/api/workspace').status_code,401)
        self.assertEqual(self.owner.get('/',follow_redirects=False).status_code,303)
        self.assertEqual(self.owner.post('/api/setup',json={'setupToken':'wrong'},headers=ORIGIN).status_code,403)
        self.setup_owner()
        self.assertEqual(self.owner.post('/api/setup',json=dict(setupToken=os.environ['SETUP_TOKEN'],email='other@example.test',password=self.password),headers=ORIGIN).status_code,409)
        state=self.owner.get('/api/workspace').json()['state']
        self.assertEqual(self.put(self.owner,state,0,ORIGIN).status_code,403)
        self.assertEqual(self.put(self.owner,state,0,{**self.csrf,'Origin':'https://attacker.example'}).status_code,403)
        page=self.owner.get('/')
        self.assertEqual(page.status_code,200)
        self.assertIn('data-hosted="true"',page.text)
        self.assertIn('nonce-',page.headers['content-security-policy'])
        self.assertIn('HttpOnly',self.owner.post('/api/login',json={'email':'owner@example.test','password':self.password},headers=ORIGIN).headers['set-cookie'])
    def test_two_users_sync_conflict_and_idempotency(self):
        self.setup_owner();self.add_employee()
        a=self.owner.get('/api/workspace').json();b=self.employee.get('/api/workspace').json();a['state']['settings']['notes']='Owner shared update'
        rid=uuid.uuid4().hex
        r=self.put(self.owner,a['state'],a['version'],self.csrf,rid);self.assertEqual(r.status_code,200,r.text)
        duplicate=self.put(self.owner,a['state'],a['version'],self.csrf,rid);self.assertEqual(duplicate.json()['version'],1)
        self.assertEqual(self.employee.get('/api/workspace').json()['state']['settings']['notes'],'Owner shared update')
        b['state']['settings']['notes']='Stale employee update'
        self.assertEqual(self.put(self.employee,b['state'],b['version'],self.employee_csrf).status_code,409)
        current=self.employee.get('/api/workspace').json();current['state']['settings']['notes']='Employee current update'
        self.assertEqual(self.put(self.employee,current['state'],current['version'],self.employee_csrf).status_code,200)
        self.assertEqual(self.owner.get('/api/workspace').json()['state']['settings']['notes'],'Employee current update')
        with mod.DB() as db:self.assertEqual(db.one('SELECT COUNT(*) AS n FROM workspace_revisions')['n'],2)
        self.assertEqual(self.owner.get('/api/workspace',headers={'If-None-Match':'2'}).status_code,304)
    def test_roles_invite_replay_and_disable(self):
        self.setup_owner();token=self.add_employee()
        self.assertEqual(self.employee.get('/api/admin/users').status_code,403)
        self.assertEqual(self.employee.post('/api/admin/invitations',json={'email':'third@example.test'},headers=self.employee_csrf).status_code,403)
        self.assertEqual(self.employee.post('/api/join',json={'token':token,'name':'Replay','password':self.password},headers=ORIGIN).status_code,403)
        uid=self.employee.get('/api/session').json()['email']
        user=next(x for x in self.owner.get('/api/admin/users').json()['users'] if x['email']==uid)
        self.assertEqual(self.owner.post('/api/admin/users/'+user['id']+'/disable',json={},headers=self.csrf).status_code,200)
        self.assertEqual(self.employee.get('/api/workspace').status_code,401)
    def test_order_snapshot_is_immutable_and_thb_only(self):
        self.setup_owner();state=mod.default_state();p=mod.CATALOG[0];src=p['sources'][0]
        row=dict(id=uuid.uuid4().hex,source=src['id'],qty=2,unit='piece',unitPrice=199,currency='THB',model='',size='',colour='',pack='',note='',priceKind='quote')
        order=dict(id=uuid.uuid4().hex,number='CL-test',batchId='test',createdAt='2026-10-20',updatedAt='2026-10-20',kind='order',status='prepared',supplier=src['supplier'],channel=src['channel'],url=src['url'],contact=src['contact'],settings=state['settings'],lines=[dict(product=p,row=row,source=src,info={})])
        state['orders']=[order]
        self.assertEqual(self.put(self.owner,state,0,self.csrf).status_code,200)
        bad=copy.deepcopy(state);bad['orders'][0]['lines'][0]['row']['unitPrice']=1
        self.assertEqual(self.put(self.owner,bad,1,self.csrf).status_code,422)
        state['orders'][0]['status']='received'
        self.assertEqual(self.put(self.owner,state,1,self.csrf).status_code,200)
        bad=copy.deepcopy(state);bad['orders']=[]
        self.assertEqual(self.put(self.owner,bad,2,self.csrf).status_code,422)
        bad=copy.deepcopy(state);bad['orders'][0]['lines'][0]['row']['currency']='USD'
        self.assertEqual(self.put(self.owner,bad,2,self.csrf).status_code,422)
        self.assertEqual(self.owner.get('/api/workspace').json()['state']['orders'][0]['lines'][0]['row']['unitPrice'],199)
    def test_login_logout_and_rate_limit(self):
        self.setup_owner()
        for i in range(10):self.assertEqual(self.employee.post('/api/login',json={'email':'nobody@example.test','password':'bad'},headers=ORIGIN).status_code,401)
        self.assertEqual(self.employee.post('/api/login',json={'email':'nobody@example.test','password':'bad'},headers=ORIGIN).status_code,429)
        self.assertEqual(self.owner.post('/api/logout',json={},headers=self.csrf).status_code,200)
        self.assertEqual(self.owner.get('/api/session').status_code,401)
    def test_persistence_across_new_clients_three_rounds(self):
        self.setup_owner()
        for n in range(1,4):
            current=self.owner.get('/api/workspace').json();current['state']['settings']['poReference']='PO-'+str(n)
            self.assertEqual(self.put(self.owner,current['state'],current['version'],self.csrf).status_code,200)
            mod.initialize() # simulated service restart, data must not be replaced
            fresh=TestClient(mod.app,base_url='http://localhost:8000')
            self.assertEqual(fresh.post('/api/login',json={'email':'owner@example.test','password':self.password},headers=ORIGIN).status_code,200)
            self.assertEqual(fresh.get('/api/workspace').json()['state']['settings']['poReference'],'PO-'+str(n))

    def requisition(self):
        state=mod.default_state();p=mod.CATALOG[0];src=p['sources'][0]
        row=dict(id='test-line',source=src['id'],qty=2,unit='piece',unitPrice=199,currency='THB',model='',size='',colour='',pack='',note='',priceKind='reference')
        state['orders']=[dict(id='test-requisition',number='CL-test',batchId='test',createdAt='2026-10-20',updatedAt='2026-10-20',kind='requisition',status='pending_verification',supplier=src['supplier'],channel=src['channel'],url=src['url'],contact=src['contact'],settings=copy.deepcopy(state['settings']),lines=[dict(product=p,row=row,source=src,info={})],verification=dict(lines={'test-line':dict(availableQty=None,finalPrice=None)},shippingCost=None,deliveryTime='',minimumOrder=None,invoiceConfirmed=False,invoiceType='unknown',paymentTerms='',supplierConfirmed=False,verifiedWith='',notes=''))]
        return state
    def complete_verification(self,state):
        state['orders'][0]['verification']=dict(lines={'test-line':dict(availableQty=2,finalPrice=180)},shippingCost=0,deliveryTime='2 days to 84280',minimumOrder=0,invoiceConfirmed=True,invoiceType='receipt',paymentTerms='COD',supplierConfirmed=True,verifiedWith='Synthetic supplier call',notes='Test only')
    def test_requisition_two_users_complete_workflow(self):
        self.setup_owner();self.add_employee();state=self.requisition()
        self.assertEqual(self.put(self.employee,state,0,self.employee_csrf).status_code,403)
        premature=copy.deepcopy(state);self.complete_verification(premature);premature['orders'][0]['status']='ready_for_approval'
        self.assertEqual(self.put(self.owner,premature,0,self.csrf).status_code,422)
        self.assertEqual(self.put(self.owner,state,0,self.csrf).status_code,200)
        work=self.employee.get('/api/workspace').json()['state']
        work['orders'][0]['status']='ready_for_approval'
        self.assertEqual(self.put(self.employee,work,1,self.employee_csrf).status_code,422)
        work['orders'][0]['status']='pending_verification';self.complete_verification(work)
        self.assertEqual(self.put(self.employee,work,1,self.employee_csrf).status_code,200)
        tampered=copy.deepcopy(work);tampered['orders'][0]['lines'][0]['row']['unitPrice']=180
        self.assertEqual(self.put(self.employee,tampered,2,self.employee_csrf).status_code,422)
        work['orders'][0]['status']='ready_for_approval'
        rid=uuid.uuid4().hex
        self.assertEqual(self.put(self.employee,work,2,self.employee_csrf,rid).status_code,200)
        self.assertEqual(self.put(self.employee,work,2,self.employee_csrf,rid).json()['version'],3)
        self.assertEqual(self.put(self.owner,work,2,self.csrf).status_code,409)
        final=copy.deepcopy(work);final['orders'][0]['status']='approved_to_order'
        self.assertEqual(self.put(self.employee,final,3,self.employee_csrf).status_code,403)
        self.assertEqual(self.put(self.owner,final,3,self.csrf).status_code,200)
        final['orders'][0]['verification']['shippingCost']=20
        self.assertEqual(self.put(self.owner,final,4,self.csrf).status_code,422)
        for _ in range(3):
            mod.initialize()
            saved=self.employee.get('/api/workspace').json()['state']['orders'][0]
            self.assertEqual(saved['status'],'approved_to_order')
            self.assertEqual(saved['lines'][0]['row']['unitPrice'],199)
            self.assertEqual(saved['verification']['lines']['test-line']['finalPrice'],180)
    def test_requisition_required_fields_and_return_for_revision(self):
        self.setup_owner();self.add_employee();state=self.requisition();self.complete_verification(state)
        self.assertEqual(self.put(self.owner,state,0,self.csrf).status_code,200)
        for key,value in [('invoiceConfirmed',False),('supplierConfirmed',False),('shippingCost',None),('shippingCost',-1),('deliveryTime',' '),('minimumOrder',None),('minimumOrder',9999),('paymentTerms',''),('verifiedWith',''),('invoiceType','unknown')]:
            bad=copy.deepcopy(state);bad['orders'][0]['status']='ready_for_approval';bad['orders'][0]['verification'][key]=value
            self.assertEqual(self.put(self.employee,bad,1,self.employee_csrf).status_code,422,(key,value))
        for key,value in [('availableQty',1),('availableQty',2.5),('finalPrice',None),('finalPrice',-1)]:
            bad=copy.deepcopy(state);bad['orders'][0]['status']='ready_for_approval';bad['orders'][0]['verification']['lines']['test-line'][key]=value
            self.assertEqual(self.put(self.employee,bad,1,self.employee_csrf).status_code,422,(key,value))
        bad=copy.deepcopy(state);bad['orders'][0]['status']='approved_to_order'
        self.assertEqual(self.put(self.owner,bad,1,self.csrf).status_code,403)
        state['orders'][0]['status']='ready_for_approval'
        self.assertEqual(self.put(self.employee,state,1,self.employee_csrf).status_code,200)
        state['orders'][0]['status']='pending_verification'
        self.assertEqual(self.put(self.employee,state,2,self.employee_csrf).status_code,403)
        self.assertEqual(self.put(self.owner,state,2,self.csrf).status_code,200)
        state['orders'][0]['verification']['notes']='Rechecked'
        self.assertEqual(self.put(self.employee,state,3,self.employee_csrf).status_code,200)

if __name__=='__main__':unittest.main(verbosity=2)
