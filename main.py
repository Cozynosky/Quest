from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import *
from sqlalchemy_utils.functions import database_exists
from flask_login import login_user, LoginManager, current_user, logout_user, login_required, UserMixin
import os

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default_secret_key")
Bootstrap(app)

# Rozwiązanie problemu dla nowszych wersji SQLAlchemy dzialajacych z heroku
uri = os.environ.get("DATABASE_URL",  "sqlite:///quest.db")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# Połączenie z bazą danych
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# menadzer zalogowanych uzytkownikow
login_manager = LoginManager()
login_manager.init_app(app)


# ------------------------------TABELE BAZY DANYCH --------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)


if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    db.create_all()

if db.session.query(User).filter_by(email="admin").first() is None:
    db.session.add(User(email="admin", password="admin"))
    db.session.commit()
# ---------------------------------------------------------------------------------------


# wrappery
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


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
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    else:
        login_form = Login()
        if login_form.validate_on_submit():
            entered_email = login_form.email.data
            entered_password = login_form.password.data
            selected_user = db.session.query(User).filter_by(email=entered_email).first()
            if selected_user is None:
                return redirect(url_for("account"))
            elif selected_user.password == entered_password:
                login_user(selected_user)
                return redirect(url_for("account"))
            else:
                return redirect(url_for("login"))
        return render_template("account.html", form=login_form)


@login_required
@app.route("/zalogowany_uzytkownik")
def logged_in():
    return render_template("logged_in.html")


@login_required
@app.route("/wylogowanie")
def logout():
    logout_user()
    return redirect(url_for('home'))


# obsluga zakladki wydarzenia
@app.route("/wydarzenia")
def events():
    return render_template("events.html")


if __name__ == "__main__":
    app.run(debug=True)
