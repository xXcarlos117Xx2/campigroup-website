  
import os
from flask import render_template
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .models import db, Users, Role, UserRole, SocialNetwork, UserSocial, Game, Genre, GameGenre, Server, ServerStatus, ServerStatusChange, Comment, Image, Setting, UserSetting, UserStatus, UserStatusChange, ActivityLog, Favorite, SocialAccount


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'slate'
    admin = Admin(app, name='Campigroup DB manager', template_mode='bootstrap4', index_view=MyAdminIndexView(template='admin/master.html'))

    # Models
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(UserRole, db.session))
    admin.add_view(ModelView(SocialNetwork, db.session))
    admin.add_view(ModelView(UserSocial, db.session))
    admin.add_view(ModelView(Game, db.session))
    admin.add_view(ModelView(Genre, db.session))
    admin.add_view(ModelView(GameGenre, db.session))
    admin.add_view(ModelView(Server, db.session))
    admin.add_view(ModelView(ServerStatus, db.session))
    admin.add_view(ModelView(ServerStatusChange, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Image, db.session))
    admin.add_view(ModelView(Setting, db.session))
    admin.add_view(ModelView(UserSetting, db.session))
    admin.add_view(ModelView(UserStatus, db.session))
    admin.add_view(ModelView(UserStatusChange, db.session))
    admin.add_view(ModelView(ActivityLog, db.session))
    admin.add_view(ModelView(Favorite, db.session))
    admin.add_view(ModelView(SocialAccount, db.session))
