$(function () {
    $("#account_settings_btn").click(function(e) {
      $("#user_modal").modal('show');
      e.stopPropagation();
    });

    $("#navigation_button").click(function(e) {
      $("#navigation_button").toggleClass("active");
      $("#navigation_items").collapse('toggle');
    });
});
