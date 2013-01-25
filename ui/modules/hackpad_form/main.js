$(function() {
    var link_form = $('.link_hackpad_url');
    link_form.hide();
    var modify_form = $('#modify_hackpad_url');
    modify_form.val(link_form.val());

    modify_form.keyup(function(e) {
        $('#hackpad_iframe').attr('src', $(this).val());
    });
});

