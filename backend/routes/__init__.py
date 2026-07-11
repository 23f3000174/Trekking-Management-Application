from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

CORS(auth_bp)
CORS(admin_bp)

auth_api = Api(auth_bp)
admin_api = Api(admin_bp)

from .auth import Register, Login
from .admin import Dashboard, StaffList, StaffDetail, TrackList, TrackDetail, TrekkerList, TrekkerDetail, BookingList, BookingDetail, Search

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')

admin_api.add_resource(Dashboard, '/dashboard')
admin_api.add_resource(StaffList, '/staff_list', '/staff_list/<int:staff_id>')
admin_api.add_resource(StaffDetail, '/staff/<int:staff_id>')
admin_api.add_resource(TrackList, '/trek_list', '/trek_list/<int:trek_id>')
admin_api.add_resource(TrackDetail, '/trek/<int:trek_id>')
admin_api.add_resource(TrekkerList, '/trekker_list', '/trekker_list/<int:trekker_id>')
admin_api.add_resource(TrekkerDetail, '/trekker/<int:trekker_id>')
admin_api.add_resource(BookingList, '/bookings')
admin_api.add_resource(BookingDetail, '/bookings/<int:booking_id>')
admin_api.add_resource(Search, '/search')
