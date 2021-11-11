from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)

# ------------------------------TABELE BAZY DANYCH --------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
    last_name = db.Column(db.String(250), nullable=False, server_default="Nie podano")
# ---------------------------------------------------------------------------------------
