from flask import Flask, render_template, redirect, url_for
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
@app.route("/kontakt", methods=["GET", "POST"])
def contact():
    contact_form = Contact()
    if contact_form.validate_on_submit():
        return redirect(url_for('contact'))
    return render_template("contact.html", form=contact_form)


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
