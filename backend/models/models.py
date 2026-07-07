from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
import bcrypt

db = SQLAlchemy()

class UserRole(enum.Enum):
    ADMIN = 'admin'
    STAFF = 'staff'
    TREKKER = 'trekker'

class UserStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BLACKLISTED = 'blacklisted'

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    PREFER_NOT = 'prefer not to say'

class Difficulty(enum.Enum):
    EASY = 'easy'
    MODERATE = 'moderate'
    HARD = 'hard'

class TrekStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    OPEN = 'open'
    CLOSED = 'closed'
    COMPLETED = 'completed'

class BookingStatus(enum.Enum):
    BOOKED = 'booked'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name =  db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    mobile_no = db.Column(db.String(15), unique=True, nullable=False)

    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        self.password_hash= hashed.decode('utf-8') 
    
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        stored_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_hash_bytes)

    flag = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    role = db.Column(db.Enum(UserRole), nullable=False)

    trekker_profile = db.relationship('Trekker',
                                      back_populates='user',
                                      uselist=False,
                                      cascade='all, delete-orphan')
    staff_profile = db.relationship('Staff',
                                    back_populates='user',
                                    uselist=False,
                                    cascade='all, delete-orphan')
   
    bookings = db.relationship('Booking',
                              back_populates='user',
                              lazy='dynamic',
                              cascade='all, delete-orphan',
                              foreign_keys='Booking.user_id')

class Staff(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    contact = db.Column(db.String(15))
    bio = db.Column(db.Text)
    status= db.Column(db.Boolean, nullable=False, default=True)

    user = db.relationship('User',
                           back_populates='staff_profile')

    assigned_treks = db.relationship('Trek',
                                     back_populates='staff',
                                     foreign_keys='Trek.assigned_staff',
                                     lazy='dynamic')

class Trekker(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    emergency_contact = db.Column(db.String(15))

    user = db.relationship('User',
                           back_populates='trekker_profile')
    @property
    def bookings(self):
        return self.user.bookings
    
class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(120), nullable=False)
    trek_location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    difficulty = db.Column(db.Enum(Difficulty), nullable=False)
    trek_status = db.Column(db.Enum(TrekStatus), nullable=False, default=TrekStatus.PENDING)

    duration_days = db.Column(db.Integer, nullable=False)
    total_slot = db.Column(db.Integer, nullable=False)
    available_slot = db.Column(db.Integer, nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    assigned_staff = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete='SET NULL'))
    
    staff = db.relationship('Staff',
                            back_populates='assigned_treks',
                            foreign_keys=[assigned_staff])

    bookings = db.relationship('Booking',
                               back_populates='trek',
                               lazy='dynamic',
                               cascade='all, delete-orphan')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)

    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    booking_status = db.Column(db.Enum(BookingStatus), nullable=False, default=BookingStatus.BOOKED)
    
    cancellation_date = db.Column(db.DateTime)

    user = db.relationship('User',
                           back_populates='bookings',
                           foreign_keys=[user_id])
    trek = db.relationship('Trek',
                           back_populates='bookings')

    __table_args__ = (
            db.UniqueConstraint('user_id', 'trek_id', name='unique_user_track_booking'),
            )
