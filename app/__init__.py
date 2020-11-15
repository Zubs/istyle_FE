import flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config=Config):
    app = flask.Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.signin'
    login_manager.login_message = 'You must be logged in to view that page'
    mail.init_app(app)

    # Auth blueprint
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .main import main_bp
    app.register_blueprint(main_bp)

    from .models import User


    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return flask.redirect(flask.url_for('dashboard.index'))
        return flask.render_template('index.html')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User
        }


    return app


