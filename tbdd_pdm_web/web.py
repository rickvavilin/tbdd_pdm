from flask import Flask, render_template
import flask_sqlalchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.dialects.sqlite.base import SQLiteDialect
from tbdd_pdm_core.api import exceptions
from tbdd_pdm_core.config import get_config
from .api_blueprints import register_api_blueprints
__author__ = 'Aleksandr Vavilin'


# set alternative variable parenthesis for Jinja because we use VueJS on frontend
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='^(',
        variable_end_string=')$',
    ))

config = get_config()
app = CustomFlask(__name__,
                  template_folder=config.get('template_folder', '../resources/templates'),
                  static_folder=config.get('static_folder', '../resources/static'),
                  static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_connection_string']
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = flask_sqlalchemy.SQLAlchemy(app)

if issubclass(db.engine.url.get_dialect(), SQLiteDialect):
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@app.errorhandler(exceptions.ActionNotPermitted)
def error_handler_not_permitted(_):
    return 'Access Forbidden', 403


@app.route('/')
def mainpage():
    return render_template('index.html')


with app.app_context():
    register_api_blueprints(app)
