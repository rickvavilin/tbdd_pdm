__author__ = 'Aleksandr Vavilin'
from flask import Blueprint, render_template, request, Response, current_app, session, jsonify
import flask_sqlalchemy
from werkzeug.utils import secure_filename
from tbdd_pdm_core.api import details, files, exceptions

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


@node.route('<int:detail_id>/files', methods=['POST'])
def add_files_to_detail(detail_id):
    try:
        for filename, file in request.files.items():
            files.add_file_to_detail(db.session, detail_id=detail_id, filename=filename, filedata=file.read())
    except exceptions.FileAlreadyExistsException:
        return jsonify({'result': 'Файл уже существует: {}'.format(filename)}), 400
    return jsonify({'result': 'OK'})


@node.route('<int:detail_id>/files/<filename>', methods=['GET', 'DELETE'])
def process_file_from_detail(detail_id, filename):
    if request.method == 'GET':
        response = Response(
            files.get_file_data_by_detail_and_name(
                db.session,
                detail_id=detail_id,
                filename=filename
            )
        )
        response.headers.set('Content-disposition', 'attachment', filename=filename.encode('utf8'))
        return response
    elif request.method == 'DELETE':
        files.delete_file_by_detail_and_name(db.session, detail_id=detail_id, filename=filename)
        return jsonify({'result': 'OK'})


