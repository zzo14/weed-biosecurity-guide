from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
app.secret_key = 'key'

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

#Interface
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    connection = getCursor()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        query = "SELECT * FROM userauth WHERE username = %s"
        connection.execute(query, (username,))
        user = connection.fetchall()
        print("user", user)
        if user and check_password_hash(user[0][2], password):
            session['username'] = username
            session['userType'] = user[0][3]
            flash("Successfully login, welcome! ", "success")
            return redirect(url_for('home'))
        else:
            flash("Invilid username or password, please try again.", "danger")
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    connection = getCursor()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$', password):
            flash("Password must be at least 8 characters long and conatin uppercase, lowercase, number and special characters.")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password) 
        print("hashed_password", hashed_password)
        query = "INSERT INTO userAuth (username, password_hash, userType) VALUES (%s, %s, %s)"
        connection.execute(query, (username, hashed_password, 'Gardener'))
        new_id = connection.lastrowid
        affected_rows = connection.rowcount
        if new_id and affected_rows > 0:
            query = "INSERT INTO gardener (gardener_id, username, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            connection.execute(query, (new_id, username, first_name, last_name, address, email, phone_number, datetime.now(), 'Active'))
            flash("Successfully register, welcome! ", "success")
            return redirect(url_for('login'))
        else:
            flash("Username already exists, please try another one.", "danger")
    return render_template("register.html")
        



