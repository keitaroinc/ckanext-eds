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
from ckanext.eds.logic.schema import user_extra_schema, user_roles_schema
from ckanext.eds.logic.dictization import table_dictize

log = logging.getLogger(__name__)


def user_extra_create(context, data_dict):
    '''Create user extra parameter.

        :param key: Key of the parameter.
        :type key: string

        :param value: Value of the parameter.
        :type value: string

        :param active: State of the parameter. Default is active.
        :type active: string

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
    state = data.get('state', 'active')

    user_extra = UserExtra.get(user_id, key)
    if user_extra:
        user_extra.key = key
        user_extra.value = value
        user_extra.save()
    else:
        user_extra = UserExtra(
            user_id=user_id,
            key=key,
            value=value,
            state=state
        )
        user_extra.save()

    out = table_dictize(user_extra, context)

    return out

def user_roles_create(context, data_dict):
    l.check_access('user_roles', context, data_dict)
    data, errors = df.validate(data_dict, user_roles_schema(),
                                context)

    if errors:
        raise t.ValidationError(errors)

    m = context.get('model')
    user_obj = m.User.get(data.get('user_id'))

    if user_obj is None:
        raise l.NotFound("No such user")

    user_id = user_obj.id
    role = data.get('role')

    user_roles = UserRoles.get(user_id)
    if user_roles:
        user_roles.role = role
        user_roles.save()
    else:
        user_roles = UserRoles(
            user_id=user_id,
            role=role
        )
        user_roles.save()

    out = table_dictize(user_roles, context)

    return out
