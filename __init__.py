from flask_migrate import Migrate
from app import app
from database import db

# zarzadzanie migracjami tabeli
migrate = Migrate(app, db)
