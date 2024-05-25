from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Role, UserRole, SocialNetwork, UserSocial, Game, Genre, GameGenre, Server, ServerStatus, ServerStatusChange, Comment, Image, Setting, UserSetting, UserStatus, UserStatusChange, ActivityLog, Favorite, SocialAccount
from api.utils import generate_sitemap, APIException
from flask_cors import CORS


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Funciones auxiliares

def encrypt_password(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password, salt)
    password = password.decode('utf-8')
    return password

def get_user_id_from_username(username):
    pass


# Cositas que necesito
    # response_body = {}
    # response_body['results'] = "Results"
    # response_body['msg'] = "Mensaje"
    # [row.serialize() for row in variable_name]

# User Management
@api.route('/signup', methods=['POST']) # Register
def handle_signup():

    return response_body, 200


@api.route('/signin', methods=['POST']) # Login
def handle_signin():
    
    return response_body, 200

@api.route('/users', methods=['GET'])
def handle_users():

    return response_body, 200

@api.route('/user/<string:username>', methods=['GET', 'PUT', 'DELETE'])
def handle_user():
    if request.method == 'GET':
        return response_body, 200

    if request.method == 'PUT':
        return response_body, 200

    if request.method == 'DELETE':
        return response_body, 200

@api.route('/roles', methods=['GET', 'POST'])
def handle_roles():
    if request.method == 'GET':
        return response_body, 200

    if request.method == 'POST':
        return response_body, 200

@api.route('/user-roles', methods=['GET', 'POST'])
def handle_roles():
    if request.method == 'GET':
        return response_body, 200

    if request.method == 'POST':
        return response_body, 200

@api.route('/user-roles/<string:username>', methods=['GET', 'PUT', 'DELETE'])
def handle_user_roles():
    if request.method == 'GET':
        return response_body, 200

    if request.method == 'PUT':
        return response_body, 200

    if request.method == 'DELETE':
        return response_body, 200

