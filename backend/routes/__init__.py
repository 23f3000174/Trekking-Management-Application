from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
CORS(auth_bp)
auth_api = Api(auth_bp)

from .auth import Register, Login

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
