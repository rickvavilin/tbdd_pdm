from ..db import models
from .exceptions import *
import sqlalchemy.exc
__author__ = 'Aleksandr Vavilin'


def create_detail(session, code=None, name=None, description=None, is_standard=False, **kwargs):
    try:
        try:
            detail = models.Detail(
                code=code,
                name=name,
                description=description,
                is_standard=is_standard
            )
            session.add(detail)
            session.commit()
            return detail.get_dict_fields()
        except sqlalchemy.exc.IntegrityError:
            raise DetailAlreadyExistsException(kwargs['code'])
    finally:
        session.rollback()


def update_detail(session, id=None, name=None, description=None, is_standard=False, **kwargs):
    try:
        detail = session.query(models.Detail).filter(models.Detail.id == id).first()
        if detail is None:
            raise DetailNotFoundException(id)
        detail.name = name
        detail.description = description
        detail.is_standard = is_standard
        session.commit()
        return detail.get_dict_fields()
    finally:
        session.rollback()


def delete_detail(session, detail_id=None, **kwargs):
    try:
        detail = session.query(models.Detail).filter(models.Detail.id == detail_id).first()
        if detail is None:
            raise DetailNotFoundException(id)
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


def get_list(session, results_per_page=20, page=1, filter=None):
    result = {}
    try:
        total_count = session.query(models.Detail).count()
        total_pages = int(total_count/results_per_page)+1
        result['total_count'] = total_count
        result['total_pages'] = total_pages
        result['data'] = []
        for detail in session.query(
                models.Detail
        ).offset(
            (page-1)*results_per_page
        ).limit(results_per_page):
            result['data'].append(detail.get_dict_fields())
        return result
    finally:
        session.rollback()


def get_detail_by_id(session, detail_id=None):
    detail = session.query(models.Detail).filter(models.Detail.id == detail_id).first()
    if detail is None:
        raise DetailNotFoundException
    detail_dict = detail.get_dict_fields()
    detail_files = []
    for detail_file in session.query(models.DetailFile).filter(models.DetailFile.detail_id == detail.id).all():
        detail_files.append(detail_file.get_dict_fields())
    detail_dict['files'] = detail_files
    return detail_dict


