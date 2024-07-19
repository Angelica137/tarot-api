import logging
from flask import Flask, session, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, TestingConfig, DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()


db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()


# Factory pattern
def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configuration
    if isinstance(config_class, str):
        if config_class == "testing":
            app.config.from_object(TestingConfig)
            app.config["TESTING"] = True
            app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "test-secret-key")
        elif config_class == "development":
            app.config.from_object(DevelopmentConfig)
        elif config_class == "production":
            app.config.from_object(ProductionConfig)
        else:
            app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    # Use environment variable if set, otherwise use the config object
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        os.getenv("DATABASE_URL") or app.config["SQLALCHEMY_DATABASE_URI"]
    )

    @app.before_request
    def add_auth_token():
        if "access_token" in session:
            g.access_token = session["access_token"]
            app.logger.info("Access token added to g object")
        else:
            g.access_token = None
            app.logger.info("No access token in session")

    # Set up extensions
    # CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    # Auth0 configuration
    app.config["AUTH0_DOMAIN"] = os.getenv("AUTH0_DOMAIN")
    app.config["AUTH0_AUDIENCE"] = os.getenv("API_AUDIENCE")
    app.config["AUTH0_CLIENT_ID"] = os.getenv("AUTH0_CLIENT_ID")
    app.config["AUTH0_CLIENT_SECRET"] = os.getenv("AUTH0_CLIENT_SECRET")

    # Import models
    from app.all_models import User, Reading, Spread, SpreadCard, Card, SpreadLayout

    # Register blueprints
    from app.routes.card_routes import api as card_api_blueprint

    app.register_blueprint(card_api_blueprint, url_prefix="/api")

    from app.routes.spread_routes import spread_api_bp

    app.register_blueprint(spread_api_bp, url_prefix="/api")

    from app.routes.reading_route import reading_api_bp

    app.register_blueprint(reading_api_bp, url_prefix="/api")

    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api")

    if isinstance(config_class, str) and config_class in ["development", "testing"]:
        from app.routes.dev_routes import utility_bp

        app.register_blueprint(utility_bp, url_prefix="/dev")
    elif config_class in [DevelopmentConfig, TestingConfig]:
        from app.routes.dev_routes import utility_bp

        app.register_blueprint(utility_bp, url_prefix="/dev")

    from app.routes.error_handlers import register_error_handlers

    register_error_handlers(app)

    app.secret_key = os.getenv("APP_SECRET_KEY")

    return app
