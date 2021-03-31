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
from datetime import datetime, timedelta

import ckan.plugins as p
import ckan.logic as l
import ckan.plugins.toolkit as t
import ckan.model as model
import ckan.lib.base as base
from ckanext.eds.helpers import _get_action
import ckan.lib.navl.dictization_functions as df
from ckanext.eds.model.user_extra import UserExtra
from ckanext.eds.model.user_roles import UserRoles
from ckanext.eds.logic.schema import user_extra_delete_schema
from ckanext.eds.logic.schema import user_roles_delete_schema
from ckanext.eds.logic.dictization import table_dictize
import ckanext.eds.model as eds_model

_ = base._
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

def purge_revisions_eds(context, data_dict):

    l.check_access('purge_revisions_eds', context, data_dict)

    days = data_dict.get('days', 100)
    d = datetime.today() - timedelta(days=days)
    deleted_revisions = 0

    active_revisions = model.Session.query(
        model.Revision).filter_by(state=model.State.ACTIVE).\
        filter(model.Revision.timestamp < d)

    revs_to_purge = [rev.id for rev in active_revisions]
    revs_to_purge = list(set(revs_to_purge))

    for id in revs_to_purge:
        revision = model.Session.query(model.Revision).get(id)
        try:
            # TODO deleting the head revision corrupts the edit
            # page Ensure that whatever 'head' pointer is used
            # gets moved down to the next revision
            eds_model.repo_eds.purge_revision(revision, leave_record=False)
            deleted_revisions += 1

        except Exception, inst:
            msg = _('Problem purging revision %s: %s') % (id, inst)
            log.error(msg)
        log.info(_('Purge complete'))
    result = {
        'revisions_to delete': len(revs_to_purge),
        'deleted_revisions': deleted_revisions
    }
    return result
