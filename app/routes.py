import os
import pickle
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, current_app, send_file
from flask_login import login_user, current_user, logout_user, login_required
from app import db, mail
from app.models import User, Report
from app.forms import RegistrationForm, LoginForm, PredictionForm
from app.utils import generate_pdf, send_email_report
import json

# Load the model
model = None


def get_model():
    global model
    if model is None:
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'heart_model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    return model


# Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
prediction = Blueprint('prediction', __name__)


# Main routes
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Heart Disease Predictor')


# Auth routes
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/dashboard')
@login_required
def dashboard():
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.timestamp.desc()).all()
    return render_template('dashboard.html', title='Dashboard', reports=reports)


# Prediction routes
@prediction.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictionForm()
    if form.validate_on_submit():
        # Get form data
        features = [
            form.age.data, form.gender.data, form.cp.data, form.trestbps.data,
            form.chol.data, form.fbs.data, form.restecg.data, form.thalach.data,
            form.exang.data, form.oldpeak.data, form.slope.data, form.ca.data, form.thal.data
        ]

        # Make prediction
        model = get_model()
        features_array = np.array(features).reshape(1, -1)
        prediction_result = model.predict(features_array)[0]
        prediction_proba = model.predict_proba(features_array)[0]
        confidence = prediction_proba[1] if prediction_result == 1 else prediction_proba[0]

        # Save report to database
        report = Report(
            user_id=current_user.id,
            prediction=bool(prediction_result),
            confidence=confidence,
            age=form.age.data,
            gender=form.gender.data,
            cp=form.cp.data,
            trestbps=form.trestbps.data,
            chol=form.chol.data,
            fbs=form.fbs.data,
            restecg=form.restecg.data,
            thalach=form.thalach.data,
            exang=form.exang.data,
            oldpeak=form.oldpeak.data,
            slope=form.slope.data,
            ca=form.ca.data,
            thal=form.thal.data,
            name = form.name.data
        )
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('prediction.result', report_id=report.id))

    return render_template('form.html', title='Prediction Form', form=form)


@prediction.route('/result/<int:report_id>')
@login_required
def result(report_id):
    report = Report.query.get_or_404(report_id)

    # Ensure the report belongs to the current user
    if report.user_id != current_user.id:
        flash('You do not have permission to view this report.', 'danger')
        return redirect(url_for('main.dashboard'))

    return render_template('result.html', title='Prediction Result', report=report)


@prediction.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    report = Report.query.get_or_404(report_id)

    # Ensure the report belongs to the current user
    if report.user_id != current_user.id:
        flash('You do not have permission to view this report.', 'danger')
        return redirect(url_for('main.dashboard'))

    return render_template('report.html', title='Report Details', report=report)


@prediction.route('/chart/<int:report_id>')
@login_required
def chart(report_id):
    report = Report.query.get_or_404(report_id)

    # Ensure the report belongs to the current user
    if report.user_id != current_user.id:
        flash('You do not have permission to view this report.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Get previous reports for comparison
    previous_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.timestamp.desc()).limit(5).all()

    # Generate chart data
    chart_data = {
        'labels': [],
        'current': [],
        'previous': []
    }

    # Prepare data for charts
    feature_names = report.get_feature_names()
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

    for feature in numeric_features:
        chart_data['labels'].append(feature_names[feature])
        chart_data['current'].append(getattr(report, feature))

        # Calculate average of previous reports (excluding current)
        prev_values = [getattr(r, feature) for r in previous_reports if r.id != report.id]
        if prev_values:
            chart_data['previous'].append(sum(prev_values) / len(prev_values))
        else:
            chart_data['previous'].append(0)

    return render_template('chart.html', title='Report Visualization', report=report, chart_data=json.dumps(chart_data))


@prediction.route('/download/<int:report_id>')
@login_required
def download_report(report_id):
    report = Report.query.get_or_404(report_id)

    # Ensure the report belongs to the current user
    if report.user_id != current_user.id:
        flash('You do not have permission to download this report.', 'danger')
        return redirect(url_for('main.dashboard'))

    # Generate PDF
    pdf_file = generate_pdf(report)

    return send_file(
        BytesIO(pdf_file),
        download_name=f'heart_report_{report.id}.pdf',
        as_attachment=True,
        mimetype='application/pdf'
    )


@prediction.route('/email/<int:report_id>', methods=['POST'])
@login_required
def email_report(report_id):
    report = Report.query.get_or_404(report_id)

    # Ensure the report belongs to the current user
    if report.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not have permission to email this report.'})

    # Send email
    try:
        send_email_report(report, current_user.email)
        return jsonify({'success': True, 'message': 'Report sent successfully to your email.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to send email: {str(e)}'})