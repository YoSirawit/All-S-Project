from flask import Flask, render_template
from database import shopname, orders


app = Flask(__name__)


@app.route("/")
def home():
    shopnames = shopname()
    return render_template("home.html", Shopnames = shopnames)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/shops/<shopnames>")
def shoppage(shopnames):
    order = orders(shopnames)
    return render_template("shoppage.html", Shopnames = shopnames, Order = order)

if  __name__ == "__main__":
    app.run(debug=True)