(function() {
/* begin our anon function */
	
	RegExp.escape= function(s) {
		//return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
		return s.replace("'", "\'");
	};

	
	/* Load up CSS -- remember to add "\" to the end of each line */
	document.write("<style type='text/css'>\
		@font-face { \
			font-family: 'usv-proximanova-bold'; \
			src: url('{{ base_url }}/static/fonts/proximanova-bold-webfont.eot'); \
			src: local('proximanova-bold'),  \
				 local('proximanova-bold'),  \
				 url('{{ base_url }}/static/fonts/proximanova-bold-webfont.otf') format('opentype'), \
				 url('{{ base_url }}/static/fonts/proximanova-bold-webfont.svg#font') format('svg');  \
		} \
		@font-face { \
			font-family: 'usv-proximanova-light'; \
			src: url('{{ base_url }}/static/fonts/proximanova-light-webfont.eot'); \
			src: local('proximanova-light'),  \
				 local('proximanova-bold'),  \
				 url('{{ base_url }}/static/fonts/proximanova-light-webfont.otf') format('opentype'), \
				 url('{{ base_url }}/static/fonts/proximanova-light-webfont.svg#font') format('svg');  \
		} \
		#usv-widget, \
		#usv-widget * { \
			letter-spacing: 0 !important; \
		} \
		#usv-widget { \
			font-family: 'usv-proximanova-light'; \
			font-size: 14px; \
			background: #fff !important; \
			text-transform: none !important; \
		} \
		#usv-widget a:hover { \
			text-decoration: underline !important; \
		} \
		#usv-widget h1#usv-title { \
			margin: 0 0 10px !important; \
			font-weight: normal !important; \
			padding: 0 !important; \
			background: #555 url('{{ base_url }}/static/img/usv-logo-green-50x50.png') 0 0 no-repeat; \
			height: 50px !important; \
			font-size: 16px !important; \
		} \
		#usv-widget h1#usv-title a { \
			color: #fff; \
			text-decoration: none; \
			padding-left: 57px; \
			display: block; \
			font-weight: 100; \
			font-style: normal; \
			letter-spacing: normal !important; \
			padding-top: 18px; \
			font-size: 16px !important; \
			line-height: 1em !important; \
		} \
		#usv-widget h1#usv-title a:hover { \
			color: #ddd; \
		} \
		#usv-widget ul#usv-posts { \
			padding: 0 7px;	 \		
			margin: 0 !important; \
		} \
		#usv-widget ul#usv-posts li { \
			margin: 0 0 12px; \
			color: #999; \
			padding-left: 50px; \
			position: relative; \
			display: block !important; \
		} \
		#usv-widget ul#usv-posts li.repeat { \
			display:none; \
		} \
		#usv-widget ul#usv-posts .avatar { \
			border:1px solid #DFDFD1; \
			border-radius: 3px; \
			width: 36px; \
			height: 36px; \
			position: absolute; \
			top: 2px; \
			left: 0px; \
		} \
		#usv-widget ul#usv-posts h3.usv-post-title { \
			font-family: 'usv-proximanova-bold'; \
			margin: 0px; \
			line-height: 1.2em; \
			font-weight: normal !important; \
			padding-right: 3px !important; \
		} \
		#usv-widget ul#usv-posts h3.usv-post-title a { \
			color: #000; \
		} \
		#usv-widget ul#usv-posts .usv-post-author { \
			font-size: 12px !important; \	
		} \
		#usv-widget ul#usv-posts .usv-post-comment-count { \
			margin-left: 8px; \
		} \
		#usv-widget .usv-post-comment-count:before { \
			content: '\e111'; \
			font-family: 'Glyphicons Halflings'; \
			-webkit-font-smoothing: antialiased; \
			font-style: normal; \
			font-weight: normal; \
			font-size: .9em; \
		} \
		#usv-widget ul#usv-nav { \
			padding: 0 0 5px !important; \
			text-align: center; \
			margin: 0 !important; \
		} \
		#usv-widget ul#usv-nav li { \
			display: block; \
		} \
		#usv-widget ul#usv-nav li#usv-more { \
			font-family: 'usv-proximanova-bold'; \
			font-size: 16px; \
			margin-bottom: 10px !important; \
		} \
		#usv-widget ul#usv-nav li#usv-tools { \
			font-size: 12px !important; \
		} \
		#usv-widget ul#usv-nav li#usv-tools a { \
			color: #999; \
		} \
		#usv-widget ul#usv-nav a { \
			color: #628F20; \
		} \
	</style>");
	
	document.write('<div id="usv-widget">');
		document.write('<h1 id="usv-title"><a href="http://www.usv.com?referer=widget" target="_blank">Conversation @ USV</a></h1>');
		document.write('<ul id="usv-posts">');
			{% for post in posts %}
				{% if 'previous_author_username' in locals() and previous_author_username == post.user.username %}
				  {% set repeat = True %}
				{% else %}
				  {% set repeat = False %}
				{% end %}
				var title = RegExp.escape("{{ post.title }}");
				document.write('<li {% if repeat %}class="repeat"{% end %}>');
					document.write('<img class="avatar" src="{{ post.user.profile_image_url }}" />');
					document.write('<h3 class="usv-post-title"><a href="{{ post.permalink() }}?referer=widget" target="_blank">' + title + '</a></h3>');
					document.write('<span class="usv-post-author">by @{{ post.user.username }}</span>');
					{% if post.comment_count > 0 %}
						document.write('<span class="usv-post-comment-count">');
						document.write('{{ post.comment_count }}');
						document.write('</span>');
					{% end %}
				document.write('</li>');
				{% set previous_author_username = post.user.username %}  
			{% end %}
		document.write('</ul>');
		document.write('<ul id="usv-nav">');
			document.write('<li id="usv-more"><a href="http://www.usv.com?referer=widget" target="_blank">More &rarr;</a></li>');
			document.write('<li id="usv-tools"><a href="http://www.usv.com/#tools" target="_blank">Add this to your site</a></li>');
		document.write('</ul>');
	document.write('</div>')

/* call it */
})();