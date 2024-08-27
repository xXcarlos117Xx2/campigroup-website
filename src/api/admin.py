  
import os
from flask import request, redirect, url_for, render_template
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .models import db, Users, Game, Genre, GameGenre, Server, Comment, Image, Setting, UserSetting, Favorite, SocialAccount

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'  # Dark theme, for light theme use 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Models
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Game, db.session))
    admin.add_view(ModelView(Genre, db.session))
    admin.add_view(ModelView(GameGenre, db.session))
    admin.add_view(ModelView(Server, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Image, db.session))
    admin.add_view(ModelView(Setting, db.session))
    admin.add_view(ModelView(UserSetting, db.session))
    admin.add_view(ModelView(Favorite, db.session))
    admin.add_view(ModelView(SocialAccount, db.session))
