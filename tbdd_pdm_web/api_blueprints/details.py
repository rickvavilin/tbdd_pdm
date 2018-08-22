__author__ = 'Aleksandr Vavilin'
from flask import Blueprint, render_template, request, Response, current_app, session, jsonify
import flask_sqlalchemy
from tbdd_pdm_core.api import details, exceptions

db = flask_sqlalchemy.SQLAlchemy(current_app)

node = Blueprint('details', __name__)


@node.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        results_per_page = request.args.get('results_per_page', 20)
        page = request.args.get('page', 1)
        return jsonify(details.get_list(db.session,
                                        results_per_page=results_per_page,
                                        page=page))
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({}), 400
        try:
            return jsonify(details.create_detail(db.session, **request.json))
        except exceptions.DetailAlreadyExistsException:
            return jsonify({'message': 'Деталь уже существует'}), 400


@node.route('<int:detail_id>', methods=['GET', 'POST', 'DELETE'])
def get_detail_by_id(detail_id):
    try:
        if request.method == 'GET':
            return jsonify(details.get_detail_by_id(db.session, detail_id))
        elif request.method == 'POST':
            if not request.is_json:
                return jsonify({}), 400
            request.json['id'] = int(detail_id)
            print(request.json)
            return jsonify(details.update_detail(db.session, **request.json))
        elif request.method == 'DELETE':
            return jsonify(details.delete_detail(db.session, detail_id))
    except exceptions.DetailNotFoundException as e:
        return jsonify({}), 404


