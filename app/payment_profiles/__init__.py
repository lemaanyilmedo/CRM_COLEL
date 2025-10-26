from flask import Blueprint

bp = Blueprint('payment_profiles', __name__)

from app.payment_profiles import routes