from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
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

Bootstrap(app)

db = SQLAlchemy(app)

# zarzadzanie migracjami tabeli
migrate = Migrate(app, db)

# menadzer zalogowanych uzytkownikow
login_manager = LoginManager()
login_manager.init_app(app)

import Quest.routes
