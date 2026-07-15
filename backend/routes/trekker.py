from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.models import db, User, Trekker, Trek, Booking, UserRole, UserStatus, Difficulty, Gender, TrekStatus, BookingStatus
from datetime import datetime
from . import cache, make_user_cache_key


def trekker():
    claims = get_jwt()
    return claims['role'] == 'trekker'


def get_current_trekker():
    user_id = int(get_jwt_identity())
    return Trekker.query.get(user_id)

# ==================================================================================================

class TrekkerDashboard(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        if not current:
            return {'message': 'Trekker profile not found'}, 404

        open_treks = Trek.query.filter(Trek.trek_status == TrekStatus.OPEN).all()
        open_list = []
        for t in open_treks:
            open_list.append({
                'id'              : t.id,
                'trek_name'       : t.trek_name,
                'trek_location'   : t.trek_location,
                'difficulty'      : t.difficulty.value,
                'duration_days'   : t.duration_days,
                'available_slot'  : t.available_slot,
                'total_slot'      : t.total_slot,
                'start_date'      : str(t.start_date),
                'end_date'        : str(t.end_date),
            })

        my_bookings = current.user.bookings.all()
        booked_list = []
        for b in my_bookings:
            booked_list.append({
                'booking_id'      : b.id,
                'trek_id'         : b.trek.id,
                'trek_name'       : b.trek.trek_name,
                'trek_location'   : b.trek.trek_location,
                'trek_status'     : b.trek.trek_status.value,
                'booking_date'    : str(b.booking_date),
                'booking_status'  : b.booking_status.value,
                'start_date'      : str(b.trek.start_date),
            })

        return {
            'id'             : current.id,
            'full_name'      : current.user.full_name,
            'email'          : current.user.email,
            'available_treks': open_list,
            'total_available': len(open_list),
            'my_bookings'    : booked_list,
            'total_bookings' : len(booked_list),
        }, 200

# ==================================================================================================

class TrekkerTrekList(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        query = Trek.query.filter(Trek.trek_status == TrekStatus.OPEN)

        difficulty = request.args.get('difficulty')
        location = request.args.get('location')
        duration = request.args.get('duration')

        if difficulty:
            try:
                query = query.filter(Trek.difficulty == Difficulty(difficulty))
            except ValueError:
                return {'message': 'Invalid difficulty filter'}, 400

        if location:
            query = query.filter(Trek.trek_location.ilike(f'%{location}%'))

        if duration:
            try:
                query = query.filter(Trek.duration_days == int(duration))
            except ValueError:
                return {'message': 'Invalid duration filter'}, 400

        treks = query.all()
        result = []
        for t in treks:
            result.append({
                'id'             : t.id,
                'trek_name'      : t.trek_name,
                'trek_location'  : t.trek_location,
                'description'    : t.description,
                'difficulty'     : t.difficulty.value,
                'duration_days'  : t.duration_days,
                'available_slot' : t.available_slot,
                'total_slot'     : t.total_slot,
                'start_date'     : str(t.start_date),
                'end_date'       : str(t.end_date),
            })
        return result, 200

# ==================================================================================================

class TrekkerTrekDetail(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self, trek_id):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message': 'Trek not found'}, 404

        current = get_current_trekker()
        my_booking = Booking.query.filter_by(user_id=current.id, trek_id=trek.id, deleted_by_trekker=False).first()

        assigned_staff = None
        if trek.staff:
            assigned_staff = {
                'full_name': trek.staff.user.full_name,
                'email'    : trek.staff.user.email,
            }

        return {
            'id'             : trek.id,
            'trek_name'      : trek.trek_name,
            'trek_location'  : trek.trek_location,
            'description'    : trek.description,
            'difficulty'     : trek.difficulty.value,
            'trek_status'    : trek.trek_status.value,
            'duration_days'  : trek.duration_days,
            'total_slot'     : trek.total_slot,
            'available_slot' : trek.available_slot,
            'start_date'     : str(trek.start_date),
            'end_date'       : str(trek.end_date),
            'assigned_staff' : assigned_staff,
            'my_booking'     : my_booking.booking_status.value if my_booking else None,
        }, 200

# ==================================================================================================

class TrekkerBooking(Resource):
    @jwt_required()
    def post(self, trek_id):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        if not current:
            return {'message': 'Trekker profile not found'}, 404

        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message': 'Trek not found'}, 404

        if trek.trek_status != TrekStatus.OPEN:
            return {'message': 'Trek is not open for booking'}, 400

        if trek.available_slot <= 0:
            return {'message': 'No slots available'}, 400

        existing = Booking.query.filter_by(user_id=current.id, trek_id=trek.id).first()
        if existing:
            if existing.deleted_by_trekker or existing.booking_status == BookingStatus.CANCELLED:
                existing.booking_status = BookingStatus.BOOKED
                existing.deleted_by_trekker = False
                existing.cancellation_date = None
                existing.cancelled_by = None
                existing.booking_date = datetime.utcnow()
                trek.available_slot -= 1
                db.session.commit()
                cache.clear()
                return {
                    'message'        : 'Booking re-confirmed',
                    'booking_id'     : existing.id,
                    'trek_name'      : trek.trek_name,
                    'booking_status' : existing.booking_status.value,
                    'available_slot' : trek.available_slot,
                }, 200
            else:
                return {'message': 'You have already booked this trek'}, 409

        new_booking = Booking(user_id=current.id, trek_id=trek.id)
        db.session.add(new_booking)
        trek.available_slot -= 1
        db.session.commit()
        cache.clear()

        return {
            'message'        : 'Booking confirmed',
            'booking_id'     : new_booking.id,
            'trek_name'      : trek.trek_name,
            'booking_status' : new_booking.booking_status.value,
            'available_slot' : trek.available_slot,
        }, 201

# ==================================================================================================

class TrekkerBookingList(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        if not current:
            return {'message': 'Trekker profile not found'}, 404

        bookings = current.user.bookings.filter_by(deleted_by_trekker=False).all()
        result = []
        for b in bookings:
            result.append({
                'booking_id'      : b.id,
                'trek_id'         : b.trek.id,
                'trek_name'       : b.trek.trek_name,
                'trek_location'   : b.trek.trek_location,
                'difficulty'      : b.trek.difficulty.value,
                'trek_status'     : b.trek.trek_status.value,
                'booking_date'    : str(b.booking_date),
                'booking_status'  : b.booking_status.value,
                'cancellation_date': str(b.cancellation_date) if b.cancellation_date else None,
                'start_date'      : str(b.trek.start_date),
                'end_date'        : str(b.trek.end_date),
            })
        return result, 200

# ==================================================================================================

class TrekkerBookingDetail(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self, booking_id):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        booking = Booking.query.get(booking_id)
        if not booking or booking.deleted_by_trekker:
            return {'message': 'Booking not found'}, 404

        if booking.user_id != current.id:
            return {'message': 'You can only view your own bookings'}, 403

        return {
            'booking_id'       : booking.id,
            'booking_date'     : str(booking.booking_date),
            'booking_status'   : booking.booking_status.value,
            'cancellation_date': str(booking.cancellation_date) if booking.cancellation_date else None,
            'trek': {
                'id'          : booking.trek.id,
                'trek_name'   : booking.trek.trek_name,
                'trek_location': booking.trek.trek_location,
                'difficulty'  : booking.trek.difficulty.value,
                'trek_status' : booking.trek.trek_status.value,
                'start_date'  : str(booking.trek.start_date),
                'end_date'    : str(booking.trek.end_date),
            },
        }, 200

# -------------------------------------------------------------------------------------------------
    @jwt_required()
    def put(self, booking_id):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        booking = Booking.query.get(booking_id)
        if not booking or booking.deleted_by_trekker:
            return {'message': 'Booking not found'}, 404

        if booking.user_id != current.id:
            return {'message': 'You can only cancel your own bookings'}, 403

        if booking.booking_status == BookingStatus.CANCELLED:
            return {'message': 'Booking is already cancelled'}, 400

        if booking.booking_status == BookingStatus.COMPLETED:
            return {'message': 'Cannot cancel a completed booking'}, 400

        data = request.get_json() or {}
        if data.get('booking_status') != BookingStatus.CANCELLED.value:
            return {'message': 'Trekkers can only cancel bookings'}, 400

        booking.booking_status = BookingStatus.CANCELLED
        booking.cancellation_date = datetime.utcnow()
        booking.cancelled_by = 'trekker'
        trek = booking.trek
        if trek.available_slot < trek.total_slot:
            trek.available_slot += 1

        db.session.commit()
        cache.clear()
        return {
            'message'        : 'Booking cancelled',
            'booking_status' : booking.booking_status.value,
            'available_slot' : trek.available_slot,
        }, 200

    @jwt_required()
    def delete(self, booking_id):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        booking = Booking.query.get(booking_id)
        if not booking or booking.deleted_by_trekker:
            return {'message': 'Booking not found'}, 404

        if booking.user_id != current.id:
            return {'message': 'You can only delete your own bookings'}, 403

        booking.deleted_by_trekker = True
        db.session.commit()
        cache.clear()
        return {'message': 'Booking deleted'}, 200

# ==================================================================================================

class TrekkerProfile(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        if not current:
            return {'message': 'Trekker profile not found'}, 404

        return {
            'id'               : current.id,
            'full_name'        : current.user.full_name,
            'email'            : current.user.email,
            'mobile_no'        : current.user.mobile_no,
            'dob'              : str(current.dob),
            'gender'           : current.gender.value,
            'emergency_contact': current.emergency_contact,
            'flag'             : current.user.flag.value,
        }, 200

# -------------------------------------------------------------------------------------------------
    @jwt_required()
    def put(self):
        if not trekker():
            return {'message': 'Unauthorized'}, 403

        current = get_current_trekker()
        if not current:
            return {'message': 'Trekker profile not found'}, 404

        data = request.get_json()

        if 'full_name' in data:
            current.user.full_name = data['full_name']
        if 'mobile_no' in data:
            current.user.mobile_no = data['mobile_no']
        if 'emergency_contact' in data:
            current.emergency_contact = data['emergency_contact']
        if 'dob' in data:
            try:
                current.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                return {'message': 'Invalid dob format (YYYY-MM-DD)'}, 400
        if 'gender' in data:
            try:
                current.gender = Gender(data['gender'])
            except ValueError:
                return {'message': 'Invalid gender'}, 400

        db.session.commit()
        cache.clear()
        return {'message': 'Profile updated'}, 200
