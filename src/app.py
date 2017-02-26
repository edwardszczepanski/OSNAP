from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sys, psycopg2, json
from datetime import datetime
from config import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('logout.html')

def check_duplicate(query, connection, cursor):
    cursor.execute(query)
    response = cursor.fetchall()
    if len(response) > 0:
        return True
    else:
        return False

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets;")
    res = cursor.fetchall()
    data = []
    for r in res:
        asset = {}
        asset['asset_pk'] = r[0]
        asset['facility_fk'] = r[1]
        asset['asset_tag'] = r[2]
        asset['description'] = r[3]
        asset['disposed'] = r[4]
        data.append(asset)
    session['assets'] = data

    cursor.execute("SELECT * FROM facilities;")
    res = cursor.fetchall()
    fac_data = []
    for r in res:
        fac = {}
        fac['fkey'] = r[0]
        fac['name'] = r[2]
        fac_data.append(fac)
    session['facilities'] = fac_data

    if request.method=='POST':
        facility = request.form['facility']
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        date = request.form['date']

        query = "SELECT * from assets WHERE asset_tag ='" + asset_tag + "';"

        if check_duplicate(query, conn, cursor):
            flash('Asset with the same asset tag already exists')
        else:
            query = "INSERT INTO assets (facility_fk, asset_tag, description, disposed) VALUES (" + facility + ", '" + asset_tag + "', '" + description + "', FALSE);"
            cursor.execute(query)
            conn.commit()
            query1 = "SELECT asset_pk from assets WHERE asset_tag='" + asset_tag + "';"
            cursor.execute(query1)
            res = cursor.fetchone()[0]
            dt = ''
            if date == '':
                str(datetime.now())
            else:
                dt = str(datetime.strptime(date, '%Y-%m-%d'))
            query2 = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (" + str(res) + "," + facility + ",'" + dt + "');"
            cursor.execute(query2)
            conn.commit()
            flash('Asset was successfully added')
    conn.close()
    return render_template('dispose_asset.html')
 
@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets;")
    res = cursor.fetchall()
    data = []
    for r in res:
        asset = {}
        asset['asset_pk'] = r[0]
        asset['facility_fk'] = r[1]
        asset['asset_tag'] = r[2]
        asset['description'] = r[3]
        asset['disposed'] = r[4]
        data.append(asset)
    session['assets'] = data

    cursor.execute("SELECT * FROM facilities;")
    res = cursor.fetchall()
    fac_data = []
    for r in res:
        fac = {}
        fac['fkey'] = r[0]
        fac['name'] = r[2]
        fac_data.append(fac)
    session['facilities'] = fac_data

    if request.method=='POST':
        facility = request.form['facility']
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        date = request.form['date']

        query = "SELECT * from assets WHERE asset_tag ='" + asset_tag + "';"

        if check_duplicate(query, conn, cursor):
            flash('Asset with the same asset tag already exists')
        else:
            query = "INSERT INTO assets (facility_fk, asset_tag, description, disposed) VALUES (" + facility + ", '" + asset_tag + "', '" + description + "', FALSE);"
            cursor.execute(query)
            conn.commit()
            query1 = "SELECT asset_pk from assets WHERE asset_tag='" + asset_tag + "';"
            cursor.execute(query1)
            res = cursor.fetchone()[0]
            dt = ''
            if date == '':
                str(datetime.now())
            else:
                dt = str(datetime.strptime(date, '%Y-%m-%d'))
            query2 = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (" + str(res) + "," + facility + ",'" + dt + "');"
            cursor.execute(query2)
            conn.commit()
            flash('Asset was successfully added')
    conn.close()
    return render_template('add_asset.html')

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facilities;")
    res = cursor.fetchall()
    data = []
    for r in res:
        facility = {}
        facility['fcode'] = r[1]
        facility['common_name'] = r[2]
        facility['location'] = r[3]
        data.append(facility)
    session['facilities'] = data

    if request.method=='POST':
        common = request.form['common']
        fcode = request.form['fcode']
        location = request.form['location']

        query1 = "SELECT * from facilities WHERE fcode ='" + fcode + "';"
        query2 = "SELECT * from facilities WHERE common_name ='" + common + "';"

        if check_duplicate(query1, conn, cursor) or check_duplicate(query2, conn, cursor):
            flash('Facility with the same common name or fcode already exists')
        else:
            query = "INSERT INTO facilities (common_name, fcode, location) VALUES ('" + common + "', '" + fcode + "', '" + location + "');"
            cursor.execute(query)
            conn.commit()
            flash('Facility was successfully added')
    conn.close()
    return render_template('add_facility.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        query = "SELECT * from users WHERE username ='" + username + "';"
        if check_duplicate(query, conn, cursor):
            flash('Username already exists')
        else:
            query = "INSERT INTO users (username, password, role_fk) VALUES ('" + username + "', '" + password + "', " + role + ");"
            cursor.execute(query)
            conn.commit()
            flash('Username was successfully added')
    conn.close()

    return render_template('create_user.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    error = None

    if request.method=='POST': 
        query = "SELECT password from users WHERE username ='" + request.form['username'] + "';"
        cursor.execute(query)
        response = cursor.fetchall()
        conn.close()
        if len(response) == 0:
            error = "Username doesn't exist"
        else:
            password_found = False
            for val in response:
                if val[0] == request.form['password']:
                    password_found = True
            if not password_found:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['username'] = request.form['username']
                session['password'] = request.form['password']
                flash('Welcome ' + session['username'] + '!')
                return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
