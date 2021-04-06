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

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

import ckan.logic as logic
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.mailer as mailer
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as df

from ckan.controllers.user import UserController
from ckan.common import _, c, request
from ckan.lib.base import render_jinja2
from ckan.lib.mailer import get_reset_link, create_reset_key, mail_user
from ckanext.eds.helpers import config_option_show

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

DataError = df.DataError

log = logging.getLogger(__name__)

CTRL = 'ckanext.eds.controllers.user:EDSUserController'


def _get_reset_link_body(user):
    extra_vars = {
        'reset_link': get_reset_link(user),
        'site_title_dk': config_option_show('ckan.site_title', 'da_DK'),
        'site_title_en': config_option_show('ckan.site_title', 'en'),
        'site_url': config.get('ckan.site_url'),
        'user_name': user.name,
    }
    return render_jinja2('emails/reset_password.txt', extra_vars)


def _send_reset_link(user):
    create_reset_key(user)
    body = _get_reset_link_body(user)
    extra_vars = {
        'site_title_dk': config_option_show('ckan.site_title', 'da_DK'),
        'site_title_en': config_option_show('ckan.site_title', 'en')
    }
    subject = render_jinja2('emails/reset_password_subject.txt', extra_vars)
    subject = subject.split('\n')[0]
    mail_user(user, subject, body)


class EDSUserController(UserController):
    def request_reset(self):
        context = {'model': model, 'session': model.Session, 'user': c.user,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': request.params.get('user')}
        try:
            check_access('request_reset', context)
        except NotAuthorized:
            abort(403, _('Unauthorized to request reset password.'))

        if request.method == 'POST':
            id = request.params.get('user')

            context = {'model': model,
                       'user': c.user}

            data_dict = {'id': id}
            user_obj = None
            try:
                user_dict = get_action('user_show')(context, data_dict)
                user_obj = context['user_obj']
            except NotFound:
                # Try searching the user
                del data_dict['id']
                data_dict['q'] = id

                if id and len(id) > 2:
                    user_list = get_action('user_list')(context, data_dict)
                    if len(user_list) == 1:
                        # This is ugly, but we need the user object for the
                        # mailer,
                        # and user_list does not return them
                        del data_dict['q']
                        data_dict['id'] = user_list[0]['id']
                        user_dict = get_action('user_show')(context, data_dict)
                        user_obj = context['user_obj']
                    elif len(user_list) > 1:
                        h.flash_error(_('"%s" matched several users') % (id))
                    else:
                        h.flash_error(_('No such user: %s') % id)
                else:
                    h.flash_error(_('No such user: %s') % id)

            if user_obj:
                try:
                    _send_reset_link(user_obj)
                    h.flash_success(_('Please check your inbox for '
                                      'a reset code.'))
                    h.redirect_to('/')
                except mailer.MailerException, e:
                    h.flash_error(_('Could not send reset link: %s') %
                                  unicode(e))
        return render('user/request_reset.html')

