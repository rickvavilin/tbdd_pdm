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
    login = Column(String, unique=True)
    password_hash = Column(String)


class Group(Base, DictMixin):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class UsersGroupsRel(Base):
    __tablename__ = 'users_groups_rel'
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    group_id = Column(Integer, ForeignKey(Group.id), primary_key=True)


class Detail(Base, DictMixin):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    is_standard = Column(Boolean)
    read_group_id = Column(Integer, ForeignKey(Group.id))
    write_group_id = Column(Integer, ForeignKey(Group.id))


class DetailLink(Base):
    __tablename__ = 'detail_links'
    parent_id = Column(Integer, ForeignKey(Detail.id), primary_key=True)
    child_id = Column(Integer, ForeignKey(Detail.id), primary_key=True)
    min_count = Column(Integer)
    max_count = Column(Integer)


class DetailFile(Base, DictMixin):
    __tablename__ = 'detail_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    detail_id = Column(Integer, ForeignKey(Detail.id))
    UniqueConstraint('name', 'detail_id')
