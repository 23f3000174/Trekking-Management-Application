from flask import Flask
from models.models import db, UserRole, User

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tma.db"
    app.config['SECRET_KEY'] = 'phull_sequrity'
    db.init_app(app)
    

    @app.route('/')
    def index():
        return "<h1>Hello from app.py</h1>"

    with app.app_context():
        db.create_all()
        create_admin()

    return app

def create_admin():
    if not User.query.filter_by(email='admin@admin.com').first():
        admin_user = User(
                full_name = "ADMIN",
                email= "admin@admin.com",
                role = UserRole.ADMIN
                )
        admin_user.set_password('admin@123')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

