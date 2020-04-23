import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = os.getenv("DATABASE_URI")
database_name = os.getenv("DATABASE_NAME")


class BaseConfig:
    """
    Base configurations
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """
    Development configuration
    """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 7
    SQLALCHEMY_DATABASE_URI = database_uri + database_name


class TestingConfig(BaseConfig):
    """
    Test configuration
    """
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 7
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:5432/backend_blog_test"


class Development(DevelopmentConfig):
    pass
