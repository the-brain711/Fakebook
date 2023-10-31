##### DEPENDENCIES #####
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
##### DEPENDENCIES #####

##### INITIALIZE FLASK #####
application = Flask(__name__, template_folder="templates") # This needs to be named `application`
# Change this to your secret key (it can be anything, it's for extra protection)
application.secret_key = 'secret'
##### INITIALIZE FLASK #####

##### INITIALIZE MYSQL #####
application.config['MYSQL_HOST'] = 'fakebook-db.ch5ziarjkczw.us-east-1.rds.amazonaws.com'
application.config['MYSQL_PORT'] = 3306
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = 'Fakebook!db01'
application.config['MYSQL_DB'] = 'fakebook_db'

db = MySQL(application)
##### INITIALIZE MYSQL #####

##### ROUTES #####
@application.route('/', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    
    # Output message if something goes wrong...
    msg = ''
    
    # Check if username and password POST request exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Retrieve hashed password
        hashed_password = password + application.secret_key
        hashed_password = hashlib.sha1(hashed_password.encode())
        password = hashed_password.hexdigest()
        
        # Check if user exists in database
        cursor = db.connect.cursor(MySQLdb.cursors.DictCursor)
        #cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users_tb WHERE username = %s AND password = %s',
            (username, password,)
        )
        user = cursor.fetchone()
        
        # Create session data for user if user exists
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            msg = 'Invalid username or password. Please try again.'
    
    return render_template('login.html', msg=msg)

@application.route('/logout')
def logout():
    # Remove session data, this will logout the user
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    
    return redirect(url_for('login'))

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    # Output message if something goes wrong
    msg = ''
    
    # Check if username, password, and email POST request exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Check if user exists in database
        cursor = db.connect.cursor(MySQLdb.cursors.DictCursor)
        #cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users_tb WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        
        # If user exists, show error and validation checks
        if user:
            msg = 'Username is already taken. Please choose a different one.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers.'
        elif not username or not password or not email:
            msg = 'Please fill out the form completely.'
        else:
            # Hash the password
            hashed_password = password + application.secret_key
            hashed_password = hashlib.sha1(hashed_password.encode())
            password = hashed_password.hexdigest()
            
            # Insert new account into database
            cursor.execute(
                'INSERT INTO users_tb (username, password, email) VALUES(%s, %s, %s);',
                (username, password, email,)
            )
            db.connect.commit()
            #db.connection.commit()
            msg = 'You have successfully signed up to Fakebook.'
            return redirect(url_for('login'))
    # If form is empty or missing 1 box
    elif request.method == 'POST':
        msg = 'Please fill out the form completely.'
    
    return render_template('signup.html', msg=msg)

@application.route('/home')
def home():
    # Check if user is logged in
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    
    return redirect(url_for('login'))

@application.route('/profile')
def profile():
    # Check if user is logged in
    if 'loggedin' in session:
        cursor = db.connect.cursor(MySQLdb.cursors.DictCursor)
        #cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users_tb WHERE id = %s',
            (session['id'],)
        )
        user = cursor.fetchone()
        
        # Show profile page with user info
        return render_template('profile.html', user=user)
##### ROUTES #####

# Starts the flask application
if __name__ == "__main__":
    application.run()