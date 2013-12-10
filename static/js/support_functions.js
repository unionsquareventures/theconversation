$(function() {
  $("#twitter-login-button").on('click', function() {
    window.location = '/auth/twitter/?next=' + encodeURIComponent(window.location.pathname + window.location.search);
  });
});

$('.ajax_upvote_link').on('click', function(e) {
  e.stopPropagation();
  e.preventDefault();
  var upvote_link = $(this);
  if (upvote_link.parent().hasClass('bumped')) {
    // user has already voted - this is a downvote.
    $.ajax($(this).attr('href'), {
      error: function(jqxhr, status, error) {
        alert("Could not upvote, an error occurred. Please try again.");
      },
      success: function(data, status, jqxhr) {
        if(data['data']['error']) {
          if(data['data']['redirect']) {
            $("#submit-modal").modal("show");
          } else {
            alert(data['data']['error']);
          }
          return;
        }
        upvote_link.find('.value').text(data['data']['votes'] - 1);
        upvote_link.parent().removeClass('bumped');
        upvote_link.attr('href', upvote_link.attr('href').replace('unbump', 'bump'));
      }
    });
  } else {
    // user has not already voted. this is an upvote.
    $.ajax($(this).attr('href'), {
       error: function(jqxhr, status, error) {
         alert("Could not upvote, an error occurred. Please try again.");
       },
       success: function(data, status, jqxhr) {
         if(data['data']['error']) {
           if(data['data']['redirect']) {
             $("#submit-modal").modal("show");
           } else {
             alert(data['data']['error']);
           }
           return;
         }
         upvote_link.find('.value').text(data['data']['votes'] - 1);
         upvote_link.parent().addClass('bumped');
         upvote_link.attr('href', upvote_link.attr('href').replace('bump', 'unbump'));
       }
     }); 
  }
});
