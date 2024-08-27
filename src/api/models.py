from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('UTC')), nullable=False)
    is_active = db.Column(db.Boolean(), default=False, nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='role'), nullable=False, default='user')
    activation_token = db.Column(db.String(200), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    reset_token = db.Column(db.String(200), nullable=True)

    # Relationships
    favorites = db.relationship('Favorite', back_populates='user', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='user', lazy='dynamic')
    images = db.relationship('Image', back_populates='user', lazy='dynamic')
    social_accounts = db.relationship('SocialAccount', back_populates='user', lazy='dynamic')
    settings = db.relationship('UserSetting', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "role": self.role
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_activation_token(cls, activation_token):
        return cls.query.filter_by(activation_token=activation_token).first()

    @classmethod
    def find_by_reset_token(cls, reset_token):
        return cls.query.filter_by(reset_token=reset_token).first()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    developer = db.Column(db.String(120), nullable=True)
    publisher = db.Column(db.String(120), nullable=True)

    # Relationships
    favorites = db.relationship('Favorite', back_populates='game', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='game', lazy='dynamic')
    images = db.relationship('Image', back_populates='game', lazy='dynamic')
    servers = db.relationship('Server', back_populates='game', lazy='dynamic')
    genres = db.relationship('GameGenre', back_populates='game', lazy='dynamic')

    def __repr__(self):
        return f'<Game {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "developer": self.developer,
            "publisher": self.publisher,
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)

    # Relationships
    games = db.relationship('GameGenre', back_populates='genre', lazy='dynamic')

    def __repr__(self):
        return f'<Genre {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

class GameGenre(db.Model):
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    
    # Relationships
    game = db.relationship('Game', back_populates='genres')
    genre = db.relationship('Genre', back_populates='games')

    def __repr__(self):
        return f'<GameGenre {self.game_id} - {self.genre_id}>'

    def serialize(self):
        return {
            "game_id": self.game_id,
            "genre_id": self.genre_id,
        }

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    name = db.Column(db.String(120), nullable=False, index=True)
    location = db.Column(db.String(120), nullable=True)
    ip_address = db.Column(db.String(120), nullable=False, index=True)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('ONLINE', 'OFFLINE', 'MAINTENANCE', name='Status'), nullable=False, default='ONLINE')

    # Relationships
    game = db.relationship('Game', back_populates='servers')

    def __repr__(self):
        return f'<Server {self.name} - IP {self.ip_address}>'

    def serialize(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "name": self.name,
            "location": self.location,
            "ip_address": self.ip_address,
            "port": self.port,
            "status": self.status
        }

    @classmethod
    def find_by_ip_address(cls, ip_address):
        return cls.query.filter_by(ip_address=ip_address).first()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('UTC')), nullable=False)

    # Relationships
    user = db.relationship('Users', back_populates='comments')
    game = db.relationship('Game', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.id} - User {self.user_id} on Game {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "body": self.body,
            "created_at": self.created_at.isoformat()
        }

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone('UTC')), nullable=False)

    # Relationships
    user = db.relationship('Users', back_populates='images')
    game = db.relationship('Game', back_populates='images')

    def __repr__(self):
        return f'<Image {self.id} - User {self.user_id} on Game {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "url": self.url,
            "caption": self.caption,
            "uploaded_at": self.uploaded_at.isoformat()
        }

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Setting {self.name}>'

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

    # Relationships
    user = db.relationship('Users', back_populates='settings')
    setting = db.relationship('Setting')

    def __repr__(self):
        return f'<UserSetting User {self.user_id} - Setting {self.setting_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "setting_id": self.setting_id,
            "value": self.value,
        }

class Favorite(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)

    # Relationships
    user = db.relationship('Users', back_populates='favorites')
    game = db.relationship('Game', back_populates='favorites')

    def __repr__(self):
        return f'<Favorite User {self.user_id} - Game {self.game_id}>'

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

    # Relationships
    user = db.relationship('Users', back_populates='social_accounts')

    def __repr__(self):
        return f'<SocialAccount User {self.user_id} - Provider {self.provider}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "provider": self.provider,
            "social_id": self.social_id,
        }
