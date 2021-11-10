from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, TextAreaField, DateField, DateTimeField
from wtforms.validators import DataRequired


class BookTable(FlaskForm):
    name = StringField("Imię", validators=[DataRequired()])
    last_name = StringField("Nazwisko", validators=[DataRequired()])
    phone = StringField("Telefon", validators=[DataRequired()])
    date = DateField("Data", validators=[DataRequired()], format="%d-%m-%Y")
    time = DateTimeField("Godzina", validators=[DataRequired()], format="%H:%M")
    message = TextAreaField("Wiadomość", validators=[DataRequired()])
    book_button = SubmitField("Zarezerwuj stolik")


class Login(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    login_button = SubmitField("login")


class Contact(FlaskForm):
    name = StringField("Imię", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    subject = StringField("Temat", validators=[DataRequired()])
    message = TextAreaField("Wiadomość", validators=[DataRequired()])
    submit_button = SubmitField("Wyślij wiadomość")
