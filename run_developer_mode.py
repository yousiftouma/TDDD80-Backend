__author__ = 'Yousif Touma'

#!flask/bin/python
from app import app

if __name__ == '__main__':
    app.run(port=4599, debug=True)