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
    SECURITY_PASSWORD_KEY = os.getenv("SECURITY_PASSWORD_KEY")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_SENDER")


class DevelopmentConfig(BaseConfig):
    """
    Development configuration
    """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 7
    SQLALCHEMY_DATABASE_URI = database_uri + database_name
    SECURITY_PASSWORD_KEY = os.getenv("SECURITY_PASSWORD_KEY")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_SENDER")


class TestingConfig(BaseConfig):
    """
    Test configuration
    """
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 7
    SQLALCHEMY_DATABASE_URI = os.getenv(""
                                        "")


class Development(DevelopmentConfig):
    pass
