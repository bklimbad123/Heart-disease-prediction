import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate


# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()


# def create_app(config_class=Config):
#     # Create and configure the app
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#
#     # Initialize extensions with app
#     db.init_app(app)
#     login_manager.init_app(app)
#     mail.init_app(app)
#
#     # Ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
#     # Register blueprints
#     from app.routes import main, auth, prediction
#     app.register_blueprint(main)
#     app.register_blueprint(auth)
#     app.register_blueprint(prediction)
#
#     # Create database tables
#     with app.app_context():
#         db.create_all()
#
#     return app


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.routes import main, auth, prediction
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(prediction)

    # Create database tables (if not using migrations)
    # with app.app_context():
    #     db.create_all()

    return app
