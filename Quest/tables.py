from flask_login import UserMixin
from Quest import db


# ------------------------------TABELE BAZY DANYCH --------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(250), nullable=False, server_default="User")
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
    last_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=True, server_default="Brak opisu")
    image_url = db.Column(db.String(2000), nullable=True, server_default="Brak adresu zdjęcia")
    price = db.Column(db.Numeric(10, 2), nullable=False)
# ---------------------------------------------------------------------------------------
