from api import app, mail
from flask import jsonify
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


def response_builder(data, status_code=200):
    """Build the jsonify response to return."""
    response = jsonify(data)
    response.status_code = status_code
    return response


def generate_confirmation_token(email):
    """We use the URLSafeTimedSerializer to generate a token using the email address
    Actual email address is encoded in the token
    :param email:
    :return token:
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_KEY'])


def confirm_token(token, expiration=3600):
    """As long as the token has not expired it will return the email
    :param token:
    :param expiration:
    :return email:
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            max_age=expiration,
            salt=app.config['SECURITY_PASSWORD_KEY']
        )
    except:
        return False
    return email


def send_mail(to, subject, html):
    message = Message(
        subject=subject,
        recipients=[to],
        html=html,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(message)
