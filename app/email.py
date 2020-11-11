# '''Module that handles view of everything that has to do with mailing'''
import smtplib
from socket import gaierror
from flask import current_app as app
from app import mail
from flask_mail import Message

def send_mail(subject, recipient, text, html, pdf_attachment=None, pdf_name=None, image_attachment=None):
    try:
        msg = Message(
            subject=subject, 
            sender='koikibabatunde14@gmail.com',  
            recipients=[recipient]
        )
        msg.body=text
        msg.html=html
        mail.send(msg)

    except (gaierror, ConnectionRefusedError):
        return('Failed to connect to the server. Bad connection settings?')
        
    except smtplib.SMTPServerDisconnected:
        return('Failed to connect to the server. Wrong user/password?')

    except smtplib.SMTPException as e:
        return('SMTP error occurred: ' + str(e))

    except Exception as e:
        return('Something went wrong...'+str(e))