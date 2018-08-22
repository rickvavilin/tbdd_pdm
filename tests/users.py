__author__ = 'Aleksandr Vavilin'
import os
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tbdd_pdm_core.db import init_schema
from tbdd_pdm_core.api import users, exceptions


@pytest.yield_fixture(scope='module')
def session():
    try:
        os.unlink('test.db')
    except:
        pass
    conn_string = 'sqlite+pysqlite:///test.db'
    init_schema.init_schema(conn_string)
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    _s = Session()
    yield _s
    _s.close()


def test_create_user(session):
    users.create_user(session, 'admin', 'password')


def test_double_user(session):
    with pytest.raises(exceptions.UserAlreadyExistsException):
        users.create_user(session, 'admin', 'password')


def test_login_user(session):
    assert users.login_user(session, 'admin', 'password')


def test_login_unknown_user(session):
    with pytest.raises(exceptions.UserNotFoundException):
        users.login_user(session, 'superadmin', 'password')


def test_login_incorrect_password(session):
    with pytest.raises(exceptions.IncorrectPasswordException):
        users.login_user(session, 'admin', 'superpassword')