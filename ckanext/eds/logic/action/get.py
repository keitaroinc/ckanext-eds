import logging

import ckan.plugins as p
import ckan.logic as l
import ckan.plugins.toolkit as t
from ckanext.eds.helpers import _get_action
import ckan.lib.navl.dictization_functions as df
from ckanext.eds.model.user_extra import UserExtra
from ckanext.eds.model.user_roles import UserRoles
from ckanext.eds.logic.schema import user_extra_delete_schema
from ckanext.eds.logic.schema import user_roles_delete_schema
from ckanext.eds.logic.dictization import table_dictize

log = logging.getLogger(__name__)


@p.toolkit.side_effect_free
def eds_show_datasets(context, data_dict):
    payload = {}
    # include_private parameter is used only in newer versions of CKAN (2.6+)
    if not p.toolkit.check_ckan_version(min_version='2.5.0', max_version='2.5.10'):
        payload = {'include_private': True}

    data = _get_action('package_search', payload)
    payload['rows'] = data['count']
    data = _get_action('package_search', payload)
    return data.pop('results', [])


@p.toolkit.side_effect_free
def eds_dataset_show_resources(context, data_dict):
    data = _get_action('package_show', data_dict)

    return data.pop('resources', [])


@p.toolkit.side_effect_free
def eds_resource_show_resource_views(context, data_dict):
    data = _get_action('resource_view_list', data_dict)
    data = filter(lambda i: i['view_type'] == data_dict['view_type'], data)

    return data


def user_extra_get(context, data_dict):
    '''Get user extra parameter.

            :param key: Key of the parameter.
            :type key: string

            '''

    l.check_access('user_extra', context, data_dict)
    data, errors = df.validate(data_dict, user_extra_delete_schema(),
                               context)

    if errors:
        raise t.ValidationError(errors)

    m = context.get('model')
    user_obj = m.User.get(context.get('user'))

    user_id = user_obj.id
    key = data.get('key')

    user_extra = UserExtra.get(user_id, key)
    if user_extra is None:
        return user_extra

    out = table_dictize(user_extra, context)

    return out

def user_roles_get(context, data_dict):
    '''Get user roles parameter.

            :param user_id: id of the user you want to get roles for.
            :type user_id: string

            '''
    l.check_access('user_roles', context, data_dict)
    data, errors = df.validate(data_dict, user_roles_delete_schema(),
                               context)

    if errors:
        raise t.ValidationError(errors)

    m = context.get('model')
    user_obj = m.User.get(data.get('user_id'))

    if user_obj is None:
        raise l.NotFound("No such user")

    user_id = user_obj.id
    user_role = UserRoles.get(user_id)
    if user_role is None:
        return user_role

    if not user_role:
        raise l.NotFound("User has no roles")

    out = table_dictize(user_role, context)

    return out
