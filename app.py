from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *
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

# polaczenie bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# zarzadzanie migracjami tabeli
migrate = Migrate(app, db)


# menadzer zalogowanych uzytkownikow
login_manager = LoginManager()
login_manager.init_app(app)


# ------------------------------TABELE BAZY DANYCH --------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
    last_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
# ---------------------------------------------------------------------------------------


# wrappery
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


# obsluga strony glownej
@app.route("/", methods=["GET", "POST"])
def home():
    book_table_form = BookTable()
    return render_template("home/home.html", form=book_table_form)


# obsluga zakladki menu
@app.route("/menu")
def menu():
    return render_template("menu/menu.html")


# obsluga zakladki kontakt
@app.route("/kontakt", methods=["GET", "POST"])
def contact():
    contact_form = Contact()
    if contact_form.validate_on_submit():
        return redirect(url_for('contact'))
    return render_template("contact/contact.html", form=contact_form)


# obsluga zakladki koszyk
@app.route("/koszyk")
def cart():
    return render_template("cart/cart.html")


# obsluga zakladki ksiegarnia
@app.route("/ksiegarnia")
def bookshop():
    return render_template("bookshop/bookshop.html")


# obsluga zakladki biblioteki
@app.route("/biblioteka")
def library():
    return render_template("library/library.html")


@app.route("/rejestracja", methods=["GET", "POST"])
def registration():
    register_form = Register()
    if register_form.validate_on_submit():
        entered_email = register_form.email.data
        entered_password = register_form.password.data
        entered_first_name = register_form.first_name.data
        entered_last_name = register_form.last_name.data
        user = db.session.query(User).filter_by(email=entered_email).first()
        if user is None:
            new_user = User(email=entered_email, password=entered_password, first_name=entered_first_name, last_name=entered_last_name)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("account/registration.html", form=register_form)


# obsluga zakladki logowania
@app.route("/logowanie", methods=["GET", "POST"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        entered_email = login_form.email.data
        entered_password = login_form.password.data
        selected_user = db.session.query(User).filter_by(email=entered_email).first()
        if selected_user is None:
            return redirect(url_for("login"))
        elif selected_user.password == entered_password:
            login_user(selected_user)
            return redirect(url_for("account"))
        else:
            return redirect(url_for("login"))
    return render_template("account/login.html", form=login_form)


# obsługa konta
@login_required
@app.route("/konto")
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("account/account.html")


# droga dla wylogwania
@login_required
@app.route("/wylogowanie")
def logout():
    logout_user()
    return redirect(url_for('home'))


# obsluga zakladki wydarzenia
@app.route("/wydarzenia")
def events():
    return render_template("events/events.html")


if __name__ == "__main__":
    app.run(debug=True)
