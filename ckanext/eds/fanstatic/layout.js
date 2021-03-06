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

$(document).ready(function () {

    var btnScrollTop = $('.btn-scroll-top');
    var scrollTopOffset = 250;

    // Scroll to top when .btn-scroll-top is clicked
    btnScrollTop.click(function(){
        $(window).scrollTop(0);
    });

    // Check if top-scrolling offset has been passed
    if ($(this).scrollTop() > scrollTopOffset) {
        btn_scroll_top_show();
    }

    // Show/hide top-scrolling button
    $(window).scroll(function () {

        if ($(this).scrollTop() > scrollTopOffset) {
            btn_scroll_top_show();
        } else {
            btn_scroll_top_hide();
        }

    });

    // Add CSS class when showing top-scrolling button
    function btn_scroll_top_show() {
        btnScrollTop.addClass('btn-scroll-top-show');
    }

    // Remove CSS class when hiding top-scrolling button
    function btn_scroll_top_hide() {
        btnScrollTop.removeClass('btn-scroll-top-show');
    }

});