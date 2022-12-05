from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import sqlite3

# Configuration
DATABASE = 'trading.db'
DEBUG = True
SECRET_KEY = 'development key'

# Create the Flask app
app = Flask(__name__)
app.config.from_object(__name__)

# Connect to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Initialize the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode( encoding='utf-8'))
        db.commit()

# Open a new database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Close the database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def home():
    return render_template('home.html')
# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select username from users where username = ?',
                         [request.form['username']])
        if cur.fetchone() is not None:
            error = 'Username already exists'
        else:
            db.execute('insert into users (phonenumber, username, email,password) values (?,?,?,?)',
                       
                       [request.form['phonenumber'],
                        request.form['username'],
                        request.form['password'],
                        request.form['email']])
            db.commit()
            flash('You were successfully registered')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

# Log in a user
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select phonenumber, password from users where username = ?',
                         [request.form['username']])
        user = cur.fetchone()
        if user is None:
            error = 'Invalid username'
        elif user[1] != request.form['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['phonenumber'] = user[0]
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

# Log out a user
@app.route('/logout')
def logout():
  session['logged_in']=False
  return render_template('home.html')

# Add a new trade to the journal
def add_trade(symbol, date, notes):
    db = get_db()
    phonenumber = session['phonenumber']
    db.execute('insert into entries (phonenumber, symbol, date, notes) values (?,?,?,?)',
               [phonenumber, symbol, date, notes])
    db.commit()

# Get all trade entries for the current user
def get_trades():
    db = get_db()
    phonenumber = session['phonenumber']
    cur = db.execute('select symbol, date, notes from entries where phonenumber = ?',
                     [phonenumber])
    trades = cur.fetchall()
    return trades

# Show the trading journal entries
@app.route('/show_entries')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    trades = get_trades()
    return render_template('show_entries.html', trades=trades, logged_in=True)

def add_entry(symbol, date, notes):
    db = get_db()
    phonenumber = session['phonenumber']
    db.execute('insert into entries (phonenumber, symbol, date, notes) values (?,?,?,?)',
               [phonenumber, symbol, date, notes])
    db.commit()

@app.route('/add_trade', methods=['GET', 'POST'])
def add_trade():
    if request.method == 'POST':
        symbol = request.form['symbol']
        date = request.form['date']
        notes = request.form['notes']
        add_entry(symbol, date, notes)
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    return render_template('add_trades.html')

@app.route('/idb')
def idb():
  init_db()
  return render_template('login.html')