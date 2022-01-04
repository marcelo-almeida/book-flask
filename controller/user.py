from model.user import User


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
