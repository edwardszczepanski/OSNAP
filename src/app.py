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


@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cursor = conn.cursor()
    if request.method=='POST':
        common = request.form['common']
        fcode = request.form['fcode']
        location = request.form['location']

        duplicate = False
        query1 = "SELECT * from facilities WHERE fcode ='" + fcode + "';"
        query2 = "SELECT * from facilities WHERE common_name ='" + common + "';"

        if check_duplicate(query1, conn, cursor) or check_duplicate(query2, conn, cursor):
            flash('Username already exists')
        else:
            query = "INSERT INTO users (username, password, role_fk) VALUES ('" + username + "', '" + password + "', " + role + ");"
            cursor.execute(query)
            conn.commit()
            flash('Username was successfully added')
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
