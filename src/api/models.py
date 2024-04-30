from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "created_at": self.created_at,
            "is_active": self.is_active
        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Role {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class UserRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

    def __repr__(self):
        return f'<User {self.user_id} - Role {self.role_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "role_id": self.role_id,
        }


class SocialNetwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Social {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class UserSocial(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    social_id = db.Column(db.Integer, db.ForeignKey('social_network.id'), primary_key=True)
    handle = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.user_id} - Social {self.social_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "social_id": self.social_id,
            "handle": self.handle,
        }


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    developer = db.Column(db.String(120), nullable=True)
    publisher = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<Game {self.id} - {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "release_date": self.release_date,
            "developer": self.developer,
            "publisher": self.publisher,
        }


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Genre {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class GameGenre(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

    def __repr__(self):
        return f'<Game {self.game_id} - Genre {self.genre_id}>'

    def serialize(self):
        return {
            "game_id": self.game_id,
            "genre_id": self.genre_id,
        }


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    ip_address = db.Column(db.String(120), nullable=False)
    port = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Server {self.id} - Game {self.game_id} {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "name": self.name,
            "location": self.location,
            "ip_address": self.ip_address,
            "port": self.port,
        }


class ServerStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Status {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class ServerStatusChange(db.Model):
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('server_status.id'), primary_key=True)
    changed_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Server status {self.server_id} - {self.status_id}>'

    def serialize(self):
        return {
            "server_id": self.server_id,
            "status_id": self.status_id,
            "changed_at": self.changed_at,
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Comment {self.id} - User {self.user_id} at game {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "body": self.body,
            "created_at": self.created_at,
        }


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    url = db.Column(db.String(120), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Image {self.id} - User {self.user_id} at game {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "url": self.url,
            "caption": self.caption,
            "uploaded_at": self.uploaded_at,
        }


# class File(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     filename = db.Column(db.String(120), nullable=False)
#     filetype = db.Column(db.String(120), nullable=False)
#     size = db.Column(db.Integer, nullable=False)
#     uploaded_at = db.Column(db.DateTime, nullable=False)
#
#        def __repr__(self):
#                return f'<File {self.id} - {self.filename}>'
#                
#        def serialize(self):
#                return {
#                    "id": self.id,
#                    "game_id": self.game_id,
#                    "user_id": self.user_id,
#                    "filename": self.filename,
#                    "filetype": self.filetype,
#                    "size": self.size,
#                    "uploaded_at": self.uploaded_at,
#                }


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Setting {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class UserSetting(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    setting_id = db.Column(db.Integer, db.ForeignKey('setting.id'), primary_key=True)
    value = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.user_id} - Setting {self.setting_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class UserStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Status {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class UserStatusChange(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('user_status.id'), primary_key=True)
    changed_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<User {self.user_id} - Status {self.status_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "status_id": self.status_id,
            "changed_at": self.changed_at,
        }


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<{self.timestamp}: User {self.name} - {self.action}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "timestamp": self.timestamp,
        }


class Favorite(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)

    def __repr__(self):
        return f'<Favorite {self.game_id} - User {self.user_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "game_id": self.game_id,
        }


class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    provider = db.Column(db.String(120), nullable=False)
    social_id = db.Column(db.String(120), nullable=False)
    access_token = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.user_id} - Provider {self.provider}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "provider": self.provider,
            "social_id": self.social_id,
        }
