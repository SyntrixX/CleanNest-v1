from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.professional import bp
from app.models import ServiceRequest, Professional, db

@bp.route('/')
@login_required
def home():
    professional = Professional.query.filter_by(user_id=current_user.id).first()
    if not professional:
        flash('Professional profile not found.', 'danger')
        return redirect(url_for('professional.home'))
    pending_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='pending').all()
    active_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='active').all()
    completed_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status='completed').all()
    recent_requests = ServiceRequest.query.filter_by(professional_id=professional.id).order_by(ServiceRequest.created_at.desc()).limit(5).all()
    return render_template('professional/home.html', professional=professional, pending_requests=pending_requests, active_requests=active_requests, completed_requests=completed_requests, recent_requests=recent_requests)

@bp.route('/requests')
@login_required
def requests():
    professional = Professional.query.filter_by(user_id=current_user.id).first()
    if not professional:
        flash('Professional profile not found.', 'danger')
        return redirect(url_for('main.index'))
    status = request.args.get('status', 'pending')
    service_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status=status).all()
    return render_template('professional/requests.html', requests=service_requests, status=status)

@bp.route('/accept_request/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'active'
    db.session.commit()
    return redirect(url_for('professional.requests', status='pending'))

@bp.route('/reject_request/<int:request_id>', methods=['POST'])
@login_required
def reject_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('professional.requests', status='pending'))

@bp.route('/complete_request/<int:request_id>', methods=['POST'])
@login_required
def complete_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = 'completed'
    db.session.commit()
    return redirect(url_for('professional.requests', status='active'))

@bp.route('/request_detail/<int:request_id>')
@login_required
def request_detail(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    return render_template('professional/request_detail.html', request=service_request)

@bp.route('/profile')
@login_required
def profile():
    professional = Professional.query.filter_by(user_id=current_user.id).first()
    return render_template('professional/profile.html', professional=professional)
