(function ($) {

    "use strict";

    $(".token-btn").click(function (e) {
        e.preventDefault();

        var token = $(this).prev(".token");

        token.toggleClass("show");

        if (token.hasClass("show")) {
            $(this).html("Masquer");
        } else {
            $(this).html("Afficher");
        }
    });

}(jQuery));
