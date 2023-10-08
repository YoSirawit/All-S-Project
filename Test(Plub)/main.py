from flask import Flask, render_template
from database import shopname


app = Flask(__name__)

@app.route("/")
def home():
    shopnames = shopname()
    return render_template("Home.html", Shopnames = shopnames)

@app.route("/login")
def login():
    return render_template("login.html")

if  __name__ == "__main__":
    app.run(debug=True)