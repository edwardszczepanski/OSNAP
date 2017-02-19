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
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
        username = req['username']
        password = req['password']
        query = "SELECT user_pk from users WHERE username ='" + username + "';"
        cursor.execute(query)
        response = cursor.fetchall()
        if len(response) > 0:
            flash('Username already exists')
        else:
            query = "INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');"
            cursor.execute(query)
            conn.commit()
            flash('Username was successfully added')
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            query = "INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');"
            cursor.execute(query)
            conn.commit()

    return render_template('create_user.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        query = "SELECT password from users WHERE username ='" + request.form['username'] + "';"
        cursor.execute(query)
        response = cursor.fetchall()
        print(response)
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

def connect():
    global cursor
    global conn
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()

if __name__ == '__main__':
    connect()
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0', port=8080)
