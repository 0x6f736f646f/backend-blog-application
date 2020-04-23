from api import db
from api.helpers import response_builder
from api.models.userModel import User
from flask import Blueprint, request
from flask.views import MethodView

auth = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User registration resource
    """

    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    name=post_data.get('name'),
                    photo=post_data.get('photo'),
                    email=post_data.get('email'),
                    bio=post_data.get('bio'),
                    password=post_data.get('password')
                )
                db.session.add(user)
                db.session.commit()
                auth_token = user.encode_auth_token(user.id)
                response = {
                    "status": "success",
                    "message": "Successfully registered",
                    "auth_token": auth_token.decode()
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


registration_view = RegisterAPI.as_view('register_api')
auth.add_url_rule("/auth/register",
                  view_func=registration_view,
                  methods=['POST'])
