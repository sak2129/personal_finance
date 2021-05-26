# Main program file - this file renders the mainpage and connects all routes

# Import Modules
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return home()

@app.route('/view')
def view():
    return render_template('day.html')

@app.route('/food')
def food():
    return render_template('add_food.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)

