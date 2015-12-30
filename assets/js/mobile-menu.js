(function ($) {

    "use strict";

    $("#mobile-menu-button").click(function (e) {
        e.preventDefault();
        $("html").toggleClass("show-mobile-menu");
    });

    $("#main-content").click(function (e) {
        $("html").removeClass("show-mobile-menu");
    });

})(jQuery);
