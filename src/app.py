from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sys, psycopg2, json
from datetime import datetime
from config import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = 'super secret key'
app.debug = True

@app.route('/activate_user', methods=('POST',))
def activate_user():
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cursor  = conn.cursor()
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    dat['input'] = req
    facilityOfficer = None
    roleVal = -1
    if req['role'] == "facofc":
        facilityOfficer = True
        roleVal = '1'
    elif req['role'] == "logofc":
        facilityOfficer = False
        roleVal = '2'
    else:
        dat['result'] = 'FAIL'

    if facilityOfficer != None:
        try:
            query = "SELECT * FROM users WHERE username='" + req['username'] + "';"
            cursor.execute(query)
            response = cursor.fetchall()
            if len(response) > 0:
                query = "UPDATE users SET password='" + req['password'] + "', role_fk="  + roleVal + ", active=TRUE WHERE username='" + req['username'] + "';"
                cursor.execute(query)
            elif facilityOfficer:
                query = "INSERT INTO users (username, password, role_fk) VALUES ('" + req['username'] + "', '" + req['password'] + "', 1);"
            else:
                query = "INSERT INTO users (username, password, role_fk) VALUES ('" + req['username'] + "', '" + req['password'] + "', 2);"
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            dat['result'] = 'FAIL'

    data = json.dumps(dat)
    conn.close()
    return data

@app.route('/revoke_user', methods=('POST',))
def revoke_user():
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cursor  = conn.cursor()
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    dat['input'] = req
    try:
        query = "SELECT * FROM users WHERE username='" + req['username'] + "';"
        dat['query1'] = query
        cursor.execute(query)
        response = cursor.fetchall()
        dat['do i make it'] = len(response)
        if len(response) > 0:
            dat['do i make it'] = "yes"
            query = "UPDATE users SET active=FALSE WHERE username='" + req['username'] + "';"
            dat['arst'] = query
            #query = "DELETE FROM users WHERE username='" + req['username'] + "';"
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        dat['result'] = 'FAIL'
    data = json.dumps(dat)
    return data

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['role'] = 0
    return render_template('logout.html')

def check_duplicate(query, connection, cursor):
    cursor.execute(query)
    response = cursor.fetchall()
    if len(response) > 0:
        return True
    else:
        return False

@app.route('/reports')
def reports():
    if not 'facility' in session or not 'date' in session:
        return redirect(url_for('asset_report'))
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    query = "SELECT * FROM assets a JOIN asset_at aa ON asset_pk=asset_fk INNER JOIN facilities ON facility_fk=facility_pk WHERE facilities.common_name LIKE '%"+str(session['facility'])+"%' AND '"+str(session['date'])+"' >= aa.arrive_dt;"
    cursor.execute(query)
    res = cursor.fetchall()
    processed_data = []
    for r in res:
        endDate = r[7]
        valid = False
        if endDate == None:
            valid = True
        else:
            if endDate >= session['date']:
                valid = True
        if valid:
            item = {}
            item['asset_tag'] = r[1]
            item['arrive_date'] = r[6]
            item['depart_date'] = endDate
            item['facility'] = r[10]
            item['description'] = r[2]
            processed_data.append(item)
    session['processed_data_session_name'] = processed_data
    conn.close()
    return render_template('reports.html')

