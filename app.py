from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

from config import app_config, app_active
from controller.user import UserController

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

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']
        result = user.login(email=email, password=password)
        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'login invalid', 'type': None})

    @app.route('/recovery-password/')
    def recovery_password():
        return 'recovery password'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(email=request.form['email'])
        if result:
            return render_template('recovery.html', data={'status': 200, 'msg': 'Email sent successfully.'})
        else:
            return render_template('recovery.html', data={'status': 401, 'msg': 'Error sending recovery password.',
                                                          'type': None})

    return app
