from flask import Flask, render_template, request, url_for, redirect, session
from database import shopname, orders, add_data, load_userid_from_db, find_user
import mysql.connector, MySQLdb.cursors, re
from werkzeug.security import generate_password_hash, check_password_hash

connection = mysql.connector.connect(host = "*", port = "*",
                                    database = "*",
                                    user = "*",
                                    password = "*")

cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = "*"

USER_LST = load_userid_from_db()

@app.route("/home")
def home():
    shopnames = shopname()
    return render_template("home.html", Shopnames = shopnames, username= session['username'])

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # register form
        email_regis = request.form.get('email')
        fullname_regis = request.form.get('fullname')
        password_regis = request.form.get('password')
        phone_regis = request.form.get('phone')
        if email_regis and fullname_regis and password_regis and phone_regis:
            password_regis = generate_password_hash(password_regis, method="sha256")
            add_data(fullname_regis, 1, phone_regis, email_regis, password_regis)

        # login form
        email_log = request.form.get('email_log')
        pass_log = request.form.get('password_log')
        #user = find_user(email_log, pass_log)
        if email_log:
            cursor.execute(f'SELECT * FROM userid WHERE email="{email_log}"')
            user = cursor.fetchone()
            if user:
                if check_password_hash(user[5], pass_log):
                    session["loggedin"]=True
                    session['username']=user[1]
                    return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route("/shops/<shopnames>")
def shoppage(shopnames):
    order = orders(shopnames)
    return render_template("shoppage.html", Shopnames = shopnames, Order = order, username= session['username'])

if  __name__ == "__main__":
    app.run(debug=True)
