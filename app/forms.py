from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Regexp, Length
from app.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Regexp(r'^[A-Za-z\s]+$', message="Name must contain only letters and spaces.")]) # Added name field

    username = StringField('Username', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message="Password must be between 8 and 20 characters."),
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
            message="Password must contain at least one letter, one number, and one special character."
        )])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class PredictionForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(),Regexp(r'^[A-Za-z\s]+$', message="Name must contain only letters and spaces.")])  # Added name field

    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=120, message="Age must be between 1 and 120.")])

    gender = SelectField('Gender', choices=[(-1, 'Select Gender'), (1, 'Male'), (0, 'Female')],
                         coerce=int, validators=[NumberRange(min=0, max=1, message="This field is required.")])

    cp = SelectField('Chest Pain Type', choices=[(-1, 'Select Chest Pain Type'), (0, 'Typical Angina'), (1, 'Atypical Angina'),
                              (2, 'Non-anginal Pain'), (3, 'Asymptomatic')], coerce=int, validators=[NumberRange(min=0, max=3, message="This field is required.")])

    trestbps = IntegerField('Resting Blood Pressure (mm Hg)', validators=[DataRequired(), NumberRange(min=50, max=250, message="Range is between 50 and 250.")])

    chol = IntegerField('Serum Cholesterol (mg/dl)', validators=[DataRequired(), NumberRange(min=100, max=600, message="Range is between 100 and 600.")])

    fbs = SelectField('Fasting Blood Sugar > 120 mg/dl', choices=[(-1, 'Select Option'),(1, 'True'), (0, 'False')],
                      coerce=int, validators=[NumberRange(min=0, max=1, message="This field is required.")])

    restecg = SelectField('Resting ECG Results', choices=[(-1, 'Select Option'), (0, 'Normal'), (1, 'ST-T Wave Abnormality'), (2, 'Left Ventricular Hypertrophy')],
                          coerce=int, validators=[NumberRange(min=0, max=2, message="This field is required.")])

    thalach = IntegerField('Maximum Heart Rate Achieved', validators=[DataRequired(), NumberRange(min=50, max=250, message="Range is between 50 and 250.")])

    exang = SelectField('Exercise Induced Angina', choices=[(-1, 'Select Option'), (1, 'Yes'), (0, 'No')], coerce=int, validators=[NumberRange(min=0, max=1, message="This field is required.")])

    oldpeak = FloatField('ST Depression Induced by Exercise', validators=[DataRequired(), NumberRange(min=0, max=7, message="Range is between 0 and 7.")])

    slope = SelectField('Slope of Peak Exercise ST Segment',
                        choices=[(-1, 'Select Option'), (0, 'Upsloping'), (1, 'Flat'), (2, 'Downsloping')],
                        coerce=int, validators=[NumberRange(min=0, max=2, message="This field is required.")])

    ca = SelectField('Number of Major Vessels Colored by Fluoroscopy',
                     choices=[(-1, 'Select Option'), (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')],
                     coerce=int, validators=[NumberRange(min=0, max=4, message="This field is required.")])

    thal = SelectField('Thalassemia',
                       choices=[(-1, 'Select Option'), (0, 'Normal'), (1, 'Fixed Defect'), (2, 'Reversible Defect'), (3, 'Unknown')],
                       coerce=int, validators=[NumberRange(min=0, max=3, message="This field is required.")])

    submit = SubmitField('Predict')