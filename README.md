# Currency Converter

A full-stack currency conversion project built with Python, featuring both a Flask web app and a desktop GUI app. It allows users to sign up, log in, convert currencies, view exchange rates, and keep a personal history of conversions.

This project is ideal for learning full-stack Python app patterns, working with SQLite, building authentication flows, and creating multiple interfaces for the same business logic.

## Why this project?

This repository demonstrates:

- API and web app development with Flask
- User authentication and secure password handling
- Local database storage with SQLite
- GUI development with Python desktop frameworks
- Multi-currency conversion logic and rate handling
- A clean project structure with reusable business logic across apps

## Project Highlights

- User registration and login
- Secure password hashing with Werkzeug
- Currency conversion using predefined exchange rates
- Support for 20+ currencies
- Exchange rate overview page
- Saved conversion history per user
- Local SQLite persistence
- Browser-based web app and desktop app variants

## Tech Stack

- Python 3
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-WTF
- SQLite
- customtkinter
- Flet

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
├── README.md
└── .vscode/
```

## App Versions

### 1) Flask Web Application

The Flask app is the main browser-based version of the project. It includes:

- signup page
- login page
- protected routes
- conversion form
- rates page
- flash messages for validation and auth errors

This version is suited for deployment as a lightweight web application.

### 2) Flet Desktop Application

The Flet app provides a desktop UI experience using `customtkinter`. It includes:

- login/signup screen
- source and target currency selection
- default and custom rate modes
- instant conversion result
- conversion history panel
- local database storage per user

This version is great for desktop demos and standalone usage.

## Features in Detail

### Authentication

Users can sign up with a username and password. Passwords are stored using secure hashing, and users are required to log in to access the conversion features.

### Currency Conversion

The app supports multiple currencies and converts amount values using exchange-rate logic. The project offers both:

- default system-based conversion rates
- custom user-defined rates in the desktop app

### Historical Records

Each user can view previous conversion records and see recent activity associated with their account.

### Rates View

The Flask app includes a dedicated rates page showing supported currency definitions and their basic exchange information.

## Supported Currencies

The application supports the following currencies:

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

## Getting Started

### Prerequisites

Make sure you have Python 3 installed on your machine.

### Clone the repository

```bash
git clone https://github.com/codewithavro/currency_converter.git
cd currency_converter
```

## Running the Flask Web App

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
```

2. Install dependencies:

```bash
pip install -r flask_web/requirements.txt
```

3. Start the app:

```bash
python flask_web/app.py
```

4. Open your browser and visit:

```text
http://127.0.0.1:5000
```

### Flask app user flow

- Sign up for a new account
- Log in
- Convert a value from one currency to another
- View exchange information on the `/rates` page
- Log out when done

## Running the Flet Desktop App

1. Install dependencies:

```bash
pip install -r flet_app/requirements.txt
```

2. Run the app:

```bash
python flet_app/main.py
```

### Desktop app user flow

- Create or log in to an account
- Select source and target currencies
- Enter an amount
- Convert using default or custom rate
- Save and review conversion history

## Database

The project uses SQLite databases for local data persistence.

- Web app database: `instance/currency_converter.db`
- Desktop app database: `flet_app/casheasy.db`

These databases hold user account information and conversion records.

## Configuration Notes

The Flask application sets a default `SECRET_KEY` value for local development. For production use, it is recommended to configure your own secure environment variable:

```bash
export SECRET_KEY="your_secure_secret_key"
```

You should also avoid using the fallback secret in production environments.

## Development Notes

### Web app internals

The Flask app is structured around route handlers in `flask_web/app.py` and HTML templates under `flask_web/templates/`.

Main routes:

- `/` - conversion page
- `/login` - login form
- `/signup` - registration form
- `/rates` - exchange-rate overview
- `/logout` - logout handler

### Desktop app internals

The desktop app contains its own SQLite setup, conversion logic, and UI using custom widgets. User history is stored in a local database and rendered inside the application interface.

## Example Usage

```text
Convert 100 USD to EUR
Result: approximately 85 EUR (based on configured rate)
```

```text
User signs up -> logs in -> selects currencies -> enters amount -> converts -> history saved
```

## Project Goals

This project is designed to:

- teach Python web application development
- showcase authentication and database integration
- demonstrate multiple app interfaces for one product idea
- provide a practical example of currency conversion logic

## Improvement Ideas

Possible future enhancements include:

- real-time exchange rate API integration
- admin dashboard
- dark/light theme toggle
- export conversion history as CSV
- multi-user dashboard
- improved validation and security
- deployment to cloud hosting or Docker

## License

This repository does not currently include a dedicated license file. If you plan to share or distribute the project publicly, consider adding an appropriate open-source license.

## Contributing

Contributions are welcome.

If you want to contribute:

1. Fork the project
2. Create a feature branch
3. Make your improvements
4. Commit your work
5. Open a pull request

## Author

Repository: `codewithavro/currency_converter`

Created for demonstrating a Python-based currency converter with both web and desktop interfaces.
