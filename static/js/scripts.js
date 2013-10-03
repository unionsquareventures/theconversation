/*
 * jQuery Slugify a string!
 * by Pablo Bandin
 *
 * Dual licensed under the MIT and GPL licenses:
 *   <a href="http://www.opensource.org/licenses/mit-license.php" rel="nofollow">http://www.opensource.org/licenses/mit-license.php</a>
 *   <a href="http://www.gnu.org/licenses/gpl.html" rel="nofollow">http://www.gnu.org/licenses/gpl.html</a>
 */
String.prototype.slugify = function(){
  var from = 'àáäãâèéëêìíïîòóöôõùúüûñç·/_,:;',
    to = 'aaaaaeeeeiiiiooooouuuunc------',
    i = 0,
    len = from.length,
    str = this.toLowerCase();

  for( ; i < len; i++ ){
    str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }

  return str.replace(/^\s+|\s+$/g, '') //trim
    .replace(/[^-a-zA-Z0-9\s]+/ig, '')
    .replace(/\s/gi, "-");
};


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

function hide_extra_posts() {
  if($(window).width() < 769) {
    $('.featured-feed .feed li').slice(2).hide();
    if($('.featured-feed').hasClass('mobile-hidden')) {
        $('.featured-feed').hide();
    }
  } else {
    $('.featured-feed .feed li').slice(2).show();
    $('.featured-feed').show();
  }
}

function USV_setup_tinymce() {
    if($('.mce-tinymce').length === 0) {
        // Setup TinyMCE
        var tinymce_plugins = "advlist, autolink, autosave, code, link, paste, preview";
        var tinymce_toolbar = "undo redo | bold italic strikethrough bullist numlist | blockquote link unlink | code";
        if(USV_is_admin) {
            tinymce_plugins += ", image, media";
            tinymce_toolbar += ", | image | media";
        } else {
          tinymce_plugins += ", charcount";
        }

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
    if($('.featured-feed')) {
      hide_extra_posts();
      $(window).on('resize', hide_extra_posts);
    }

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

  $("#submit-trigger").on('click', function() {
    $("#submit-modal").modal("show");
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


  function toggleCheckbox(fakebox, realbox) {
    if($(realbox).attr('checked')) {
        $(realbox).removeAttr('checked');
        $(fakebox).removeClass('checked');
    } else {
        $(realbox).attr('checked', 'true');
        $(fakebox).addClass('checked');
    }
  }

  $('#toggle-featured').on('click', function () {
      toggleCheckbox('#toggle-featured', '#post_featured');
  });

  $('#toggle-deleted').on('click', function() {
      toggleCheckbox('#toggle-deleted', '#post_deleted');
  });

  function initCheckbox(fakebox, realbox) {
    if($(realbox).attr('checked')) {
        $(fakebox).addClass('checked');
    } else {
        $(fakebox).removeClass('checked');
    }
  }

  initCheckbox('#toggle-featured', '#post_featured');
  initCheckbox('#toggle-deleted', '#post_deleted');

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
