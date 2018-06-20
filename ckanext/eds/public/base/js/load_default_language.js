(function () {
    'use strict';

    var locales = ['en', 'da_DK'];
    var location = window.location;
    var default_language = document.querySelector('head').getAttribute('data-user-locale');
    console.log(default_language);
    var locale_str = location.pathname.split('/')[1];

    if (default_language && default_language != 'None') {

         if (locales.indexOf(locale_str) > -1) {

             if (default_language != locale_str) {

                 var loc = location.pathname.split('/');
                 loc[1] = default_language
                 var pathname = loc.join('/')

                 location.href = pathname + location.search;
             }

         } else {

             var loc = location.pathname.split('/');
             loc[0] = default_language
             var pathname = loc.join('/')

             window.location.href = '/'+pathname + location.search;

         }
    }

 })();
