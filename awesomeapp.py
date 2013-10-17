#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import wraps
from hashlib import md5
from pprint import pprint
from flask import Flask, request, flash, Response, session, g, redirect, url_for, abort, render_template
import MySQLdb
from AAR_config import AUTH_USERS, SECRET_KEY, CONNECTION_ARGS

silly_text = '''I'm terribly sorry. I've looked everywhere but I can't find that combination of credentials in my records. Perhaps you mistyped your password? Or maybe you simply don't have an account with us yet. I am sorry to be so thick. I'm a bad server, I know, but what can you do: these are the wages of unskilled labor.'''

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

<<<<<<< HEAD
@app.route('/logout')
def logout():
    if session.get('username') or session.get('logged_in') or session.pop('role'):
        session.pop('username')
        session.pop('role')
        session.pop('logged_in')
    return redirect(url_for('login'))

=======
>>>>>>> 772583266c240c1a7807c1c63495890180eb26b0
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
<<<<<<< HEAD
            session['logged_in'] = True
            session['username'] = uname
            session['role'] = AUTH_USERS[authhash]['role']
            
            if session['role'] == 'admin':
                return redirect(url_for('dispacher'))
            elif session['role'] == 'customer':
                return redirect(url_for('tempTest'))
=======
            session['username'] = uname
            session['logged_in'] = True
            role = AUTH_USERS[authhash]['role']
            
            if role == 'admin':
                return redirect(url_for('dispacher'))
            else:
                if next:
                    flash('redirected ' + uname + ' to next')
                    return redirect(next)
                else: return redirect(url_for('tempTest'))
>>>>>>> 772583266c240c1a7807c1c63495890180eb26b0

    return render_template('login.html', error=error, session=session)

@app.route('/dispacher')
@logged_in
def dispacher():
<<<<<<< HEAD
    if session.get('role') == 'customer':
        return logout()
    else:
        db = MySQLdb.connect(**CONNECTION_ARGS)
        cur = db.cursor()
        cur.execute("select * from pet where sex = 'f'")
        name, owner, type, sex, bdate, ddate = cur.fetchone()
        legend = """
                mysql> select * from pet;
                +------+---------+---------+------+------------+------------+
                | name | owner   | species | sex  | birth      | death      |
                +------+---------+---------+------+------------+------------+
                | fido | jon     | dog     | m    | 0000-00-00 | 0000-00-00 |
                | odif | deborah | dog     | f    | 2000-01-01 | 2010-01-01 |
                +------+---------+---------+------+------------+------------+
           """
        response = "%s\n<span style='background-color: #FCD'>%s</span> had a <span style='background-color: #FCD'>%s</span> whose name was <span style='background-color: #FCD'>%s</span>. She was born on <span style='background-color: #FCD'>%s</span>" % (legend, owner.title(), type, name.title(), bdate)
    
        return render_template("dispacher.html",
            title = "Dispacher Interface",
            user = session['username'],
            reqenviron = request.environ,
            ses = session,
            legend = legend,
            response = response,
            owner = owner.title(), 
            type = type, 
            name = name.title(),
            bdate = bdate)


=======
    db = MySQLdb.connect(**CONNECTION_ARGS)
    cur = db.cursor()
    cur.execute("select * from pet where sex = 'f'")
    name, owner, type, sex, bdate, ddate = cur.fetchone()
    legend = """
            mysql> select * from pet;
            +------+---------+---------+------+------------+------------+
            | name | owner   | species | sex  | birth      | death      |
            +------+---------+---------+------+------------+------------+
            | fido | jon     | dog     | m    | 0000-00-00 | 0000-00-00 |
            | odif | deborah | dog     | f    | 2000-01-01 | 2010-01-01 |
            +------+---------+---------+------+------------+------------+
       """
    response = "%s\n<span style='background-color: #FCD'>%s</span> had a <span style='background-color: #FCD'>%s</span> whose name was <span style='background-color: #FCD'>%s</span>. She was born on <span style='background-color: #FCD'>%s</span>" % (legend, owner.title(), type, name.title(), bdate)
    
    return render_template("dispacher.html",
        title = "Dispacher Interface",
        user = session['username'],
        reqenviron = request.environ,
        ses = session,
        legend = legend,
        response = response,
        owner = owner.title(), 
        type = type, 
        name = name.title(),
        bdate = bdate)


@app.route('/logout')
def logout():
    if session.get('username') or session.get('logged_in'):
        session.pop('username')
        session.pop('logged_in')
    return redirect(url_for('login'))

>>>>>>> 772583266c240c1a7807c1c63495890180eb26b0
@app.route('/testTemplate')
@logged_in
def tempTest():
    session['objects'] = 42
    session.permanent = False
    user = { 'nickname': "Handsome" } # fake user
    return render_template("testTemplate.html",
        title = "Testing",
        user = user,
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
<<<<<<< HEAD
    
    
### RANDOM JUNK TO GET RID OF ###

#                 if next:
#                     flash('redirected ' + uname + ' to next')
#                     return redirect(next)
#                 else: return redirect(url_for('tempTest'))

=======
    
>>>>>>> 772583266c240c1a7807c1c63495890180eb26b0
