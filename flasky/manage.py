# A flask-script manager

from flask.ext.script import Manager

from flasky.app import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()