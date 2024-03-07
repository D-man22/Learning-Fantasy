#!/usr/bin/python3

import cgi

import sqlite3, json
import mysql.connector
# import MySQLdb

formDataLocal = cgi.FieldStorage()
import pymysql

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, g, current_app
from flask_cors import CORS

from flask.cli import with_appcontext

#Set up Flask:
app = Flask(__name__)
#Set up Flask to bypass CORS:
cors = CORS(app)

# db = sqlite3.connect('app.db', check_same_thread=False)
# connection = mysql.connector.connect(
#   host="mysql-rds-noted-cherry-pz2e.cjaeoe84erpr.ca-central-1.rds.amazonaws.com",
#   user="root",
#   password="DjMqeN1ePD7NHQ2A",
#   database="primarydb"
# )
hostname = 'mysql-rds-noted-cherry-pz2e.cjaeoe84erpr.ca-central-1.rds.amazonaws.com'
user = 'root'
password = 'DjMqeN1ePD7NHQ2A'
database = 'primarydb'


db = mysql.connector.connect(
    host=hostname,
    user=user,
    password=password,
    database=database
)

print(db)

sql = db.cursor()

# with app.app_context():
#     def getdb():
#         if 'db' not in g or not g.db.is_connected():
#             g.db = mysql.connector.connect(
#                 host='mysql://root:DjMqeN1ePD7NHQ2A@mysql-rds-noted-cherry-pz2e.cjaeoe84erpr.ca-central-1.rds.amazonaws.com:3306/primarydb',
#                 user=user,
#                 password=password,
#                 database=database
#             )
#         return g.db
# with app.app_context():
#     db = getdb()

# def close_db(e=None):
#     db = g.pop('db', None)
#     if db is not None and db.is_connected():
#         db.close()

# current_app.teardown_appcontext(close_db)

# sql = db.cursor(dictionary=True)



# account and questions tables
# with app.app_context():
#     sql.execute('''create table if not exists users(
#     "userId" integer primary key autoincrement,
#     "username" Text,
#     "password" Text,
#     "questionsKnown" Text,
#     "health" integer)''')

#     sql.execute('''
# create table if not exists questions(
#     "questionId" integer primary key autoincrement,
#     "questions" Text,
#     "possibleAnswers" Text,
#     "rightAnswers" Text, 
#     "isMath" integer,
#     "isFrench" integer,
#     "isHistory" integer,
#     "isScience" integer,
#     "difficulty" integer
    
# )''')


# sql.execute('insert into questions (questions, possibleAnswers, rightAnswers, isMath, isFrench, isHistory, isScience, difficulty) values ("a", "b", "c", 1, 2 ,3, 4, 5)')
# mysql.connection.commit()

def add_question(question, possibleAnswers, rightAnswer, isMath, isFrench, isHistory, isScience, difficulty):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('select * from questions where questions = ?', [question])
    total_rows = len(data.fetchall())
    if total_rows > 0:
        print("<script>alert('There is already this question in the database.'); window.location.reload();</script>")
    else:
        sql.execute('insert into questions (questions, possibleAnswers, rightAnswers, isMath, isFrench, isHistory, isScience, difficulty) values (?, ?, ?, ?, ?, ?, ?, ?)', [question, possibleAnswers, rightAnswer, isMath, isFrench, isHistory, isScience, difficulty])
        mysql.connection.commit()


def add_user(username, password):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('select * from users where username = ?', [username])
    total_rows = len(data.fetchall())
    if total_rows > 0:
        return "There already is an account with that name!"
    else:
        sql.execute('insert into users (username, password, health) values (?, ?, 1)', [username, password])
        mysql.connection.commit()
        return "Account created Succesfully!"

def check_user(username, password):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('select * from users where username = ? and password = ?', [username, password])
    data = result.fetchone()
    if data:
        return True
    else:
        return False
    

def update_user_question(question_id, user_id):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('select questionsKnown from users where userId = ?', [user_id])
    data = data.fetchone()
    new_data = data + question_id + " "
    sql.execute('''update users set questionsKnown = ? where userId = ?''', [new_data, user_id])
    mysql.connection.commit()


def get_user_questions(user_id):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('select questionsKnown from users where userId = ?', [user_id])
    data = data.fetchone()
    return data.split(" ")


def remove_user(user_id):
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''delete from users where userId = ?''', [user_id])
    mysql.connection.commit()


def update_user_health(user_id, amount):
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''update users set health = ? where userId = ?''', [amount, user_id])
    mysql.connection.commit()


def get_user_data(user_id):
    connection = get_db()
    sql = connection.cursor()
    data = sql.execute('''select * from users where userId = ?''', [user_id])
    return data
    

def get_user_id(username):
    connection = get_db()
    sql = connection.cursor()
    data1 = sql.execute('''select userId from users where username = ?''', [username])
    data2 = data1.fetchone()
    return data2[0]
    
def get_questions(user_id):
    connection = get_db()
    sql = connection.cursor()
    user_q_list = get_user_questions(user_id)
    q_data = sql.execute('''select * from questions where userId not in ?'''[user_q_list])
    data = q_data.fetchall()
    return data



# user_input = get_input()
# if user_input:
#     print("<script>alert('YESSSSSS');</script>")
#     mode = user_input["mode"]
#     if mode == 'createAccount':
#         print(user_input)
#         add_user(user_input["username"], user_input["password"])

#     elif mode == "logIn":
#         print("<script>alert('WIP');</script>")
#     else:
#         print("<script>alert('Invalid mode');</script>")



###############################################################

#flask


app.secret_key = "0123456789876543210"


@app.route("/makeAccount", methods=["GET", "POST"])
def application_launch():
    msg = ""
    if session.get("logged_in"):
        return redirect(url_for("main_menue"))
    if request.method == "POST":
        username = request.form.get('username1')
        password = request.form.get('password1')
        password2 = request.form.get('password1')
        if not username or not password:
            msg = "Fill out the form"
        elif password != password2:
            msg = "Passwords don't match"
        else:
            msg = add_user(username, password)
            if msg == "Account created Succesfully!":
                session["logged_in"] = True
                session["username"] = username
                session["user_id"] = get_user_id(username)
                return redirect(url_for("main_menue"))

    return render_template("index.html", message = msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if session.get("logged_in"):
        return redirect(url_for("main_menue"))
    
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user_check = check_user(username, password)
        user_check = True
        if user_check != False:
            session["logged_in"] = True
            session["username"] = username
            session["user_id"] = get_user_id(username)
            return redirect(url_for("main_menue"))
        else: 
            msg = "Incorrect Username or Password"

    return render_template("index.html", message = msg)


@app.route("/test", methods=["GET", "POST"])
def testFlask():
    
    return "<p>Hello World</p> <h1>This is a new tag</h1>"

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def main_menue():
    if session.get("logged_in") != True:
        return redirect(url_for("login"))    
    id_obj = session.get("user_id")
    return render_template("mainMenue.html", username=session.get("username"), user_id=id_obj)

@app.route("/learning", methods=["GET", "POST"])
def learn():
    if session.get("logged_in") != True:
        return redirect(url_for("login"))    
    id_obj = session.get("user_id")
    
    return render_template("learn.html", username=session.get("username"), user_id=id_obj)

@app.route("/get_questions", methods=["GET", "POST"])
def questions():
    data = get_questions(session.get("user_id"))
    questions_py = data
    return render_template("learn.html", questions_raw=questions_py)

@app.route("/add_questions", methods=["GET", "POST"])
def questions_add():
    
    return render_template("mainMenue.html")

app.run(host="0.0.0.0", port=3000)






