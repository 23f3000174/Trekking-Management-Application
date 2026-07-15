from flask import Flask
from models.models import db, UserRole, User
from routes import auth_bp, admin_bp, staff_bp, trekker_bp, export_bp, cache
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)


    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(backend_dir, "tma.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config['SECRET_KEY'] = 'phull_sequrity'
    db.init_app(app)
    
    app.config["JWT_SECRET_KEY"] = "PHULL_SEQURITY"
    jwt = JWTManager(app)
    
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/2'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 1800

    cache.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(trekker_bp)
    app.register_blueprint(export_bp)

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
        admin_user.set_password('admin@admin.com')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

