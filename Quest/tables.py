from flask_login import UserMixin
from Quest import db


# ------------------------------TABELE BAZY DANYCH --------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
    last_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
# ---------------------------------------------------------------------------------------
