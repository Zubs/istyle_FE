'''Module that handles view of everything that has to do with authN and authZ'''
from werkzeug.security import (generate_password_hash, 
                    check_password_hash)
import flask
from flask_login import login_user, logout_user, current_user
from app import db
from . import auth_bp
from ..models import User
from ..email import send_mail

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('dashboard.index'))
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        email = flask.request.form['email']
        password = flask.request.form['password']
        u = User.query.filter_by(email=email).first()
        if u:
            flask.flash('Email taken, choose another', 'error')
        elif len(password) < 8:
            flask.flash('Password too short', 'error')
        else:
            u = User(name=name, email=email)
            u.create_password_hash(password)
            db.session.add(u)
            db.session.commit()
            login_user(u, remember=True)
            return flask.redirect(flask.url_for('dashboard.index'))
    return flask.render_template('auth/Sign Up.html')

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('dashboard.index'))
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        password = flask.request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flask.flash('You are logged in', 'success')
            next_page=flask.request.args.get('next')
            return flask.redirect(next_page) if next_page else \
                 flask.redirect(flask.url_for('dashboard.index'))
        flask.flash('Invalid login details', 'error')
    return flask.render_template('auth/Sign In.html')

@auth_bp.route('/logout')
def signout():
    logout_user()
    return flask.redirect(flask.url_for('index'))

@auth_bp.route('/get_password_token', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('dashboard.index'))
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_reset_password_token()
            msg = flask.render_template('mail/reset_password.txt', 
                                        token=token,
                                        sender=flask.current_app.config['MAIL_USERNAME'], 
                                        user=user)
            msg_html = flask.render_template('mail/reset_password.html', 
                                        token=token,
                                        sender=flask.current_app.config['MAIL_USERNAME'], 
                                        user=user)
            mail = send_mail(
                'iStyle -- Reset Your Password', 
                user.email, msg, msg_html
            )
            if mail:
                flask.abort(500)
            flask.flash('Instructions on how to reset your password has been sent to your mail', 'info')
    return flask.render_template('auth/forgotpassword.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('dashboard.index'))
    # verify token
    user = User.verify_reset_password_token(token)
    if not user:
        return flask.redirect(flask.url_for('dashboard.index'))
    if flask.request.method == 'POST':
        password = flask.request.form['password']
        confirm_password = flask.request.form['confirm password']
        if password != confirm_password:
            flask.flash('Password and confirm password field must be the same')
        elif len(password) < 8:
            flask.flash('Password too short', 'error')
        else:
            user.create_password_hash(password)
            db.session.commit()

            return flask.redirect(flask.url_for('auth.signin'))
    return flask.render_template('auth/resetpassword.html')