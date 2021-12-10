from datetime import timedelta, datetime
from decimal import Decimal
from functools import wraps
from os import environ

from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from Quest import app, db, login_manager
from Quest.books_genres import genres
from Quest.forms import Contact, Login, Register, MenuPosition, Book, EditAccountData, EditPassword, NewTable, FindTable
from Quest.tabels import User, Menu, Client, Stock, BookForSale, BookInfo, Order, OrderItem, Worker, Table, \
    TableReservations


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


def user_only(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if current_user.privileges == "User":
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_fun


def admin_and_user_only(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if current_user.privileges == "User" or current_user.privileges == "Admin":
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_fun


# -------------------------------------------------


# -------- konfiguracja sesji ---------
@app.before_first_request
def session_settings():
    session.clear()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    # konto administratora
    if db.session.query(User).filter_by(login="admin").first() is None:
        admin = User(login="admin", password=generate_password_hash(environ.get('ADMIN_PASSWORD', 'admin')),
                     first_name="admin", last_name="admin",
                     email="admin@admin.admin", privileges="Admin")
        db.session.add(admin)
    # domyslne konto uzytkownika niezalogowanego
    if db.session.query(User).filter_by(login="default").first() is None:
        default = User(login="default", password=generate_password_hash("default"),
                       first_name="default", last_name="default",
                       email="default@default.default", privileges="User")
        default_client = Client()
        default.client = default_client
        default_worker = Worker()
        default.worker = default_worker
        db.session.add(default)
    # konto uzytkownika klienta testowe
    if db.session.query(User).filter_by(login="client").first() is None:
        test = User(login="client", password=generate_password_hash("client"),
                    first_name="client", last_name="client",
                    email="client@client.client", privileges="User")
        test_client = Client()
        test.client = test_client
        db.session.add(test)

    db.session.commit()


# -------- konfiguracja sesji --------


# ------------ sciezki na serwerze ------------
# obsluga strony glownej
@app.route("/")
def home():
    return render_template("home/home.html")


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
    books_for_borrow = False
    menu_positions = False
    books_for_sell = False
    subtotal = 0
    discount = 0
    in_cart = session.get('cart', False)
    if in_cart and len(in_cart) > 0:
        books_for_borrow = []
        menu_positions = []
        books_for_sell = []
        all_products = [[Stock.query.get(stock_id), number_of] for stock_id, number_of in in_cart.items()]
        for product in all_products:
            if product[0].article_type == 'book_for_sale':
                books_for_sell.append(product)
                if product[0].book_for_sale.new_price > 0:
                    discount = (product[0].book_for_sale.price - product[0].book_for_sale.new_price) * product[1]

                subtotal += product[0].book_for_sale.price * product[1]
            elif product[0].article_type == 'menu_position':
                menu_positions.append(product)
                subtotal += product[0].menu_position.price * product[1]
            elif product[0].article_type == 'book_for_borrow':
                books_for_borrow.append(product)
    else:
        in_cart = False

    return render_template("cart/cart.html", in_cart=in_cart, books_for_borrow=books_for_borrow,
                           books_for_sell=books_for_sell, menu_positions=menu_positions, subtotal=subtotal,
                           discount=discount)


# dodanie do koszyka
@app.route("/koszyk/dodaj/<int:stock_id>")
def add_to_cart(stock_id):
    if session.get('cart', False) is False:
        session['cart'] = {}

    session['cart'][str(stock_id)] = session['cart'].get(str(stock_id), 0) + 1

    if session.get('number_in_cart', False) is False:
        session['number_in_cart'] = 1
    else:
        session['number_in_cart'] += 1

    return redirect(request.referrer)


# usuwanie z koszyka
@app.route("/koszyk/usun/<string:stock_id>")
def delete_from_cart(stock_id):
    session['number_in_cart'] -= session['cart'][stock_id]
    session['cart'].pop(stock_id, None)
    return redirect(url_for('cart'))


# zwiekszenie ilosci artykułu
@app.route("/koszyk/zwieksz/<string:stock_id>")
def increase_number_in_cart(stock_id):
    session['number_in_cart'] += 1
    session['cart'][stock_id] += 1
    return redirect(url_for('cart'))


# zmniejszenie ilosci artykułu
@app.route("/koszyk/zmniejsz/<string:stock_id>")
def decrease_number_in_cart(stock_id):
    session['number_in_cart'] -= 1
    session['cart'][stock_id] -= 1
    return redirect(url_for('cart'))


# zmniejszenie ilosci artykułu
@app.route("/koszyk/zloz_zamowienie")
def make_order():
    order_time = datetime.today()

    if current_user.is_authenticated and current_user.privileges == "User":
        order = Order(date_of_order=order_time, client=current_user.client, total_price=0, total_number_of_items=0)
    else:
        order = Order(date_of_order=order_time, total_price=0, total_number_of_items=0,
                      client=db.session.query(User).filter_by(login="anonymous").first().client)
    db.session.add(order)

    total_price = 0
    total_items_number = 0
    for stock_id, number_of in session['cart'].items():
        stock_item = Stock.query.get(stock_id)
        if stock_item.article_type == 'book_for_sale' or stock_item.article_type == 'menu_position':

            if stock_item.article_type == 'book_for_sale':
                if stock_item.book_for_sale.new_price > 0:
                    total_price += stock_item.book_for_sale.new_price * number_of
                else:
                    total_price += stock_item.book_for_sale.price * number_of
            else:
                total_price += stock_item.menu_position.price * number_of

            total_items_number += number_of
            new_order_item = OrderItem(number_of_item=number_of, order=order, stock=stock_item)
            stock_item.number_in_stock -= number_of
            db.session.add(new_order_item)

    order.total_price = total_price
    order.total_number_of_items = total_items_number
    db.session.commit()

    session.pop('cart', None)
    session.pop('number_in_cart', None)
    flash("Zamówienie zostało złożone :) Dziękujemy!")

    return redirect(url_for('cart'))


# obsluga zakladki ksiegarnia
@app.route("/ksiegarnia")
def bookshop():
    books_for_sale = db.session.query(BookForSale).all()
    return render_template("bookshop/bookshop.html", books=books_for_sale)


# obsluga zakladki konkretnej ksiazki
@app.route("/ksiegarnia/ksiazka/<int:book_id>")
def show_book_for_sell(book_id):
    book = BookForSale.query.get(book_id)
    return render_template("bookshop/book_single.html", book=book, genres=genres)


@app.route("/ksiegarnia/edycja_pozycji/<int:book_id>", methods=["GET", "POST"])
@admin_only
def edit_book_for_sell(book_id):
    edited_book = BookForSale.query.get(book_id)
    edit_book_form = Book(
        number_in_stock=edited_book.stock.number_in_stock,
        price=edited_book.price,
        title=edited_book.stock.book_info.title,
        author=edited_book.stock.book_info.author,
        publisher=edited_book.stock.book_info.publisher,
        genre=edited_book.stock.book_info.genre,
        description=edited_book.stock.book_info.description,
        publish_date=edited_book.stock.book_info.publish_date,
        image_url=edited_book.stock.book_info.image_url
    )
    if edit_book_form.validate_on_submit():
        entered_number_in_stock = edit_book_form.number_in_stock.data

        entered_price = edit_book_form.price.data
        entered_discount = edit_book_form.discount.data

        if entered_discount > 0:
            new_price = round(entered_price - (Decimal(entered_discount / 100) * entered_price), 2)
        else:
            new_price = Decimal(0)

        entered_title = edit_book_form.title.data
        entered_author = edit_book_form.author.data
        entered_publisher = edit_book_form.publisher.data
        entered_genre = edit_book_form.genre.data
        entered_description = edit_book_form.description.data
        entered_publish_date = edit_book_form.publish_date.data
        entered_image_url = edit_book_form.image_url.data

        edited_book.price = entered_price
        edited_book.new_price = new_price
        edited_book.stock.number_in_stock = entered_number_in_stock
        edited_book.stock.book_info.title = entered_title
        edited_book.stock.book_info.author = entered_author
        edited_book.stock.book_info.publisher = entered_publisher
        edited_book.stock.book_info.genre = entered_genre
        edited_book.stock.book_info.description = entered_description
        edited_book.stock.book_info.publish_date = entered_publish_date
        edited_book.stock.book_info.image_url = entered_image_url

        db.session.commit()

        return redirect(url_for('bookshop'))
    return render_template('bookshop/book_item.html', form=edit_book_form)


# obsluga dodania nowej pozycji
@app.route("/ksiegarnia/nowa_pozycja", methods=["GET", "POST"])
@admin_only
def new_book_for_sale():
    new_book_form = Book()
    if new_book_form.validate_on_submit():
        entered_number_in_stock = new_book_form.number_in_stock.data

        entered_price = new_book_form.price.data
        entered_discount = new_book_form.discount.data

        if entered_discount > 0:
            new_price = round(entered_price - (Decimal(entered_discount / 100) * entered_price), 2)
        else:
            new_price = Decimal(0)

        entered_title = new_book_form.title.data
        entered_author = new_book_form.author.data
        entered_publisher = new_book_form.publisher.data
        entered_genre = new_book_form.genre.data
        entered_description = new_book_form.description.data
        entered_publish_date = new_book_form.publish_date.data
        entered_image_url = new_book_form.image_url.data

        new_stock = Stock(number_in_stock=entered_number_in_stock, article_type="book_for_sale")
        new_book_for_sale = BookForSale(price=entered_price, new_price=new_price)
        new_book_info = BookInfo(title=entered_title, author=entered_author, publisher=entered_publisher,
                                 genre=entered_genre, description=entered_description,
                                 publish_date=entered_publish_date, image_url=entered_image_url)
        new_stock.book_info = new_book_info
        new_stock.book_for_sale = new_book_for_sale
        db.session.add(new_stock)
        db.session.commit()

        return redirect(url_for('bookshop'))
    return render_template("bookshop/book_item.html", form=new_book_form)


# usuniecie ksiazki z bazy
@app.route("/ksiegarnia/usuniecie_pozycji/<int:book_id>")
@admin_only
def delete_book_for_sell(book_id):
    book_to_delete = BookForSale.query.get(book_id)
    db.session.delete(book_to_delete.stock.book_info)
    db.session.delete(book_to_delete.stock)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('bookshop'))


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
        entered_password = generate_password_hash(register_form.password.data)
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
        app.permanent_session_lifetime = timedelta(minutes=20)
        return redirect(url_for("account"))

    return render_template("account/login.html", form=login_form)


# obsługa konta
@app.route("/konto")
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('account_data'))


