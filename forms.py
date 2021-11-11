from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, TextAreaField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class BookTable(FlaskForm):
    name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    last_name = StringField("Nazwisko", validators=[DataRequired(message="To pole jest wymagane!")])
    phone = StringField("Telefon", validators=[DataRequired(message="To pole jest wymagane!")])
    date = DateField("Data", validators=[DataRequired(message="To pole jest wymagane!")], format="%d-%m-%Y")
    time = DateTimeField("Godzina", validators=[DataRequired(message="To pole jest wymagane!")], format="%H:%M")
    message = TextAreaField("Wiadomość", validators=[DataRequired(message="To pole jest wymagane!")])
    book_button = SubmitField("Zarezerwuj stolik")


class Login(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!")])
    password = PasswordField("Hasło", validators=[InputRequired(message="To pole jest wymagane!")])
    login_button = SubmitField("login")


class Register(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!"), Email(message="To nie jest poprawny adres email!")])
    password = PasswordField("Hasło", validators=[InputRequired(message="To pole jest wymagane!")])
    confirm_password = PasswordField("Powtórz hasło", validators=[InputRequired(message="To pole jest wymagane!"), EqualTo('password', message="Hasła muszą się zgadzać")])
    first_name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    last_name = StringField("Nazwisko", validators=[DataRequired(message="To pole jest wymagane!")])
    register_button = SubmitField("register")


class Contact(FlaskForm):
    name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!"), Email(message="To nie jest poprawny adres email!")])
    subject = StringField("Temat", validators=[DataRequired(message="To pole jest wymagane!")])
    message = TextAreaField("Wiadomość", validators=[DataRequired(message="To pole jest wymagane!")])
    submit_button = SubmitField("Wyślij wiadomość")
