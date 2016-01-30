#!/usr/bin/env python3

import os
from flasky import create_app, db
from flasky.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app((os.environ.get('FLASKY_CONFIG')) or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """ Run unittests
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
