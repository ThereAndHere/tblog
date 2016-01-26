#!/bin/env python3

import os
from app import create_app, db
from app.models import User, Role, Post, Commit
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_comtext():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Commit=Commit)

manager.add_command("shell", Shell(make_context=make_shell_comtext))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()