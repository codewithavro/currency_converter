from datetime import datetime
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
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"  # Change this to a secure random key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///currency_converter.db"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# --- Database Models ---
class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(150), nullable=False)
  conversions = db.relationship("ConversionHistory", backref="user", lazy=True)


class ConversionHistory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  from_curr = db.Column(db.String(10), nullable=False)
  to_curr = db.Column(db.String(10), nullable=False)
  amount = db.Column(db.Float, nullable=False)
  result = db.Column(db.Float, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


# --- Routes ---
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
  result = None
  if request.method == "POST":
    try:
      amount = float(request.form.get("amount"))
      from_curr = request.form.get("from_curr")
      to_curr = request.form.get("to_curr")

      # Simple conversion logic (replace or integrate your existing conversion rates)
      rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.75, "INR": 83.0}
      amount_in_usd = amount / rates.get(from_curr, 1.0)
      result = amount_in_usd * rates.get(to_curr, 1.0)

      # Save conversion record to the database
      new_conversion = ConversionHistory(
          from_curr=from_curr,
          to_curr=to_curr,
          amount=amount,
          result=round(result, 2),
          user_id=current_user.id,
      )
      db.session.add(new_conversion)
      db.session.commit()
    except Exception as e:
      flash("Error processing conversion.", "danger")

  # Fetch past conversion history for the logged-in user
  history = (
      ConversionHistory.query.filter_by(user_id=current_user.id)
      .order_by(ConversionHistory.timestamp.desc())
      .all()
  )
  return render_template("index.html", result=result, history=history)


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
    db.create_all()  # Automatically creates the SQLite database file
  app.run(debug=True)