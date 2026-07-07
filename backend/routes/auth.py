from flask import request
from flask_restful import Resource
from models.models import db, User, UserRole, Trekker, Gender

class Register(Resource):
    def post(self):
        data = request.get_json()
        required_field = ['email', 'full_name', 'password', 'mobile_no', 'dob', 'gender']
        if not all(i in data for i in required_field):
            return {'message' : 'Missing Fields'}, 400

        if User.query.filter_by(email=data['email']).first():
            return {'message' : 'Email already exist'}, 409

        new_user = User(full_name = data['full_name'],
                        email = data['email'],
                        mobile_no = data['mobile_no'],
                        role = UserRole.TREKKER
                        )
        new_user.set_password(data['password'])
        
        try:
            check_gender = data['gender'].lower()
            valid_gender = Gender(check_gender)
            new_trekker = Trekker(dob = data['dob'],
                                  gender = valid_gender,
                                  emergency_contact = data['emergency_contact'])
            
            new_user.trekker_profile = new_trekker
        except:
            return {'message' : 'Invalid gender, Choose one of these: male, female, other, prefer not to say'}, 400

        db.session.add(new_user)
        db.session.add(new_trekker)
        db.session.commit()

        return {'message' : 'Trekker registered sucessfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Email and password required'}, 400

        user = User.query.filter_by(email = data.get('email')).first()

        if not user or not user.check_password(data.get('password')):
            return {'message' : 'Invalid credentials'}, 401
        
        if user.flag.value == 'blacklisted':
            return {'message' : 'Account blacklisted'}, 403
    
        access_token = create_access_token(
                                identity = user.id,
                                role_claims = user.role.value
                            )

        return {'message' : 'Login sucessfully',
                'access_token' : access_token,
                'role' : user.role.value,
                'user_id' : user.id,
                'full_name' : user.full_name
                }, 200
