
# Wprowadzenie / Introduction

Strona Internetowa wyimaginowanej kawiarnii "Quest", 
stworzona na potrzeby przedmiotu "Inzynieria oprogramowania".
Wizualna część została utworzona na podstawie darmowego szablonu Bootstrap, 
a za część serwerową odpowiedzialny jest framework Flask uruchomiony w serwisie Heroku

Project "Quest" is a website created for a imaginary cafe on purpouse of passing "Software
Engineering" class. Its made with Bootstrap/HTML/CSS and all backend is managed by Flask framework
deployed on Heroku.
## Funkcjonalności / Functionalities
Tworząc aplikację skupiłem się na zaimplementowaniu kluczowych funkcjonalności, 
niezbędnych do usprawnionego działania standardowej kawiarnii.

- Przechowywanie danych z bazie danych PostgreSQL
- Logowanie oraz Rejestracja
- Szyfrowanie haseł metodą hashującą
- Operacje CRUD artykułów oferowanych przez kawiarnię
- Składanie zamówień zapisywanych do konta
- Rezerwowanie stolików

While creating this app I focused on the most important functionalities that a cafe needs.

- Storing data in PostgreSQL database
- Login and Registration
- Passwords hashings
- Articles CRUD operations
- Making orders
- Online table booking
## Wdrożenie systemu / Deployment
W celu umożliwienia dostępu do działającej wersji demonstracyjnej, 
utworzone repozytorium zostało umieszczone na zewnętrznym serwisie Heroku, 
który obsługuje serwer Flask oraz udostępnia bazę danych PostgreSQL.


Created project is running on Flask server deployed with free Heroku service on the link below.
Because of free account unused app is put to sleep after 30min of being idle and that may cause
slow loading so please be patient :)

**[https://kbk-quest.herokuapp.com/](https://kbk-quest.herokuapp.com/)**
## Technologie / Technologies
**Backend**
- Python 3.8
- Flask 2.0.2
- SQLAlchemy 1.4.26
- WTForms 3.0.0
- Jinja2 3.0.2

**Frontend**
- HTML5
- CSS3
- Bootstrap
