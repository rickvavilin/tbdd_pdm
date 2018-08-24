__author__ = 'Aleksandr Vavilin'
from ..db import models
from hashlib import sha256
from .exceptions import *
from . import permissions
import sqlalchemy.exc


@permissions.check_permissions
def create_user(session, login=None, password=None, **kwargs):
    try:
        try:
            session.add(models.User(login=login, password_hash=sha256(password.encode('utf8')).hexdigest()))
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise UserAlreadyExistsException()
    finally:
        session.rollback()


@permissions.check_permissions
def delete_user(session, login=None, **kwargs):
    try:
        user = session.query(models.User).filter(models.User.login == login).first()
        session.delete(user)
        session.commit()
    finally:
        session.rollback()


def login_user_by_password_hash(session, login=None, password_hash=None, **kwargs):
    try:
        user = session.query(models.User).filter(models.User.login == login).first()
        if user:
            if user.password_hash == password_hash:
                return True
            else:
                raise IncorrectPasswordException()
        else:
            raise UserNotFoundException(login)
    finally:
        session.rollback()


def login_user(session, login=None, password=None, **kwargs):
    login_user_by_password_hash(session, login=login, password_hash=sha256(password.encode('utf8')).hexdigest())


def get_user_info(session, login=None, **kwargs):
    user = session.query(models.User).filter(models.User.login == login).first()
    if user is None:
        raise UserNotFoundException
    return user.get_dict_fields()