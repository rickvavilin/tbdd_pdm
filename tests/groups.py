__author__ = 'Aleksandr Vavilin'
import os
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from tbdd_pdm_core.db import init_schema
from tbdd_pdm_core.api import users, groups, exceptions


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.yield_fixture(scope='module')
def session():
    try:
        os.unlink('test_groups.db')
    except:
        pass
    conn_string = 'sqlite+pysqlite:///test_groups.db'
    init_schema.init_schema(conn_string)
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    _s = Session()
    yield _s
    _s.close()


def test_create_users(session):
    users.create_user(session, 'admin', 'password')
    users.create_user(session, 'user', '1')


def test_create_group(session):
    groups.create_group(session, 'tbdd')


def test_create_double_group(session):
    with pytest.raises(exceptions.GroupAlreadyExistsException):
        groups.create_group(session, 'tbdd')


def test_add_user_to_group(session):
    groups.add_user_to_group(session, 'tbdd', 'admin')


def test_get_users_of_group(session):
    assert len(groups.get_users_of_group(session, 'tbdd')) == 1


def test_get_groups_of_user(session):
    assert len(groups.get_groups_of_user(session, 'admin')) == 1


def test_get_groups_of_user_empty(session):
    assert len(groups.get_groups_of_user(session, 'user')) == 0


def test_remove_user_from_group(session):
    groups.remove_user_from_group(session, 'tbdd', 'admin')


def test_add_user_to_group_1(session):
    groups.add_user_to_group(session, 'tbdd', 'admin')


def test_delete_group(session):
    with pytest.raises(exceptions.GroupNotEmptyException):
        groups.delete_group(session, 'tbdd')