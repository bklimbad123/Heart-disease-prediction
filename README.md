# Heart Disease Prediction

A Flask web application that uses a bundled, pre-trained machine-learning model to estimate heart-disease risk from user-provided health measurements. Users can register, submit predictions, review saved reports and charts, and download reports as PDFs. Emailing reports is available when SMTP settings are configured.

> **Important:** This project is for educational and demonstration purposes only. Its prediction is not a diagnosis or a substitute for advice from a qualified healthcare professional.

## Features

- User registration, login, and logout
- Heart-disease risk prediction using `app/model/heart_model.pkl`
- A personal dashboard with saved prediction reports
- Report detail pages and comparisons of health measurements
- PDF report downloads
- Optional email delivery of reports
- SQLite storage for users and reports

## Requirements

- Python 3.11 is recommended. The pinned scientific Python packages in `requirements.txt` are most straightforward to install with this version.
- `pip` and `venv` (included with most Python installations)
- Git, if you are cloning the project
- Internet access for installing packages

No training dataset is needed to run the web app: the pre-trained model is included in the repository. PDF generation has a ReportLab fallback; installing the separate `wkhtmltopdf` operating-system program is optional.

## Install and Run

Run these commands from the project root, the directory containing `run.py` and `requirements.txt`.

### 1. Get the project

If you have not already downloaded or cloned it:

```bash
git clone <repository-url>
cd Heart-disease-prediction
```

Replace `<repository-url>` with the repository's clone URL. If the project is already open in VS Code, open a terminal in its root directory instead.

### 2. Create and activate a virtual environment

**Linux or macOS:**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow it for the current terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

When activated, the terminal prompt normally shows `(.venv)`. If Python 3.11 is installed under a different command on your system, use that interpreter to create the environment.

### 3. Install dependencies

With the virtual environment active:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Initialize the database

Apply the included database migration once for a new local installation:

```bash
python -m flask --app run.py db upgrade
```

This creates or updates the SQLite database at `instance/database.db`. The application factory initializes Flask-Migrate but does not create the database tables automatically, so do not skip this step on a fresh setup.

### 5. Start the development server

```bash
python run.py
```

The app runs in Flask debug mode and is normally available at [http://127.0.0.1:5000](http://127.0.0.1:5000). You can also start it with Flask's CLI:

```bash
python -m flask --app run.py run --debug
```

Stop the development server with `Ctrl+C` in the terminal. For a different port, use `python -m flask --app run.py run --debug --port 5001`.

## Use the App

1. Open `http://127.0.0.1:5000` in a browser.
2. Register an account, then log in.
3. Open the prediction form, enter the requested measurements, and submit it.
4. View the result, then use the dashboard to revisit saved reports and their charts or download a PDF.

New accounts and prediction reports are stored in the local SQLite database. The model is loaded when the first prediction is submitted.

## Optional Configuration

The app can run without email configured. To enable email delivery, create a `.env` file in the project root and set values for an SMTP account your provider permits for application use:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-smtp-username
MAIL_PASSWORD=your-smtp-password
MAIL_DEFAULT_SENDER=your-sender@example.com
```

Replace the example values with your provider's actual SMTP settings. Keep `.env` private and never commit real credentials. `SECRET_KEY` should be set to a long, randomly generated value outside local development; the built-in fallback is intended only for development. Email sending will fail until valid SMTP settings are present.

PDF downloads use `pdfkit` and the external `wkhtmltopdf` executable when it is available. If that executable is missing or PDF generation through it fails, the application falls back to ReportLab, which is installed from `requirements.txt`.

## Project Layout

```text
.
├── app/
│   ├── __init__.py          # Flask app factory and extension setup
│   ├── forms.py             # Registration, login, and prediction forms
│   ├── models.py            # User and prediction-report database models
│   ├── routes.py            # Pages, authentication, prediction, and reports
│   ├── utils.py             # PDF and email helpers
│   ├── model/
│   │   └── heart_model.pkl  # Pre-trained prediction model
│   ├── static/
│   │   ├── css/             # Page stylesheets
│   │   ├── image/           # Background images
│   │   └── js/              # Browser-side scripts
│   └── templates/            # Jinja HTML templates
├── instance/                 # Local SQLite database
├── migrations/               # Flask-Migrate/Alembic schema history
├── config.py                 # Database, secret, and mail configuration
├── requirements.txt          # Pinned Python dependencies
├── run.py                    # Development entry point
└── README.md
```

## Troubleshooting

- **`ModuleNotFoundError` while starting:** Activate `.venv` in the project root and run `python -m pip install -r requirements.txt` again.
- **A database table is missing:** From the project root, activate `.venv` and run `python -m flask --app run.py db upgrade`.
- **The prediction model cannot be opened:** Confirm that `app/model/heart_model.pkl` exists; it must remain at that path for predictions to work.
- **Email sending fails:** Check the SMTP host, port, TLS setting, sender, username, and provider-specific authentication requirements in `.env`.
- **Port 5000 is already in use:** Start the Flask CLI server on another port, for example `python -m flask --app run.py run --debug --port 5001`.

## Notes

- Run commands from the project root so Flask can find `run.py`, migrations, and configuration.
- `python run.py` enables Flask debug mode and is intended for local development, not production deployment.
- The local database contains account and health-report information; treat it as sensitive and do not publish it.