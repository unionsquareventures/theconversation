$(function() {
	var jPM = $.jPanelMenu({
		menu: '#mobile-menu',
		trigger: '#menu-trigger',
		animated: false,
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

	$('.header-submit-button, #submit-trigger').magnificPopup({
		type: 'inline',
		preloader: false,
		focus: '#title',

		callbacks: {
			beforeOpen: function() {
				if($(window).width() < 700) {
					this.st.focus = false;
				} else {
					this.st.focus = '#name';
				}
			}
		}
	});

	$('#toggle-hackpad-url').click(function(){
		$(this).toggleClass('checked');

		if( $(this).hasClass('checked') ) {
			$('#hackpad_url').show();
		} else {
			$('#hackpad_url').hide();
		}
	});
});