# obsługa konta
@app.route("/konto/moje_dane")
@login_required
def account_data():
    return render_template("account/mydata.html")


# obsługa konta
@app.route("/konto/edytuj_moje_dane", methods=["GET", "POST"])
@login_required
def edit_account_data():
    edit_form = EditAccountData(
        login=current_user.login,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name
    )
    if edit_form.validate_on_submit():
        current_user.login = edit_form.login.data
        current_user.email = edit_form.email.data
        current_user.first_name = edit_form.first_name.data
        current_user.last_name = edit_form.last_name.data

        db.session.commit()

        return redirect(url_for('account_data'))
    return render_template("account/mydata_edit.html", form=edit_form)


# obsługa konta
@app.route("/konto/moje_haslo", methods=["GET", "POST"])
@login_required
def account_password():
    password_edit_form = EditPassword()
    if password_edit_form.validate_on_submit():
        current_user.password = generate_password_hash(password_edit_form.new_password.data)
        db.session.commit()
        return redirect(url_for('account_data'))
    return render_template("account/mypassword.html", form=password_edit_form)


# obsługa konta
@app.route("/konto/moje_zamowienia")
@login_required
@user_only
def account_orders_story():
    orders = current_user.client.orders
    return render_template("account/orders_story.html", orders=orders)


