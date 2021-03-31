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

from ckan.plugins import toolkit as t
import ckanext.eds.helpers as _h

log = logging.getLogger(__name__)


def user_extra(context, data_dict):
    '''
        Authorization check for user extra
    '''
    success = _h.user_is_registered(context)
    out = {
        'success': success,
        'msg': '' if success else
        t._('You must be a registered user to use this action')
    }
    return out

def user_roles(context, data_dict):
    '''
        Authorization check for user roles
    '''
    m = context.get('model')
    user_obj = m.User.get(context.get('user'))
    success = user_obj.sysadmin
    out = {
        'success': success,
        'msg': '' if success else
        t._('You must be a system administrator to use this action')
    }
    return out

def activity_create(context, data_dict):
    #sysadmins and editors only
    success = _h.user_is_editor(context)
    if success:
        return { 'success': True }
    return {'success': False}

def purge_revisions_eds(context, data_dict):
    '''
        Authorization check for deleting revisions
    '''
    # sysadmins only
    return {'success': False}

