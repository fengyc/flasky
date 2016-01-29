import datetime
import hashlib
import os
import threading

from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = hashlib.sha256('TOP_SECRET'.encode()).hexdigest()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# email
app.config['MAIL_SERVER'] = 'smtp.ym.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = os.environ.get('MAIL_SENDER') or os.environ.get('MAIL_USERNAME')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %s>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %s>' % self.username


def init_db():
    db.drop_all()
    db.create_all()
    admin_role = Role(name='Admin')
    mod_role = Role(name='Moderator')
    user_role = Role(name='User')
    user_john = User(username='john', role=admin_role)
    user_susan = User(username='susan', role=user_role)
    user_david = User(username='david', role=user_role)
    db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan,
                       user_david])
    db.session.commit()


def async_send_mail(app, msg):
    with app.app_context:
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thread = threading.Thread(target=async_send_mail, args=[app, msg])
    thread.start()
    return thread


@app.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(username = name).first()
        if user is None:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        oldname = session.get('name')
        if oldname is not None and oldname != name:
            flash('Look like you have changed your name!')
        session['name'] = name
        form.name.data = ''
        return redirect(url_for('index'))   # post redirect to get pattern
    return render_template('index.html',
                           user_agent=user_agent,
                           current_time=datetime.datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/')
@app.route('/user/<string:name>')
def user(name=None):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def handle_404():
    return render_template('404.html')


@app.errorhandler(500)
def handle_500():
    return render_template('500.html')


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')



if __name__ == '__main__':
    app.run(debug=True)