# obsługa konta
@app.route("/konto/szczegoly_zamowienia/<int:order_id>")
@login_required
def account_order_details(order_id):
    order = Order.query.get(order_id)
    books = [item for item in order.order_items if item.stock.article_type == "book_for_sale"]
    menu_positions = [item for item in order.order_items if item.stock.article_type == "menu_position"]
    return render_template("account/order_details.html", menu_positions=menu_positions, books=books)


@app.route("/konto/nowy_klient", methods=["GET", "POST"])
@login_required
@admin_and_user_only
def create_new_client():
    register_form = Register()
    if register_form.validate_on_submit():
        entered_login = register_form.login.data
        entered_email = register_form.email.data
        entered_password = generate_password_hash(register_form.password.data)
        entered_first_name = register_form.first_name.data
        entered_last_name = register_form.last_name.data

        new_user = User(login=entered_login, email=entered_email, password=entered_password,
                        first_name=entered_first_name,
                        last_name=entered_last_name)
        new_client = Client()
        new_user.client = new_client
        db.session.add(new_user)
        db.session.commit()
        flash("Poprawnie utworzono konto klienckie!")

        return redirect(url_for('create_new_client'))
    return render_template("account/new_user.html", form=register_form, account_type="klienta")


@app.route("/konto/nowy_pracownik", methods=["GET", "POST"])
@login_required
@admin_only
def create_new_worker():
    register_form = Register()
    if register_form.validate_on_submit():
        entered_login = register_form.login.data
        entered_email = register_form.email.data
        entered_password = generate_password_hash(register_form.password.data)
        entered_first_name = register_form.first_name.data
        entered_last_name = register_form.last_name.data

        new_user = User(login=entered_login, email=entered_email, password=entered_password,
                        first_name=entered_first_name,
                        last_name=entered_last_name, privileges="Worker")
        new_worker = Worker()
        new_user.worker = new_worker
        db.session.add(new_user)
        db.session.commit()
        flash("Poprawnie utworzono konto pracownika!")

        return redirect(url_for('create_new_client'))
    return render_template("account/new_user.html", form=register_form, account_type="pracownika")


