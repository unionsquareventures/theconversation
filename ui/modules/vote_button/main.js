$(function() {
    $(".vote_button").on("click", function(e) {
        window.location = $(this).closest(".vote_button").children("li").children("a").attr('href');
        e.stopPropagation();
    });
});
