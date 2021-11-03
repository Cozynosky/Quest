from flask import Flask, render_template

# setup app
app = Flask(__name__)
app.config['SECRET_KEY'] = "kawiarnia_ksiegarnia_quest"


# obsluga strony glownej
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


if __name__ == "__main__":
    app.run(debug=True)
