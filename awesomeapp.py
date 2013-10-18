#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import wraps
from hashlib import md5
from pprint import pprint
from flask import Flask, request, flash, Response, session, g, redirect, url_for, abort, render_template
import MySQLdb
from AAR_config import AUTH_USERS, SECRET_KEY, CONNECTION_ARGS

silly_text = '''I'm terribly sorry. I've looked everywhere but I can't find that combination of credentials in my records. Perhaps you mistyped your password? Or maybe you simply don't have an account with us yet. I am sorry to be so thick. I'm a bad server, I know. I really wanted to be a refrigerator.'''

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')

def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is not None:
            return f(*args, **kwargs)
        else:
            flash('Please log in first...', 'error')
            next_url = request.url
            login_url = '%s?next=%s' % (url_for('login'), next_url)
            return redirect(login_url)
    return decorated_function

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next = request.args.get('next')
    
    if request.method == 'POST':
        uname = request.form['username']
        upswd = request.form['password']
        authstr = uname + upswd
        authhash = md5(authstr).hexdigest()
        if authhash not in AUTH_USERS:
            error = silly_text
        else:
            session['logged_in'] = True
            session['username'] = uname
            session['role'] = AUTH_USERS[authhash]['role']
            
            if session['role'] == 'admin':
                return redirect(url_for('dispacher'))
            elif session['role'] == 'customer':
                return redirect(url_for('tempTest'))

    return render_template('login.html', error=error, session=session)

@app.route('/dispacher')
@logged_in
def dispacher():
    if session.get('role') == 'customer':
        return logout()
    else:
        db = MySQLdb.connect(**CONNECTION_ARGS)
        cur = db.cursor()
        cur.execute("select j.jid, c.cid, c.lname, j.make, j.appliance, j.job_status, j.appointment, j.description from jobs j, customer c where j.cid = c.cid")
        result = cur.fetchall()


        return render_template("dispacher.html",
            title = "Dispacher Interface",
            user = session['username'],
            reqenviron = request.environ,
            ses = session,
            result = result)

@app.route('/testTemplate')
@logged_in
def tempTest():
    session['objects'] = 42
    session.permanent = False
    
    return render_template("testTemplate.html",
        title = "Testing",
        user = session['username'],
        reqenviron = request.environ,
        ses = session)
        
    
##### Shut down the simple server from the browser address bar #####
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(port=9229)
    
### RANDOM JUNK TO GET RID OF ###

#                 if next:
#                     flash('redirected ' + uname + ' to next')
#                     return redirect(next)
#                 else: return redirect(url_for('tempTest'))

