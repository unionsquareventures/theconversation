$(function() {
    $("#twitter-login-button").on('click', function() {
        window.location = '/auth/twitter/?next=' + encodeURIComponent(window.location.pathname + window.location.search);
    });
});

$('.ajax_upvote_link').on('click', function(e) {
    e.stopPropagation();
    e.preventDefault();
    var upvote_link = $(this);
    $.ajax($(this).attr('href'), {
        error: function(jqxhr, status, error) {
            alert("Could not upvote, an error occurred. Please try again.");
        },
        success: function(data, status, jqxhr) {
            var resp = $.parseJSON(data);
            if(resp['error']) {
                if(resp['redirect']) {
                    $("#submit-modal").modal("show");
                } else {
                  alert(resp['error']);
                }
                return;
            }
            var plural = '';
            if(resp['votes'] != 1) {
                plural = 's';
            }
            upvote_link.children('.value').text(resp['votes'] + ' vote' + plural);
        }
    });
});
