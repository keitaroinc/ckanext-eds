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