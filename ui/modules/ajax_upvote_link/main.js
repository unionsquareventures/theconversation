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
                alert(resp['error']);
                return;
            }
            upvote_link.children('.value').text(resp['votes'] + ' votes');
        }
    });
});
