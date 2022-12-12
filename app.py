from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import sqlite3
from model import User, Entry

# Configuration
DATABASE = 'trading.db'
DEBUG = True
SECRET_KEY = 'development key'




# Create the Flask app
app = Flask(__name__)
app.config.from_object(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# Connect to the database
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE']);
    conn.row_factory = sqlite3.Row
    return conn

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
            db.execute('insert into users (phonenumber, username, password,email) values (?,?,?,?)',
                       
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
            print(user[1])
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


    

# Get all trade entries for the current user
def get_trades():
    
    db = get_db()
    phonenumber = session['phonenumber']
    print(phonenumber)
    cur = db.execute('select symbol, date, notes,quantity,SL,oprice,cprice from entries where phonenumber = ?',
                     [phonenumber])
    
    trades =dict(result=[dict(r) for r in cur.fetchall()])
      
    return trades

# Show the trading journal entries
@app.route('/show_entries')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    trades = get_trades()
    return render_template('show_entries.html', trades=trades, logged_in=True)



@app.route('/add_trade', methods=['GET', 'POST'])
def add_trade():
    if request.method == 'POST':
        
        db = get_db()
        rr = 0.0
    
        phonenumber = session['phonenumber']
        symbol = request.form['symbol']
        date = request.form['date']       
        qty = int(request.form['qty'])
        notes = request.form['notes']
        sl = int(request.form['sl'])
        oprice = int(request.form['oprice'])
        cprice = int(request.form['cprice'])       
        profit = (cprice-oprice)*qty
        if (cprice != 0):
            rr = (cprice-oprice)/(oprice-sl)
        print(oprice,cprice,qty,profit)
        db.execute('insert into entries (phonenumber, symbol,date,quantity,notes,SL,oprice, cprice, profit,rr) values (?,?,?,?,?,?,?,?,?,?)',
               [phonenumber, symbol, date,qty,notes,sl,oprice,cprice,profit,rr])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    return render_template('add_trades.html')

@app.route('/stats')
def stats():
    numtrades = 0
    db = get_db()
    phonenumber = session['phonenumber']
    cur = db.execute('select symbol, profit,rr from entries where phonenumber = ?', [phonenumber])
    
    pnl =dict(result=[dict(r) for r in cur.fetchall()])
    numtrades = db.execute('select COUNT() from entries where phonenumber= ?',[phonenumber]).fetchone()[0]
    for pl in pnl['result']:
        print(pl)
       
    return render_template('stats.html', pnl=pnl, numtrades=numtrades, logged_in=True)

@app.route('/zerodha')
def zerodha():
    return render_template('zerodha.html')  


@app.route('/idb')
def idb():
  init_db()
  return render_template('login.html')