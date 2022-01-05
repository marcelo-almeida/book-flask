from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from admin.views import UserView

from model.category import Category
from model.product import Product
from model.role import Role
from model.user import User


def start_views(app, db):
    admin = Admin(app, name='My store', template_mode='bootstrap3')

    admin.add_view(ModelView(Role, db.session, "Functions", category="Users"))
    admin.add_view(UserView(User, db.session, "Users", category="Users"))
    admin.add_view(ModelView(Category, db.session, 'Categories', category="Products"))
    admin.add_view(ModelView(Product, db.session, "Products", category="Products"))
