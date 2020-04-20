import os
basedir = os.path.abspath(os.path.dirname(__file__))
database_uri = ""
database_name = ""

class BaseConfig:
    """
    Base configurations
    """
    SECRET_KEY = os.getenv()