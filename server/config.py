import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import MetaData


def get_database_uri():
    """
    Get database URI with Railway persistent storage support
    """
    # Check if we're on Railway with persistent storage
    if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'):
        # Railway persistent storage path
        data_dir = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
        # Create directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        return f'sqlite:///{os.path.join(data_dir, "skeeps.db")}'
    
    # Fall back to environment variable or default
    return os.environ.get('DATABASE_URI', 'sqlite:///app.db')


class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    JSONIFY_PRETTYPRINT_REGULAR = False
    JWT_ACCESS_TOKEN_EXPIRES = False

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = True  # Optional: show SQL queries in development

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Use the appropriate config based on FLASK_ENV
    env = os.environ.get('FLASK_ENV', config_name)
    config_obj = config.get(env, config['default'])
    app.config.from_object(config_obj)
    
    # Set admin token
    app.config['ADMIN_TOKEN'] = os.environ.get('ADMIN_TOKEN', 'secret-token-123')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)

    with app.app_context():
        from models import Order, OrderItem, Bag, Hoodie, Tshirt
        # Create tables if they don't exist
        db.create_all()

    return app

# Instantiate extensions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api()