import coverage
import os
import unittest

from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

COV = coverage.coverage(
    branch=True,
    include="api/*",
    omit=[
        'tests/*',
        'config.py'
        'app.py'
    ]
)

COV.start()
migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """
    Runs the unit tests without test coverage
    """
    tests = unittest.TestLoader().discover('tests', pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """
    Runs the unit tests with coverage
    """
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage summary: ")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverga')
        COV.html_report(directory=covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_database():
    """
    Creates the database tables
    """
    db.create_all()


@manager.command
def drop_database():
    """
    Drops the database tables
    """
    db.drop_all()


if __name__ == "__main__":
    manager.run()