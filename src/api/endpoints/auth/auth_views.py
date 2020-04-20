from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app import bcrypt, db
from models import User, BlacklistToken

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User registration resource
    """
    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(email=post_data.get('email')).first()
        if no user:
            try:
                user = User(
                    name = post_data.get('name'),
                    photo = post_data.get('photo'),
                    email = post_data.get('email'),
                    password = post_data.get('password')
                )
                db.session.add(user)
                db.session.commit()
                auth_token = user.encode_auth_token(user_id=user.id)
                response = {
                    "status": "success",
                    "message": "Successfully registered",
                    "auth_token": auth_token.decode()
                }
                return make_response(jsonify(response)) 201
            except Exception as e:
                response = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again"
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                "status": "fail",
                "message": "User already exists. Please log in"
            }
            return make_response(jsonify(response)), 202

registration_view = RegisterAPI.as_view('register_api')
auth_blueprint.add_url_rule("auth/register",
                            view_func=registration_view,
                            methods=['POST'])