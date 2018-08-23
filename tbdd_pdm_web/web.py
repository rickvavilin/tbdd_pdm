__author__ = 'Aleksandr Vavilin'
from flask import Flask, render_template
import flask_sqlalchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .api_blueprints import register_api_blueprints


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='^(',
        variable_end_string=')$',
    ))


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = CustomFlask(__name__, template_folder='../resources/templates', static_folder='../resources/static', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///test_web.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = flask_sqlalchemy.SQLAlchemy(app)


@app.route('/')
def mainpage():
    return render_template('index.html')

with app.app_context():
    register_api_blueprints(app)