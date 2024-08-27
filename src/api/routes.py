from flask import Flask, request, jsonify, url_for, Blueprint, current_app as app, render_template
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt, jwt_required, create_access_token, get_jwt_identity
from flask_mail import Mail, Message

from api.models import db, Users, Game, Genre, GameGenre, Server, Comment, Image, Setting, UserSetting, Favorite, SocialAccount
from api.utils import generate_sitemap, APIException

from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from pytz import timezone

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
    if request.method != 'POST':
        response_body['error'] = 'Método no soportado'
        return jsonify(response_body), 405
    
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

        response_body['error'] = str(e)
        response_body['token_provided'] = token
        response_body['token in db'] = user.activation_token
        response_body['message'] = 'El token es inválido o ha expirado. Se ha enviado un nuevo token de activación a tu correo electrónico.'
        return response_body, 400
    
    user.is_active = True
    user.token_expiry = None
    db.session.commit()
    response_body['message'] = 'Cuenta activada con éxito'
    return response_body, 200