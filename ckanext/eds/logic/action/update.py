"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
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
from ckanext.eds.logic.schema import user_extra_schema, user_roles_schema
from ckanext.eds.logic.dictization import table_dictize
from ckanext.eds.logic.action.create import user_roles_create

log = logging.getLogger(__name__)


def user_extra_update(context, data_dict):
    '''Update user extra parameter.

        :param key: Key of the parameter you want to update.
        :type key: string

        :param value: The new value of the parameter.
        :type value: string

        '''


    l.check_access('user_extra', context, data_dict)
    data, errors = df.validate(data_dict, user_extra_schema(),
                               context)

    if errors:
        raise t.ValidationError(errors)

    m = context.get('model')
    user_obj = m.User.get(context.get('user'))


    user_id = user_obj.id
    key = data.get('key')
    value = data.get('value')

    user_extra = UserExtra.get(user_id, key)
    if user_extra is None:
        raise l.NotFound

    user_extra.key = key
    user_extra.value = value
    user_extra.save()

    out = table_dictize(user_extra, context)

    return out

def user_roles_update(context, data_dict):
    '''Update user role parameter.

        :param user_id: Id of the user whose role you wish to update.
        :type user_id: string

        :param role: The role for the user.
        :type role: string

        '''
    return user_roles_create(context, data_dict)

