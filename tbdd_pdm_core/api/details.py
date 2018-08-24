from ..db import models
from .exceptions import *
from . import permissions
import sqlalchemy.exc
from sqlalchemy import or_
__author__ = 'Aleksandr Vavilin'


@permissions.check_permissions
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
            session.flush()
            session.commit()
            tmp_id = detail.id
            return detail.get_dict_fields()
        except sqlalchemy.exc.IntegrityError:
            raise DetailAlreadyExistsException(kwargs['code'])
    finally:
        session.rollback()


@permissions.check_permissions
def update_detail(session, id=None, name=None, description=None, is_standard=False, **kwargs):
    try:
        detail = session.query(models.Detail).filter(models.Detail.id == id).first()
        if detail is None:
            raise DetailNotFoundException(id)
        detail.name = name
        detail.description = description
        detail.is_standard = is_standard
        session.flush()
        session.commit()
        tmp_id = detail.id
        return get_detail_by_id(session, detail_id=detail.id)
    finally:
        session.rollback()


@permissions.check_permissions
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


@permissions.check_permissions
def add_detail_to_assembly(session, parent_id=None, child_id=None, min_count=0, max_count=0, count=1, **kwargs):
    try:
        if parent_id == child_id:
            raise CycleLinkNotAllowedException()

        detail_ref = session.query(models.DetailLink).filter(models.DetailLink.parent_id == parent_id,
                                                             models.DetailLink.child_id == child_id).first()

        if detail_ref is not None:
            detail_ref.count += count
            session.commit()
            return
        detail_ref = models.DetailLink(
            parent_id=parent_id,
            child_id=child_id,
            min_count=min_count,
            max_count=max_count,
            count=count
        )
        session.add(detail_ref)
        session.commit()
    finally:
        session.rollback()


@permissions.check_permissions
def remove_detail_from_assembly(session, parent_id=None, child_id=None, min_count=0, max_count=0, **kwargs):
    try:
        detail_ref = session.query(models.DetailLink).filter(
            models.DetailLink.child_id == child_id,
            models.DetailLink.parent_id == parent_id
        ).first()
        if detail_ref is None:
            raise DetailNotFoundException()
        if detail_ref.count > 1:
            detail_ref.count -= 1
        else:
            session.delete(detail_ref)
        session.commit()
    finally:
        session.rollback()


def _get_assembly_tree_internal(session, parent_id=None, level=0, count_multiplier=1, use_count_multiplier=False):
    result = []
    try:
        for child, link in session.query(
                models.Detail,
                models.DetailLink
        ).outerjoin(
                models.DetailLink,
                models.DetailLink.child_id == models.Detail.id
        ).filter(
                models.DetailLink.parent_id == parent_id
        ).all():
            tmp_id = child.id  # strange ugly hack
            child_dict = child.get_dict_fields()
            child_dict['level'] = level+1
            if use_count_multiplier:
                count_mul = link.count
            else:
                count_mul = 1
            child_dict['children'] = _get_assembly_tree_internal(session,
                                                                 parent_id=child.id,
                                                                 level=level+1,
                                                                 count_multiplier=count_mul,
                                                                 use_count_multiplier=use_count_multiplier)
            child_dict['count'] = link.count*count_multiplier
            result.append(child_dict)
        return result
    finally:
        session.rollback()


@permissions.check_permissions
def get_assembly_tree(session, parent_id=None, use_count_multiplier=False):
    detail_dict = get_detail_by_id(session, parent_id)
    detail_dict['level'] = 0
    detail_dict['count'] = 1
    detail_dict['children'] = _get_assembly_tree_internal(session,
                                                          parent_id=parent_id,
                                                          use_count_multiplier=use_count_multiplier)
    return detail_dict


def _calculate_bom(item, bom=None):
    if item['id'] in bom:
        bom[item['id']]['count'] = bom[item['id']]['count'] + item['count']
    else:
        bom[item['id']] = {
            "item": item,
            "count": item['count']
        }
    for child in item['children']:
        _calculate_bom(child, bom)


def calculate_bom(session, parent_id=None):
    tree = get_assembly_tree(session, parent_id, use_count_multiplier=True)
    bom = {}
    _calculate_bom(tree, bom)
    return bom


@permissions.check_permissions
def get_list(session, results_per_page=20, page=1, simple_filter=None, filter=None):
    result = {}
    try:
        q = session.query(models.Detail)
        if simple_filter is not None:
            simple_filter = '%'+simple_filter+'%'
            q = q.filter(or_(models.Detail.code.like(simple_filter),
                         models.Detail.name.like(simple_filter),
                         models.Detail.description.like(simple_filter)))
        total_count = q.count()
        total_pages = int(total_count/results_per_page)+1
        result['total_count'] = total_count
        result['total_pages'] = total_pages
        result['data'] = []

        for detail in q.offset(
            (page-1)*results_per_page
        ).limit(results_per_page):
            result['data'].append(detail.get_dict_fields())
        return result
    finally:
        session.rollback()


@permissions.check_permissions
def get_assembly_list(session, results_per_page=20, page=1, simple_filter=None, filter=None):
    result = {}
    try:
        q = session.query(models.Detail).join(
            models.DetailLink,
            models.DetailLink.parent_id == models.Detail.id).distinct()
        if simple_filter is not None:
            simple_filter = '%'+simple_filter+'%'
            q = q.filter(or_(models.Detail.code.like(simple_filter),
                         models.Detail.name.like(simple_filter),
                         models.Detail.description.like(simple_filter)))
        total_count = q.count()
        total_pages = int(total_count/results_per_page)+1
        result['total_count'] = total_count
        result['total_pages'] = total_pages
        result['data'] = []

        for detail in q.offset((page-1)*results_per_page).limit(results_per_page):
            result['data'].append(detail.get_dict_fields())
        return result
    finally:
        session.rollback()


@permissions.check_permissions
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


