from flask_login import UserMixin
from sqlalchemy.orm import relationship
from Quest import db


# ------------------------------TABELE BAZY DANYCH --------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    privileges = db.Column(db.String(250), nullable=False, server_default="User")
    client = relationship("Client", uselist=False, back_populates="user")
    worker = relationship("Worker", uselist=False, back_populates="user")


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="client")
    orders = relationship("Order", back_populates="client")
    table_reservations = relationship("TableReservations", back_populates="client")


class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="worker")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date_of_order = db.Column(db.DateTime(), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_number_of_items = db.Column(db.Integer, nullable=False)
    order_items = relationship("OrderItem", back_populates="order")
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = relationship("Client", back_populates="orders")


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    number_of_item = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = relationship('Order', back_populates="order_items")
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="order_items")


class BookInfo(db.Model):
    __tablename__ = "books_info"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    publisher = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(250), nullable=False, server_default="other")
    publish_date = db.Column(db.Integer, nullable=False, server_default="2000")
    description = db.Column(db.String(2000), nullable=True)
    image_url = db.Column(db.String(2000), nullable=True, server_default="https://miro.medium.com/max/1400/1*KOAfAOQ9FwAp9i2muTkGWw.png")
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="book_info")


class BookForSale(db.Model):
    __tablename__ = "books_for_sale"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    new_price = db.Column(db.Numeric(10, 2), nullable=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="book_for_sale")


class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    number_in_stock = db.Column(db.Integer, nullable=False)
    article_type = db.Column(db.String(250), nullable=False)
    menu_position = relationship("Menu", uselist=False, back_populates="stock")
    book_info = relationship("BookInfo", uselist=False, back_populates="stock")
    book_for_sale = relationship("BookForSale", uselist=False, back_populates="stock")
    order_items = relationship("OrderItem", back_populates="stock")


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True, server_default="Brak opisu")
    image_url = db.Column(db.String(2000), nullable=True, server_default="https://miro.medium.com/max/1400/1*KOAfAOQ9FwAp9i2muTkGWw.png")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="menu_position")


class Table(db.Model):
    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    reservations = relationship("TableReservations", back_populates="table")


class TableReservations(db.Model):
    __tablename__ = "table_reservations"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(9), nullable=False)
    message = db.Column(db.String(500), nullable=True)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))
    table = relationship("Table", back_populates="reservations")
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = relationship("Client", back_populates="table_reservations")

# ---------------------------------------------------------------------------------------
