from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sys, psycopg2, json
from datetime import datetime
from config import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
    return render_template('report_filter.html')
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
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    work_mem = 2048
    cursor.execute('SET work_mem TO ' + str(work_mem))
    print("Connected to server")

if __name__ == '__main__':
    connect()
    app.debug = True
    app.run()
