from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sys, psycopg2

app = Flask(__name__)

@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
    val = None
    if request.method == 'POST':
        if 'facility_name' in request.form:
            session['facility_name'] = request.form['facility_name']
            return redirect(url_for('facility_inventory'))
        elif 'in_transit' in request.form:
            session['in_transit'] = request.form['in_transit']
            return redirect(url_for('in_transit'))
    return render_template('report_filter.html')

@app.route('/facility_inventory')
def facility_inventory():
    return session['facility_name']
    return render_template('facility_inventory.html')

@app.route('/in_transit')
def in_transit():
    return render_template('in_transit.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('login.html')

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

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

