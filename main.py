from flask import Flask, render_template

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = "kawiarnia_ksiegarnia_quest"


# obsluga strony glownej
@app.route("/")
def home():
    return render_template("index.html")


# obsluga zakladki menu
@app.route("/menu")
def menu():
    return render_template("menu.html")


# obsluga zakladki kontakt
@app.route("/kontakt")
def contact():
    return render_template("contact.html")


# obsluga zakladki o nas
@app.route("/o_nas")
def about():
    return render_template("about.html")


# obsluga zakladki koszyk
@app.route("/koszyk")
def cart():
    return render_template("cart.html")


# obsluga zakladki ksiegarnia
@app.route("/ksiegarnia")
def shop():
    return render_template("shop.html")


# obsluga zakladki konto
@app.route("/konto")
def account():
    return render_template("account.html")


# obsluga zakladki wydarzenia
@app.route("/wydarzenia")
def events():
    return render_template("events.html")


if __name__ == "__main__":
    app.run(debug=True)
