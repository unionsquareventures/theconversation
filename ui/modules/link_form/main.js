$(function() {
  // Transform checkboxes into labeled buttons
  $('.link_form input[type=checkbox]').each(function(i, o) {
    var checkbox = $(this);
    // Extract label
    var label = $(".link_form label[for='"+checkbox.attr('id')+"']");
    var label_unselected = label.html();
    var label_selected = label.attr('data-selected');
    // Hide
    label.remove();
    checkbox.hide();

    var button = '<button type="button" data-toggle="button" class="btn btn-large btn-block">';
    button += label_unselected;
    button += '</button>';
    button = $(button);

    if(checkbox.attr('checked')) {
      button.addClass('active');
      button.html(label_selected);
    }

    button.on('click', function(e) {
      if(checkbox.attr('checked')) {
        // Uncheck
        checkbox.attr('checked', false);
        button.html(label_unselected);
      } else {
        // Check
        checkbox.attr('checked', true);
        button.html(label_selected);
      }
    });

    $(this).after(button);
  });

});

