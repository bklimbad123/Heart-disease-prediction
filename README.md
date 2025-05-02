# Heart Disease Predictor Web Application

A full-featured Flask web application that predicts heart disease risk based on user input. The application uses a pre-trained machine learning model for predictions and provides a modern, responsive user interface powered by Bootstrap 5.

## Features

- User authentication (register, login, logout)
- Heart disease risk prediction using a pre-trained machine learning model
- Dashboard to view previous prediction reports
- Detailed report view with comprehensive health metrics
- Chart visualization for comparing current and previous health metrics
- Download reports as PDF
- Email reports to users
- Responsive design with Bootstrap 5
- Background images on all pages

## Project Structure

\`\`\`
heart_disease_predictor/
├── app/
│   ├── __init__.py          # App factory and initialization code
│   ├── routes.py            # Flask route definitions
│   ├── models.py            # Database models (User, Report)
│   ├── forms.py             # WTForms classes for handling input forms
│   ├── utils.py             # Utility functions (PDF generation, email sending)
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── auth.css
│   │   │   ├── dashboard.css
│   │   │   ├── form.css
│   │   │   ├── result.css
│   │   │   └── report.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── form-handler.js
│   │   │   ├── chart.js
│   │   │   └── email-report.js
│   │   └── images/
│   │       ├── logo.png
│   │       └── backgrounds/
│   │           ├── index-bg.jpg
│   │           ├── login-bg.jpg
│   │           ├── register-bg.jpg
│   │           ├── dashboard-bg.jpg
│   │           ├── form-bg.jpg
│   │           ├── result-bg.jpg
│   │           └── report-bg.jpg
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── form.html
│   │   ├── result.html
│   │   ├── report.html
│   │   ├── chart.html
│   │   └── pdf_template.html
│   └── model/
│       └── heart_model.pkl  # Pre-trained model for prediction
│
├── instance/
│   └── app.db               # SQLite database file
│
├── .env                     # Environment variables
├── requirements.txt         # List of necessary packages
├── config.py                # Application configuration
├── run.py                   # App entry point
└── README.md                # Project documentation
\`\`\`

## Setup and Installation

1. Clone the repository: