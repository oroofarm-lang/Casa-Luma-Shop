"""Private single-company purchasing workspace. No anonymous access to shop or API."""
from __future__ import annotations
import hashlib, hmac, html, json, os, re, secrets, sqlite3, threading, time, uuid
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlsplit
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

ROOT=Path(__file__).resolve().parent.parent
PRODUCTION=os.getenv('APP_ENV')=='production'
DATABASE_URL=os.getenv('DATABASE_URL','')
SQLITE_PATH=os.getenv('SQLITE_PATH',str(ROOT/'private-data'/'workspace.sqlite3'))
APP_ORIGIN=os.getenv('APP_ORIGIN') or os.getenv('RENDER_EXTERNAL_URL','http://localhost:8000')
APP_ORIGIN=APP_ORIGIN.rstrip('/')
SETUP_TOKEN=os.getenv('SETUP_TOKEN','')
COOKIE='__Host-casa_session' if PRODUCTION else 'casa_session'
SESSION_SECONDS=7*86400
PASSWORDS=PasswordHasher(time_cost=3,memory_cost=65536,parallelism=1)
HASH_LIMIT=threading.Semaphore(2)
app=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
CATALOG=json.loads((ROOT/'research/catalog-data.json').read_text())['products']
PRODUCTS={p['id']:p for p in CATALOG}

class DB:
    def __init__(self):
        if DATABASE_URL:
            import psycopg
            from psycopg.rows import dict_row
            self.conn=psycopg.connect(DATABASE_URL,row_factory=dict_row,connect_timeout=10)
            self.pg=True
        else:
            if PRODUCTION:raise RuntimeError('Production requires durable DATABASE_URL; ephemeral SQLite is refused')
            Path(SQLITE_PATH).parent.mkdir(parents=True,exist_ok=True)
            self.conn=sqlite3.connect(SQLITE_PATH,timeout=20)
            self.conn.row_factory=sqlite3.Row
            self.conn.execute('PRAGMA foreign_keys=ON')
            self.pg=False
    def execute(self,sql,args=()):return self.conn.execute(sql.replace('?','%s') if self.pg else sql,args)
    def one(self,sql,args=()):
        row=self.execute(sql,args).fetchone()
        return dict(row) if row is not None else None
    def all(self,sql,args=()):return [dict(row) for row in self.execute(sql,args).fetchall()]
    def lock(self):
        if self.pg:self.execute('SELECT id FROM workspace WHERE id=1 FOR UPDATE')
        else:self.execute('BEGIN IMMEDIATE')
    def __enter__(self):return self
    def __exit__(self,t,v,tb):
        if t:self.conn.rollback()
        else:self.conn.commit()
        self.conn.close()

def default_state():return dict(version=2,updatedAt='',settings=dict(lang='he',messageLang='en',buyer='Casa Luma Shop',address='Koh Phangan, Surat Thani 84280, Thailand',contact='',neededBy='',notes='',deliveryMode='door',requestedInvoice='tax_invoice',poReference=''),items={},orders=[])

def initialize():
    with DB() as db:
        for sql in [
          'CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY,email TEXT NOT NULL UNIQUE,name TEXT NOT NULL,role TEXT NOT NULL,password_hash TEXT NOT NULL,active INTEGER NOT NULL DEFAULT 1,created_at BIGINT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS sessions (token_hash TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),csrf TEXT NOT NULL,expires_at BIGINT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS invitations (token_hash TEXT PRIMARY KEY,email TEXT NOT NULL,role TEXT NOT NULL,created_by TEXT NOT NULL REFERENCES users(id),expires_at BIGINT NOT NULL,used_at BIGINT)',
          'CREATE TABLE IF NOT EXISTS workspace (id INTEGER PRIMARY KEY,version INTEGER NOT NULL,data TEXT NOT NULL,updated_by TEXT,updated_at BIGINT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS workspace_revisions (version INTEGER PRIMARY KEY,data TEXT NOT NULL,actor TEXT NOT NULL,created_at BIGINT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS audit_events (id TEXT PRIMARY KEY,actor TEXT NOT NULL,action TEXT NOT NULL,created_at BIGINT NOT NULL,metadata TEXT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS workspace_requests (id TEXT PRIMARY KEY,actor TEXT NOT NULL,payload_hash TEXT NOT NULL,version INTEGER NOT NULL,created_at BIGINT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS rate_limits (bucket TEXT PRIMARY KEY,attempts INTEGER NOT NULL,window_start BIGINT NOT NULL)',
        ]:db.execute(sql)
        db.execute('INSERT INTO workspace(id,version,data,updated_at) VALUES(1,0,?,?) ON CONFLICT(id) DO NOTHING',(json.dumps(default_state()),int(time.time())))

