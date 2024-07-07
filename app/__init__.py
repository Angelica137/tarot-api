from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, TestingConfig, DevelopmentConfig, ProductionConfig


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)

    if isinstance(config_class, TestingConfig):
        app.config.from_object(TestingConfig)
    elif isinstance(config_class, DevelopmentConfig):
        app.config.from_object(DevelopmentConfig)
    elif isinstance(config_class, ProductionConfig):
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
