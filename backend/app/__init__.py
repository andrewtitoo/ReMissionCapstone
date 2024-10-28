from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Create instances of extensions to be used across the application
db = SQLAlchemy()  # SQLAlchemy instance for database interaction
bcrypt = Bcrypt()  # Bcrypt instance for password hashing
jwt = JWTManager()  # JWTManager instance for managing JWT tokens

def create_app(config_class=Config):
    """
    Factory function to create an instance of the Flask application.
    Configures the app, initializes extensions, and registers blueprints.

    Args:
        config_class (class): Configuration class to provide application settings.

    Returns:
        Flask: Configured Flask application instance.
    """

    # Create an instance of the Flask app
    app = Flask(__name__)

    # Load configuration settings from the provided Config class
    app.config.from_object(config_class)

    # Initialize extensions with the Flask app
    db.init_app(app)  # Bind SQLAlchemy to the Flask app
    bcrypt.init_app(app)  # Bind Bcrypt to the Flask app for password hashing
    jwt.init_app(app)  # Bind JWTManager to the Flask app for JWT authentication
    CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for interacting with frontend

    # Register blueprints for modular routes
    from .routes import bp as routes_bp  # Relative import of blueprint from 'routes.py'
    app.register_blueprint(routes_bp, url_prefix='/api')  # Register blueprint with '/api' prefix

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """
        Handle 404 - Not Found errors.

        Args:
            error (Exception): The raised 404 error.

        Returns:
            dict: JSON response indicating resource not found.
        """
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 - Internal Server errors.

        Args:
            error (Exception): The raised 500 error.

        Returns:
            dict: JSON response indicating an internal server error.
        """
        return {"error": "An internal error occurred"}, 500

    return app