@app.on_event('startup')
def startup():initialize()

def digest(token):return hashlib.sha256(token.encode()).hexdigest()
def audit(db,actor,action,metadata=None):db.execute('INSERT INTO audit_events VALUES(?,?,?,?,?)',(uuid.uuid4().hex,actor,action,int(time.time()),json.dumps(metadata or {})))
def require_origin(request):
    if request.headers.get('origin')!=APP_ORIGIN:raise HTTPException(403,'Untrusted request origin')
def user_for(request,csrf=False):
    token=request.cookies.get(COOKIE,'')
    with DB() as db:
        row=db.one('SELECT s.csrf,s.expires_at,u.id,u.email,u.name,u.role,u.active FROM sessions s JOIN users u ON s.user_id=u.id WHERE s.token_hash=?',(digest(token),)) if token else None
    if not row or row['expires_at']<int(time.time()) or not row['active']:raise HTTPException(401,'Sign in required')
    if csrf:
        require_origin(request)
        if not hmac.compare_digest(request.headers.get('x-csrf-token',''),row['csrf']):raise HTTPException(403,'CSRF token required')
    return row

def owner_for(request):
    user=user_for(request,csrf=request.method not in ['GET','HEAD'])
    if user['role']!='owner':raise HTTPException(403,'Owner permission required')
    return user

def rate_limit(key,limit=10):
    bucket=digest(key);now=int(time.time())
    with DB() as db:
        db.execute('INSERT INTO rate_limits(bucket,attempts,window_start) VALUES(?,0,?) ON CONFLICT(bucket) DO NOTHING',(bucket,now))
        db.execute('UPDATE rate_limits SET attempts=CASE WHEN window_start<? THEN 1 ELSE attempts+1 END,window_start=CASE WHEN window_start<? THEN ? ELSE window_start END WHERE bucket=?',(now-900,now-900,now,bucket))
        row=db.one('SELECT attempts FROM rate_limits WHERE bucket=?',(bucket,))
    if row['attempts']>limit:raise HTTPException(429,'Too many attempts; try again in 15 minutes')

def email_address(value):
    value=str(value or '').strip().lower()
    if len(value)>254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',value):raise HTTPException(422,'Valid email required')
    return value

def password_hash(value):
    if not isinstance(value,str) or len(value)<12 or len(value)>256:raise HTTPException(422,'Use a password of 12–256 characters')
    with HASH_LIMIT:return PASSWORDS.hash(value)

def session_response(user):
    token=secrets.token_urlsafe(32);csrf=secrets.token_urlsafe(32);expires=int(time.time())+SESSION_SECONDS
    with DB() as db:
        db.execute('DELETE FROM sessions WHERE expires_at<?',(int(time.time()),))
        db.execute('INSERT INTO sessions VALUES(?,?,?,?)',(digest(token),user['id'],csrf,expires))
    response=JSONResponse({'ok':True})
    response.set_cookie(COOKIE,token,httponly=True,secure=PRODUCTION,samesite='lax',max_age=SESSION_SECONDS,path='/')
    return response

@app.middleware('http')
async def security(request,call_next):
    if int(request.headers.get('content-length','0') or '0')>8_000_000:return JSONResponse({'detail':'Workspace too large'},status_code=413)
    response=await call_next(request)
    response.headers['Cache-Control']='no-store'
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='same-origin'
    response.headers['X-Frame-Options']='DENY'
    if PRODUCTION:response.headers['Strict-Transport-Security']='max-age=31536000'
    return response

