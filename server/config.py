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
    ALWAYS use /data/app.db on Railway, instance/app.db locally
    """
    # ALWAYS use /data on Railway - this is the persistent volume
    if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'):
        data_dir = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
        # Ensure the directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        
        db_path = os.path.join(data_dir, "app.db")
        return f'sqlite:///{db_path}'
    
    # Local development only
    return 'sqlite:///instance/app.db'


class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    JSONIFY_PRETTYPRINT_REGULAR = False
    JWT_ACCESS_TOKEN_EXPIRES = False

class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = True

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
    
    env = os.environ.get('FLASK_ENV', config_name)
    config_obj = config.get(env, config['default'])
    app.config.from_object(config_obj)
    
    app.config['ADMIN_TOKEN'] = os.environ.get('ADMIN_TOKEN', 'secret-token-123')
    
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)

    with app.app_context():
        from models import Order, OrderItem, Bag, Hoodie, Tshirt
        db.create_all()

    return app

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api()