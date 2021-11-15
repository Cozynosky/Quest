from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, TextAreaField, DateField, DateTimeField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError
from Quest import db
from Quest.tables import User


class BookTable(FlaskForm):
    name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    last_name = StringField("Nazwisko", validators=[DataRequired(message="To pole jest wymagane!")])
    phone = StringField("Telefon", validators=[DataRequired(message="To pole jest wymagane!")])
    date = DateField("Data", validators=[DataRequired(message="To pole jest wymagane!")], format="%d-%m-%Y")
    time = DateTimeField("Godzina", validators=[DataRequired(message="To pole jest wymagane!")], format="%H:%M")
    message = TextAreaField("Wiadomość", validators=[DataRequired(message="To pole jest wymagane!")])
    book_button = SubmitField("Zarezerwuj stolik")


class MenuPosition(FlaskForm):
    category = SelectField("Kategoria", choices=[("hot_drinks", "Ciepłe napoje"), ("cold_drinks", "Zimne napoje"), ("desserts", "Desery"), ("special_offers", "Oferty specjalne")])
    name = StringField("Nazwa", validators=[DataRequired(message="To pole jest wymagane!")])
    description = StringField("Opis")
    price = DecimalField("Cena", places=2, validators=[DataRequired(message="To pole jest wymagane!")])
    img_url = StringField("Link do zdjęcia")
    submit_button = SubmitField("Zatwierdź pozycję")


class Login(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!")])
    password = PasswordField("Hasło", validators=[InputRequired(message="To pole jest wymagane!")])
    login_button = SubmitField("login")

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first() is None:
            raise ValidationError('Nie istnieje konto o podanym adresie email')

    def validate_password(self, field):
        user = db.session.query(User).filter_by(email=self.email.data).first()
        if user and field.data != user.password:
            raise ValidationError('Podano błędne hasło!')


class Register(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!"), Email(message="To nie jest poprawny adres email!")])
    password = PasswordField("Hasło", validators=[InputRequired(message="To pole jest wymagane!")])
    confirm_password = PasswordField("Powtórz hasło", validators=[InputRequired(message="To pole jest wymagane!"), EqualTo('password', message="Hasła muszą się zgadzać")])
    first_name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    last_name = StringField("Nazwisko", validators=[DataRequired(message="To pole jest wymagane!")])
    register_button = SubmitField("register")

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Istnieje użytkownik zarejestrowany na podany email!')


class Contact(FlaskForm):
    name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!"), Email(message="To nie jest poprawny adres email!")])
    subject = StringField("Temat", validators=[DataRequired(message="To pole jest wymagane!")])
    message = TextAreaField("Wiadomość", validators=[DataRequired(message="To pole jest wymagane!")])
    submit_button = SubmitField("Wyślij wiadomość")