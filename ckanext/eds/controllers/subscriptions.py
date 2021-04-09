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

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

import logging
import ckan.logic as logic
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.helpers as h

from ckan.controllers.user import UserController
from ckan.common import _, c, request
from paste.deploy.converters import asbool

render = base.render
abort = base.abort

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params

log = logging.getLogger(__name__)

CTRL = 'ckanext.eds.controllers.subscriptions:SubscriptionController'

SUBSCRIPTION_TYPES = ('dataset', 'group', 'user')


class SubscriptionController(UserController):
    def _get_ctx(self):
        return {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}

    def subscription_delete(self, type, id):
        context = self._get_ctx()
        action = logic.get_action('unfollow_{0}'.format(type))
        action(context, {'id': id})

        h.flash_success(_('Successfully unsubscribed from the selected {0}!'.format(type)))
        base.redirect(h.url_for(controller=CTRL, action='subscription_manage', type=type))

    def subscription_manage(self, type):
        vars = {'data': {}, 'errors': {}, 'error_summary': {}}
        data_dict = {'id': c.userobj.id}
        context = self._get_ctx()

        super(SubscriptionController, self)._setup_template_variables(
            {'model': model,
             'session': model.Session,
             'user': c.user}, data_dict
        )

        c.is_myself = True
        c.show_email_notifications = asbool(
            config.get('ckan.activity_streams_email_notifications'))

        if type not in SUBSCRIPTION_TYPES:
            h.flash_error(_('Subscription type: {0} is not supported!'.format(type)))
            base.redirect(h.url_for(controller=CTRL, action='subscription_manage', type='dataset'))

        if request.POST:
            sub_type = request.POST['subscription_type']
            for _type in SUBSCRIPTION_TYPES:
                if _type != sub_type:
                    continue

                action = logic.get_action('unfollow_{0}'.format(_type))
                objects = request.POST.getall(_type)
                map(lambda o: action(context, {'id': o}), objects)

                h.flash_success(_('Successfully unsubscribed from the selected {0}(s)!'.format(_type)))
                base.redirect(h.url_for(controller=CTRL, action='subscription_manage', type=_type))

        c.subscription_type = type
        c.user_list = logic.get_action('user_followee_list')(context, data_dict)
        c.group_list = logic.get_action('group_followee_list')(context, data_dict)
        c.dataset_list = logic.get_action('dataset_followee_list')(context, data_dict)
        c.form = render(super(SubscriptionController, self).edit_user_form, extra_vars=vars)

        return render('user/edit.html')

