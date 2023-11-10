from flask import Flask, render_template, request, url_for, redirect, session
from database import shopname, orders, add_data, load_userid_from_db, add_menu, delete_order
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

connection = mysql.connector.connect(host = HOST, port = PORT,
                                    database = DATABASE,
                                    user = USERNAME,
                                    password = PASSWORD)

cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = "*"

USER_LST = load_userid_from_db()

@app.route("/home")
def home():
    shopnames = shopname()
    return render_template("Home.html", Shopnames = shopnames, username = session['username'], usertype = session['usertype'])

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
                    session['userid']=user[0]
                    session['usertype']=user[2]
                    return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('usertype', None)
    return redirect(url_for("login"))

@app.route("/shops/<shopnames>", methods=['GET', 'POST'])
def shoppage(shopnames):
    order = orders(shopnames)
    if request.method == 'POST':
        user = session['username']
        menu = request.form.get('menu')
        time = request.form.get('times')
        add_menu(user, time, menu, shopnames)
        # cursor.execute(f"INSERT INTO orders(username, time_want, menu, shopname) VALUES('{user}', {time}, '{menu}', '{note}')")
    return render_template("shoppage.html", Shopnames = shopnames, Order = order, username= session['username'], usertype = session['usertype'])

@app.route("/help")
def help():
    shopowner = session['userid']
    cursor.execute(f"SELECT shopname FROM shoplist WHERE shopownerid = {shopowner}")
    shopname = cursor.fetchone()
    if session['usertype'] != 2:
        return redirect(url_for('home'))
    order = orders(shopname[0])
    return render_template("order_list.html", Order = order, userid = session['userid'], usertype = session['usertype'])

@app.route('/delete_menu/<int:menu_id>')
def delete_menu(menu_id):
    delete_order(menu_id)
    return redirect(url_for('help'))

if  __name__ == "__main__":
    app.run(debug=True)
 