from datetime import datetime
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "fallback-dev-secret-key-change-in-production"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///currency_converter.db"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# --- Complete Currency Data ---
CURRENCY_RATES = {
    "USD": {"name": "United States Dollar", "symbol": "$", "rate": 1.0},
    "BDT": {"name": "Bangladeshi Taka", "symbol": "৳", "rate": 110.0},
    "EUR": {"name": "Euro", "symbol": "€", "rate": 0.85},
    "GBP": {"name": "British Pound", "symbol": "£", "rate": 0.75},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "rate": 150.0},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "rate": 83.0},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨", "rate": 280.0},
    "CNY": {"name": "Chinese Yuan", "symbol": "元 / ¥", "rate": 7.2},
    "RUB": {"name": "Russian Ruble", "symbol": "₽", "rate": 90.0},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "rate": 32.0},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "rate": 1350.0},
    "THB": {"name": "Thai Baht", "symbol": "฿", "rate": 36.0},
    "VND": {"name": "Vietnamese Dong", "symbol": "₫", "rate": 25000.0},
    "NGN": {"name": "Nigerian Naira", "symbol": "₦", "rate": 1300.0},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "rate": 5.0},
    "CHF": {"name": "Swiss Franc", "symbol": "CHF", "rate": 0.90},
    "SAR": {"name": "Saudi Riyal", "symbol": "ر.س", "rate": 3.75},
    "AED": {"name": "United Arab Emirates Dirham", "symbol": "د.إ", "rate": 3.67},
    "ZAR": {"name": "South African Rand", "symbol": "R", "rate": 18.0},
    "MXN": {"name": "Mexican Peso", "symbol": "MX$", "rate": 17.0},
}


# --- Database Model ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- Routes ---
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                flash("Please enter a valid amount greater than zero.", "danger")
                return redirect(url_for("index"))

            from_curr = request.form.get("from_curr")
            to_curr = request.form.get("to_curr")

            from_rate = CURRENCY_RATES.get(from_curr, {"rate": 1.0})["rate"]
            to_rate = CURRENCY_RATES.get(to_curr, {"rate": 1.0})["rate"]

            amount_in_usd = amount / from_rate
            result = round(amount_in_usd * to_rate, 2)
        except Exception:
            flash("Error processing conversion.", "danger")

    return render_template(
        "index.html", result=result, currency_rates=CURRENCY_RATES
    )


@app.route("/rates")
@login_required
def rates():
    return render_template("rates.html", currency_rates=CURRENCY_RATES)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Username already exists.", "danger")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="scrypt")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
    