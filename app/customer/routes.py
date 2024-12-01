from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db
from app.customer import bp
from app.models import Service, ServiceRequest, Customer

@bp.route('/')
@login_required
def home():
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    return render_template('customer/home.html', customer=customer)

@bp.route('/services')
@login_required
def services():
    services = Service.query.all()
    return render_template('customer/services.html', services=services)

@bp.route('/requests')
@login_required
def requests():
    requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    return render_template('customer/requests.html', requests=requests)

# Remove the profile route
# @bp.route('/profile')
# @login_required
# def profile():
#     customer = Customer.query.filter_by(user_id=current_user.id).first()
#     return render_template('customer/profile.html', customer=customer)

@bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        # Update customer details with form data
        customer.name = request.form['name']
        customer.phone = request.form['phone']
        customer.address = request.form['address']
        # Handle profile image upload if provided
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image.filename != '':
                # Save the profile image and update the customer profile_image attribute
                filename = secure_filename(profile_image.filename)
                profile_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                customer.profile_image = filename
        db.session.commit()
    return render_template('customer/update_profile.html', customer=customer)