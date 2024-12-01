from flask import Blueprint

bp = Blueprint('professional', __name__)

from app.professional import routes