import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    "APP_SETTINGS",
    "config.DevelopmentConfig"
)

app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
