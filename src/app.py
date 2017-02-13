from flask import Flask, render_template, request
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2
import datetime

app = Flask(__name__)

@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/list_products', methods=('POST',))
def list_products():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    else:
        redirect('rest')
    
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    
    if len(req['compartments'])==0:
        print("have not compartment")
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from products p
left join security_tags t on p.product_pk=t.product_fk
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            SQLstart += " group by vendor,description"
            cur.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from security_tags t
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk
left join products p on t.product_fk=p.product_pk
where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cur.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    
    dbres = cur.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)
    
    # Prepare the response
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)
    
    conn.close()
    return data
    
@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/activate_user', methods=('POST',))
def activate_user():
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'

    try:
        cur.execute("INSERT INTO users (username) VALUES ('" + req['username'] + "');")
        conn.commit()
    except Exception as e:
        dat['result'] = 'FAIL'

    data = json.dumps(dat)
    conn.close()
    return data

@app.route('/rest/add_products', methods=('POST',))
def add_products():
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'

    try:
        cur.execute("INSERT INTO products (description, vendor) VALUEs ('" + "description" + "', 'vendor');")
        conn.commit()
    except Exception as e:
        dat['result'] = 'FAIL'

    data = json.dumps(dat)
    conn.close()
    return data

@app.route('/rest/add_asset', methods=('POST',))
def add_asset():
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'

    try:
        cur.execute("INSERT INTO assets (description) VALUES ('" + req['description'] + "');")
        conn.commit()
    except Exception as e:
        dat['result'] = 'FAIL'

    data = json.dumps(dat)
    conn.close()
    return data

@app.route('/rest/lost_key', methods=('POST',))
def lost_key():
    dat = dict()
    dat['timestamp'] = str(datetime.datetime.now())
    dat['result'] = 'OK'
    dat['key'] = 'bksaoudu......aoelchsauh'
    data = json.dumps(dat)
    return data
