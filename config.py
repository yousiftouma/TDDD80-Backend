__author__ = 'Yousif Touma'

import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Checks if we have access to openshift, if we don't we use our local database file
# I.e. we can run locally without changing anything in our code
# If we have access, we simply refer to the external data storage on openshift
if os.environ.get('OPENSHIFT_DATA_DIR') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'database.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
