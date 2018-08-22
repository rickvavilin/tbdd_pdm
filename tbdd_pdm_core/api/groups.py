__author__ = 'Aleksandr Vavilin'
from ..db import models
from .exceptions import *
import sqlalchemy.exc


def create_group(session, name=None, **kwargs):
    try:
        group = models.Group(name=name)
        try:
            session.add(group)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise GroupAlreadyExistsException()
    finally:
        session.rollback()


def delete_group(session, name=None, **kwargs):
    try:
        try:
            group = session.query(models.Group).filter(models.Group.name == name).first()
            if group is None:
                raise GroupNotFoundException(group)
            session.delete(group)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise GroupNotEmptyException(name)
    finally:
        session.rollback()


def add_user_to_group(session, group_name=None, user_login=None, **kwargs):
    try:
        group = session.query(models.Group).filter(models.Group.name == group_name).first()
        user = session.query(models.User).filter(models.User.login == user_login).first()
        if group is None:
            raise GroupNotFoundException(group)
        if user is None:
            raise UserNotFoundException(user)
        user_group_rel = models.UsersGroupsRel(user_id=user.id, group_id=group.id)
        session.add(user_group_rel)
        session.commit()
    finally:
        session.rollback()


def remove_user_from_group(session, group_name=None, user_login=None, **kwargs):
    try:
        group = session.query(models.Group).filter(models.Group.name == group_name).first()
        user = session.query(models.User).filter(models.User.login == user_login).first()
        if group is None:
            raise GroupNotFoundException(group)
        if user is None:
            raise UserNotFoundException(user)
        user_group_rel = session.query(models.UsersGroupsRel).filter(models.UsersGroupsRel.user_id == user.id, models.UsersGroupsRel.group_id == group.id).first()
        if user_group_rel:
            session.delete(user_group_rel)
            session.commit()
    finally:
        session.rollback()


def get_users_of_group(session, group_name=None, **kwargs):
    try:
        group = session.query(models.Group).filter(models.Group.name == group_name).first()
        if group is None:
            raise GroupNotFoundException(group)
        result = []
        for user in session.query(models.User).join(
                models.UsersGroupsRel).filter(models.UsersGroupsRel.group_id == group.id):
            result.append(user.get_dict_fields())
        return result
    finally:
        session.rollback()


def get_groups_of_user(session, user_login=None, **kwargs):
    try:
        user = session.query(models.User).filter(models.User.login == user_login).first()
        if user is None:
            raise UserNotFoundException(user)
        result = []
        for group in session.query(models.Group).join(
                models.UsersGroupsRel).filter(models.UsersGroupsRel.user_id == user.id):
            result.append(group.get_dict_fields())
        return result

    finally:
        session.rollback()