from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.models import db, User, Staff, Trek, Booking, UserRole, UserStatus, TrekStatus, BookingStatus
from datetime import datetime
from . import cache, make_user_cache_key


def staff():
    claims = get_jwt()
    return claims['role'] == 'staff'


def get_current_staff():
    user_id = int(get_jwt_identity())
    return Staff.query.get(user_id)

# ==================================================================================================

class StaffDashboard(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self):
        if not staff():
            return {'message': 'Unauthorized'}, 403

        current = get_current_staff()
        if not current:
            return {'message': 'Staff profile not found'}, 404

        treks = current.assigned_treks.all()
        trek_list = []
        total_participants = 0
        for trek in treks:
            booked_count = trek.bookings.filter(
                Booking.booking_status == BookingStatus.BOOKED
            ).count()
            total_participants += booked_count
            trek_list.append({
                'id'             : trek.id,
                'trek_name'      : trek.trek_name,
                'trek_location'  : trek.trek_location,
                'trek_status'    : trek.trek_status.value,
                'difficulty'     : trek.difficulty.value,
                'available_slot' : trek.available_slot,
                'total_slot'     : trek.total_slot,
                'start_date'     : str(trek.start_date),
                'end_date'       : str(trek.end_date),
                'booked_count'   : booked_count,
            })

        return {
            'id'                : current.id,
            'full_name'         : current.user.full_name,
            'email'             : current.user.email,
            'assigned_treks'    : trek_list,
            'total_treks'       : len(trek_list),
            'total_participants': total_participants,
        }, 200

# ==================================================================================================

class StaffTrekList(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self):
        if not staff():
            return {'message': 'Unauthorized'}, 403

        current = get_current_staff()
        if not current:
            return {'message': 'Staff profile not found'}, 404

        treks = current.assigned_treks.all()
        result = []
        for trek in treks:
            booked_count = trek.bookings.filter(
                Booking.booking_status == BookingStatus.BOOKED
            ).count()
            result.append({
                'id'             : trek.id,
                'trek_name'      : trek.trek_name,
                'trek_location'  : trek.trek_location,
                'trek_status'    : trek.trek_status.value,
                'difficulty'     : trek.difficulty.value,
                'available_slot' : trek.available_slot,
                'total_slot'     : trek.total_slot,
                'start_date'      : str(trek.start_date),
                'end_date'        : str(trek.end_date),
                'booked_count'   : booked_count,
            })
        return result, 200

# ==================================================================================================

class StaffTrekDetail(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self, trek_id):
        if not staff():
            return {'message': 'Unauthorized'}, 403

        current = get_current_staff()
        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message': 'Trek not found'}, 404

        if trek.assigned_staff != current.id:
            return {'message': 'You are not assigned to this trek'}, 403

        booked_count = trek.bookings.filter(
            Booking.booking_status == BookingStatus.BOOKED
        ).count()

        participants = []
        for b in trek.bookings.order_by(Booking.booking_date.desc()).all():
            participants.append({
                'booking_id'      : b.id,
                'user_id'         : b.user.id,
                'full_name'       : b.user.full_name,
                'email'           : b.user.email,
                'mobile_no'       : b.user.mobile_no,
                'booking_date'    : str(b.booking_date),
                'booking_status'  : b.booking_status.value,
                'cancellation_date': str(b.cancellation_date) if b.cancellation_date else None,
                'cancelled_by'    : b.cancelled_by,
            })

        return {
            'id'               : trek.id,
            'trek_name'        : trek.trek_name,
            'trek_location'    : trek.trek_location,
            'description'      : trek.description,
            'difficulty'       : trek.difficulty.value,
            'trek_status'      : trek.trek_status.value,
            'duration_days'    : trek.duration_days,
            'total_slot'       : trek.total_slot,
            'available_slot'   : trek.available_slot,
            'start_date'       : str(trek.start_date),
            'end_date'         : str(trek.end_date),
            'booked_count'     : booked_count,
            'participants'     : participants,
        }, 200

