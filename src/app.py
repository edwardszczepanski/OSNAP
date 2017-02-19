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

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');"
        print(query)
        cur.execute(query)
        conn.commit()
    elif request.method == 'GET':
        if True:
            flash('Username already exists')
        else:
            flash('Username was successfully added')
    return render_template('create_user.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if False and request.form['username'] != 'USERNAME':
            error = 'Invalid username'
        elif False and request.form['password'] != 'PASSWORD':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            flash('Welcome ' + session['username'] + '!')
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

def connect():
    global cursor
    global conn
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()

if __name__ == '__main__':
    connect()
    app.debug = True
    app.run()
