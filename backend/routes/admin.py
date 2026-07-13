from flask import request
# pyrefly: ignore [missing-import]
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models.models import db, User, Staff, Trekker, Trek, Booking, UserRole, UserStatus, Difficulty, TrekStatus 
from datetime import datetime

def admin():
    claims = get_jwt()
    return claims['role'] == 'admin'
# ------------------------------------------------------------------------------------------------- 

class Dashboard(Resource):
    @jwt_required()
    def get(self):
        if not admin():
            return {'message' : 'Unauthorized'}, 403
        
        return {
            'total_staff'    : Staff.query.count(),
            'total_treks'    : Trek.query.count(),
            'active_treks'   : Trek.query.filter(Trek.trek_status == TrekStatus.OPEN).count(),
            'total_trekkers' : Trekker.query.count(),
            'total_bookings' : Booking.query.count()
        }, 200

# ==================================================================================================

class StaffList(Resource):
    @jwt_required()
    def get(self):
        if not admin():
            return {'message' : 'Unauthorized'}, 403
        
        staff = Staff.query.all()
        result = []
        for s in staff:
            result.append({
                'id'        : s.id,
                'full_name' : s.user.full_name,
                'email'     : s.user.email,
                'mobile_no' : s.user.mobile_no,
                'flag'      : s.user.flag.value,
            })
        return result, 200
# ------------------------------------------------------------------------------------------------- 

    @jwt_required()
    def post(self):
        if not admin():
            return {'message' : 'Unauthorized'}, 403

        data = request.get_json()
        
        required = ['full_name', 'email', 'password', 'mobile_no',]
        if not all(f in data for f in required):
            return {'message' : 'Missing fields'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'message' : 'Email already registered'}, 400

        new_user = User(
            full_name = data['full_name'],
            email = data['email'],
            role = UserRole.STAFF,
            mobile_no = data['mobile_no'],
            )
        new_user.set_password(data['password'])
        
        new_staff = Staff()

        new_user.staff_profile = new_staff

        db.session.add(new_user)
        db.session.commit()
        return {'message' : 'Staff added successfully', 'id' : new_user.id}, 200

# ==================================================================================================

