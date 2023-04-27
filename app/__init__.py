from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 

db = SQLAlchemy()
bootstrap = Bootstrap()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    
    app.secret_key = '5d65148e9473eb74cd2f94bc8085bfce'
    app.config.from_object(config[config_name])
    
    config[config_name].init_app(app)
    
    login_manager = LoginManager(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    bootstrap.init_app(app)
    db.init_app(app)
    return app
