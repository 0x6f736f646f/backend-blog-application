import os

basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = "postgres://postgres:postgres@localhost:5432/"
database_name = "backend_blog"


class BaseConfig:
    """
    Base configurations
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "backend_blog")
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
    SQLALCHEMY_DATABASE_URI = database_uri + database_name + "_test"


class Development(DevelopmentConfig):
    pass
