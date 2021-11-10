from main import db,app
from sqlalchemy_utils.functions import database_exists
from flask_login import UserMixin


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

