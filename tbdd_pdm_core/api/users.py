from hashlib import sha256

import sqlalchemy.exc
from sqlalchemy import or_

from . import permissions
from .exceptions import *
from ..db import models

__author__ = 'Aleksandr Vavilin'


def _get_password_hash(password):
    return sha256(password.encode('utf8')).hexdigest()


@permissions.check_permissions
def create_user(session, login=None, password=None, display_name=None, **kwargs):
    try:
        try:
            session.add(models.User(login=login,
                                    display_name=display_name,
                                    password_hash=_get_password_hash(password)))
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise UserAlreadyExistsException()
    finally:
        session.rollback()


@permissions.check_permissions
def update_user(session, login=None, display_name=None, **kwargs):
    try:
        user = session.query(models.User).filter(models.User.login == login).first()
        if user is None:
            raise UserNotFoundException(login)
        user.display_name = display_name
        session.commit()
    finally:
        session.rollback()


def _change_password_internal(session, login=None, password=None, **kwargs):
    try:
        user = session.query(models.User).filter(models.User.login == login).first()
        if user is None:
            raise UserNotFoundException(login)
        user.password_hash = _get_password_hash(password)
        session.commit()
    finally:
        session.rollback()


@permissions.check_permissions
def change_password(session, login=None, password=None, **kwargs):
    _change_password_internal(session, login=login, password=password, **kwargs)


def change_own_password(session, password=None, _current_user_login=None, **kwargs):
    if _current_user_login is None:
        _change_password_internal(session, login=_current_user_login, password=password, **kwargs)
    else:
        raise ActionNotPermitted()


@permissions.check_permissions
def delete_user(session, login=None, **kwargs):
    try:
        user = session.query(models.User).filter(models.User.login == login).first()
        if user is None:
            raise UserNotFoundException(login)
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
    user_info = user.get_dict_fields()
    user_permissions = []
    for gp in session.query(
                models.GroupPermissions
            ).join(
                models.UsersGroupsRel,
                models.UsersGroupsRel.group_id == models.GroupPermissions.group_id
            ).join(
                models.User
            ).filter(
                models.User.id == user.id,
                models.GroupPermissions.allowed == True
            ):
        if gp.function_name not in user_permissions:
            user_permissions.append(gp.function_name)
    user_info['user_permissions'] = user_permissions
    return user_info


def get_list(session, results_per_page=20, page=1, simple_filter=None, remove_password_hash=True, filter=None, **kwargs):
    result = {}
    try:
        q = session.query(models.User)
        if simple_filter is not None:
            simple_filter = '%'+simple_filter+'%'
            q = q.filter(or_(models.User.login.like(simple_filter),
                         models.User.display_name.like(simple_filter)))
        total_count = q.count()
        total_pages = int(total_count/results_per_page)+1
        result['total_count'] = total_count
        result['total_pages'] = total_pages
        result['data'] = []

        for user in q.offset(
            (page-1)*results_per_page
        ).limit(results_per_page):
            user_dict = user.get_dict_fields()
            if remove_password_hash:
                del user_dict['password_hash']
            result['data'].append(user_dict)
        return result
    finally:
        session.rollback()
