from flask import Flask, render_template, request, url_for, redirect
from database import shopname, orders, add_data, load_userid_from_db, find_user


app = Flask(__name__)
USER_LST = load_userid_from_db()

@app.route("/")
def home():
    shopnames = shopname()
    return render_template("home.html", Shopnames = shopnames)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_regis = request.form.get('email')
        fullname_regis = request.form.get('fullname')
        password_regis = request.form.get('password')
        phone_regis = request.form.get('phone')
        add_data(fullname_regis, 1, phone_regis, email_regis, password_regis)

        email_log = request.form.get('email_log')
        pass_log = request.form.get('password_log')
        user = find_user(email_log, pass_log)
        if user != []:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/shops/<shopnames>")
def shoppage(shopnames):
    order = orders(shopnames)
    return render_template("shoppage.html", Shopnames = shopnames, Order = order)

if  __name__ == "__main__":
    app.run(debug=True)