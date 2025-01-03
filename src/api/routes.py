from flask import Flask, redirect, request, jsonify, url_for, Blueprint, current_app as app, render_template
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_mail import Mail, Message

from api.models import db, Users, Game, Genre, GameGenre, Server, Comment, Image, Setting, UserSetting, Favorite, SocialAccount
from api.utils import generate_sitemap, APIException

from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from pytz import timezone

import socket

# DEBUG
import traceback

# Crear el blueprint
api = Blueprint('api', __name__)
CORS(api)

# Inicializar bcrypt
bcrypt = Bcrypt()

# Métodos auxiliares
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    app.extensions['mail'].send(msg)

# Estado de los servidores
@api.route('/server-status', methods=['GET'])
def get_servers_status():
    try:
        servers = Server.query.all()
        server_list = []

        for server in servers:
            # Verificamos el estado del servidor usando socket
            try:
                with socket.create_connection((server.ip_address, server.port), timeout=5):
                    status = "🟢"
            except (socket.timeout, socket.error):
                status = "🔴"

            server_list.append({
                "game_id": server.game_id,
                "name": server.name,
                "ip_address": server.ip_address,
                "port": server.port,
                "status": status
            })

        return jsonify({"servers": server_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Configuración de rutas
@api.route('/debug-send-test-email', methods=['GET'])
def send_test_email():
    send_email('to@example.com', 'Prueba de correo electrónico', 
               '''
               <h1>Esto es un correo electrónico de prueba</h1>
               <p>Este correo electrónico ha sido enviado desde un script de prueba.</p>
               <p>Puedes borrar este correo electrónico si no lo deseas recibir más.</p>
               ''')
    return 'Correo electrónico de prueba enviado.'

@api.route('/signup', methods=['POST'])
def handle_signup():
    response_body = {}
    safe_time = app.config['safeTime']    
    data = request.get_json()
    required_data = ['username','email','password']
    for key in required_data:
        if key not in data:
            response_body['message'] = f"Falta {key} en el body"
            return response_body, 400
        
    # DEPRECATED:
    # user = db.session.execute(db.select(Users).filter(Users.username.ilike(data.get('username')))).scalar()
    email_lowercase = data.get('email').lower()
    user = Users.find_by_username(data.get('username'))
    userEmail = Users.find_by_email(email_lowercase)
    if user or userEmail:
        response_body['message'] = f"Usuario ya existente."
        return response_body, 401
    
    hashed_password = bcrypt.generate_password_hash(str(data.get('password'))).decode('utf-8')
    user = Users(username=data.get('username'), email=email_lowercase, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    # Creamos el activation_token
    user.activation_token = safe_time.dumps(user.email, salt=app.config['JWT_SECRET_KEY'])
    user.token_expiry = datetime.now(timezone('UTC')) + timedelta(hours=24)
    db.session.commit()
    send_email(user.email, 'Activate Your Account', 
               f'''
                <h1>Activa tu cuenta!</h1>
                <p>Gracias por su registro. Por favor haz click en el enlace para activar tu cuenta:</p>
                <a href="{url_for('api.activate_account', token=user.activation_token, _external=True)}">Activar tu cuenta!</a>
                <p>El link expirará en 24 horas.</p>
                '''
               )
    
    response_body['token'] = user.activation_token
    response_body['message'] = f"Usuario registrado, correo enviado a {user.email} para activar la cuenta."
    return response_body, 200

@api.route('/activate/<token>', methods=['GET'])
def activate_account(token):
    response_body = {}
    safe_time = app.config['safeTime']
    user = Users.find_by_activation_token(token)
    if not user:
        response_body['message'] = 'El token es inválido o no se pudo encontrar al usuario.'
        return jsonify(response_body), 400
    
    if user.is_active:
        response_body['message'] = 'La cuenta ya está activa'
        return response_body, 200
    
    try:
        email = safe_time.loads(token, salt=app.config['JWT_SECRET_KEY'], max_age=86400)  # Token válido por 24 horas
    except Exception as e: # Si el token es inválido o ha expirado
        user.activation_token = safe_time.dumps(user.email, salt=app.config['JWT_SECRET_KEY'])
        user.token_expiry = datetime.now(timezone('UTC')) + timedelta(hours=24)
        db.session.commit()

        send_email(
            to=user.email,
            subject='Nuevo token de activación',
            template=f'''
            <h1>Tu token ha expirado</h1>
            <p>Tu token de activación ha expirado. Por favor, haz clic en el siguiente enlace para activar tu cuenta:</p>
            <a href="{url_for('api.activate_account', token=user.activation_token, _external=True)}">Activar tu cuenta!</a>
            <p>El nuevo enlace expirará en 24 horas.</p>
            '''
        )
        response_body['token'] = user.activation_token
        response_body['message'] = 'El token es inválido o ha expirado. Se ha enviado un nuevo token de activación a tu correo electrónico.'
        return response_body, 400
    
    user.is_active = True
    user.token_expiry = None
    db.session.commit()
    response_body['message'] = 'Cuenta activada con éxito'
    return response_body, 200

@api.route('/check-pwd', methods=['POST'])
@jwt_required()
def check_password():
    response_body = {}  
    current_user = get_jwt_identity()
    data = request.get_json()
    required_data = ['password']
    for key in required_data:
        if key not in data:
            response_body['message'] = f"Falta {key} en el body"
            return response_body, 400

    user = Users.find_by_email(current_user['email'])
    if not user or not bcrypt.check_password_hash(user.password, data.get('password')):
        response_body['message'] = "Contraseña incorrecta"
        return response_body, 401

    response_body['message'] = "Contraseña correcta"
    return response_body, 200

@api.route('/forgot-pwd', methods=['POST'])
def forgot_password():
    response_body = {}  
    data = request.get_json()
    required_data = ['email']
    for key in required_data:
        if key not in data:
            response_body['message'] = f"Falta {key} en el body"
            return response_body, 400

    user = Users.find_by_email(data.get('email'))
    if not user:
        response_body['message'] = "No se encontró un usuario con ese correo electrónico"
        return response_body, 404

    user.reset_token = app.config['safeTime'].dumps(user.email, salt=app.config['JWT_SECRET_KEY'])
    user.token_expiry = datetime.now(timezone('UTC')) + timedelta(hours=1)
    db.session.commit()

    send_email(
            to=user.email,
            subject='Reinicio de contraseña',
            template=f'''
            <h1>Has pedido un reinicio de tu contraseña</h1>
            <p>Si no has pedido un reinicio de contraseña, por favor, ignora este email.</p>
            <p>En caso contrario, haz click en el enlace para reiniciar tu contraseña:</p>
            <a href="{url_for('api.reset_pwd', token=user.reset_token, _external=True)}">Recuperar contraseña</a>
            <p>El enlace expirará en 1 hora.</p>
            '''
        )
    response_body['token'] = user.reset_token
    response_body['message'] = f"Correo electrónico enviado a {user.email} para reiniciar tu contraseña."
    return response_body, 200

@api.route('/reset-pwd/<token>', methods=['GET'])
def reset_pwd(token):
    response_body = {}  
    safe_time = app.config['safeTime']
    user = Users.find_by_reset_token(token)
    if not user:
        response_body['message'] = 'El token es inválido o no se pudo encontrar al usuario.'
        return response_body, 400
    
    try:
        email = safe_time.loads(token, salt=app.config['JWT_SECRET_KEY'], max_age=3600)  # Token válido por 1 hora
    except Exception as e: # Si el token es inválido o ha expirado
        user.reset_token = app.config['safeTime'].dumps(user.email, salt=app.config['JWT_SECRET_KEY'])
        user.token_expiry = datetime.now(timezone('UTC')) + timedelta(hours=1)
        db.session.commit()

        send_email(
            to=user.email,
            subject='Nuevo token de reinicio de contraseña',
            template=f'''
            <h1>Tu token de reinicio de contraseña ha expirado</h1>
            <p>Tu token de reinicio de contraseña ha expirado. Por favor, haz clic en el siguiente enlace para reiniciar tu contraseña:</p>
            <a href="{url_for('api.reset_pwd', token=user.reset_token, _external=True)}">Recuperar contraseña</a>
            <p>El nuevo enlace expirará en 1 hora.</p>
            '''
        )
        response_body['token'] = user.reset_token
        response_body['message'] = 'El token ha expirado. Se ha enviado un nuevo token a tu correo electrónico.'
        return jsonify(response_body), 400
    
    return redirect(f"{app.config['FRONTEND_URL']}/reset-password?token={token}")

@api.route('/update-pwd', methods=['POST'])
def update_password():
    response_body = {}
    safe_time = app.config['safeTime']
    data = request.get_json()
    token = data.get('token')
    new_password = str(data.get('password'))
    confirm_password = str(data.get('confirmPassword'))

    if new_password != confirm_password:
        response_body['message'] = 'Las contraseñas no coinciden.'
        return response_body, 400
  
    user = Users.find_by_reset_token(token)
    if not user:
        response_body['message'] = 'El token es inválido o no se pudo encontrar al usuario.'
        return response_body, 400

    try:
        email = safe_time.loads(token, salt=app.config['JWT_SECRET_KEY'], max_age=3600)  # Token válido por 1 hora
    except Exception as e:  # Si el token es inválido o ha expirado
        response_body['message'] = 'El token es inválido o ha expirado.'
        return response_body, 400

    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.reset_token = None
    user.token_expiry = None
    db.session.commit()

    response_body['message'] = 'Contraseña actualizada con éxito.'
    return response_body, 200

@api.route('/login', methods=['POST'])
def login():
    response_body = {}
    data = request.get_json()
    username = data.get('username', None)
    email = data.get('email', None).lower()
    if not email and not username:
        response_body['message'] = f"Falta un username o un email en el body"
        return response_body, 400
    
    password = data.get('password', None)
    if not password:
        response_body['message'] = "Falta password en el body"
        return response_body, 400
    
    if email:
        user = Users.find_by_email(email)
    if username:
        user = Users.find_by_username(username)

    if not user:
        response_body['message'] = "Usuario no registrado."
        return response_body, 404
    
    if not user.is_active:
        response_body['message'] = "Cuenta inactiva."
        return response_body, 403

    if bcrypt.check_password_hash(user.password, str(data.get('password'))):
        response_body['message'] = "Inicio de sesión exitoso."
        response_body['access_token'] = create_access_token(identity=user.serialize(), expires_delta=timedelta(hours=1))
        response_body['refresh_token'] = create_refresh_token(identity=user.serialize())
        response_body['results'] = user.serialize()
        
        return response_body, 200
    
    response_body['message'] = "Contraseña incorrecta."
    return response_body, 401

@api.route('/game-info/<int:game_id>', methods=['GET'])
def get_game_info(game_id):
    try:
        game = Game.query.get(game_id)
        if not game:
            return jsonify({"error": "Juego no encontrado"}), 404

        # Obtener géneros desde la relación intermedia
        genres = [relation.genre.name for relation in game.genres]

        # Construir la respuesta
        game_info = {
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "release_date": game.release_date.isoformat() if game.release_date else None,
            "developer": game.developer,
            "publisher": game.publisher,
            "genres": genres,
        }
        return jsonify(game_info), 200
    except Exception as e:
        # Registro del error para depuración
        print("Error en get_game_info:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    
@api.route('/game-images/<int:game_id>', methods=['GET'])
def get_game_images(game_id):
    try:
        # Consulta para obtener imágenes relacionadas con el juego
        images = Image.query.filter_by(game_id=game_id).all()

        # Construir respuesta con la información de cada imagen
        image_data = [
            {
                "url": image.url,
                "caption": image.caption,
                "user": image.user.username if image.user else None,  # Relación con la tabla de usuarios
                "uploaded_at": image.uploaded_at.isoformat() if image.uploaded_at else None
            }
            for image in images
        ]

        return jsonify({"images": image_data}), 200
    except Exception as e:
        import traceback
        print("Error en get_game_images:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

