/*
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
*/

(function () {
    'use strict';
    var api = {
        get: function (action, params) {
            var api_ver = 3
            var base_url = ckan.sandbox().client.endpoint;
            params = $.param(params);
            var url = base_url + '/api/' + api_ver + '/action/' + action + '?' + params;
            return $.getJSON(url);
        },
        post: function (action, data, api_key) {
            var api_ver = 3
            var base_url = ckan.sandbox().client.endpoint;
            var url = base_url + '/api/' + api_ver + '/action/' + action;
            var headers = {
                'Authorization': api_key
            }; // set api key in headers
            return $.ajax({
                url: url,
                data: JSON.stringify(data),
                contentType: "application/json",
                type: 'POST',
                headers: headers
            });

        }
    };

    var is_subscribed = false;

    $(document).ready(function () {

        if (window.location.hash != "") {
            $('a[href="' + window.location.hash + '"]').click()
        }

        // Mark all existing checkboxes in the nearest table
        $('.mark-all').click(function (e) {

            var table = $(e.target).closest('table');
            $('td input:checkbox', table).prop('checked', this.checked);

        });

        var subscriptionFilters = $('.list-subscription-filters .btn');

        subscriptionFilters.first().addClass('btn-primary');

        subscriptionFilters.click(function () {
            subscriptionFilters.removeClass('btn-primary');
            $(this).removeClass('btn-primary').addClass('btn-primary');
        });


        function initNewsSubscription(data) {

            $('.flash-messages', document.body).html('');
            $('#mark_all_checkbox').prop('checked', false);

            if (data.success) {
                if (data.result && !data.result.message) {

                    is_subscribed = true;
                    $('#news_subscription').prop('checked', true);

                    if (data.result.notify_by_mail) {
                        $('#news_mail_subscription').prop('checked', true);
                    }
                } else {
                    is_subscribed = false;
                    $('#news_subscription').prop('checked', false);
                    $('#news_mail_subscription').prop('checked', false);
                }
            }
        }

        api.post('news_subscription_show', {}).done(function (data) {
            initNewsSubscription(data);
        });


        $('#update_subscription_button').click(function (e) {
            e.preventDefault();

            var news_subscription = $('#news_subscription').prop('checked');
            var news_mail_subscription = $('#news_mail_subscription').prop('checked');

            if (news_subscription && !is_subscribed) {

                api.post('news_subscription_create', {
                    notify_by_mail: news_mail_subscription
                }).done(function (data) {
                    initNewsSubscription(data);
                    window.location.href = window.location.pathname + window.location.search + '#other_settings';
                    var msg = ckan.i18n.ngettext('You have successfully subscribed to news');
                    ckan.notify('', msg, 'success');
                });

            } else if (news_subscription && is_subscribed) {

                api.post('news_subscription_update', {
                    notify_by_mail: news_mail_subscription
                }).done(function (data) {
                    initNewsSubscription(data);
                    window.location.href = window.location.pathname + window.location.search + '#other_settings';
                    var msg = ckan.i18n.ngettext('Subscription successfully updated');
                    ckan.notify('', msg, 'success');
                });

            } else if (!news_subscription && is_subscribed) {

                api.post('news_subscription_delete', {}).done(function (data) {
                    initNewsSubscription(data);
                    window.location.href = window.location.pathname + window.location.search + '#other_settings';
                    var msg = ckan.i18n.ngettext('You have successfully unsubscribed from news');
                    ckan.notify('', msg, 'success');
                });
            } else if (!news_subscription && !is_subscribed && news_mail_subscription) {

                api.post('news_subscription_create', {
                    notify_by_mail: news_mail_subscription
                }).done(function (data) {
                    initNewsSubscription(data);
                    window.location.href = window.location.pathname + window.location.search + '#other_settings';
                    var msg = ckan.i18n.ngettext('You have successfully subscribed to news and email notifications');
                    ckan.notify('', msg, 'success');
                });

            } else {
                $('.flash-messages', document.body).html('');
                window.location.href = window.location.pathname + window.location.search + '#other_settings';
            }
        });
    });

})($);