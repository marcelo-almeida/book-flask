from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from config import app_config, app_active

config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(config.APP)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/')
    def login():
        return 'login'

    @app.route('/recovery-password/')
    def recovery_password():
        return 'recovery password'

    @app.route('/profile/<int:user_id>/action/<action>')
    def profile(user_id, action):
        if action == 'action1':
            return f'Action1 for userId {user_id}'
        elif action == 'action2':
            return f'Action2 for userId {user_id}'
        else:
            return f'Action default for userId {user_id}'

    @app.route('/profile/', methods=['POST'])
    def create_profile():
        username = request.form['username']
        password = request.form['password']
        return f'POST - username: {username}, password: {password}'

    @app.route('/profile/<int:user_id>', methods=['PUT'])
    def edit_total_profile(user_id):
        username = request.form['username']
        password = request.form['password']
        return f'PUT - username: {username}, password: {password}'

    return app
