import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import MetaData


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    JSONIFY_PRETTYPRINT_REGULAR = False
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens will not expire for this example

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI','sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    JSONIFY_PRETTYPRINT_REGULAR = False
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens will not expire for this example


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
ADMIN_TOKEN = "secret-token-123"  # Store securely in env variables in production

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Set admin token here:
    app.config['ADMIN_TOKEN'] = os.environ.get('ADMIN_TOKEN', 'secret-token-123')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)

    with app.app_context():
        from models import Order, OrderItem, Bag,Hoodie, Tshirt

    return app

# Instantiate extensions (deferred to use with app factory)
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api()
