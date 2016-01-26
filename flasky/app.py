import datetime
import hashlib

from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

app.config['SECRET_KEY'] = hashlib.sha256('TOP_SECRET'.encode()).hexdigest()

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html',
                           user_agent=user_agent,
                           current_time=datetime.datetime.utcnow(),
                           form=form,
                           name=name)


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