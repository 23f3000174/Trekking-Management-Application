import os
from celery import Celery
from celery.schedules import crontab
from flask import Flask
from models.models import db, User, Booking, Trek, UserRole, BookingStatus
from mail import send_mail
from datetime import date, timedelta

celeryApp = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

celeryApp.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

def make_celery_app():
    app = Flask(__name__)
    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(backend_dir, "tma.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)
    return app

@celeryApp.task()
def daily_reminder():
    app = make_celery_app()
    with app.app_context():
        try:
            tomorrow = date.today() + timedelta(days=1)
            
            treks = Trek.query.filter_by(start_date=tomorrow).all()
            for trek in treks:
                bookings = Booking.query.filter_by(
                    trek_id=trek.id,
                    booking_status=BookingStatus.BOOKED
                ).all()
                for booking in bookings:
                    user = booking.user
                    subject = f"Trek Reminder: {trek.trek_name}"
                    body = f"""
                    <h3>Hello {user.full_name},</h3>
                    <p>This is a reminder that your registered trek <strong>{trek.trek_name}</strong> is scheduled to start tomorrow ({trek.start_date}).</p>
                    <p>Location: {trek.trek_location}</p>
                    <p>Please ensure you are ready and have packed all essentials.</p>
                    <p>Best regards,<br>TMA Team</p>
                    """
                    send_mail(user.email, subject, body)
        finally:
            db.session.remove()

@celeryApp.task()
def monthly_reminder():
    app = make_celery_app()
    with app.app_context():
        try:
            from datetime import date, timedelta
            
            today = date.today()
            first_of_month = today.replace(day=1)
            last_month_end = first_of_month - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            
            # Count all treks in the last month
            total_treks = Trek.query.filter(
                Trek.start_date >= last_month_start,
                Trek.start_date <= last_month_end
            ).count()
            
            # Count all bookings with BOOKED or COMPLETED status on last month's treks
            total_participants = Booking.query.join(Trek).filter(
                Trek.start_date >= last_month_start,
                Trek.start_date <= last_month_end,
                Booking.booking_status.in_([BookingStatus.BOOKED, BookingStatus.COMPLETED])
            ).count()
            
            subject = f"Monthly Trekking Activity Report: {last_month_start.strftime('%B %Y')}"
            body = f"""
            <h2>Monthly Trekking Activity Report ({last_month_start.strftime('%B %Y')})</h2>
            <p>Here is the activity summary for the month of {last_month_start.strftime('%B %Y')}:</p>
            <ul>
                <li><strong>Total Treks Conducted:</strong> {total_treks}</li>
                <li><strong>Total Registered Participants:</strong> {total_participants}</li>
            </ul>
            """
            
            admins = User.query.filter_by(role=UserRole.ADMIN).all()
            for admin in admins:
                send_mail(admin.email, subject, body)
        finally:
            db.session.remove()

@celeryApp.task()
def export_csv(user_id, email):
    import csv
    from datetime import datetime
    app = make_celery_app()
    with app.app_context():
        try:
            user = User.query.get(user_id)
            if not user:
                return
                
            exports_dir = os.path.join(os.path.dirname(__file__), "exports")
            os.makedirs(exports_dir, exist_ok=True)
            
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"trekking_history_{user_id}_{timestamp}.csv"
            filepath = os.path.join(exports_dir, filename)
            
            if user.role == UserRole.ADMIN:
                bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
            elif user.role == UserRole.STAFF:
                bookings = Booking.query.join(Trek).filter(Trek.assigned_staff == user.id).order_by(Booking.booking_date.desc()).all()
            else:
                bookings = Booking.query.filter_by(user_id=user.id, deleted_by_trekker=False).order_by(Booking.booking_date.desc()).all()
                
            with open(filepath, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Booking ID", "Trek Name", "Location", "Difficulty", "Start Date", 
                    "End Date", "Booking Date", "Status", "Cancellation Date", "Cancelled By"
                ])
                for b in bookings:
                    writer.writerow([
                        b.id,
                        b.trek.trek_name,
                        b.trek.trek_location,
                        b.trek.difficulty.value,
                        b.trek.start_date,
                        b.trek.end_date,
                        b.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
                        b.booking_status.value,
                        b.cancellation_date.strftime("%Y-%m-%d %H:%M:%S") if b.cancellation_date else "—",
                        b.cancelled_by or "—"
                    ])
                    
            base_url = os.environ.get("BASE_API_URL", "http://127.0.0.1:5000")
            download_url = f"{base_url}/api/exports/download/{filename}"
            
            subject = "Your Trekking History CSV Export is ready!"
            body = f"""
            <p>Hello {user.full_name},</p>
            <p>Your request to export trekking history has been processed successfully.</p>
            <p>You can download your CSV file using the following link:</p>
            <p><a href="{download_url}">{download_url}</a></p>
            <p>Best regards,<br>TMA Team</p>
            """
            send_mail(email, subject, body)
        finally:
            db.session.remove()

@celeryApp.task()
def send_staff_welcome_email(email, password, name):
    app = make_celery_app()
    with app.app_context():
        try:
            subject = "Welcome to the Trekking Management Application Team!"
            body = f"""
            <h3>Welcome {name}!</h3>
            <p>You have been registered as a Staff member on our Trekking Management Application.</p>
            <p>Here are your login credentials:</p>
            <ul>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Password:</strong> {password}</li>
            </ul>
            <p>Best regards,<br>TMA Admin</p>
            """
            send_mail(email, subject, body)
        finally:
            db.session.remove()

celeryApp.conf.beat_schedule = {
    'daily_reminders': {
        'task': 'celery_app.daily_reminder',
        'schedule': crontab(hour=8, minute=0)
    },
    'monthly_reminders': {
        'task': 'celery_app.monthly_reminder',
        'schedule': crontab(day_of_month=2, hour=16, minute=30)
    }
}