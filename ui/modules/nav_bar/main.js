$(function () {
    $("#navigation_button").tappable(function() {
      $("#navigation_button").toggleClass("active");
      $("#navigation_items").collapse('toggle');
    });
});
