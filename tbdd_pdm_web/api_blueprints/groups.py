from flask import Blueprint, request, Response, current_app, session, jsonify
import flask_sqlalchemy
from tbdd_pdm_core.api import exceptions, groups
__author__ = 'Aleksandr Vavilin'

db = flask_sqlalchemy.SQLAlchemy(current_app)

node = Blueprint('groups', __name__)


@node.route('')
def index():
    results_per_page = request.args.get('results_per_page', 20)
    page = request.args.get('page', 1)
    return jsonify(groups.get_list(db.session,
                                  results_per_page=results_per_page,
                                  page=page,
                                  simple_filter=request.args.get('simple_filter')))