def secured_html(page):
    nonce=secrets.token_urlsafe(20)
    page=page.replace('<script',f'<script nonce="{nonce}"').replace('<style',f'<style nonce="{nonce}"')
    response=HTMLResponse(page)
    response.headers['Content-Security-Policy']=f"default-src 'self'; script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'; img-src 'self' https: data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
    return response

@app.get('/healthz')
def health():
    with DB() as db:db.one('SELECT version FROM workspace WHERE id=1')
    return {'ok':True}

@app.get('/login')
@app.get('/setup')
@app.get('/join')
def auth_page():return secured_html((ROOT/'server/auth.html').read_text())

@app.get('/')
def shop(request:Request):
    try:user=user_for(request)
    except HTTPException:return RedirectResponse('/login',status_code=303)
    with DB() as db:row=db.one('SELECT version,data FROM workspace WHERE id=1')
    page=(ROOT/'docs/index.html').read_text()
    page=page.replace('<html ',f'<html data-hosted="true" data-revision="{row["version"]}" data-role="{user["role"]}" data-csrf="{user["csrf"]}" ')
    page=page.replace('<script id="initial-state" type="application/json">null</script>','<script id="initial-state" type="application/json">'+row['data'].replace('<','\\u003c')+'</script>')
    return secured_html(page)

@app.get('/{filename}')
def companion(filename:str,request:Request):
    user_for(request)
    if filename not in ['Ordering-Guide.md','Casa-Luma-Sourcing-Research-2026-10-18.md']:raise HTTPException(404)
    return Response((ROOT/'docs'/filename).read_text(),media_type='text/plain; charset=utf-8')

@app.get('/api/session')
def session(request:Request):
    u=user_for(request)
    return {'email':u['email'],'name':u['name'],'role':u['role'],'csrf':u['csrf']}

@app.post('/api/setup')
def setup(request:Request,body:dict):
    require_origin(request);rate_limit('setup:'+str(request.client.host))
    if not SETUP_TOKEN or not hmac.compare_digest(str(body.get('setupToken','')),SETUP_TOKEN):raise HTTPException(403,'Invalid setup token')
    email=email_address(body.get('email'));hashed=password_hash(body.get('password'));uid=uuid.uuid4().hex
    with DB() as db:
        db.lock()
        if db.one('SELECT id FROM users LIMIT 1'):raise HTTPException(409,'Initial setup already completed')
        db.execute('INSERT INTO users(id,email,name,role,password_hash,created_at) VALUES(?,?,?,?,?,?)',(uid,email,str(body.get('name','Owner'))[:200],'owner',hashed,int(time.time())))
        audit(db,uid,'owner_setup')
    return session_response({'id':uid})

@app.post('/api/login')
def login(request:Request,body:dict):
    require_origin(request);email=email_address(body.get('email'));rate_limit('login:'+email)
    with DB() as db:user=db.one('SELECT * FROM users WHERE email=?',(email,))
    valid=False
    # A dummy hash keeps unknown-user verification on the same expensive path.
    hashed=user['password_hash'] if user else DUMMY_HASH
    try:
        with HASH_LIMIT:valid=PASSWORDS.verify(hashed,str(body.get('password',''))[:257])
    except (VerifyMismatchError,InvalidHashError):pass
    if not user or not user['active'] or not valid:raise HTTPException(401,'Email or password incorrect')
    with DB() as db:audit(db,user['id'],'login')
    return session_response(user)

DUMMY_HASH=PASSWORDS.hash(secrets.token_urlsafe(24))

@app.post('/api/logout')
def logout(request:Request):
    user_for(request,csrf=True)
    with DB() as db:db.execute('DELETE FROM sessions WHERE token_hash=?',(digest(request.cookies.get(COOKIE,'')),))
    r=JSONResponse({'ok':True});r.delete_cookie(COOKIE,path='/');return r

