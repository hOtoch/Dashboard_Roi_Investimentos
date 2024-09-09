from flask import Blueprint

# Importar os blueprints das rotas
from .usuarios import usuarios_bp
from .login import login_bp
from .contas import contas_bp
from .ciclomes import ciclomes_bp
from .dias import dias_bp

def register_blueprints(app):
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(contas_bp)
    app.register_blueprint(ciclomes_bp)
    app.register_blueprint(dias_bp)
 
