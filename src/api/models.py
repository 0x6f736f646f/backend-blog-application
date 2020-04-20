import datetime
import jwt
from api import app, db, bcrypt


class User(db.Model):
    """
    User model for storing user related details
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text())
    registered_on = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, photo, email, password, bio, role=False):
        self.name = name
        self.photo = photo
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get("BCRYPT_LOG_ROUNDS")
        )
        self.registered_on = datetime.datetime.now()
        self.role = role

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the auth token
        :return string
        """
        try:
            payload = {
                'expiry': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0,
                    seconds=60),
                'time_now': datetime.datetime.utcnow(),
                'user': user_id
            }
            return jwt.encode(payload,
                              app.config.get("SECRET_KEY"),
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token
        :return integer|string
        """
        try:
            payload = jwt.decode(auth_token,
                                 app.config.get("SECRET_KEY"))
            is_blacklist = BlackListToken.check_blacklist(auth_token)
            if is_blacklist:
                return "Token blacklisted. Please log in again"
            else:
                return payload['user']
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again"
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again"


class BlackListToken(db.Model):
    """
    Token model for storing jwt tokens
    """
    __tablename__ = "blacklist_tokens"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return "<id: token: {}>".format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        result = BlackListToken.query.filter_by(token=str(auth_token)).first()
        if result:
            return True
        else:
            return False
