from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', user_agent=user_agent)


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


if __name__ == '__main__':
    app.run(debug=True)