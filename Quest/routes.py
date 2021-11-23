from Quest import app, db, login_manager
from Quest.forms import BookTable, Contact, Login, Register, MenuPosition, Book
from Quest.tables import User, Menu, Client, Stock, BookForSale, BookInfo
from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from werkzeug.exceptions import abort


# ---------------- flask login -----------------
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


def admin_only(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if current_user.privileges == "Admin":
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_fun


# -------------------------------------------------


# ------------ sciezki na serwerze ------------
# obsluga strony glownej
@app.route("/", methods=["GET", "POST"])
def home():
    book_table_form = BookTable()
    return render_template("home/home.html", form=book_table_form)


# obsluga zakladki menu
@app.route("/menu")
def menu():
    hot_drinks = db.session.query(Menu).filter_by(category="hot_drinks").all()
    cold_drinks = db.session.query(Menu).filter_by(category="cold_drinks").all()
    desserts = db.session.query(Menu).filter_by(category="desserts").all()
    special_offers = db.session.query(Menu).filter_by(category="special_offers").all()
    return render_template("menu/menu.html", hot_drinks=hot_drinks, cold_drinks=cold_drinks, desserts=desserts,
                           special_offers=special_offers)


@app.route("/menu/nowa_pozycja", methods=["GET", "POST"])
@admin_only
def new_menu_item():
    new_menu_position_form = MenuPosition()
    if new_menu_position_form.validate_on_submit():
        entered_category = new_menu_position_form.category.data
        entered_name = new_menu_position_form.name.data
        entered_description = new_menu_position_form.description.data
        entered_price = new_menu_position_form.price.data
        entered_img_url = new_menu_position_form.image_url.data
        entered_number_in_stock = new_menu_position_form.number_in_stock.data

        new_stock = Stock(number_in_stock=entered_number_in_stock, article_type="menu_position")
        new_position = Menu(category=entered_category, name=entered_name, description=entered_description,
                            image_url=entered_img_url, price=entered_price)
        new_stock.menu_position = new_position
        db.session.add(new_stock)
        db.session.commit()

        return redirect(url_for('menu'))
    return render_template("menu/menu_item.html", form=new_menu_position_form)


@app.route("/menu/usuniecie_pozycji/<int:item_id>")
@admin_only
def delete_menu_item(item_id):
    item_to_delete = Menu.query.get(item_id)
    db.session.delete(item_to_delete.stock)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('menu'))


@app.route("/menu/edycja_pozycji/<int:item_id>", methods=["GET", "POST"])
@admin_only
def edit_menu_item(item_id):
    item_to_edit = Menu.query.get(item_id)
    edit_form = MenuPosition(
        name=item_to_edit.name,
        category=item_to_edit.category,
        price=item_to_edit.price,
        image_url=item_to_edit.image_url,
        description=item_to_edit.description,
        number_in_stock=item_to_edit.stock.number_in_stock
    )
    if edit_form.validate_on_submit():
        item_to_edit.name = edit_form.name.data
        item_to_edit.category = edit_form.category.data
        item_to_edit.price = edit_form.price.data
        item_to_edit.image_url = edit_form.image_url.data
        item_to_edit.description = edit_form.description.data
        item_to_edit.stock.number_in_stock = edit_form.number_in_stock
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template("menu/menu_item.html", form=edit_form)


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
    books_for_sale = db.session.query(BookForSale).all()
    return render_template("bookshop/bookshop.html", books=books_for_sale)


# obsluga zakladki konkretnej ksiazki
@app.route("/ksiegarnia/ksiazka/<int:book_id>")
def show_book_for_sell(book_id):
    return render_template("bookshop/book_single.html")


# obsluga dodania nowej pozycji
@app.route("/ksiegarnia/nowa_pozycja", methods=["GET", "POST"])
@admin_only
def new_book_for_sale():
    new_book_form = Book()
    if new_book_form.validate_on_submit():
        entered_number_in_stock = new_book_form.number_in_stock.data

        entered_price = new_book_form.price.data
        entered_discount = new_book_form.discount.data

        entered_title = new_book_form.title.data
        entered_author = new_book_form.author.data
        entered_publisher = new_book_form.publisher.data
        entered_genre = new_book_form.genre.data
        entered_description = new_book_form.description.data
        entered_publish_date = new_book_form.publish_date.data
        entered_image_url = new_book_form.image_url.data

        new_stock = Stock(number_in_stock=entered_number_in_stock, article_type="book_for_sale")
        new_book_for_sale = BookForSale(price=entered_price, discount=entered_discount)
        new_book_info = BookInfo(title=entered_title, author=entered_author, publisher=entered_publisher,
                                 genre=entered_genre, description=entered_description, publish_date=entered_publish_date, image_url=entered_image_url)
        new_stock.book_info = new_book_info
        new_stock.book_for_sale = new_book_for_sale
        db.session.add(new_stock)
        db.session.commit()

        return redirect(url_for('bookshop'))
    return render_template("bookshop/book_item.html", form=new_book_form)


# obsluga zakladki biblioteki
@app.route("/biblioteka")
def library():
    return render_template("library/library.html")


@app.route("/rejestracja", methods=["GET", "POST"])
def registration():
    register_form = Register()
    if register_form.validate_on_submit():
        entered_login = register_form.login.data
        entered_email = register_form.email.data
        entered_password = register_form.password.data
        entered_first_name = register_form.first_name.data
        entered_last_name = register_form.last_name.data

        new_user = User(login=entered_login, email=entered_email, password=entered_password,
                        first_name=entered_first_name,
                        last_name=entered_last_name)
        new_client = Client()
        new_user.client = new_client
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template("account/registration.html", form=register_form)


# obsluga zakladki logowania
@app.route("/logowanie", methods=["GET", "POST"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        entered_login = login_form.login.data
        selected_user = db.session.query(User).filter_by(login=entered_login).first()
        login_user(selected_user)
        return redirect(url_for("account"))

    return render_template("account/login.html", form=login_form)


# obsługa konta
@app.route("/konto")
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("account/account.html")


# droga dla wylogwania
@app.route("/wylogowanie")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# obsluga zakladki wydarzenia
@app.route("/wydarzenia")
def events():
    return render_template("events/events.html")
