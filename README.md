# Currency Converter

A Python project that includes a Flask web application and a Flet desktop application for converting between currencies with user authentication, exchange-rate views, and conversion history.

## Overview

This repository contains two implementations of the same currency conversion concept:

- Flask web app with sign-up, login, conversion, and rate display
- Flet desktop app with customtkinter-based UI and local SQLite storage

The Flask app is the main web interface and is designed for browser-based use, while the Flet app provides a standalone desktop experience.

## Features

- User registration and login
- Secure password hashing
- Currency conversion using predefined exchange rates
- Support for multiple currencies
- View exchange-rate information
- Save and view recent conversion history
- Local SQLite database persistence
- Separate app entry points for web and desktop use

## Tech Stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-WTF
- SQLite
- Flet
- customtkinter

## Repository Structure

```text
currency_converter/
├── flask_web/
│   ├── app.py
│   ├── requirements.txt
│   ├── tempCodeRunnerFile.py
│   ├── 10358.jpg
│   ├── static/
│   ├── templates/
│   └── instance/
├── flet_app/
│   ├── main.py
│   ├── requirements.txt
│   ├── tempCodeRunnerFile.py
│   ├── casheasy.db
│   ├── description.txt
│   └── assets/
├── instance/
│   └── currency_converter.db
├── curency symbol.txt
├── .gitattributes
└── README.md
```

## Flask Web App

The web app is located in `flask_web/` and provides a browser-based experience with authentication and currency conversion features.

### Run the Flask app

1. Open a terminal in the project root.
2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r flask_web/requirements.txt
```

4. Start the application:

```bash
python flask_web/app.py
```

5. Open the app in your browser:

```text
http://127.0.0.1:5000
```

### Flask app features

- Sign-up and login pages
- Protected routes using Flask-Login
- Currency conversion form
- Exchange-rate overview page at `/rates`
- SQLite-backed user storage
- Flash-based messaging for validation and login errors

## Flet Desktop App

The desktop app is located in `flet_app/` and provides a GUI-based experience using Flet and customtkinter.

### Run the Flet app

1. Navigate to the project root.
2. Install dependencies:

```bash
pip install -r flet_app/requirements.txt
```

3. Start the desktop app:

```bash
python flet_app/main.py
```

### Flet app features

- Sign in / sign up screen
- Currency conversion form with amount input
- Source and target currency selection
- Default and custom exchange rates
- Conversion history saved per user
- Local SQLite database for user accounts and conversion records

## Database

The project uses SQLite for persistence:

- Web app database: `instance/currency_converter.db`
- Desktop app database: `flet_app/casheasy.db`

These databases store user accounts and conversion data locally.

## Default Currency Support

The application supports a range of commonly used currencies, including:

- USD
- BDT
- EUR
- GBP
- JPY
- INR
- PKR
- CNY
- RUB
- TRY
- KRW
- THB
- VND
- NGN
- BRL
- CHF
- SAR
- AED
- ZAR
- MXN

## Notes

- The Flask app uses a `SECRET_KEY` with a fallback development value. For production, set your own environment variable:

```bash
export SECRET_KEY="your_secure_secret_key"
```

- The app is intended for learning, demo, and local-development use.

## License

This project does not appear to include an explicit license file. If you plan to distribute or reuse this code, add a suitable license as needed.

## Contributing

Contributions are welcome. If you want to improve the app, add features, or fix issues:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## Author

Project repository: `codewithavro/currency_converter`
