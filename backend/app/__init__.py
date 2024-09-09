from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar SQLAlchemy
db = SQLAlchemy()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurar o banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    expiration = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=expiration)

    # Inicializar a conexão com o banco de dados
    db.init_app(app)
    jwt.init_app(app)
    
    from .routes import register_blueprints
    register_blueprints(app)

    return app
