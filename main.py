from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from forms import *

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = "kawiarnia_ksiegarnia_quest"
Bootstrap(app)

# obsluga strony glownej
@app.route("/", methods=["GET", "POST"])
def home():
    book_table_form = BookTable()
    return render_template("index.html", form=book_table_form)


# obsluga zakladki menu
@app.route("/menu")
def menu():
    return render_template("menu.html")


# obsluga zakladki kontakt
@app.route("/kontakt")
def contact():
    return render_template("contact.html")


# obsluga zakladki koszyk
@app.route("/koszyk")
def cart():
    return render_template("cart.html")


# obsluga zakladki ksiegarnia
@app.route("/ksiegarnia")
def bookshop():
    return render_template("bookshop.html")


# obsluga zakladki biblioteki
@app.route("/biblioteka")
def library():
    return render_template("library.html")


# obsluga zakladki konto
@app.route("/konto", methods=["GET", "POST"])
def account():
    login_form = Login()

    return render_template("account.html", form=login_form)


# obsluga zakladki wydarzenia
@app.route("/wydarzenia")
def events():
    return render_template("events.html")


if __name__ == "__main__":
    app.run(debug=True)
