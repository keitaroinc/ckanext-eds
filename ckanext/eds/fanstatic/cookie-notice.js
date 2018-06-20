$(document).ready(function () {
    var cookie_agreement = localStorage.getItem('eds_cookie_agreement');
    $('.btn-accept-cookie').on('click', function (evt) {
        evt.preventDefault();
        localStorage.setItem('eds_cookie_agreement', true);
        $('.cookie-notice').addClass('hidden');
    });
    if (cookie_agreement == null || cookie_agreement == false) {
        $('.cookie-notice').delay(1000).removeClass('hidden');
    }
});