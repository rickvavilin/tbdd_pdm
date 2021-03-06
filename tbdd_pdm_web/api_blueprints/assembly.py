import csv
from flask import Blueprint, render_template, request, Response, current_app, session, jsonify
import flask_sqlalchemy
import io
from tbdd_pdm_core.api import details, files, exceptions
__author__ = 'Aleksandr Vavilin'



db = flask_sqlalchemy.SQLAlchemy(current_app)

node = Blueprint('assembly', __name__)


@node.route('', methods=['GET'])
def index():
    results_per_page = request.args.get('results_per_page', 20)
    page = request.args.get('page', 1)
    return jsonify(details.get_assembly_list(db.session,
                                    results_per_page=results_per_page,
                                    page=page,
                                    simple_filter=request.args.get('simple_filter'),
                                    _current_user_login=session.get('login')))


@node.route('/tree/<int:parent_id>', methods=['GET'])
def get_assembly_tree(parent_id):
    return jsonify(details.get_assembly_tree(db.session,
                                    parent_id=parent_id,
                                    _current_user_login=session.get('login')))


@node.route('/add/<int:parent_id>/<int:child_id>/<int:count>')
def add_detail_to_assembly(parent_id, child_id, count):
    if count < 1:
        raise exceptions.CountMustBeGreaterThanZeroException()
    return jsonify(details.add_detail_to_assembly(db.session, parent_id=parent_id, child_id=child_id, count=count))


@node.route('/remove/<int:parent_id>/<int:child_id>')
def remove_detail_from_assembly(parent_id, child_id):
    return jsonify(details.remove_detail_from_assembly(db.session, parent_id=parent_id, child_id=child_id))


@node.route('/bom/<int:parent_id>')
def calculate_bom(parent_id):
    bom = details.calculate_bom(db.session, parent_id=parent_id)
    strio = io.StringIO()
    writer = csv.writer(strio)
    for b in bom:
        writer.writerow([b['item']['code'], b['item']['name'], b['item']['description'], b['count']])
    strio.seek(0)
    response = Response(strio.read())
    response.headers.set('Content-disposition', 'attachment', filename='out.csv')
    return response

