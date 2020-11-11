'''Main BluePrint'''
from flask import Blueprint

main_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from . import routes