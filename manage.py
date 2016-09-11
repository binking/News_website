#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from IPython import embed
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from flask_migrate import MigrateCommand

from test_website.app import create_app
from test_website.models.user import User
from test_website.settings import OSxConfig, TestConfig
from test_website.database import db

if os.environ.get("HOME") == '/Users/chibin':  # Mac book env
    app = create_app(OSxConfig)
else:  # linux env
    app = create_app(TestConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


class IShell(Shell):
    def run(self, **kwargs):
        context = self.get_context()
        embed(context=context)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', IShell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    manager.run()
