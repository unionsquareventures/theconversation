function USV_fill_hackpad_url() {
    if(!$('#post_hackpad_url').val()) {
      $.ajax('/generate_hackpad', {
        success: function(data) {
          $('#post_hackpad_url').val(data);
        }
      });
    }
}

function USV_remove_tinymce() {
    if($('.mce-tinymce').length > 0) {
        $('#post_body_raw').tinymce().remove();
    }
}

function USV_setup_tinymce() {
    if($('.mce-tinymce').length === 0) {
        // Setup TinyMCE
        var tinymce_plugins = "advlist, autolink, autosave, code, fullscreen, link, paste, preview";
        var tinymce_toolbar = "undo redo | bold italic strikethrough bullist numlist | blockquote link unlink | code";
        if(USV_is_admin) {
            tinymce_plugins += ", image, media";
            tinymce_toolbar += ", | image | media";
        } else {
          tinymce_plugins += ", charcount";
        }
        tinymce_toolbar += ", | fullscreen";

        if(/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
            tinymce_toolbar = false;
        }

        $('#post_body_raw').tinymce({
          // Location of TinyMCE script
          script_url : '/static/js/tinymce/tinymce.min.js',

          // General options
          theme : "modern",
          width: '100%',
          height: '300px',

          valid_elements: USV_tinymce_valid_elements,
          charcount_max_chars: USV_tinymce_post_char_limit,

          // Styling
          content_css: "/static/css/tinymce_content.css",
          menubar: false,
          document_base_url: "/",

          // Plugins and toolbar
          plugins: tinymce_plugins,
          toolbar: tinymce_toolbar,
        });
    }
}

$(function() {
    var jPM = $.jPanelMenu({
		menu: '#mobile-menu',
		trigger: '#menu-trigger',
		animated: false,
    keyboardShortcuts: false,
		closeOnContentClick: false,
		beforeOpen: function(){
			$('#jPanelMenu-menu').css("visibility","visible");
		}
	});

	jPM.on();

	$(window).resize(function(){
		var sw = $(window).width();
		if( sw > 768 && jPM.isOpen() ) {
			jPM.close();
		}
	}).resize();

  USV_remove_tinymce();
  USV_setup_tinymce();

	$('.header-submit-button, #submit-trigger').magnificPopup({
		type: 'inline',
		preloader: false,
		focus: '#post_title',

		callbacks: {
			open: function() {
				if($(window).width() < 700) {
					this.st.focus = false;
				} else {
					this.st.focus = '#name';
				}
        USV_remove_tinymce();
        USV_setup_tinymce();
        USV_fill_hackpad_url();
			}
		}
	});

	$('#toggle-hackpad-url').click(function(){

		$(this).toggleClass('checked');

		if( $(this).hasClass('checked') ) {
            USV_fill_hackpad_url();
            $('#post_has_hackpad').val('true');
			$('#post_hackpad_url').show();
		} else {
            $('#post_has_hackpad').val('');
			$('#post_hackpad_url').hide();
		}
	});

  $('#toggle-featured').click(function(){
    $(this).toggleClass('checked');
  });

  $('#toggle-deleted').click(function(){
    $(this).toggleClass('checked');
  });

  //share widget
  $('.share-twitter').sharrre({
    share: {
      twitter: true
    },
    enableHover: false,
    enableTracking: true,
    click: function(api, options){
      api.simulateClick();
      api.openPopup('twitter');
    }
  });

  $('.share-facebook').sharrre({
    share: {
      facebook: true
    },
    enableHover: false,
    enableTracking: true,
    click: function(api, options){
      api.simulateClick();
      api.openPopup('facebook');
    }
  });

  $('.share-googleplus').sharrre({
    share: {
      googlePlus: true
    },
    enableHover: false,
    enableTracking: true,
    urlCurl: '',
    click: function(api, options){
      api.simulateClick();
      api.openPopup('googlePlus');
    }
  });

});
