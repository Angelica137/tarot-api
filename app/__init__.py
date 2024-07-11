from flask import Flask
from config import Config, TestingConfig, DevelopmentConfig, ProductionConfig
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)

    if isinstance(config_class, str):
        if config_class == 'testing':
            app.config.from_object(TestingConfig)
        elif config_class == 'development':
            app.config.from_object(DevelopmentConfig)
        elif config_class == 'production':
            app.config.from_object(ProductionConfig)
        else:
            app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from app.routes.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app.models import Spread, Card, SpreadCard, SpreadLayout
