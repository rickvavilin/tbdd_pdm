__author__ = 'Aleksandr Vavilin'
import os
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tbdd_pdm_core.db import init_schema
from tbdd_pdm_core.api import details, exceptions
import pprint

@pytest.yield_fixture(scope='module')
def session():
    try:
        os.unlink('test_details.db')
    except:
        pass
    conn_string = 'sqlite+pysqlite:///test_details.db'
    init_schema.init_schema(conn_string)
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    _s = Session()
    yield _s
    _s.close()


def test_create_details(session):
    details.create_detail(session, code='D001', name='detail 1', description='detail 1 description')
    details.create_detail(session, code='D002', name='detail 2', description='detail 2 description')
    details.create_detail(session, code='D003', name='detail 3', description='detail 3 description')
    details.create_detail(session, code='D004', name='detail 4', description='detail 4 description')
    details.create_detail(session, code='D005', name='detail 5', description='detail 5 description')


def test_link_details(session):
    details.add_detail_to_assembly(session,
                                   details.get_id_by_code(session, 'D001'),
                                   details.get_id_by_code(session, 'D002'))
    details.add_detail_to_assembly(session,
                                   details.get_id_by_code(session, 'D001'),
                                   details.get_id_by_code(session, 'D003'))
    details.add_detail_to_assembly(session,
                                   details.get_id_by_code(session, 'D002'),
                                   details.get_id_by_code(session, 'D004'))


def test_cycle_link(session):
    with pytest.raises(exceptions.CycleLinkNotAllowedException):
        details.add_detail_to_assembly(session, details.get_id_by_code(session, 'D001'), details.get_id_by_code(session, 'D001'))


def test_get_tree(session):
    pprint.pprint(details.get_assembly_tree(session, details.get_id_by_code(session, 'D001')))