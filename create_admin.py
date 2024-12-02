
from app import create_app, db
from app.models import User, Admin

app = create_app()

ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin123'

with app.app_context():
    # Check if admin user already exists
    admin_user = User.query.filter_by(email=ADMIN_EMAIL).first()
    if not admin_user:
        # Create admin user
        admin_user = User(email=ADMIN_EMAIL, role='admin')
        admin_user.set_password(ADMIN_PASSWORD)
        db.session.add(admin_user)
        db.session.commit()
        
        # Create admin profile
        admin_profile = Admin(user_id=admin_user.id)
        db.session.add(admin_profile)
        db.session.commit()
        
        print('Admin user created successfully.')
    else:
        print('Admin user already exists.')