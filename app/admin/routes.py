from flask import render_template, redirect, url_for, request
from flask_login import login_required
from app.admin import bp
from app.models import User, Service, ServiceRequest, Professional
from app import db

@bp.route('/')
@login_required
def home():
    return render_template('admin/home.html')

@bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/services')
@login_required
def services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@bp.route('/service_requests')
@login_required
def service_requests():
    requests = ServiceRequest.query.all()
    professionals = Professional.query.all()
    return render_template('admin/service_requests.html', requests=requests, professionals=professionals)

@bp.route('/edit-user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    # Logic to update user details
    # ...
    return redirect(url_for('admin.users'))

@bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@bp.route('/add-service', methods=['POST'])
@login_required
def add_service():
    name = request.form.get('name')
    category = request.form.get('category')
    description = request.form.get('description')
    price = request.form.get('price')
    professional_id = request.form.get('professional_id')  # Get professional ID from form
    new_service = Service(name=name, category=category, description=description, price=price)
    db.session.add(new_service)
    db.session.commit()
    
    # Assign professional if provided
    if professional_id:
        service_request = ServiceRequest(service_id=new_service.id, professional_id=professional_id, status='pending')
        db.session.add(service_request)
        db.session.commit()
    
    return redirect(url_for('admin.services'))

@bp.route('/edit_service_request/<int:request_id>', methods=['POST'])
@login_required
def edit_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = request.form.get('status')
    service_request.professional_id = request.form.get('professional_id') or None
    db.session.commit()
    return redirect(url_for('admin.service_requests'))

@bp.route('/delete_service_request/<int:request_id>', methods=['POST'])
@login_required
def delete_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    db.session.delete(service_request)
    db.session.commit()
    return redirect(url_for('admin.service_requests'))