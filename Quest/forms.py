import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, TextAreaField, DateField, DateTimeField, SelectField, \
    DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError
from werkzeug.security import check_password_hash
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


class Book(FlaskForm):
    # stock table
    number_in_stock = IntegerField("Liczba w magazynie", validators=[DataRequired(message="To pole jest wymagane!")])
    # books_for_sale table
    price = DecimalField("Cena", places=2, validators=[DataRequired(message="To pole jest wymagane!")])
    discount = IntegerField("Zniżka w %", default=0)
    # book info
    title = StringField("Tytuł", validators=[DataRequired(message="To pole jest wymagane!")])
    author = StringField("Autor", validators=[DataRequired(message="To pole jest wymagane!")])
    publisher = StringField("Wydawnictwo", validators=[DataRequired(message="To pole jest wymagane!")])
    genre = SelectField("Gatunek", choices=[("other", "Inny"), ("", "")])
    description = TextAreaField("Opis")
    publish_date = IntegerField("Data publikacji", default=2000)
    image_url = StringField("Link do zdjęcia", default="https://miro.medium.com/max/1400/1*KOAfAOQ9FwAp9i2muTkGWw.png")
    submit_button = SubmitField("Zatwierdź pozycję")

    def validate_publish_date(self,field):
        year = int(field.data)
        if year < 0 or year > datetime.datetime.now().year:
            raise ValidationError('Podano zły rok!')


class MenuPosition(FlaskForm):
    category = SelectField("Kategoria", choices=[("hot_drinks", "Ciepłe napoje"), ("cold_drinks", "Zimne napoje"),
                                                 ("desserts", "Desery"), ("special_offers", "Oferty specjalne")])
    name = StringField("Nazwa", validators=[DataRequired(message="To pole jest wymagane!")])
    description = StringField("Opis")
    price = DecimalField("Cena", places=2, validators=[DataRequired(message="To pole jest wymagane!")], default=0)
    image_url = StringField("Link do zdjęcia", default="https://miro.medium.com/max/1400/1*KOAfAOQ9FwAp9i2muTkGWw.png")
    number_in_stock = IntegerField("Liczba w magazynie", validators=[DataRequired(message="To pole jest wymagane!")])
    submit_button = SubmitField("Zatwierdź pozycję")


class Login(FlaskForm):
    login = StringField("Login", validators=[DataRequired(message="To pole jest wymagane!")])
    password = PasswordField("Hasło", validators=[InputRequired(message="To pole jest wymagane!")])
    login_button = SubmitField("login")

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=field.data).first() is None:
            raise ValidationError('Podane konto nie istnieje')

    def validate_password(self, field):
        user = db.session.query(User).filter_by(login=self.login.data).first()
        if user and not check_password_hash(user.password, field.data):
            raise ValidationError('Podano błędne hasło!')


class Register(FlaskForm):
    login = StringField("Login", validators=[DataRequired(message="To pole jest wymagane!")])
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!"),
                                              Email(message="To nie jest poprawny adres email!")])
    password = PasswordField("Hasło", validators=[InputRequired(message="To pole jest wymagane!")])
    confirm_password = PasswordField("Powtórz hasło", validators=[InputRequired(message="To pole jest wymagane!"),
                                                                  EqualTo('password',
                                                                          message="Hasła muszą się zgadzać")])
    first_name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    last_name = StringField("Nazwisko", validators=[DataRequired(message="To pole jest wymagane!")])
    register_button = SubmitField("register")

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=field.data).first():
            raise ValidationError('Podany login jest zajęty!')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Istnieje użytkownik zarejestrowany na podany email!')


class Contact(FlaskForm):
    name = StringField("Imię", validators=[DataRequired(message="To pole jest wymagane!")])
    email = StringField("E-mail", validators=[DataRequired(message="To pole jest wymagane!"),
                                              Email(message="To nie jest poprawny adres email!")])
    subject = StringField("Temat", validators=[DataRequired(message="To pole jest wymagane!")])
    message = TextAreaField("Wiadomość", validators=[DataRequired(message="To pole jest wymagane!")])
    submit_button = SubmitField("Wyślij wiadomość")
