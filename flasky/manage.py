# A flask-script manager

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from flasky.app import app
from flasky.app import db

migrate = Migrate(app, db=db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()