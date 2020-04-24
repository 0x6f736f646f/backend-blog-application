from api import db, bcrypt
from api.helpers import (response_builder,
                         generate_confirmation_token,
                         confirm_token,
                         send_mail)
from api.models.userModel import UserModel, BlackListToken
from flask import Blueprint, request, url_for
from flask.views import MethodView

auth = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User registration resource
    """

    def post(self):
        post_data = request.get_json()
        user = UserModel.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = UserModel(post_data)
                db.session.add(user)
                db.session.commit()
                auth_token = UserModel.encode_auth_token(user_id=user.id)
                validated_user = UserModel.query.filter_by(id=user.id).first()
                token = generate_confirmation_token(validated_user.email)
                confirm_url = url_for("auth.confirm_email_api",
                                      token=token,
                                      _external=True)
                send_mail(user.email, "Please confirm email", confirm_url)
                response = {
                    "status": "success",
                    "message":
                        "Successfully registered. "
                        "Confirmation email has been sent to your email",
                    "auth_token": auth_token.decode(),
                    "user_data": {
                        "name": validated_user.id,
                        "photo": validated_user.photo,
                        "email": validated_user.email,
                        "bio": validated_user.bio,
                        "role": validated_user.role
                    }
                }
                return response_builder(response, 201)
            except Exception as e:
                response = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again",
                    "error": e
                }
                return response_builder(response, 401)
        else:
            response = {
                "status": "fail",
                "message": "User already exists. Please log in"
            }
            return response_builder(response, status_code=202)


class LoginApi(MethodView):
    """
    User login resource
    """

    def post(self):
        post_data = request.get_json()
        print(post_data)
        try:
            user = UserModel.query.filter_by(
                email=post_data.get('email')).first()
            if user and bcrypt.check_password_hash(
                    user.password, post_data.get("password")):
                print(user.id)
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response = {
                        "status": "success",
                        "message": "Successfully logged in",
                        "auth_token": auth_token.decode()
                    }
                    return response_builder(response, 200)
            else:
                response = {
                    "status": "fail",
                    "message": "User does not exist",
                }
                return response_builder(response, 404)
        except Exception as e:
            response = {
                "status": "fail",
                "message": "Try again",
                "erro": e
            }
            return response_builder(response, 500)


class LogoutApi(MethodView):
    """
    Logout resource
    """

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response = {
                    "status": "fail",
                    "message": "Bearer token malformed"
                }
                return response_builder(response, 401)
        else:
            auth_token = ""
        if auth_token:
            response = UserModel.decode_auth_token(auth_token)
            if not isinstance(response, str):
                blacklist_token = BlackListToken(token=auth_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response = {
                        "status": "success",
                        "message": "Successfully logged out"
                    }
                    return response_builder(response, 200)
                except Exception as e:
                    response = {
                        "status": "fail",
                        "message": e
                    }
                    response_builder(response, 200)

                user = UserModel.query.filter_by(id=response).first()
                response = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                        "registered_on": user.registered_on
                    }
                }
                return response_builder(response, 200)
            else:
                response = {
                    "status": "fail",
                    "message": response,
                }
                return response_builder(response, 401)
        else:
            response = {
                "status": "fail",
                "message": "Provide a valid token"
            }
            return response_builder(response, status_code=202)


class ConfirmEmail(MethodView):

    def get(self, token):
        try:
            email = confirm_token(token)
        except Exception as e:
            response = {
                "status": "fail",
                "message": "The confirmation link is invalid or has expired",
                "error": e
            }
            return response_builder(response, status_code=202)
        user = UserModel.query.filter_by(email=email).first()
        if user.confirmed:
            response = {
                "status": "fail",
                "message": "The confirmation link is invalid or has expired"
            }
            return response_builder(response, status_code=202)
        else:
            user.update_confirmation()
            response = {
                "status": "fail",
                "message": "You have confirmed your account"
            }
            return response_builder(response, status_code=202)


registration_view = RegisterAPI.as_view('register_api')
login_view = LoginApi.as_view('login_api')
logout_view = LogoutApi.as_view('logout_api')
confirm_email_view = ConfirmEmail.as_view('confirm_email_api')

auth.add_url_rule("/auth/register",
                  view_func=registration_view,
                  methods=['POST'])
auth.add_url_rule("/auth/login",
                  view_func=login_view,
                  methods=['POST'])
auth.add_url_rule("/auth/logout",
                  view_func=logout_view,
                  methods=['POST'])
auth.add_url_rule("/auth/confirm/<token>",
                  view_func=confirm_email_view,
                  methods=['GET'])
