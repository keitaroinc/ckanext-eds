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