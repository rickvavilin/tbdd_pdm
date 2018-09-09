__author__ = 'Aleksandr Vavilin'
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, foreign, remote, query
from sqlalchemy.sql import func

Base = declarative_base()


class DictMixin(object):
    def get_dict_fields(self):
        result = {}
        for d in self.__dict__.keys():
            if not d.startswith('_'):
                attr = getattr(self, d)
                result[d] = attr
        return result


class User(Base, DictMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True, index=True)
    display_name = Column(String(255))
    password_hash = Column(String(255))


class Group(Base, DictMixin):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True)


class UsersGroupsRel(Base):
    __tablename__ = 'users_groups_rel'
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey(Group.id), primary_key=True, index=True)


class GroupPermissions(Base):
    __tablename__ = 'group_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey(Group.id), index=True)
    function_name = Column(String(255), index=True)
    allowed = Column(Boolean, index=True)
    UniqueConstraint('group_id', 'function_name')


class Detail(Base, DictMixin):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    is_standard = Column(Boolean)
    read_group_id = Column(Integer, ForeignKey(Group.id))
    write_group_id = Column(Integer, ForeignKey(Group.id))


class DetailLink(Base):
    __tablename__ = 'detail_links'
    parent_id = Column(Integer, ForeignKey(Detail.id), primary_key=True)
    child_id = Column(Integer, ForeignKey(Detail.id), primary_key=True)
    min_count = Column(Integer)
    max_count = Column(Integer)
    count = Column(Integer)


class DetailFile(Base, DictMixin):
    __tablename__ = 'detail_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    detail_id = Column(Integer, ForeignKey(Detail.id), index=True)
    UniqueConstraint('name', 'detail_id')
