from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from app.filters import status_color

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.professional import bp as professional_bp
    app.register_blueprint(professional_bp, url_prefix='/professional')

    from app.customer import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customer')

    app.jinja_env.filters['status_color'] = status_color

    @app.route('/')
    def home():
        return render_template('home.html')

    return app