import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    """
    Base configuration class for ReMission.
    Contains default settings used across all environments.
    """

    #Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite://remission.db') #Use SQLite database as a default
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Default secret key for development (change in production!)

    # JWT configurations
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecretkey')  # Secret key for JWTs
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expiration in seconds (default: 1 hour)

    # Application settings
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configuration class for ReMission.
    Enables debugging and uses a development database.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///remission_dev.db')


class TestingConfig(Config):
    """
    Testing configuration class for ReMission.
    Uses an in-memory SQLite database for testing purposes.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    JWT_ACCESS_TOKEN_EXPIRES = 300  # Shorter token lifetime for testing


class ProductionConfig(Config):
    """
    Production configuration class for ReMission.
    Uses the production database.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL', 'sqlite:///remission_prod.db')  # Update this in production!
    DEBUG = False
    TESTING = False


# Dictionary to map environment to the appropriate configuration
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}