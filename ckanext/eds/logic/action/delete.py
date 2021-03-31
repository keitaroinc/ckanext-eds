"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging

import ckan.plugins as p
import ckan.logic as l
import ckan.plugins.toolkit as t
import ckan.lib.navl.dictization_functions as df
from ckanext.eds.model.user_extra import UserExtra
from ckanext.eds.model.user_roles import UserRoles
from ckanext.eds.logic.schema import user_extra_delete_schema, user_roles_delete_schema

log = logging.getLogger(__name__)


def user_extra_delete(context, data_dict):
    '''Delete user extra parameter.

        :param key: Key of the parameter you want to delete.
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
    UserExtra.delete(user_id, key)

    return {
        'message': 'Extra with key: %s, deleted' % key
    }

def user_roles_delete(context, data_dict):
    '''Delete user roles parameter.

        :param user_id: id of the user you want to remove roles for.
        :type user_id: string

        '''
    l.check_access('user_roles', context, data_dict)
    data, errors = df.validate(data_dict, user_roles_delete_schema(),
                                context)

    if error:
        raise t.ValidationError(errors)

    m = context.get('model')
    user_obj = m.User.get(data.get('user_id'))

    if user_obj is None:
        l.NotFound("No such user")

    user_id = user_obj.id
    UserExtra.delete(user_id)

    return {
        'message': 'User\'s (id=%s) role deleted' % user_id
    }
