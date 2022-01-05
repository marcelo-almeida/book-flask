from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from config import app_config, app_active

config = app_config[app_active]


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('home_admin.html', data={'username': 'malmeida'})


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
