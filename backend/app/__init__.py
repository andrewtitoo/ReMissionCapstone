from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Create instances of extensions to be used across the application
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    """
    Factory function to create an instance of the Flask application.
    Configures the app, initializes extensions, and registers blueprints.

    Args:
        config_class (class): Configuration class to provide application settings.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Enable CORS for specific origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "An internal error occurred"}, 500

    return app
