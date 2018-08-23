__author__ = 'Aleksandr Vavilin'
import os
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tbdd_pdm_core.db import init_schema
from tbdd_pdm_core.api import details, files, exceptions
import pprint


@pytest.yield_fixture(scope='module')
def session():
    try:
        os.unlink('test_files.db')
    except:
        pass
    conn_string = 'sqlite+pysqlite:///test_files.db'
    init_schema.init_schema(conn_string)
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    _s = Session()
    yield _s
    _s.close()


def test_create_details(session):
    details.create_detail(session, code='D001', name='detail 1', description='detail 1 description')
    details.create_detail(session, code='D002', name='detail 2', description='detail 2 description')


def test_add_file(session):
    with open('test_data/test.txt', 'rb') as f:
        detail_id = details.get_id_by_code(session, 'D001')
        files.add_file_to_detail(session, detail_id=detail_id, filename='test.txt', filedata=f.read())


def test_get_file(session):
    with open('test_data/test_out.txt', 'wb') as f:
        f.write(files.get_file_data_by_detail_and_name(session,
                                                       detail_id=details.get_id_by_code(session, 'D001'),
                                                       filename='test.txt'))


