(function ($) {

    "use strict";

    $(".has-dropdown").click(function (e) {
        e.preventDefault();
        $(this).toggleClass("active");
    });

})(jQuery);