@app.get('/api/workspace')
def workspace(request:Request):
    user_for(request)
    with DB() as db:row=db.one('SELECT version,data,updated_at FROM workspace WHERE id=1')
    if request.headers.get('if-none-match')==str(row['version']):return Response(status_code=304)
    return {'version':row['version'],'state':json.loads(row['data']),'updatedAt':row['updated_at']}

def validate_state(state):
    if not isinstance(state,dict) or state.get('version')!=2 or not isinstance(state.get('items'),dict) or not isinstance(state.get('orders',[]),list):raise HTTPException(422,'Invalid workspace format')
    if len(state['items'])>len(PRODUCTS)+20 or len(state.get('orders',[]))>2000:raise HTTPException(422,'Workspace limit exceeded')
    if not isinstance(state.get('settings'),dict) or any(not isinstance(v,str) or len(v)>2000 for v in state['settings'].values()):raise HTTPException(422,'Invalid buyer settings')
    def row_check(row,known=True,product=None):
        if not isinstance(row,dict) or not isinstance(row.get('qty'),int) or isinstance(row['qty'],bool) or not 0<=row['qty']<=100000:raise HTTPException(422,'Invalid quantity')
        price=row.get('unitPrice')
        if row.get('currency')!='THB' or (price is not None and (isinstance(price,bool) or not isinstance(price,(int,float)) or not 0<=price<=1_000_000_000)):raise HTTPException(422,'THB prices only')
        if row.get('unit') not in ['piece','set','pack','box','carton','kg']:raise HTTPException(422,'Invalid unit')
        if known and row.get('source') not in [s['id'] for s in product['sources']]:raise HTTPException(422,'Unknown purchasing channel')
        for key in ['model','size','colour','pack','note']:
            if not isinstance(row.get(key,''),str) or len(row.get(key,''))>2000:raise HTTPException(422,'Invalid line details')
    for pid,item in state['items'].items():
        if pid not in PRODUCTS or not isinstance(item,dict) or not isinstance(item.get('lines',[]),list) or len(item.get('lines',[]))>200:raise HTTPException(422,'Invalid product')
        for row in item.get('lines',[]):row_check(row,product=PRODUCTS[pid])
        if item.get('draft'):row_check(item['draft'],product=PRODUCTS[pid])
    ids=set()
    for order in state.get('orders',[]):
        if not isinstance(order,dict) or not isinstance(order.get('id'),str) or order['id'] in ids or not isinstance(order.get('lines'),list) or len(order['lines'])>1000:raise HTTPException(422,'Invalid saved order')
        ids.add(order['id'])
        if order.get('status') not in ['prepared','sent','confirmed','ordered','received','cancelled'] or order.get('kind') not in ['order','quote']:raise HTTPException(422,'Invalid order status')
        for line in order['lines']:
            if not isinstance(line,dict) or not isinstance(line.get('row'),dict) or not isinstance(line.get('product'),dict) or not isinstance(line.get('source'),dict):raise HTTPException(422,'Invalid saved line')
            row_check(line['row'],known=False)
    # Reject JSON NaN/Infinity, oversized strings and dangerous unbounded nesting.
    encoded=json.dumps(state,ensure_ascii=False,allow_nan=False)
    if len(encoded.encode())>7_000_000:raise HTTPException(413,'Export/archive older orders before adding more data')
    return encoded

