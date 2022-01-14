from datetime import datetime, timedelta

import jwt

from config import app_config, app_active
from model.user import User

config = app_config[app_active]


class UserController:
    def __init__(self):
        self.user_model = User()

    def login(self, email, password):
        self.user_model.email = email
        result = self.user_model.get_user_by_email()
        if result:
            return result if self.user_model.verify_password(password_no_hash=password,
                                                             password_database=result.password) else {}
        return {}

    def recovery(self, email):
        return ''

    def get_user_by_id(self, user_id):
        result = {}
        try:
            self.user_model.id = user_id
            res = self.user_model.get_user_by_id()
            result = {
                'id': res.id,
                'name': res.username,
                'email': res.email,
                'date_created': res.date_created
            }
            status = 200
        except Exception as e:
            print(e)
            result = {}
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }

    def verify_auth_token(self, access_token):
        status = 401
        try:
            jwt.decode(access_token, config.SECRET, algorithms='HS256')
            message = 'Token is valid'
            status = 200
        except jwt.ExpiredSignatureError:
            message = 'Token is expired'
        except Exception:
            message = 'Token is invalid'
        return {
            'message': message,
            'status': status
        }

    def generate_auth_token(self, data, exp=30, time_exp=False):
        if time_exp:
            date_time = data['exp']
        else:
            date_time = datetime.utcnow() + timedelta(minutes=exp)
        dict_jwt = {
            'id': data['id'],
            'username': data['username'],
            'exp': date_time
        }
        return jwt.encode(dict_jwt, config.SECRET, algorithm='HS256')

    def get_admin_login(self, user_id):
        self.user_model.id = user_id
        response = self.user_model.get_user_by_id()
        return response
