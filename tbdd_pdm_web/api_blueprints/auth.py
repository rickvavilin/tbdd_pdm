__author__ = 'Aleksandr Vavilin'
from flask import Blueprint, render_template, request, Response, current_app, session, jsonify
import flask_sqlalchemy
from tbdd_pdm_core.api import users, exceptions

db = flask_sqlalchemy.SQLAlchemy(current_app)

node = Blueprint('auth', __name__)


@node.route('login', methods=['POST'])
def login():
    user_login = request.json.get('login')
    user_password_hash = request.json.get('password_hash')
    try:
        if users.login_user_by_password_hash(db.session, user_login, user_password_hash):
            session['login'] = user_login
            return jsonify({'result': 'OK'}), 200
    except exceptions.LoginFailedException:
        return jsonify({'result': 'login failed'}), 200


@node.route('logout')
def logout():
    session.pop('login')
    return jsonify({'result': 'OK'}), 200


@node.route('loggedin')
def loggedin():
    result = {'result': 'login' in session}
    if result['result']:
        result['userinfo'] = users.get_user_info(db.session, login=session['login'])
        del result['userinfo']['password_hash']
    return jsonify(result), 200
