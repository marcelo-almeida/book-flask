from flask import redirect
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from config import app_config, app_active
from model.category import Category
from model.product import Product
from model.user import User

config = app_config[app_active]


class HomeView(AdminIndexView):
    extra_css = [config.URL_MAIN + 'static/css/home.css',
                 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']

    @expose('/')
    def index(self):
        user_model = User()
        category_model = Category()
        product_model = Product()
        users = user_model.get_total_users()
        categories = category_model.get_total_categories()
        products = product_model.get_total_products()
        last_products = product_model.get_last_products()
        return self.render('home_admin.html', last_products=last_products, report={
            'users': 0 if not users else users[0],
            'categories': 0 if not categories else categories[0],
            'products': 0 if not products else products[0]
        })

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class UserView(ModelView):
    column_labels = {
        'function': 'Function',
        'username': 'Username',
        'email': 'E-mail',
        'date_created': 'Created Date',
        'last_updated': 'Last updated on',
        'active': 'Active',
        'password': 'Password'
    }

    column_descriptions = {
        'function': 'Function in administrative panel.',
        'active': 'state active or inactive'
    }
    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']

    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'function']
    column_editable_list = ['username', 'email', 'function', 'active']
    create_modal = True
    edit_modal = True
    can_export = True
    column_sortable_list = ['username']
    column_default_sort = ('username', True)
    column_details_exclude_list = ['password', 'recovery_code']
    column_export_exclude_list = ['password', 'recovery_code']
    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password

    def is_accessible(self):
        if current_user.is_authenticated:
            role = current_user.role
            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class RoleView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            role = current_user.role
            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class CategoryView(ModelView):
    can_view_details = True

    def is_accessible(self):
        if current_user.is_authenticated:
            role = current_user.role
            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated
            elif role == 2:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


class ProductView(ModelView):
    can_view_details = True

    def is_accessible(self):
        if current_user.is_authenticated:
            role = current_user.role
            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
            elif role == 2:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
            elif role == 3:
                self.can_create = True
                self.can_edit = True
                self.can_delete = False
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')
