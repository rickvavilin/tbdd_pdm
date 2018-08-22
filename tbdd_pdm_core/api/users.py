__author__ = 'Aleksandr Vavilin'
from ..db import models
from hashlib import sha256
from .exceptions import *


def create_user(session, login=None, password=None, **kwargs):
    session.add(models.User(login=login, passwordhash=sha256(password)))
    session.commit()


def delete_user(session, login=None, **kwargs):
    user = session.query(models.User).filter_by(models.User.login == login).first()
    session.delete(user)
    session.commit()


def login_user(session, login=None, password=None, **kwargs):
    user = session.query(models.User).filter_by(models.User.login == login).first()
    if user:
        if user.password_hash == sha256(password):
            return True
        else:
            raise IncorrectPasswordException()
    else:
        raise UserNotFoundException(login)
