import flask
from flask_login import login_required, current_user
from . import main_bp
from ..models import User

@main_bp.route('/')
@login_required
def index():
    return flask.render_template('iStyleApp/welcome.html')

@main_bp.route('/select')
@login_required
def select():
    return flask.render_template('iStyleApp/select.html')

@main_bp.route('/transactions')
@login_required
def transaction():
    return flask.render_template('iStyleApp/transactions.html')

@main_bp.route('/category')
@login_required
def category():
    return flask.render_template('iStyleApp/category.html')
