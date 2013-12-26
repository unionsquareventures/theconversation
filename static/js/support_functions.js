$(function() {
  $("#twitter-login-button").on('click', function() {
    window.location = '/auth/twitter/?next=' + encodeURIComponent(window.location.pathname + window.location.search);
  });
});