@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
    if request.method == 'POST':
        if request.form['facility'] == '':
            session['facility'] = ""
        else:
            session['facility'] = str(request.form['facility'])
        if request.form['date'] == '':
            flash('Must input a date')
        else:
            session['date'] = datetime.strptime(request.form['date'], '%Y-%m-%d')
            return redirect(url_for('reports'))
    return render_template('asset_report.html')

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    if not 'logged_in' in session:
        flash("You must be logged in to dispose assets")
        return redirect(url_for('login'))
    if session['logged_in'] == False:
        flash("You must be logged in to dispose assets")
        return redirect(url_for('login'))
    elif session['role'] != 2:
        flash("You must be a logistics officer to dispose assets")
        return redirect(url_for('login'))

    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()

    if request.method=='POST':
        asset_tag = request.form['asset_tag']
        date = request.form['date']
        query = "SELECT * FROM assets WHERE asset_tag ='" + asset_tag + "';"
        
        if not check_duplicate(query, conn, cursor):
            flash('No asset exists with that asset tag')
        else:
            cursor.execute(query)
            response = cursor.fetchall()
            if response[0][3]:
                flash("That asset has already been disposed")
            else:
                query = "UPDATE assets SET disposed=TRUE WHERE asset_tag = '" + asset_tag + "';"
                cursor.execute(query)
                conn.commit()
                query1 = "SELECT asset_pk from assets WHERE asset_tag='" + asset_tag + "';"
                cursor.execute(query1)
                res = cursor.fetchone()[0]
                dt = ''
                if date == '' or date == None:
                    dt = str(datetime.now())
                else:
                    dt = str(datetime.strptime(date, '%Y-%m-%d'))
                query2 = "UPDATE asset_at SET depart_dt='" + dt + "' WHERE asset_fk=" + str(res) + ";"
                cursor.execute(query2)
                conn.commit()
                flash('Asset was successfully disposed')
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
        asset['asset_tag'] = r[1]
        asset['description'] = r[2]
        asset['disposed'] = r[3]
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
        if not 'facility' in request.form or not 'asset_tag' in request.form or not 'description' in request.form:
            flash("All values must be valid")
            return redirect(url_for("add_asset"))
        facility = request.form['facility']
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        date = request.form['date']

        query = "SELECT * from assets WHERE asset_tag ='" + asset_tag + "';"

        if check_duplicate(query, conn, cursor):
            flash('Asset with the same asset tag already exists')
        elif facility == "" or asset_tag == "" or description == "":
            flash('Fill out all values to add an asset')
        else:
            query = "INSERT INTO assets (asset_tag, description, disposed) VALUES ('" + asset_tag + "', '" + description + "', FALSE);"
            cursor.execute(query)
            conn.commit()
            query1 = "SELECT asset_pk from assets WHERE asset_tag='" + asset_tag + "';"
            cursor.execute(query1)
            res = cursor.fetchone()[0]
            dt = ''
            if date == '':
                dt = str(datetime.now())
            else:
                dt = str(datetime.strptime(date, '%Y-%m-%d'))
            query2 = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (" + str(res) + "," + facility + ",'" + dt + "');"
            cursor.execute(query2)
            conn.commit()
            flash('Asset was successfully added')
            return redirect(url_for('dashboard'))
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
        elif common == "" or fcode == "" or location == "":
            flash('Fill out all values to add a facility')
        else:
            query = "INSERT INTO facilities (common_name, fcode, location) VALUES ('" + common + "', '" + fcode + "', '" + location + "');"
            cursor.execute(query)
            conn.commit()
            flash('Facility was successfully added')
            return redirect(url_for('dashboard'))
    conn.close()
    return render_template('add_facility.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    if session['role'] == 1: # Facility Officers
        query = "SELECT * FROM requests WHERE approved=FALSE;"
        cursor.execute(query)
        res = cursor.fetchall()
        requests = []
        for r in res:
            dict = {}
            dict['request_pk'] = r[0]
            dict['asset_fk'] = r[1]
            dict['user_fk'] = r[2]
            dict['src_fac'] = r[3]
            dict['dest_fac'] = r[4]
            requests.append(dict)
        session['requests'] = requests
        if request.method == 'POST':
            if 'myRequest' not in request.form:
                flash("Please have a request selected to approve or reject")
            else:
                if 'approveButton' in request.form:
                    dt = str(datetime.now())
                    query = "UPDATE requests SET approve_user_fk=" + str(session['user_pk']) + ", approved=TRUE" + ", approve_dt='" + dt + "' WHERE request_pk = " + str(request.form['myRequest']) + ";"
                    cursor.execute(query)
                    conn.commit()
                    flash("Request was successfully approved")
                    return redirect(url_for('dashboard'))
                elif 'rejectButton' in request.form:
                    query = "DELETE FROM requests WHERE request_pk=" + str(request.form['myRequest']) + ";"
                    cursor.execute(query)
                    conn.commit()
                    flash("Request was successfully rejected")
                    return redirect(url_for('dashboard'))
    elif session['role'] == 2:
        cursor.execute("SELECT * FROM requests WHERE approved=TRUE;")
        res = cursor.fetchall()
        requests = []
        for r in res:
            dict = {}
            dict['request_pk'] = r[0]
            dict['asset_fk'] = r[1]
            dict['user_fk'] = r[2]
            dict['src_fac'] = r[3]
            dict['dest_fac'] = r[4]
            requests.append(dict)
        session['requests'] = requests
        if request.method == 'POST':
            if 'myRequest' not in request.form or request.form['load'] == "" or request.form['unload'] == "":
                flash("Please include both dates and select an entry")
            else:
                if datetime.strptime(request.form['load'], '%Y-%m-%d') > datetime.strptime(request.form['unload'], '%Y-%m-%d'):
                    flash("Load date must come before the unload date")
                    return redirect(url_for('dashboard'))

                load = str(datetime.strptime(request.form['load'], '%Y-%m-%d'))
                unload = str(datetime.strptime(request.form['unload'], '%Y-%m-%d'))
                query = "INSERT INTO in_transit (request_fk, load_dt, unload_dt) VALUES (" + str(request.form['myRequest']) + ",'" + load + "','" + unload + "');"
                cursor.execute(query)
                query = "UPDATE requests SET approved=FALSE WHERE request_pk = '" + str(request.form['myRequest']) + "';"
                cursor.execute(query)
                conn.commit()
                flash("Successfully updated the transit information")
                return redirect(url_for('dashboard'))
                    
    conn.close()
    return render_template('dashboard.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    error = None

    if request.method=='POST': 
        query = "SELECT password FROM users WHERE username ='" + request.form['username'] + "';"
        cursor.execute(query)
        response = cursor.fetchall()
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
                query = "SELECT active FROM users where username='" + request.form['username'] + "';"
                cursor.execute(query)
                response = cursor.fetchone()
                if not response[0]:
                    error = 'Account is not activated'
                else:
                    query = "SELECT role_fk FROM users where username='" + request.form['username'] + "';"
                    cursor.execute(query)
                    response = cursor.fetchone()
                    session['role'] = response[0]
                    query2 = "SELECT user_pk FROM users where username='" + request.form['username'] + "';"
                    cursor.execute(query2)
                    response = cursor.fetchone()
                    session['user_pk'] = response[0]
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    session['password'] = request.form['password']
                    flash('Welcome ' + session['username'] + '!')
                    conn.close()
                    return redirect(url_for('dashboard'))
    conn.close()
    return render_template('login.html', error=error)

@app.route('/approve_req', methods=['GET', 'POST'])
def approve_req():
    if not 'logged_in' in session:
        flash("You must be logged in to approve requests")
        return redirect(url_for('login'))
    elif session['logged_in'] == False:
        flash("You must be logged in to approve requests")
        return redirect(url_for('login'))
    elif session['role'] != 1:
        flash("You must be a facilities officer to approve requests")
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/update_transit', methods=['GET', 'POST'])
def update_transit():
    if not 'logged_in' in session:
        flash("You must be logged in to update transit")
        return redirect(url_for('login'))
    elif session['logged_in'] == False:
        flash("You must be logged in to update transit")
        return redirect(url_for('login'))
    elif session['role'] != 3:
        flash("You must be a logistics officer to update transit")
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
    if not 'logged_in' in session:
        flash("You must be logged in to initiate transfers")
        return redirect(url_for('login'))
    elif session['logged_in'] == False:
        flash("You must be logged in to initiate transfers")
        return redirect(url_for('login'))
    elif session['role'] != 2:
        flash("You must be a logistics officer to initiate transfers")
        return redirect(url_for('login'))

    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM facilities;")
    res = cursor.fetchall()
    fac_data = []
    for r in res:
        fac = {}
        fac['fkey'] = r[0]
        fac['name'] = r[2]
        fac_data.append(fac)
    session['facilities'] = fac_data

    cursor.execute("SELECT * FROM assets WHERE disposed=FALSE;")
    res = cursor.fetchall()
    fac_data = []
    for r in res:
        fac = {}
        fac['asset_fk'] = r[0]
        fac['asset_tag'] = r[1]
        fac_data.append(fac)
    session['asset_tag'] = fac_data

    if request.method=='POST':
        if not 'asset_tag' in request.form or not 'src_facility' in request.form or not 'dest_facility' in request.form:
            flash("All values must be valid")
            return redirect(url_for('transfer_req'))

        asset_tag = str(request.form['asset_tag'])
        src_facility = str(request.form['src_facility'])
        dest_facility = str(request.form['dest_facility'])
        dt = str(datetime.now())

        if src_facility == dest_facility:
            flash("Ensure that the source and destination facilities are different")
            return redirect(url_for('transfer_req'))

        query = "INSERT INTO requests (asset_fk, user_fk, src_fk, dest_fk, request_dt, approved) VALUES (" +  asset_tag + "," + str(session['user_pk']) + "," + src_facility + "," + dest_facility + ",'" + dt + "', FALSE" + ");"
        cursor.execute(query)
        conn.commit()
        flash("Transfer request was successfully submitted")
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('transfer_req.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
