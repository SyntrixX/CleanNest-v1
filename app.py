from flask import Flask
from app.auth.routes import bp as auth_bp
from app.professional.routes import bp as professional_bp
from app.admin.routes import bp as admin_bp
from app.customer.routes import bp as customer_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.DevelopmentConfig')
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(professional_bp, url_prefix='/professional')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    
    @app.route('/')
    def home():
        return 'Hello, World!'
    
    # Custom error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return 'Page not found', 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return 'Internal server error', 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)