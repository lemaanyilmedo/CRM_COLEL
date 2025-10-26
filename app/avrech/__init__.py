from flask import Blueprint

bp = Blueprint('avrech', __name__)

from app.avrech import routes