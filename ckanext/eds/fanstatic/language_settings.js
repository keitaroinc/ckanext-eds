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

    $(document).ready(function () {

        $('.language-switcher').on('click', function (e){

            var locale = e.target.getAttribute('data-language');

            api.post('user_extra_create', {
                key: 'language',
                value: locale
            }).done(function (data) {
                console.log(data);

            });

        });
    });
})($);