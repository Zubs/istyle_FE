from . import db, login_manager
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, time, jwt


@login_manager.user_loader
def load_user(id):
    try:return User.query.get(int(id))
    except: return None

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    password_hash=db.Column(db.String(80))
    admin=db.Column(db.Boolean)
    is_seller=db.Column(db.Boolean)
    author=db.Column(db.Boolean)
    address=db.Column(db.String(100))
    company=db.Column(db.String(50))
    
    def __repr__(self):
        return f'<User {self.name}>'

    def create_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)        

    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time()+expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
            current_app.config['SECRET_KEY'],
             algorithm='HS256'
            )['reset_password']
        except:
            return None
        return User.query.get(int(id))