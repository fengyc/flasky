import threading
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail

app = current_app


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # app is a proxy, we need a real object by calling app._get_current_object()
    thread = threading.Thread(target=async_send_mail, args=[app._get_current_object(), msg])
    thread.start()
    return thread
