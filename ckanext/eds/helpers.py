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

import re
import logging

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

from ckan.plugins import toolkit
from ckan import model, logic
from ckan.common import c
from datetime import datetime, timedelta
from decimal import Decimal
import ckanext.eds.model.user_roles as _ur

log = logging.getLogger(__name__)


def show_update_indicator(id_or_name):
    pkg = model.Package.get(id_or_name)
    if pkg is None:
        return False

    field = None
    if 'update_frequency' in pkg.extras:
        field = pkg.extras['update_frequency']

    if field is None:
        return False

    diff = datetime.utcnow() - pkg.metadata_modified
    diff_in_hours = Decimal(diff.total_seconds() / 3600)

    cond = 0
    if any(re.findall(r'\d+\.?\d*', field)):
        cond = Decimal(re.findall(r'\d+\.?\d*', field)[0])

    if field.lower().startswith('pt'):
        if field.lower().endswith('h'):
            pass
        elif field.lower().endswith('m'):
            cond = cond / 60
        elif field.lower().endswith('s'):
            cond = cond / 3600
    else:
        if field.lower().endswith('d'):
            cond = cond * 24
        elif field.lower().endswith('w'):
            cond = cond * 168
        elif field.lower().endswith('m'):
            cond = cond * 730
        elif field.lower().endswith('y'):
            cond = cond * 8760

    if diff_in_hours <= cond:
        return True

    return False


def config_option_show(key, lang):
    _ = '{0}_{1}'.format(key, lang)
    res = ''
    try:
        res = toolkit.get_action('config_option_show')(dict(ignore_auth=True), {'key': _})
    except Exception as e:
        log.error(e)

    return res


def _get_context():
    return {
        'model': model,
        'session': model.Session,
        'user': c.user or c.author,
        'auth_user_obj': c.userobj
    }


def _get_action(action, data_dict):
    return toolkit.get_action(action)(_get_context(), data_dict)


def get_chart_resources(resource_view_id):
    if not resource_view_id:
        return None

    data_dict = {
        'id': resource_view_id
    }

    try:
        resource_view = _get_action('resource_view_show', data_dict)
    except logic.NotFound:
        return None

    data_dict = {
        'id': resource_view['resource_id']
    }

    try:
        resource = _get_action('resource_show', data_dict)
    except logic.NotFound:
        return None

    data_dict = {
        'id': resource['package_id']
    }

    try:
        package = _get_action('package_show', data_dict)
    except logic.NotFound:
        return None

    return [resource_view, resource, package]


def get_events(limit=5):
    events = _get_action('event_list', {'limit': limit, 'future_events': True})['events']

    return events


def get_news(limit=5):
    news = _get_action('news_list', {'limit': limit, 'active_news': True})['news']
    return news


def _get_logic_functions(module_root, logic_functions={}):
    '''Helper function that scans extension logic dir for all logic functions.'''
    for module_name in ['create', 'delete', 'get', 'patch', 'update']:
        module_path = '%s.%s' % (module_root, module_name,)

        module = __import__(module_path)

        for part in module_path.split('.')[1:]:
            module = getattr(module, part)

        for key, value in module.__dict__.items():
            if not key.startswith('_') and (hasattr(value, '__call__')
                                            and (value.__module__ == module_path)):
                logic_functions[key] = value

    return logic_functions


def get_quick_facts_views():
    schema = logic.schema.update_configuration_schema()
    quick_facts_keys = []
    quick_facts = []

    for key in schema:
        if key.startswith('ckanext.eds.chart_') and not \
                key.startswith('_subheader', len(key) - 10, len(key)):
            quick_facts_keys.append(key)

    for key in quick_facts_keys:
        if config.get(key):
            quick_facts.append(config.get(key))

    return quick_facts[:get_nubmer_of_charts()]


def get_nubmer_of_charts():
    return int(config.get('ckanext.eds.quick_facts_number', 3))

def user_is_editor(context):
    '''
        Checks if the user defined in the context is an editor 
        rtype: boolean
    '''
    roleObj =_ur.UserRoles.get(context['auth_user_obj'].id)
    if roleObj:
        if _ur.UserRoles.get(context['auth_user_obj'].id).role == "editor":
            return True
    return False



def user_is_registered(context):
    '''
        Checks if the user is registered user
    '''
    model = context['model']
    user = context['user']
    user_obj = model.User.get(user)
    if not user_obj:
        return False

    return True

def get_user_locale():
    context = _get_context()
    if user_is_registered(context):
        default_language = _get_action('user_extra_get', {'key':'language'})
        if default_language:
            return default_language.get('value')
        else:
            return None
    else:
        return None




