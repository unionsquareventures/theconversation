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
        checkbox.attr('checked', false).change();
        button.html(label_unselected);
      } else {
        // Check
        checkbox.attr('checked', true).change();
        button.html(label_selected);
      }
    });

    $(this).after(button);
  });

  // Render hackpad
  if($('#link_has_hackpad').attr('checked')) {
    $('#hackpad').show();
  } else {
    $('#hackpad').hide();
  }

  $('#link_has_hackpad').change(function(e) {
    if($(this).attr('checked')) {
      $('#hackpad').show();
    } else {
      $('#hackpad').hide();
    }
  });

  // Setup TinyMCE
  $('.link_body_raw').tinymce({
    // Location of TinyMCE script
    script_url : '/static/js/tiny_mce/tiny_mce.js',

    // General options
    theme : "advanced",
    plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

    // Theme options
    theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,bullist,numlist,blockquote,pagebreak,|,link,unlink,image,|" +
                              "|,iespell,media,emotions,|,fullscreen",
    theme_advanced_resizing : true,
    theme_advanced_toolbar_align : "center",
    theme_advanced_statusbar_location: "none",

    // Example content CSS (should be your site CSS)
    content_css : "/static/css/tinymce_content.css",

    // Drop lists for link/image/media/template dialogs
    template_external_list_url : "lists/template_list.js",
    external_link_list_url : "lists/link_list.js",
    external_image_list_url : "lists/image_list.js",
    media_external_list_url : "lists/media_list.js",
  });
});

