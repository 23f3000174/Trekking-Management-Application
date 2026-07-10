from flask import request
from flask_restful import Resource
from models.models import db, User, UserRole, Trekker, Gender
from flask_jwt_extended import create_access_token
from datetime import datetime
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
       
        dob_str = data.get('dob')
        parsed_dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        try:
            print(data['dob'])
            check_gender = data['gender']
            valid_gender = Gender(check_gender)
            new_trekker = Trekker(dob = parsed_dob,
                                  gender = valid_gender,
                                  emergency_contact = data['emergency_contact'])
            
            new_user.trekker_profile = new_trekker
        except:
            return {'message' : 'Invalid gendere....'}, 400
        
        print('before commit')
        db.session.add(new_user)
        print('after addint user')
        db.session.add(new_trekker)
        print('after adding trekker')
        db.session.commit()
        print('after commit')

        return {'message' : 'Trekker registered sucessfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Email and password required'}, 400

        user = User.query.filter_by(email = data.get('email')).first()

        if not user or not user.check_password(data.get('password')):
            return {'message' : 'Invalid credentials'}, 401
        
        if user.flag == 'blacklisted':
            return {'message' : 'Account blacklisted'}, 403
    
        access_token = create_access_token(
                                identity = user.id,
                                additional_claims= {'role' : user.role.value}
                            )

        return {'message' : 'Login sucessfully',
                'access_token' : access_token,
                'role' : user.role.value,
                'user_id' : user.id,
                'full_name' : user.full_name
                }, 200
