$(function () {
    $('#navigation_bar .submit_content').on("click", function(e) {
        window.location = "/links/new";
    });
    $("#navigation_button").tappable(function() {
      $("#navigation_button").toggleClass("active");
      $("#navigation_items").collapse('toggle');
    });
});