# wyswietlenie rezerwacji stolikow
@app.route("/konto/rezerwacje/<int:client_id>")
def show_table_reservations(client_id):
    client = Client.query.get(client_id)
    today = datetime.today()
    today = datetime(today.year, today.month, today.day, today.hour)
    prepared_reservations = []
    for res in client.table_reservations:
        cant_cancel = True
        if today < res.date:
            cant_cancel = False
        prepared_reservations.append((res, cant_cancel))

    return render_template("account/table_reservations.html", reservations=prepared_reservations)


# droga dla wylogwania
@app.route("/wylogowanie")
@login_required
def logout():
    logout_user()
    app.permanent_session_lifetime = timedelta(minutes=10)
    return redirect(url_for('login'))


# obsluga zakladki wydarzenia
@app.route("/wydarzenia")
def events():
    return render_template("events/events.html")


# obsluga zakladki stoliki
@app.route("/stoliki", methods=["GET", "POST"])
def tables():
    today = datetime.today()

    return redirect(url_for('specified_tables', r_year=today.year, r_month=today.month, r_day=today.day, r_hour=0,
                            r_number_of_seats=0))


# obsluga zakladki stoliki z wyborem daty i godziny
@app.route("/stoliki/<int:r_year>/<int:r_month>/<int:r_day>/<int:r_number_of_seats>/<int:r_hour>",
           methods=["GET", "POST"])
