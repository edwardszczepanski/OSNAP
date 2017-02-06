from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sys, psycopg2
from datetime import datetime

app = Flask(__name__)

@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
    val = None
    if request.method == 'POST':
        if 'facility_name' in request.form:
            session['facility_name'] = request.form['facility_name']
            session['facility_date'] = request.form['facility_date']
            session['facility_inventory'] = True;
        elif 'in_transit' in request.form:
            session['facility_date'] = request.form['in_transit']
            session['facility_inventory'] = False;
        return redirect(url_for('reports'))
    return render_template('report_filter.html')

@app.route('/reports')
def reports():
    sql_query = sql_query_generator()
    connect()
    cursor.execute(sql_query)
    res = cursor.fetchall()
    processed_data = []
    for r in res:
        item = {}
        item['fcode'] = r[0]
        item['asset_tag'] = r[1]
        item['src_facility'] = r[2]
        item['dest_facility'] = r[3]
        item['arrive_date'] = r[4]
        item['depart_date'] = r[5]
        item['expunge_date'] = r[6]
        processed_data.append(item)
    session['processed_data_session_name'] = processed_data

    return render_template('reports.html')

def sql_query_generator():
    sql_query = "SELECT * FROM assets"
    if session['facility_inventory']:
        facility_defined = False
        if session['facility_name'] != "*":
            sql_query += " WHERE fcode='" + session['facility_name'] + "'"
            facility_defined = True
        if not session['facility_date'] == "":
            dt = str(datetime.strptime(session['facility_date'], "%Y-%m-%d"))
            if facility_defined:
                sql_query += " AND "
            else:
                sql_query += " WHERE "
            sql_query += "('" + dt + "') >= depart_date"
    else:
        if not session['facility_date'] == "":
            dt = str(datetime.strptime(session['facility_date'], "%Y-%m-%d"))
            sql_query += " WHERE ('" + dt + "') >= arrive_date"
            sql_query += " AND ('" + dt + "') <= depart_date"
    sql_query += ";"
    return sql_query

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('logout.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if False and request.form['username'] != 'USERNAME': #!= app.config['USERNAME']:
            error = 'Invalid username'
        elif False and request.form['password'] != 'PASSWORD': #app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            flash('Welcome ' + session['username'] + '!')
            return redirect(url_for('report_filter'))
    return render_template('login.html', error=error)

def connect():
    global cursor
    global conn
    connection_string = "host='localhost' port='" + "5432" + "' dbname='" + db_name + "' user='osnapdev' password='secret'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    work_mem = 2048
    cursor.execute('SET work_mem TO ' + str(work_mem))
    print("Connected to server")

if __name__ == '__main__':
    global db_name
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    else:
        db_name = "lost"
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
