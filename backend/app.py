from flask import Flask
from models.models import db, UserRole, User
from routes import auth_bp
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tma.db"
    app.config['SECRET_KEY'] = 'phull_sequrity'
    db.init_app(app)
    
    app.config["JWT_SECRET_KEY"] = "PHULL_SEQURITY"
    jwt = JWTManager(app)
    
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        create_admin()

    return app

def create_admin():
    if not User.query.filter_by(email='admin@admin.com').first():
        admin_user = User(
                full_name = "ADMIN",
                email= "admin@admin.com",
                mobile_no = "xxx",
                role = UserRole.ADMIN
                )
        admin_user.set_password('admin@123')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

