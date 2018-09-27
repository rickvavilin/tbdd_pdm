from flask import Blueprint, request, Response, current_app, session, jsonify
import flask_sqlalchemy
from tbdd_pdm_core.api import exceptions, users, groups
__author__ = 'Aleksandr Vavilin'

db = flask_sqlalchemy.SQLAlchemy(current_app)

node = Blueprint('users', __name__)


@node.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        results_per_page = request.args.get('results_per_page', 20)
        page = request.args.get('page', 1)
        return jsonify(users.get_list(db.session,
                                      results_per_page=results_per_page,
                                      page=page,
                                      simple_filter=request.args.get('simple_filter')))
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({}), 400
        try:
            return jsonify(users.create_user(db.session, _current_user_login=session.get('login'), **request.json))
        except exceptions.UserAlreadyExistsException:
            return jsonify({'message': 'Пользователь уже существует'}), 400


@node.route('/<string:login>', methods=['GET', 'POST', 'DELETE'])
def get_user_by_id(login):
    try:
        if request.method == 'GET':
            return jsonify(users.get_user_info(db.session, login, _current_user_login=session.get('login')))
        elif request.method == 'POST':
            if not request.is_json:
                return jsonify({}), 400
            request.json['login'] = login
            return jsonify(users.update_user(db.session, _current_user_login=session.get('login'), **request.json))
        elif request.method == 'DELETE':
            logged_in_user = session.get('login')
            if logged_in_user == login:
                return jsonify({'message': 'Пользователь не может удалить свою учетную запись'}), 400
            return jsonify(users.delete_user(db.session, login, _current_user_login=logged_in_user))
    except exceptions.DetailNotFoundException as e:
        return jsonify({}), 404


@node.route('/password', methods=['POST'])
def change_own_password():
    if not request.is_json:
        return jsonify({}), 400
    users.change_own_password(db.session,
                              password=request.json['password'],
                              _current_user_login=session.get('login'))


@node.route('/password/<string:login>', methods=['POST'])
def change_password(login):
    if not request.is_json:
        return jsonify({}), 400
    users.change_password(db.session,
                          login=login,
                          password=request.json['password'],
                          _current_user_login=session.get('login'))


@node.route('/<string:login>/groups', methods=['GET', 'POST'])
def get_user_groups(login):
    if request.method == 'GET':
        return jsonify(groups.get_groups_of_user(db.session,
                                                 user_login=login,
                                                 _current_user_login=session.get('login')))
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({}), 400
        group_name = request.json['group']
        return jsonify(groups.add_user_to_group(db.session,
                                                group_name=group_name,
                                                user_login=login,
                                                _current_user_login=session.get('login')))


@node.route('/<string:login>/groups/<string:group_name>', methods=['DELETE'])
def remove_user_from_group(login, group_name):
    return jsonify(groups.remove_user_from_group(db.session,
                                                 group_name=group_name,
                                                 user_login=login,
                                                 _current_user_login=session.get('login')))
