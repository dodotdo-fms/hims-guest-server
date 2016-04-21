# -*- coding: utf-8 -*-

import csv
import logging
import logging.config
import random
import sys
import requests
from datetime import datetime
from hims_guest import app, db
from flask import current_app
from hims_guest.models.db_models import Phone
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell, Manager, Server
from coverage import coverage

reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate()
migrate.init_app(app, db, directory="./migrations")

server = Server(host="0.0.0.0", port=8080)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

@manager.command
def initall():
    createdb()

@manager.command
def createdb():
    db.init_app(current_app)
    db.create_all()


@manager.command
def dropdb():
    db.init_app(current_app)
    db.drop_all()


@manager.command
def testphone():
    from tests.test_phone import PhoneTestCase
    import unittest
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(unittest.makeSuite(PhoneTestCase))


@manager.command
def testnotice():
    from tests.test_notice import NoticeTestCase
    import unittest
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(unittest.makeSuite(NoticeTestCase))


@manager.command
def testall():
    cov = coverage(branch=True, omit=['venv/*', 'manager.py', 'tests/*'])
    cov.start()

    testphone()
    testnotice()
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()

@manager.command
def run():
    manager.run()

if __name__ == "__main__":
    manager.run()
