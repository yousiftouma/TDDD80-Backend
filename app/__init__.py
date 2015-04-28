from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#so that flask doesn't swallow error messages
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config.from_object('config')
db = SQLAlchemy(app)


from app import rest_api, models