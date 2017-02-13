import csv
import psycopg2
import sys
import datetime
import re
from pathlib import Path

def normalized_date(s):
    m = re.match(r'(\d+)/(\d+)/(\d+)',s)
    if m:
        month = int(m.group(1))
        day   = int(m.group(2))
        year  = int(m.group(3))
        if year < 100: 
            if year < 50:
                year += 2000
            else:
                year += 1900
        return datetime.datetime(year,month,day)

    m = re.match(r'(\d+)-(\w{3})-(\d+)',s)
    if m:
        day   = int(m.group(1))
        month = MONTH[m.group(2)]
        year  = int(m.group(3))
        if year < 100:
            if year < 50:
                year += 2000
            else:
                year += 1900
        return datetime.datetime(year,month,day)
    m = re.match(r'(\w{3})-(\d+)',s)
    if m:
        day   = int(m.group(2))
        month = MONTH[m.group(1)]
        now   = datetime.datetime.utcnow()
        ret   = datetime.datetime(now.year,month,day)
        if ret > now:
            ret = datetime.datetime(now.year-1,month,day)
        return ret

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cursor = conn.cursor()



def asset_upsert(asset_tag):
    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(asset_tag,))
    r = cursor.fetchone()
    if r:
        return r[0]
    cursor.execute("INSERT INTO assets (asset_tag) VALUES (%s)",(asset_tag,))
    cursor.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(asset_tag,))
    return cursor.fetchone()[0]

def ffind(fname):
    if fname=='MB 005':
        fname='Moonbase'
    if fname=='Los Alamous, NM':
        fname='Los Alamos, NM'
    if fname=='Las Alamos, NM':
        fname='Los Alamos, NM'
    if fname=='Washington, D.C.':
        fname='Washington, DC'

    cursor.execute("SELECT facility_pk FROM facilities WHERE common_name=%s",(fname,))
    r = cursor.fetchone()
    if r:
        return r[0]
#    raise Exception("Bad facility name %s"%fname)

#def convoy_upsert(req, src_pk, dst_pk, load_dt, unload_dt):
#    cursor.execute("SELECT convoy_pk FROM convoys WHERE request_id=%s",(req,))
#    r = cursor.fetchone()
#    if r:
#        return r[0]
#    cursor.execute("INSERT INTO convoys (request_id,src_fk,dst_fk,depart_dt,arrive_dt) VALUES (%s,%s,%s,%s,%s)",(req,src_pk,dst_pk,load_dt,unload_dt))
#    cursor.execute("SELECT convoy_pk FROM convoys WHERE request_id=%s",(req,))
#    return cursor.fetchone()[0]

#def on_insert(asset_pk,convoy_pk,load_dt,unload_dt):
#    cur.execute("SELECT count(*) FROM asset_on WHERE asset_fk=%s and convoy_fk=%s",(asset_pk,convoy_pk))
#    r = cur.fetchone()
#    if r[0] > 0:
#        raise Exception("Duplicated data?")
#    cur.execute("INSERT INTO asset_on (asset_fk,convoy_fk,load_dt,unload_dt) VALUES (%s,%s,%s,%s)",(asset_pk,convoy_pk,load_dt,unload_dt))

#def process_transit():
#    with open('/home/osnapdev/CIS322/sql/osnap_legacy/transit.csv') as f:
#        data = csv.DictReader(f)
#        for r in data:
#            asset_pk = asset_upsert(r['asset tag'])
#            src_pk = ffind(r['src facility'])
#            dst_pk = ffind(r['dst facility'])
#            load_dt = normalized_date(r['depart date'])
#            unload_dt = normalized_date(r['arrive date'])
#            convoy_pk = convoy_upsert(r['transport request #'],src_pk,dst_pk,load_dt,unload_dt)
#            on_insert(asset_pk,convoy_pk,load_dt,unload_dt)
#    conn.commit()




def process_file(fname):
    p = Path(fname)
    name = p.name
    m = re.match('([^_]+)_inventory.csv',name)
    if not m:
        return 
    with p.open() as f:
        f.readline()
        for line in f:
            line = line.strip()
            print("%s,%s"%(m.group(1),line))

def import_DC_inventory():
    with open('/home/osnapdev/CIS322/sql/osnap_legacy/DC_inventory.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            description = row['product']
            cursor.execute("INSERT INTO assets (asset_tag,description) VALUES (%s, %s)",(asset_tag,description,))
            conn.commit()
    return

def import_HQ_inventory():                                                                           
    with open('/home/osnapdev/CIS322/sql/osnap_legacy/HQ_inventory.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            description = row['product']
            cursor.execute("INSERT INTO assets (asset_tag,description) VALUES (%s, %s)",(asset_tag,description,))
            conn.commit()
    return

def import_NC_inventory():
    with open('/home/osnapdev/CIS322/sql/osnap_legacy/NC_inventory.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            description = row['product']
            cursor.execute("INSERT INTO assets (asset_tag,description) VALUES(%s,%s)",(asset_tag,description,))
            conn.commit()
    return 

def import_product_list():
    with open('/home/osnapdev/CIS322/sql/osnap_legacy/product_list.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vendor = row['vendor']
            description = row['description']
            cursor.execute("INSERT INTO products (vendor,description) VALUES(%s,%s)",(vendor,description,))
            conn.commit()
    return


def import_vendors():
    with open('/home/osnapdev/CIS322/sql/osnap_legacy/vendors.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vendor = row['vendor']
            cursor.execute("INSERT INTO products (vendor) VALUES (%s)",(vendor,))
            conn.commit()
    return



def main():
    import_DC_inventory()
    import_HQ_inventory()
    import_NC_inventory()
    import_product_list()
    import_vendors()


    for arg in sys.argv[1:]:
        process_file(arg)
#        process_transit()

if __name__ =='__main__':
    main()
