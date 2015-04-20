#!/usr/bin/env python
import os

virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR', '.'), 'virtenv')

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

from app import app as application


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 4599, application)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()

