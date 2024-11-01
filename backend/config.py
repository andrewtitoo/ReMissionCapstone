import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Define the base directory for easy path management
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    """
    Base configuration class for ReMission.
    Contains default settings used across all environments.
    """

    # Database configuration with a default SQLite database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "database", "remission.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Default secret key for development (change in production!)

    # JWT configurations for authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecretkey')  # Secret key for JWTs
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expiration in seconds (default: 1 hour)

    # General application settings
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """
    Development configuration class for ReMission.
    Enables debugging and uses a development database.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "database", "remission_dev.db")}')


class TestingConfig(Config):
    """
    Testing configuration class for ReMission.
    Uses an in-memory SQLite database for isolated, temporary testing purposes.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')  # In-memory database for tests
    JWT_ACCESS_TOKEN_EXPIRES = 300  # Shorter token lifetime for testing


class ProductionConfig(Config):
    """
    Production configuration class for ReMission.
    Uses the production database with strict security settings.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "database", "remission.db")}')
    DEBUG = False
    TESTING = False


# Dictionary to map environment to the appropriate configuration
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
