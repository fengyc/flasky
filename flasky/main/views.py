import datetime
from flask import render_template, session, url_for, redirect, request, flash, current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_mail

app = current_app


@main.route('/', methods=['GET', 'POST'])
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
            if app.config.get('FLASKY_ADMIN'):
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        oldname = session.get('name')
        if oldname is not None and oldname != name:
            flash('Look like you have changed your name!')
        session['name'] = name
        form.name.data = ''
        return redirect(url_for('.index'))   # post redirect to get pattern
    return render_template('index.html',
                           user_agent=user_agent,
                           current_time=datetime.datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


@main.route('/user/')
@main.route('/user/<string:name>')
def user(name=None):
    return render_template('user.html', name=name)