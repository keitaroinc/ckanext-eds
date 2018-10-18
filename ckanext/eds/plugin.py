import os
import json

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.lib.plugins import DefaultTranslation
from ckanext.eds import helpers
from ckan.lib.i18n import get_available_locales

from ckanext.eds.model.user_extra import setup as setup_user_extra
from ckanext.eds.model.user_roles import setup as setup_user_roles
from ckanext.eds.logic import auth
from ckanext.eds.controllers.user import CTRL


try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config


class EdsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)


    # IRoutes

    def before_map(self, map):

        eds_ctrl = 'ckanext.eds.controllers.eds_controller:EdsController'

        map.connect('eds_quick_facts', '/quick-facts',
                    action='quick_facts', controller=eds_ctrl)

        guides_ctrl = 'ckanext.eds.controllers.eds_guides_controller:EdsGuidesController'
        map.connect('eds_api_guides', '/api-guides',
                    action='api_guides', controller=guides_ctrl)
        map.connect('eds_api_guides_edit', '/api-guides/edit',
                    action='api_guides_edit', controller=guides_ctrl)

        map.connect('eds_simple_guides', '/simple-guides',
                    action='simple_guides', controller=guides_ctrl)
        map.connect('eds_simple_guides_edit', '/simple-guides/edit',
                    action='simple_guides_edit', controller=guides_ctrl)



        subscriptions_ctrl = 'ckanext.eds.controllers.subscriptions:SubscriptionController'
        map.connect('subscription_manage', '/subscription/{type}/manage',
                    action='subscription_manage', ckan_icon='pie-chart', controller=subscriptions_ctrl)
        map.connect('subscription_delete', '/subscription/{type}/{id}/delete',
                    action='subscription_delete', ckan_icon='pie-chart', controller=subscriptions_ctrl)
        map.connect('request_reset', '/user/reset', controller=CTRL, action='request_reset')

        return map

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'eds')

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')

        charts = {}
        for _ in range(1, 5):
            charts.update({'ckanext.eds.chart_{idx}'.format(idx=_): [ignore_missing, unicode],
                           'ckanext.eds.chart_{idx}_subheader'.format(idx=_): [ignore_missing, unicode]})


        for l in get_available_locales():
            if l.short_name in toolkit.aslist(config.get('ckanext.eds.available_locales', 'en da_DK')):
                schema.update({'ckan.site_intro_text_{0}'.format(l): [ignore_missing, unicode],
                               'ckan.site_description_{0}'.format(l): [ignore_missing, unicode],
                               'ckan.site_about_{0}'.format(l): [ignore_missing, unicode],
                               'ckan.site_title_{0}'.format(l): [ignore_missing, unicode],
                               'ckan.cookie_notice_content_{0}'.format(l): [ignore_missing, unicode],
                               'api_guides_content_{0}'.format(l): [ignore_missing, unicode],
                               'simple_guides_content_{0}'.format(l): [ignore_missing, unicode]})

        schema.update(charts)

        return schema

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'eds_get_chart_resources': helpers.get_chart_resources,
            'eds_get_events': helpers.get_events,
            'eds_get_news': helpers.get_news,
            'eds_get_quick_facts_views': helpers.get_quick_facts_views,
            'eds_get_nubmer_of_charts': helpers.get_nubmer_of_charts,
            'show_update_indicator': helpers.show_update_indicator,
            'config_option_show': helpers.config_option_show,
            'get_user_locale': helpers.get_user_locale
        }

    ## IActions

    def get_actions(self):
        module_root = 'ckanext.eds.logic.action'
        action_functions = helpers._get_logic_functions(module_root)

        return action_functions

    def configure(self, config):
        self.startup = True

        # Setup licenses
        _setup_licenses()

        # Setup model
        setup_user_extra()
        setup_user_roles()

        self.startup = False

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'user_extra': auth.user_extra,
            'user_roles': auth.user_roles,
            'activity_create': auth.activity_create,
            'purge_revisions_eds': auth.purge_revisions_eds
        }

    # IPackageController

    def before_search(self, data_dict):
        if not data_dict.get('sort'):
            data_dict['sort'] = 'title_string asc'
        return data_dict


def _setup_licenses():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'licenses.json')) as f:
        licenses = json.loads(f.read())
        for l in licenses:
            if l['id'] != 'eds-license':
                continue

            url = config.get('ckan.site_url')
            name = 'Conditions_for_use_of_Danish_public_sector_data-License_for_use_of_data_in_ED.pdf'
            if not url.endswith('/'):
                url = url + '/'
            l['url'] = '{0}{1}'.format(url, name)
            break

        with open(os.path.join(here, 'public', 'licenses.json'), 'w') as o:
            o.write(json.dumps(licenses, indent=4, sort_keys=True,
                               separators=(',', ': '), ensure_ascii=False))
