from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sys, psycopg2

app = Flask(__name__)

@app.route('/report_filter')
def report_filter():
    return render_template('report_filter.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('logout.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'USERNAME':#!= app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != 'PASSWORD':#app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            flash('You were logged in')
            return redirect(url_for('report_filter'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True

    app.run(host='0.0.0.0', port=8080)
    #app.run(port=8080)
