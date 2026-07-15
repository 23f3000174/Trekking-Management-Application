import os
from datetime import date, timedelta, datetime
from app import create_app
from models.models import db, User, Staff, Trekker, Trek, Booking, UserRole, UserStatus, Gender, Difficulty, TrekStatus, BookingStatus

def seed_database():
    app = create_app()
    with app.app_context():
        print("Clearing existing database...")
        db.drop_all()
        db.create_all()

        print("Creating Admin...")
        admin_user = User(
            full_name="System Admin",
            email="admin@admin.com",
            mobile_no="9999999999",
            role=UserRole.ADMIN,
            flag=UserStatus.ACTIVE
        )
        admin_user.set_password("admin@admin.com")
        db.session.add(admin_user)

        print("Creating 3 Staff members...")
        staff_users = []
        for i in range(1, 4):
            user = User(
                full_name=f"Staff Member {i}",
                email=f"staff{i}@admin.com",
                mobile_no=f"888888888{i}",
                role=UserRole.STAFF,
                flag=UserStatus.ACTIVE
            )
            user.set_password("password123")
            
            staff_profile = Staff(
                contact=f"123-456-789{i}",
                bio=f"Experienced mountain guide specializing in route {i}."
            )
            user.staff_profile = staff_profile
            db.session.add(user)
            staff_users.append(user)

        # Flush to get IDs
        db.session.flush()

        print("Creating 20 Trekkers...")
        trekkers = []
        for i in range(1, 21):
            user = User(
                full_name=f"Trekker Candidate {i}",
                email=f"trekker{i}@gmail.com",
                mobile_no=f"77777777{i:02d}",
                role=UserRole.TREKKER,
                flag=UserStatus.ACTIVE
            )
            user.set_password("password123")
            
            trekker_profile = Trekker(
                dob=date(1990 + (i % 10), 1 + (i % 12), 1 + (i % 28)),
                gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                emergency_contact=f"90000000{i:02d}"
            )
            user.trekker_profile = trekker_profile
            db.session.add(user)
            trekkers.append(user)

        # Flush to get IDs
        db.session.flush()

        print("Creating 5 Treks...")
        today = date.today()
        treks = []
        
        # Trek 1: starts TOMORROW (this will trigger daily reminder mail)
        trek1 = Trek(
            trek_name="Himalayan Peak Expedition",
            trek_location="Manali, Himachal Pradesh",
            description="A scenic trek starting tomorrow exploring snowy ranges.",
            difficulty=Difficulty.HARD,
            trek_status=TrekStatus.OPEN,
            duration_days=5,
            total_slot=15,
            available_slot=5, # 10 booked
            start_date=today + timedelta(days=1),
            end_date=today + timedelta(days=6),
            assigned_staff=staff_users[0].id
        )
        db.session.add(trek1)
        treks.append(trek1)

        # Trek 2: starts in 5 days
        trek2 = Trek(
            trek_name="Valley of Flowers",
            trek_location="Chamoli, Uttarakhand",
            description="Explore the beautiful flower valley in peak season.",
            difficulty=Difficulty.EASY,
            trek_status=TrekStatus.OPEN,
            duration_days=4,
            total_slot=20,
            available_slot=12, # 8 booked
            start_date=today + timedelta(days=5),
            end_date=today + timedelta(days=9),
            assigned_staff=staff_users[1].id
        )
        db.session.add(trek2)
        treks.append(trek2)

        # Trek 3: starts in 15 days
        trek3 = Trek(
            trek_name="Kedar Kantha Trek",
            trek_location="Uttarkashi, Uttarakhand",
            description="A popular winter summit trek.",
            difficulty=Difficulty.MODERATE,
            trek_status=TrekStatus.OPEN,
            duration_days=6,
            total_slot=30,
            available_slot=30, # 0 booked
            start_date=today + timedelta(days=15),
            end_date=today + timedelta(days=21),
            assigned_staff=staff_users[2].id
        )
        db.session.add(trek3)
        treks.append(trek3)

        # Trek 4: starts in 30 days
        trek4 = Trek(
            trek_name="Markha Valley Trek",
            trek_location="Leh, Ladakh",
            description="An adventurous high altitude desert trek.",
            difficulty=Difficulty.HARD,
            trek_status=TrekStatus.OPEN,
            duration_days=8,
            total_slot=10,
            available_slot=10, # 0 booked
            start_date=today + timedelta(days=30),
            end_date=today + timedelta(days=38),
            assigned_staff=staff_users[0].id
        )
        db.session.add(trek4)
        treks.append(trek4)

        # Trek 5: starts in 45 days
        trek5 = Trek(
            trek_name="Triund Ridge Trek",
            trek_location="Dharamshala, Himachal Pradesh",
            description="A quick weekend hiking trip to Triund.",
            difficulty=Difficulty.EASY,
            trek_status=TrekStatus.OPEN,
            duration_days=2,
            total_slot=25,
            available_slot=25, # 0 booked
            start_date=today + timedelta(days=45),
            end_date=today + timedelta(days=47),
            assigned_staff=staff_users[1].id
        )
        db.session.add(trek5)
        treks.append(trek5)

        # June 2026 Treks (for monthly report testing)
        trek6 = Trek(
            trek_name="June Summer Meadow Trek",
            trek_location="Shimla, Himachal Pradesh",
            description="A summer trek in June.",
            difficulty=Difficulty.EASY,
            trek_status=TrekStatus.COMPLETED,
            duration_days=5,
            total_slot=15,
            available_slot=10,
            start_date=date(2026, 6, 5),
            end_date=date(2026, 6, 10),
            assigned_staff=staff_users[0].id
        )
        db.session.add(trek6)
        treks.append(trek6)

        trek7 = Trek(
            trek_name="June Summit Challenge",
            trek_location="Manali, Himachal Pradesh",
            description="High altitude June climb.",
            difficulty=Difficulty.HARD,
            trek_status=TrekStatus.COMPLETED,
            duration_days=6,
            total_slot=10,
            available_slot=7,
            start_date=date(2026, 6, 18),
            end_date=date(2026, 6, 24),
            assigned_staff=staff_users[1].id
        )
        db.session.add(trek7)
        treks.append(trek7)

        # Flush to get IDs
        db.session.flush()

        print("Booking trekkers on the treks...")
        # Book 10 trekkers on Trek 1 (starts tomorrow)
        for i in range(10):
            booking = Booking(
                user_id=trekkers[i].id,
                trek_id=trek1.id,
                booking_status=BookingStatus.BOOKED,
                booking_date=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add(booking)

        # Book 8 trekkers on Trek 2
        for i in range(8):
            booking = Booking(
                user_id=trekkers[i+10].id,
                trek_id=trek2.id,
                booking_status=BookingStatus.BOOKED,
                booking_date=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(booking)

        # Book 5 trekkers on Trek 6 (June trek)
        for i in range(5):
            booking = Booking(
                user_id=trekkers[i].id,
                trek_id=trek6.id,
                booking_status=BookingStatus.COMPLETED,
                booking_date=datetime(2026, 6, 2, 10, 0, 0)
            )
            db.session.add(booking)

        # Book 3 trekkers on Trek 7 (June trek)
        for i in range(3):
            booking = Booking(
                user_id=trekkers[i+5].id,
                trek_id=trek7.id,
                booking_status=BookingStatus.COMPLETED,
                booking_date=datetime(2026, 6, 15, 11, 30, 0)
            )
            db.session.add(booking)

        db.session.commit()
        print("Database successfully seeded with:")
        print(" - 1 Admin (admin@admin.com / admin@admin.com)")
        print(" - 3 Staff members (staff1@admin.com to staff3@admin.com / password123)")
        print(" - 20 Trekkers (trekker1@gmail.com to trekker20@gmail.com / password123)")
        print(" - 5 Treks (with 10 trekkers booked on tomorrow's trek to test reminders)")

if __name__ == "__main__":
    seed_database()
