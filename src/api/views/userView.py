from api.helpers import response_builder
from api.models.userModel import UserModel
from flask import Blueprint, request
from flask.views import MethodView

user = Blueprint('user', __name__)


class UserApi(MethodView):
    """
    User resource
    """

    def get(self):
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


user_view = UserApi.as_view('user_api')

user.add_url_rule("/auth/status",
                  view_func=user_view,
                  methods=['GET'])
