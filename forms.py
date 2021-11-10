from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField,TextAreaField
from wtforms.validators import DataRequired


class BookTable(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    last_name = StringField("last name", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    date = StringField("date", validators=[DataRequired()])
    time = StringField("time", validators=[DataRequired()])
    message = TextAreaField("message", validators=[DataRequired()])


class Login(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    login_button = SubmitField("login")
