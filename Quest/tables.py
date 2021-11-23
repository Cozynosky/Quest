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


class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="worker")

# class BookInfo(db.Model):
#     __tablename__ = "books_info"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), nullable=False)
#     author = db.Column(db.String(250), nullable=False)
#     publisher = db.Column(db.String(250), nullable=False)
#     genre = db.Column(db.String(250), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#
#
# class BookForSale(db.Model):
#     __tablename__ = "books_for_sale"
#     id = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Integer, nullable=False)


class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    number_in_stock = db.Column(db.Integer, nullable=False)
    article_type = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    menu_position = relationship("Menu", uselist=False, back_populates="stock")


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True, server_default="Brak opisu")
    image_url = db.Column(db.String(2000), nullable=True, server_default="Brak adresu zdjęcia")
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="menu_position")
# ---------------------------------------------------------------------------------------