@app.put('/api/workspace')
def save_workspace(request:Request,body:dict):
    user=user_for(request,csrf=True);state=body.get('state');encoded=validate_state(state);request_id=body.get('requestId','')
    if not isinstance(request_id,str) or not re.fullmatch(r'[a-zA-Z0-9_-]{12,100}',request_id):raise HTTPException(422,'Unique save request ID required')
    fingerprint=digest(encoded)
    if not isinstance(body.get('version'),int):raise HTTPException(422,'Version required')
    with DB() as db:
        db.lock();completed=db.one('SELECT actor,payload_hash,version FROM workspace_requests WHERE id=?',(request_id,))
        if completed:
            if completed['actor']!=user['id'] or completed['payload_hash']!=fingerprint:raise HTTPException(409,'Save request ID was already used')
            return {'version':completed['version']}
        old=db.one('SELECT version,data FROM workspace WHERE id=1')
        if old['version']!=body['version']:raise HTTPException(409,'A teammate saved newer changes. Back up your edits and reload.')
        previous=json.loads(old['data']);new_orders={o['id']:o for o in state.get('orders',[])}
        for o in previous.get('orders',[]):
            newer=new_orders.get(o['id'])
            if not newer or {k:v for k,v in newer.items() if k not in ['status','updatedAt']}!={k:v for k,v in o.items() if k not in ['status','updatedAt']}:raise HTTPException(422,'Saved order contents are immutable; cancel or repeat the order instead')
        version=old['version']+1
        db.execute('UPDATE workspace SET version=?,data=?,updated_by=?,updated_at=? WHERE id=1',(version,encoded,user['id'],int(time.time())))
        db.execute('INSERT INTO workspace_revisions VALUES(?,?,?,?)',(version,encoded,user['id'],int(time.time())))
        db.execute('DELETE FROM workspace_revisions WHERE version<?',(version-20,))
        db.execute('INSERT INTO workspace_requests VALUES(?,?,?,?,?)',(request_id,user['id'],fingerprint,version,int(time.time())))
        db.execute('DELETE FROM workspace_requests WHERE created_at<?',(int(time.time())-7*86400,))
        audit(db,user['id'],'workspace_saved',{'revision':version,'orders':len(state.get('orders',[]))})
    return {'version':version}

@app.get('/api/admin/users')
def users(request:Request):
    owner_for(request)
    with DB() as db:return {'users':db.all('SELECT id,email,name,role,active FROM users ORDER BY created_at')}

@app.post('/api/admin/invitations')
def invite(request:Request,body:dict):
    user=owner_for(request);email=email_address(body.get('email'));token=secrets.token_urlsafe(32)
    with DB() as db:
        if db.one('SELECT id FROM users WHERE email=?',(email,)):raise HTTPException(409,'This employee already has an account')
        db.execute('INSERT INTO invitations VALUES(?,?,?,?,?,NULL)',(digest(token),email,'employee',user['id'],int(time.time())+86400))
        audit(db,user['id'],'employee_invited',{'email':email})
    return {'url':APP_ORIGIN+'/join#'+token,'expiresInHours':24}

@app.post('/api/join')
def join(request:Request,body:dict):
    require_origin(request);rate_limit('join:'+str(request.client.host));token=str(body.get('token',''));hashed=password_hash(body.get('password'));uid=uuid.uuid4().hex
    with DB() as db:
        db.lock();invitation=db.one('SELECT * FROM invitations WHERE token_hash=?',(digest(token),))
        if not invitation or invitation['used_at'] or invitation['expires_at']<int(time.time()):raise HTTPException(403,'Invitation invalid or expired')
        if db.one('SELECT id FROM users WHERE email=?',(invitation['email'],)):raise HTTPException(409,'Account already exists')
        db.execute('INSERT INTO users(id,email,name,role,password_hash,created_at) VALUES(?,?,?,?,?,?)',(uid,invitation['email'],str(body.get('name','Employee'))[:200],'employee',hashed,int(time.time())))
        db.execute('UPDATE invitations SET used_at=? WHERE token_hash=?',(int(time.time()),digest(token)))
        audit(db,uid,'employee_joined')
    return session_response({'id':uid})

@app.post('/api/admin/users/{uid}/disable')
def disable(uid:str,request:Request):
    user=owner_for(request)
    if uid==user['id']:raise HTTPException(422,'Cannot disable your own owner account')
    with DB() as db:
        target=db.one('SELECT role FROM users WHERE id=?',(uid,))
        if not target or target['role']=='owner':raise HTTPException(422,'Employee account required')
        db.execute('UPDATE users SET active=0 WHERE id=?',(uid,));db.execute('DELETE FROM sessions WHERE user_id=?',(uid,));audit(db,user['id'],'employee_disabled',{'userId':uid})
    return {'ok':True}
