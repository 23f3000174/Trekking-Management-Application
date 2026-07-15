from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
staff_bp = Blueprint('staff', __name__, url_prefix='/api/staff')
trekker_bp = Blueprint('trekker', __name__, url_prefix='/api/trekker')
from .export_routes import export_bp
from flask_caching import Cache

cache = Cache()

def make_user_cache_key(*args, **kwargs):
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    from flask import request
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        user_id = None
    query_str = "&".join(f"{k}={v}" for k, v in sorted(request.args.items()))
    return f"{request.path}:{user_id or 'anonymous'}:{query_str}"

CORS(auth_bp)
CORS(admin_bp)
CORS(staff_bp)
CORS(trekker_bp)
CORS(export_bp)

auth_api = Api(auth_bp)
admin_api = Api(admin_bp)
staff_api = Api(staff_bp)
trekker_api = Api(trekker_bp)

from .auth import Register, Login
from .admin import Dashboard, StaffList, StaffDetail, TrackList, TrackDetail, TrekkerList, TrekkerDetail, BookingList, BookingDetail, Search
from .staff import StaffDashboard, StaffTrekList, StaffTrekDetail, StaffTrekParticipants, StaffBookingStatus
from .trekker import TrekkerDashboard, TrekkerTrekList, TrekkerTrekDetail, TrekkerBooking, TrekkerBookingList, TrekkerBookingDetail, TrekkerProfile

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

staff_api.add_resource(StaffDashboard, '/dashboard')
staff_api.add_resource(StaffTrekList, '/treks')
staff_api.add_resource(StaffTrekDetail, '/treks/<int:trek_id>')
staff_api.add_resource(StaffTrekParticipants, '/treks/<int:trek_id>/participants')
staff_api.add_resource(StaffBookingStatus, '/bookings/<int:booking_id>')

trekker_api.add_resource(TrekkerDashboard, '/dashboard')
trekker_api.add_resource(TrekkerTrekList, '/treks')
trekker_api.add_resource(TrekkerTrekDetail, '/treks/<int:trek_id>')
trekker_api.add_resource(TrekkerBooking, '/bookings/<int:trek_id>')
trekker_api.add_resource(TrekkerBookingList, '/bookings')
trekker_api.add_resource(TrekkerBookingDetail, '/bookings/<int:booking_id>')
trekker_api.add_resource(TrekkerProfile, '/profile')
