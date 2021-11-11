from flask import Flask
import os

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default_secret_key")

# Rozwiązanie problemu dla nowszych wersji SQLAlchemy dzialajacych z heroku
uri = os.environ.get("DATABASE_URL",  "sqlite:///quest.db")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# polaczenie bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
