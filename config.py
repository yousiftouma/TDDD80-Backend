__author__ = 'Yousif Touma'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# for unit tests, make server local
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# for deployment
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'database.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')