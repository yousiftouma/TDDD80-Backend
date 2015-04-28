__author__ = 'Yousif Touma'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_SQLITE_DB_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#'sqlite:///' + os.path.join(basedir, 'database.db')