# -------------------------------------------------------------------------------------------------
    @jwt_required()
    def put(self, trek_id):
        if not staff():
            return {'message': 'Unauthorized'}, 403

        current = get_current_staff()
        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message': 'Trek not found'}, 404

        if trek.assigned_staff != current.id:
            return {'message': 'You are not assigned to this trek'}, 403

        data = request.get_json()
        changed = False

        if 'total_slot' in data:
            new_total = data['total_slot']
            if not isinstance(new_total, int) or new_total < 0:
                return {'message': 'total_slot must be a non-negative integer'}, 400

            booked_count = trek.bookings.filter(
                Booking.booking_status == BookingStatus.BOOKED
            ).count()
            if new_total < booked_count:
                return {
                    'message': f'total_slot cannot be less than booked count ({booked_count})'
                }, 400

            trek.total_slot = new_total
            trek.available_slot = new_total - booked_count
            changed = True

        if 'trek_status' in data:
            try:
                new_status = TrekStatus(data['trek_status'])
            except ValueError:
                return {'message': 'Invalid trek_status'}, 400

            if new_status == TrekStatus.PENDING:
                return {'message': 'Staff cannot set trek back to pending'}, 400

            trek.trek_status = new_status
            changed = True

        if 'description' in data:
            trek.description = data['description']
            changed = True

        if not changed:
            return {'message': 'No updatable fields provided'}, 400

        db.session.commit()
        cache.clear()
        return {
            'message'         : 'Trek updated',
            'trek_status'     : trek.trek_status.value,
            'total_slot'      : trek.total_slot,
            'available_slot'  : trek.available_slot,
        }, 200

# ==================================================================================================

class StaffTrekParticipants(Resource):
    @jwt_required()
    @cache.cached(timeout=1800, make_cache_key=make_user_cache_key)
    def get(self, trek_id):
        if not staff():
            return {'message': 'Unauthorized'}, 403

        current = get_current_staff()
        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message': 'Trek not found'}, 404

        if trek.assigned_staff != current.id:
            return {'message': 'You are not assigned to this trek'}, 403

        participants = []
        for b in trek.bookings.order_by(Booking.booking_date.desc()).all():
            participants.append({
                'booking_id'       : b.id,
                'user_id'          : b.user.id,
                'full_name'        : b.user.full_name,
                'email'            : b.user.email,
                'mobile_no'        : b.user.mobile_no,
                'booking_date'     : str(b.booking_date),
                'booking_status'   : b.booking_status.value,
                'cancellation_date': str(b.cancellation_date) if b.cancellation_date else None,
                'cancelled_by'     : b.cancelled_by,
            })

        return {
            'trek_id'       : trek.id,
            'trek_name'     : trek.trek_name,
            'participants'  : participants,
            'total'         : len(participants),
        }, 200

# ==================================================================================================

class StaffBookingStatus(Resource):
    @jwt_required()
    def put(self, booking_id):
        if not staff():
            return {'message': 'Unauthorized'}, 403

        current = get_current_staff()
        booking = Booking.query.get(booking_id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        trek = booking.trek
        if trek.assigned_staff != current.id:
            return {'message': 'You are not assigned to this trek'}, 403

        data = request.get_json()
        if 'booking_status' not in data:
            return {'message': 'Provide booking_status'}, 400

        try:
            new_status = BookingStatus(data['booking_status'])
        except ValueError:
            return {'message': 'Invalid booking_status'}, 400

        old_status = booking.booking_status
        now = datetime.utcnow()

        if new_status == BookingStatus.CANCELLED and old_status != BookingStatus.CANCELLED:
            booking.cancellation_date = now
            booking.booking_status = BookingStatus.CANCELLED
            booking.cancelled_by = 'staff'
            trek.available_slot += 1

        elif new_status == BookingStatus.COMPLETED and old_status == BookingStatus.BOOKED:
            booking.booking_status = BookingStatus.COMPLETED
            booking.cancelled_by = None

        elif new_status == BookingStatus.BOOKED and old_status == BookingStatus.CANCELLED:
            if trek.available_slot <= 0:
                return {'message': 'No slots available to rebook'}, 400
            booking.cancellation_date = None
            booking.booking_status = BookingStatus.BOOKED
            booking.cancelled_by = None
            trek.available_slot -= 1

        else:
            return {
                'message': f'Invalid transition from {old_status.value} to {new_status.value}'
            }, 400

        db.session.commit()
        cache.clear()
        return {
            'message'        : 'Booking status updated',
            'booking_status' : booking.booking_status.value,
            'available_slot' : trek.available_slot,
            'cancelled_by'   : booking.cancelled_by,
        }, 200
