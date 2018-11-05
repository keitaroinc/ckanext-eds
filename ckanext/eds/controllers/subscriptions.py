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
        h.redirect_to(h.url_for(controller=CTRL, action='subscription_manage', type=type))

    def subscription_manage(self, type):
        vars = {'data': {}, 'errors': {}, 'error_summary': {}}

        if c.userobj:
            id = c.userobj.id
        else:
            abort(400, _('No user specified'))

        data_dict = {'id': id}
        context = self._get_ctx()

        try:
            user_dict = get_action('user_show')(context, data_dict)
        except NotFound:
            h.flash_error(_('Not authorized to see this page'))
            h.redirect_to(controller='user', action='login')
        except NotAuthorized:
            abort(403, _('Not authorized to see this page'))

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
            h.redirect_to(h.url_for(controller=CTRL, action='subscription_manage', type='dataset'))

        if request.POST:
            sub_type = request.POST['subscription_type']
            for _type in SUBSCRIPTION_TYPES:
                if _type != sub_type:
                    continue

                action = logic.get_action('unfollow_{0}'.format(_type))
                objects = request.POST.getall(_type)
                map(lambda o: action(context, {'id': o}), objects)

                h.flash_success(_('Successfully unsubscribed from the selected {0}(s)!'.format(_type)))
                h.redirect_to(h.url_for(controller=CTRL, action='subscription_manage', type=_type))

        c.subscription_type = type
        c.user_list = logic.get_action('user_followee_list')(context, data_dict)
        c.group_list = logic.get_action('group_followee_list')(context, data_dict)
        c.dataset_list = logic.get_action('dataset_followee_list')(context, data_dict)
        form = render(super(SubscriptionController, self).edit_user_form, extra_vars=vars)

        return render('user/edit.html', extra_vars={'user_dict': user_dict, 'form': form})
