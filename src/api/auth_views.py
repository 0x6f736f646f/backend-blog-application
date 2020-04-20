from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from api import db
from api.models import User

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
                auth_token = user.encode_auth_token(user_id=user.id)
                response = {
                    "status": "success",
                    "message": "Successfully registered",
                    "auth_token": auth_token
                }
                return make_response(jsonify(response))
            except Exception as e:
                response = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again",
                    "error": e
                }
                return make_response(jsonify(response))
        else:
            response = {
                "status": "fail",
                "message": "User already exists. Please log in"
            }
            return make_response(jsonify(response))


registration_view = RegisterAPI.as_view('register_api')
auth.add_url_rule("/auth/register",
                  view_func=registration_view,
                  methods=['POST'])
