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

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

import ckan.model as model
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic

check_access = logic.check_access
NotAuthorized = logic.NotAuthorized
request = base.request
abort = base.abort
c = base.c
_ = base._

log = logging.getLogger(__name__)

def _get_context():
    context = {'model': model,
               'session': model.Session,
               'user': c.user,
               'auth_user_obj': c.userobj}

    return context


class EdsGuidesController(base.BaseController):

    ctrl = 'ckanext.eds.controllers.eds_guides_controller:EdsGuidesController'

    def api_guides(self):

        data = {}
        for l in ['en', 'da_DK']:
            key = 'api_guides_content_{0}'.format(l)
            data[key] = config.get(key)

        vars = {'data': data, 'errors': {}}
        return base.render('guides/api_guides.html',
                           extra_vars=vars)

    def api_guides_edit(self):

        context = _get_context()
        try:
            check_access('sysadmin', context)
        except NotAuthorized:
            abort(403, _('Not authorized to see this page'))

        data = request.POST
        if 'save' in data:
            try:
                data_dict = dict(request.POST)

                del data_dict['save']
                log.debug(data_dict)

                data = logic.get_action('config_option_update')(
                    {'user': c.user}, data_dict)

            except logic.ValidationError, e:
                log.debug(e)
                errors = e.error_dict
                error_summary = e.error_summary
                vars = {'data': data, 'errors': errors,
                        'error_summary': error_summary}
                return base.render('guides/api_guides_form.html', extra_vars=vars)

            h.redirect_to(controller=self.ctrl, action='api_guides')

        data = {}
        for l in ['en', 'da_DK']:
            key = 'api_guides_content_{0}'.format(l)
            data[key] = config.get(key)

        vars = {'data': data, 'errors': {}}

        return base.render('guides/api_guides_form.html',
                           extra_vars=vars)

    def simple_guides(self):

        data = {}
        for l in ['en', 'da_DK']:
            key = 'simple_guides_content_{0}'.format(l)
            data[key] = config.get(key)

        vars = {'data': data, 'errors': {}}
        return base.render('guides/simple_guides.html',
                           extra_vars=vars)

    def simple_guides_edit(self):

        context = _get_context()
        try:
            check_access('sysadmin', context)
        except NotAuthorized:
            abort(403, _('Not authorized to see this page'))

        data = request.POST
        if 'save' in data:
            try:
                data_dict = dict(request.POST)

                del data_dict['save']
                log.debug(data_dict)

                data = logic.get_action('config_option_update')(
                    {'user': c.user}, data_dict)

            except logic.ValidationError, e:
                log.debug(e)
                errors = e.error_dict
                error_summary = e.error_summary
                vars = {'data': data, 'errors': errors,
                        'error_summary': error_summary}
                return base.render('guides/simple_guides_form.html', extra_vars=vars)

            h.redirect_to(controller=self.ctrl, action='simple_guides')

        data = {}
        for l in ['en', 'da_DK']:
            key = 'simple_guides_content_{0}'.format(l)
            data[key] = config.get(key)

        vars = {'data': data, 'errors': {}}

        return base.render('guides/simple_guides_form.html',
                           extra_vars=vars)
