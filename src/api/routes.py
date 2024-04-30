from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Role, UserRole, SocialNetwork, UserSocial, Game, Genre, GameGenre, Server, ServerStatus, ServerStatusChange, Comment, Image, Setting, UserSetting, UserStatus, UserStatusChange, ActivityLog, Favorite, SocialAccount
from api.utils import generate_sitemap, APIException
from flask_cors import CORS


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Funciones auxiliares


# Cositas que necesito
    # response_body = {}
    # response_body['results'] = "Results"
    # response_body['msg'] = "Mensaje"
    # [row.serialize() for row in variable_name]

@api.route('/signup', methods=['POST'])
def handle_signup():

    return response_body, 200


@api.route('/signin', methods=['POST'])
def handle_signin():
    
    return response_body, 200

@api.route('/users', methods=['GET'])
def handle_users():
    response_body = {}
    users = db.session.execute(db.select(Users)).scalars()
    response_body['msg'] = "User list obtained"
    response_body['results'] = [row.serialize() for row in users]
    return response_body, 200
