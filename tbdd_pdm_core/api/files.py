from ..db import models
import os
from .exceptions import *
import sqlalchemy.exc
__author__ = 'Aleksandr Vavilin'
STORAGE_PATH = 'files'


def _get_full_file_name(detail, detail_file):
    return os.path.join(STORAGE_PATH, detail.code.replace('/', '-'), detail_file.name)


def add_file_to_detail(session, detail_id=None, filename=None, filedata=None, **kwargs):
    detail = session.query(models.Detail).filter(models.Detail.id == detail_id).first()
    if detail is None:
        raise DetailNotFoundException(detail_id)
    detail_file = models.DetailFile(detail_id=detail_id, name=filename)
    try:
        full_file_name = _get_full_file_name(detail, detail_file)
        if os.path.exists(full_file_name):
            raise FileAlreadyExistsException('{0} {1}'.format(detail_id, filename))

        session.add(detail_file)
        os.makedirs(os.path.dirname(full_file_name), exist_ok=True)
        with open(full_file_name, 'wb') as f:
            f.write(filedata)
        session.commit()
    finally:
        session.rollback()


def get_file_data(session, file_id=None, **kwargs):
    try:
        detail_file, detail = session.query(models.DetailFile, models.Detail).join(models.Detail).filter(models.DetailFile.id == file_id).first()
        if detail_file is None:
            raise DetailFileNotFoundException()
        if detail is None:
            raise DetailNotFoundException()
        full_file_name = _get_full_file_name(detail, detail_file)
        with open(full_file_name, 'rb') as f:
            return f.read()
    finally:
        session.rollback()


def get_file_data_by_detail_and_name(session, detail_id=None, filename=None, **kwargs):
    try:
        detail_file = session.query(models.DetailFile).filter(models.DetailFile.detail_id == detail_id, models.DetailFile.name == filename).first()
        if detail_file is None:
            raise DetailFileNotFoundException('{} {}'.format(detail_id, filename))
        return get_file_data(session, file_id=detail_file.id)
    finally:
        session.rollback()


def delete_file_by_detail_and_name(session, detail_id=None, filename=None, **kwargs):
    try:
        detail_file, detail = session.query(models.DetailFile, models.Detail).join(models.Detail).filter(
            models.DetailFile.detail_id == detail_id, models.DetailFile.name == filename
        ).first()
        if detail_file is None:
            raise DetailFileNotFoundException(detail_id+' '+filename)
        full_file_name = _get_full_file_name(detail, detail_file)
        if os.path.exists(full_file_name):
            os.rename(full_file_name, full_file_name+'.deleted')
        try:
            session.delete(detail_file)
            session.commit()
        except:
            if os.path.exists(full_file_name):
                os.rename(full_file_name+'.deleted', full_file_name)
            raise
        if os.path.exists(full_file_name):
            os.unlink(full_file_name+'.deleted')
    finally:
        session.rollback()
