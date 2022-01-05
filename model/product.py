from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from config import app_config, app_active
from model.category import Category
from model.user import User

config = app_config[app_active]
db = SQLAlchemy(config.APP)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    qtd = db.Column(db.Integer, default=0, nullable=True)
    image = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.Boolean(), default=1, nullable=True)
    user_created = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    user = relationship(User)
    cat = relationship(Category)