def specified_tables(r_year, r_month, r_day, r_number_of_seats, r_hour):
    date = datetime(r_year, r_month, r_day)
    today = datetime.today()
    today_hour = today.hour
    today = datetime(today.year, today.month, today.day)
    seats = r_number_of_seats
    prepared_tables = []

    if request.method == "GET":

        if seats == 0:
            all_tables = db.session.query(Table).all()
        else:
            all_tables = db.session.query(Table).filter_by(number_of_seats=seats).all()

        if r_hour != 0:
            available_tables = []
            for table in all_tables:
                temp_date = datetime(date.year, date.month, date.day, r_hour)
                table_free = True
                for res in table.reservations:
                    if res.date == temp_date:
                        table_free = False
                if table_free:
                    available_tables.append(table)
            all_tables = available_tables

        if today > date:
            flash("Nie obsługujemy rezerwacji wstecz :(", "error")

        elif today == date:
            if today_hour in [21, 22, 23]:
                flash("Pracujemy tylko w godzinach 8-21 :( Zapraszamy jutro!", "info")
            elif r_hour != 0 and r_hour <= today_hour:
                flash("Nie obsługujemy rezerwacji wstecz :(", "error")
            else:
                for table in all_tables:
                    if len(table.reservations) == 0:
                        if today_hour < 8:
                            hours = [(hour, False) for hour in range(8, 21)]
                        else:
                            hours = [(hour, True) for hour in range(8, today_hour + 1)] + [(hour, False) for hour in
                                                                                       range(today_hour + 1, 21)]
                    else:
                        if today_hour < 8:
                            hours = []
                            for hour in range(8, 21):
                                temp_date = datetime(date.year, date.month, date.day, hour)
                                table_taken = False
                                for res in table.reservations:
                                    if res.date == temp_date:
                                        table_taken = True
                                hours.append((hour, table_taken))
                        else:
                            hours = [(hour, True) for hour in range(8, today_hour + 1)]
                            for hour in range(today_hour + 1, 21):
                                temp_date = datetime(today.year, today.month, today.day, hour)
                                table_taken = False
                                for reservation in table.reservations:
                                    if reservation.date == temp_date:
                                        table_taken = True
                                hours.append((hour, table_taken))
                    prepared_tables.append((table, hours))

                if not prepared_tables:
                    flash("Nie znaleziono stolika", "error")

        else:
            for table in all_tables:
                if len(table.reservations) == 0:
                    hours = [(hour, False) for hour in range(8, 21)]
                else:
                    hours = []
                    for hour in range(8, 21):
                        temp_date = datetime(date.year, date.month, date.day, hour)
                        table_taken = False
                        for res in table.reservations:
                            if res.date == temp_date:
                                table_taken = True
                        hours.append((hour, table_taken))
                prepared_tables.append((table, hours))

            if not prepared_tables:
                flash("Nie znaleziono stolika", "error")

    find_table_form = FindTable(date=date, number_of_seats=seats, time=r_hour)
    if find_table_form.validate_on_submit() and find_table_form.find_table_button.data:
        date = find_table_form.date.data
        number_of_seats = find_table_form.number_of_seats.data
        hour = find_table_form.time.data
        return redirect(url_for('specified_tables', r_year=date.year, r_month=date.month, r_day=date.day, r_hour=hour,
                                r_number_of_seats=number_of_seats))

    new_table_form = NewTable()
    if new_table_form.validate_on_submit() and new_table_form.new_table_button.data:
        number_of_seats = new_table_form.number_of_seats.data
        new_table = Table(number_of_seats=number_of_seats)
        db.session.add(new_table)
        db.session.commit()
        return redirect(request.referrer)

    return render_template("tables/tables.html", find_table_form=find_table_form, new_table_form=new_table_form,
                           tables=prepared_tables, r_date=date, r_hour=r_hour)


# opcja usuniecia stolika
@app.route("/stoliki/usun_<int:table_id>")
@login_required
def delete_table(table_id):
    table_to_delete = Table.query.get(table_id)

    for reservation in table_to_delete.reservations:
        db.session.delete(reservation)

    db.session.delete(table_to_delete)
    db.session.commit()
    return redirect(request.referrer)


# rezerwacja stolika
@app.route("/stoliki/rezerwuj/<int:r_year>/<int:r_month>/<int:r_day>/<int:r_hour>/<int:table_id>", methods=["POST"])
def book_table(r_year, r_month, r_day, r_hour, table_id):
    date_obj = datetime(r_year, r_month, r_day, r_hour)
    table = Table.query.get(table_id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    message = request.form.get('message')

    new_reservation = TableReservations(date=date_obj, first_name=first_name, last_name=last_name, phone=phone, message=message)

    if current_user.is_authenticated:
        new_reservation.client = current_user.client
    else:
        def_usr = db.session.query(User).filter_by(login="default").first()
        new_reservation.client = def_usr.client

    new_reservation.table = table
    db.session.add(new_reservation)
    db.session.commit()
    flash(f"Zarezerwowano stolik nr: {table_id} dla {table.number_of_seats} osób, na godzinę {r_hour}:00", "success")
    return redirect(request.referrer)


@app.route("/stoliki/anuluj_rezerwacje/<int:res_id>")
@login_required
def cancel_table_booking(res_id):
    res = TableReservations.query.get(res_id)
    db.session.delete(res)
    db.session.commit()

    return redirect(request.referrer)
