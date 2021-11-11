from flask import render_template, redirect, url_for
from forms import User,BookTable,Contact,Register,Login
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from app import app
from database import db

# inicjalizacja
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)




# wrappery
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


# obsluga strony glownej
@app.route("/", methods=["GET", "POST"])
def home():
    book_table_form = BookTable()
    if book_table_form.validate_on_submit():
        return redirect(url_for('home'))
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


@app.route("/rejestracja", methods=["GET", "POST"])
def register():
    register_form = Register()
    if register_form.validate_on_submit():
        entered_email = register_form.email.data
        entered_password = register_form.password.data
        entered_first_name = register_form.first_name.data
        entered_last_name = register_form.last_name.data

        new_user = User(email=entered_email, password=entered_password, first_name=entered_first_name, last_name=entered_last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("registration.html", form=register_form)


# obsluga zakladki logowania
@app.route("/logowanie", methods=["GET", "POST"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        entered_email = login_form.email.data
        selected_user = db.session.query(User).filter_by(email=entered_email).first()
        login_user(selected_user)
        return redirect(url_for("account"))
    return render_template("login.html", form=login_form)


# obsługa konta
@login_required
@app.route("/konto")
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("account.html")


# droga dla wylogwania
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
