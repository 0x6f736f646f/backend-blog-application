import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    "APP_SETTINGS",
    "api.config.DevelopmentConfig"
)

app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.auth_views import auth
app.register_blueprint(auth)
