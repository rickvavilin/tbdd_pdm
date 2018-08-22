__author__ = 'Aleksandr Vavilin'
from ..db import models
from .exceptions import *
from sqlalchemy.orm import joinedload
import sqlalchemy.exc


def create_detail(session, **kwargs):
    try:
        try:
            session.add(models.Detail(
                **kwargs
            ))
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise DetailAlreadyExistsException(kwargs['code'])
    finally:
        session.rollback()


def delete_detail(session, detail_id=None, **kwargs):
    try:
        detail = session.query(models.Detail).filter(models.Detail.id == detail_id).first()
        session.delete(detail)
        session.commit()
    finally:
        session.rollback()


def get_id_by_code(session, detail_code=None):
    try:
        detail = session.query(models.Detail).filter(models.Detail.code == detail_code).first()
        if detail is None:
            raise DetailNotFoundException(detail_code)
        return detail.id
    finally:
        session.rollback()


def add_detail_to_assembly(session, parent_id=None, child_id=None, min_count=0, max_count=0, **kwargs):
    try:
        if parent_id == child_id:
            raise CycleLinkNotAllowedException()
        detail_ref = models.DetailLink(
            parent_id=parent_id,
            child_id=child_id,
            min_count=min_count,
            max_count=max_count
        )
        session.add(detail_ref)
        session.commit()
    finally:
        session.rollback()


def get_assembly_tree(session, parent_id=None):
    result = []
    try:
        for child in session.query(
               models.Detail
        ).outerjoin(
                models.DetailLink,
                models.DetailLink.child_id == models.Detail.id
        ).filter(
                models.DetailLink.parent_id == parent_id
        ).all():
            tmp_id = child.id  # strange ugly hack
            child_dict = child.get_dict_fields()
            child_dict['children'] = get_assembly_tree(session, parent_id=child.id)
            result.append(child_dict)
        return result
    finally:
        session.rollback()

