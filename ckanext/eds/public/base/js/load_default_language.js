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

