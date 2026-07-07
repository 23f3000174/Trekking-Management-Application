from flask import Blueprint
from flask_restful import Api

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_api = Api(auth_bp)

from .auth import Register, Login

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, 'login')
