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

from ckan.controllers.admin import AdminController
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic

c = base.c
request = base.request
_ = base._

log = logging.getLogger(__name__)

class EdsController(AdminController):
    ctrl = 'ckanext.eds.controllers.eds_controller:EdsController'

    def quick_facts(self):

        data = request.POST
        if 'save' in data:
            try:
                data_dict = dict(request.POST)

                del data_dict['save']
                log.debug(data_dict)

                for n in range(1, 5):
                    if not data_dict.get('ckanext.eds.chart_' + str(n)):
                        data_dict['ckanext.eds.chart_' + str(n)] = ''

                data = logic.get_action('config_option_update')(
                    {'user': c.user}, data_dict)

            except logic.ValidationError, e:
                log.debug(e)
                errors = e.error_dict
                error_summary = e.error_summary
                vars = {'data': data, 'errors': errors,
                        'error_summary': error_summary}
                return base.render('admin/quick_facts.html', extra_vars=vars)

            h.redirect_to(controller=self.ctrl, action='quick_facts')

        schema = logic.schema.update_configuration_schema()
        data = {}
        for key in schema:
            data[key] = config.get(key)

        vars = {'data': data, 'errors': {}}
        return base.render('admin/quick_facts.html',
                           extra_vars=vars)



