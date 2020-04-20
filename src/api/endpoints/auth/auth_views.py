from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app import bcrypt, db
from models import User, BlacklistToken