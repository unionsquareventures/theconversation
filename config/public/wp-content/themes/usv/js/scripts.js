(function($){
	
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

	//USV JOBS
	var h = location.hash;

	$(".tab_content").hide();

	$('.side-nav a').click(function(e) {
		e.preventDefault();
		var cur_item = $(this).attr("href");
		if(cur_item){ window.location.hash = cur_item; }
	});
	
	if (h !== '' && h !== '#top') {
		var slug = h.split("#")[1];
		var target = slug.split(",")[0];
		// set the new tab active
		$('a[rel=' + target + ']').parent().addClass("active").show();
		$("div#" + target).show();
		// side nav
		$("#yo #" + target).addClass("active").show();
	} else {
		// by default, activate the tab, tab content, and side nav
		$("ul.job-tabs li:first").addClass("active").show();
		$("#yo #in").addClass("active").show();
		$(".tab_content:first").show();
	}

	//when category is clicked on single column mobile layout
	$(".cat").click(function(){
		$(".cat").removeClass("current");
		$(this).addClass("current");
		$('.jobs').hide();
		$(this).find('.jobs').show();
		$('body,html').animate({scrollTop: $(this).offset().top - 10 }, 0);
	});

	// set the click handler
	$("ul.job-tabs li").click(function(e) {
		e.preventDefault();

		// deactivate where we were
		var prevTab = $("ul.job-tabs li.active").find("a").attr("rel");
		$("yo ul.active").removeClass("active");
		$("#yo #" + prevTab).hide();
		$("ul.job-tabs li").removeClass("active");
		$(".tab_content").hide();

		// set the new tab active
		$(this).addClass("active");
		var activeTab = $(this).find("a").attr("href");

		//window.location.hash = activeTab;
		$("div" + activeTab).fadeIn('fast');

		// side nav
		$("#yo " + activeTab).addClass("active");
		$("#yo " + activeTab).fadeIn('fast');
	});

}(jQuery));