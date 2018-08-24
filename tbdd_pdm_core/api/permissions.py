__author__ = 'Aleksandr Vavilin'
from ..db import models
from . import exceptions

default_user_permissions = [
    'tbdd_pdm_core.api.details.get_list',
    'tbdd_pdm_core.api.details.get_detail_by_id',
    'tbdd_pdm_core.api.details.get_assembly_tree',
    'tbdd_pdm_core.api.files.get_file_data'
]

default_admin_permissions = [
    'tbdd_pdm_core.api.details.create_detail',
    'tbdd_pdm_core.api.details.update_detail',
    'tbdd_pdm_core.api.details.delete_detail',
    'tbdd_pdm_core.api.details.add_detail_to_assembly',
    'tbdd_pdm_core.api.files.add_file_to_detail',
    'tbdd_pdm_core.api.files.delete_file_by_detail_and_name',
    'tbdd_pdm_core.api.users.create_user',
    'tbdd_pdm_core.api.users.delete_user',
    'tbdd_pdm_core.api.groups.create_group',
    'tbdd_pdm_core.api.groups.delete_group',
    'tbdd_pdm_core.api.groups.add_user_to_group',
    'tbdd_pdm_core.api.groups.remove_user_from_group',
    'tbdd_pdm_core.api.groups.add_permission_to_group'
]


def check_function_allowed(session, login, func_name):
    from . import groups
    user_groups = groups.get_groups_of_user(session, user_login=login)
    user_groups_ids = [user_group['id'] for user_group in user_groups]
    if session.query(models.GroupPermissions).filter(
        models.GroupPermissions.group_id.in_(user_groups_ids),
        models.GroupPermissions.function_name == func_name,
        models.GroupPermissions.allowed == True
    ).first() is None and func_name not in default_user_permissions:
        raise exceptions.ActionNotPermitted('{} {}'.format(login, func_name))


def check_permissions(func):
    def _check_wrapper(session, *args, **kwargs):
        if '_current_user_login' in kwargs:
            func_name = func.__module__+'.'+func.__name__
            check_function_allowed(session, kwargs['_current_user_login'], func_name)
            del kwargs['_current_user_login']
        return func(session, *args, **kwargs)
    return _check_wrapper