class StaffDetail(Resource): 
    @jwt_required()
    def get(self, staff_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403

        staff = Staff.query.get(staff_id)
        if not staff:
            return {'message': 'Staff not found'}, 404
        
        assigned = []
        for trek in staff.assigned_treks:
            assigned.append({
                'trek_id' : trek.id,
                'trek_name' : trek.trek_name,
                'trek_status' : trek.trek_status.value,
                'start_date' : str(trek.start_date),
                })

        return {
            'id'             : staff.id,
            'full_name'      : staff.user.full_name,
            'email'          : staff.user.email,
            'mobile_no'      : staff.user.mobile_no,
            'contact'        : staff.contact,
            'bio'            : staff.bio,
            'flag'           : staff.user.flag.value,
            'assigned_treks' : assigned,
        }, 200

# ------------------------------------------------------------------------------------------------- 
    @jwt_required()
    def put(self, staff_id):
        if not admin():
            return {'message' : 'Unauthorized'}, 403
        
        staff = Staff.query.get(staff_id)
        if not staff:
            return {'message' : 'Staff member not found'}, 404

        data = request.get_json()
        
        if 'full_name' in data:
            staff.user.full_name = data['full_name']
        if 'mobile_no' in data:
            staff.user.mobile_no = data['mobile_no']
        if 'flag' in data:
            try:
                staff.user.flag = UserStatus(data['flag'])
            except ValueError:
                return {'message' : 'Invalid flag ....'}, 400

        db.session.commit()
        return {'message' : 'Staff updated'} , 200

# ------------------------------------------------------------------------------------------------- 

    @jwt_required()
    def delete(self, staff_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403

        staff = User.query.get(staff_id)
        if not staff or staff.role != UserRole.STAFF:
            return {'message' : 'Staff not found'}, 404

        db.session.delete(staff)
        db.session.commit()
        return {'message' : 'Staff deleted'}, 200

# ==================================================================================================

class TrackList(Resource):
    @jwt_required()
    def get(self):
        if not admin():
            return {'message' : 'Unauthorized'}, 403

        treks = Trek.query.all()

        result = []
        for trek in treks:
            result.append({
                'id'            : trek.id,
                'trek_name'     : trek.trek_name,
                'trek_location' : trek.trek_location,
                'trek_status'   : trek.trek_status.value,
                'difficulty'    : trek.difficulty.value,
                'available_slot': trek.available_slot,
                'total_slot'    : trek.total_slot,
                'start_date'    : str(trek.start_date),
                'end_date'      : str(trek.end_date),
            })
        return result, 200

# ------------------------------------------------------------------------------------------------- 
    @jwt_required()
    def post(self):
        if not admin():
            return {'message' : 'Unauthorized'}, 403       

        data = request.get_json()

        required = ['trek_name', 'trek_location', 'difficulty', 'total_slot', 'start_date', 'end_date']
        if not all(f in data for f in required):
            return {'message' : 'Missing fields'}, 400

        try: 
            valid_difficulty = Difficulty(data['difficulty'])
        except ValueError:
             return {'message' : 'Invalid Difficulty....'} , 400
        try: 
            start = datetime.strptime(data['start_date'], '%Y-%m-%d').date() 
            end = datetime.strptime(data['end_date'], '%Y-%m-%d').date() 
        except ValueError:
            return {'message' : 'Invalid date format'}, 400
            
        if end <= start:
            return {'message' : 'end_date must be after start_date'}, 400
            
        duration_days = (end - start).days

        new_trek = Trek(
            trek_name      = data['trek_name'],
            trek_location  = data['trek_location'],
            description    = data.get('description'),
            difficulty     = valid_difficulty,
            duration_days  = duration_days,
            total_slot     = data['total_slot'],
            available_slot = data['total_slot'],
            start_date     = start,
            end_date       = end,
        )
        
        db.session.add(new_trek)
        db.session.commit()
        return {'message' : 'Trek created' , 'id' : new_trek.id}, 201

# ==================================================================================================

class TrackDetail(Resource):
    @jwt_required()
    def get(self, trek_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403
        
        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message' : 'Trek not found'}, 404
        
        staff_info = None
        if trek.staff:
            staff_info = {
                    'id' : trek.staff.id,
                    'full_name' : trek.staff.user.full_name,
                    'email' : trek.staff.user.email,
                    }

        return {
            'id'              : trek.id,
            'trek_name'       : trek.trek_name,
            'trek_location'   : trek.trek_location,
            'description'     : trek.description,
            'difficulty'      : trek.difficulty.value,
            'trek_status'     : trek.trek_status.value,
            'duration_days'   : trek.duration_days,
            'total_slot'      : trek.total_slot,
            'available_slot'  : trek.available_slot,
            'start_date'      : str(trek.start_date),
            'end_date'        : str(trek.end_date),
            'assigned_staff'  : staff_info,
        }, 200

# ------------------------------------------------------------------------------------------------- 
    @jwt_required()
    def put(self, trek_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403

        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message' : 'Trek not found'}, 404

        data = request.get_json()

        if 'trek_name' in data:
            trek.trek_name = data['trek_name']
        if 'trek_location' in data:
            trek.trek_location = data['trek_location']
        if 'description' in data:
            trek.description = data['description']
        if 'total_slot' in data:
            trek.total_slot = data['total_slot']
        
        if 'difficulty' in data:
            try:
                trek.difficulty = Difficulty(data['difficulty'])
            except ValueError:
                return {'message' : 'Invalid difficulty'}, 400

        if 'trek_status' in data:
            try:
                trek.trek_status = TrekStatus(data['trek_status'])
            except ValueError:
                return {'message' : 'Invalid status'}, 400
        
        if 'assigned_staff_id' in data:
            staff_id = data['assigned_staff_id']
            if staff_id is None:
                trek.assigned_staff = None
            else:
                staff = Staff.query.get(staff_id)
                if not staff:
                    return {'message' : 'Staff not found'}, 404
                trek.assigned_staff = staff.id

        db.session.commit()
        return {'message' : 'Trek updated'}, 200

# ------------------------------------------------------------------------------------------------- 
    @jwt_required()
    def delete(self, trek_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403

        trek = Trek.query.get(trek_id)
        if not trek:
            return {'message' : 'Trek not found'}, 404

        db.session.delete(trek)
        db.session.commit()
        return {'message' : 'Trek deleted'}, 200

# ==================================================================================================

class TrekkerList(Resource):
    @jwt_required()
    def get(self):
        if not admin():
            return {'message': 'Unauthorized'}, 403
        
        trekker = Trekker.query.all()
        result = []
    
        for t in trekker:
            result.append({
                'id' : t.id,
                'full_name' : t.user.full_name,
                'email' : t.user.email,
                'mobile_no' : t.user.mobile_no,
                'flag' : t.user.flag.value,
                'dob' : str(t.dob),
                'gender' : t.gender.value,
                'emergency_contact' : t.emergency_contact 
                })
        return result, 200

# ==================================================================================================

class TrekkerDetail(Resource):  
    @jwt_required()
    def get(self, trekker_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403
        
        trekker = Trekker.query.get(trekker_id)
        if not trekker:
            return {'message' : 'Trekker not found'}, 404

        bookings = []
        for b in trekker.user.bookings:
            bookings.append({
                'booking_id' : b.id,
                'trek_name'      : b.trek.trek_name,
                'trek_location'  : b.trek.trek_location,
                'booking_date'   : str(b.booking_date),
                'booking_status' : b.booking_status.value,
                })

        return {
                'id'                : trekker.id,
                'full_name'         : trekker.user.full_name,
                'email'             : trekker.user.email,
                'mobile_no'         : trekker.user.mobile_no,
                'dob'               : str(trekker.dob),
                'gender'            : trekker.gender.value,
                'emergency_contact' : trekker.emergency_contact,
                'flag'              : trekker.user.flag.value,
                'booking_history'   : bookings,
                }, 200

# ------------------------------------------------------------------------------------------------- 
    @jwt_required()
    def put(self, trekker_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403
        
        user = User.query.get(trekker_id)
        if not user or user.role != UserRole.TREKKER:
            return {'message' : 'Trekker not found'}, 404

        data = request.get_json()
        if 'flag' not in data:
            return {'message' : 'Provide flag....'}, 400
        
        try:
            user.flag = UserStatus(data['flag'])
        except ValueError:
            return {'message' : 'Invalid flag....'}, 400

        db.session.commit()
        return {'message' : f'User status updated to {user.flag.value}'}, 200

# ------------------------------------------------------------------------------------------------- 
    @jwt_required()
    def delete(self, trekker_id):
        if not admin():
            return {'message': 'Unauthorized'}, 403

        user = User.query.get(trekker_id)
        if not user:
            return {'message' : 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message' : 'User deleted'}, 200


class BookingList(Resource):
    @jwt_required()
    def get(self):
        if not admin():
            return {'message' : 'Unauthorized'},403

        bookings = Booking.query.all()
        result = []
        for b in bookings:
            result.append({
                'booking_id': b.id,
                'user_id' : b.user_id,
                'user_name' : b.user.full_name,
                'trek_id' : b.trek_id,
                'trek_name' : b.trek.trek_name,
                'trek_location' : b.trek.trek_location,
                'booking_date' : str(b.booking_date),
                'booking_status' : b.booking_status.value,
                'cancellation_date' : str(b.cancellation_date) 
            })
        return result, 200


class BookingDetail(Resource):
    @jwt_required()
    def get(self, booking_id):
        if not admin():
            return {'message' : 'Unauthorized'}, 403

        booking = Booking.query.get(booking_id)
        if not booking:
            return {'message' : 'Booking not found'}, 404

        return{
                'booking_id'        : booking.id,
                'booking_date'      : str(booking.booking_date),
                'booking_status'    : booking.booking_status.value,
                'cancellation_date' : str(booking.cancellation_date) ,
                'user': {
                    'id' : booking.user.id,
                    'full_name' : booking.user.full_name,
                    'email' : booking.user.email
                    },
                'trek' : {
                    'id'           : booking.trek.id,
                    'trek_name'    : booking.trek.trek_name,
                    'trek_location': booking.trek.trek_location,
                    'start_date'   : str(booking.trek.start_date),
                    'end_date'     : str(booking.trek.end_date),
                    'trek_status'  : booking.trek.trek_status.value,
                    },
                }, 200


class Search(Resource):
    @jwt_required()
    def get(self):
        if not admin():
            return {'message' : 'Unauthorized'}, 403
        
        q = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all').lower()

        if not q:
            return {'message' : 'Provide a search query ?q=....'}, 400

        pattern = f'%{q}%'
        result = {}

        if search_type in ('staff', 'all'):
            staff_users = User.query.filter(
                    User.role == UserRole.STAFF,
                    User.full_name.ilike(pattern) | User.email.ilike(pattern)
                    ).all()

            result['staff'] = [{
                'id' : u.id,
                'full_name' : u.full_name,
                'email' : u.email,
                'flag' : u.flag.value,
                } for u in staff_users]

        if search_type in ('trek', 'all'):
            treks = Trek.query.filter(
                Trek.trek_name.ilike(pattern) |
                Trek.trek_location.ilike(pattern)
            ).all()

            result['treks'] = [{
                'id'          : t.id,
                'trek_name'   : t.trek_name,
                'trek_location': t.trek_location,
                'trek_status' : t.trek_status.value,
                'difficulty'  : t.difficulty.value,
            } for t in treks]
                    
        if search_type in ('trekker', 'all'):
            trekker_users = User.query.filter(
                User.role == UserRole.TREKKER,
                User.full_name.ilike(pattern) |
                User.email.ilike(pattern)
            ).all()

            result['trekkers'] = [{
                'id'        : u.id,
                'full_name' : u.full_name,
                'email'     : u.email,
                'flag'      : u.flag.value,
            } for u in trekker_users]

        return result, 200
