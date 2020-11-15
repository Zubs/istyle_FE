import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, os.environ.get('DATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    MAIL_SERVER = (os.environ.get('MAIL_SERVER') or 'localhost')
    MAIL_PORT = (os.environ.get('MAIL_PORT') or 1025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
