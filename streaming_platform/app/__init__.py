from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes import auth, main, video
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(video.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 