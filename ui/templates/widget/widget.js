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
			src: url('/static/fonts/proximanova-bold-webfont.eot'); \
			src: local('proximanova-bold'),  \
				 local('proximanova-bold'),  \
				 url('/static/fonts/proximanova-bold-webfont.otf') format('opentype'), \
				 url('/static/fonts/proximanova-bold-webfont.svg#font') format('svg');  \
		} \
		@font-face { \
			font-family: 'usv-proximanova-light'; \
			src: url('/static/fonts/proximanova-light-webfont.eot'); \
			src: local('proximanova-light'),  \
				 local('proximanova-bold'),  \
				 url('/static/fonts/proximanova-light-webfont.otf') format('opentype'), \
				 url('/static/fonts/proximanova-light-webfont.svg#font') format('svg');  \
		} \
		#usv-widget { \
			font-family: 'usv-proximanova-light'; \
			font-size: 14px; \
		} \
		#usv-widget h1 { \
			margin: 0 0 15px; \
			font-weight: normal !important; \
		} \
		#usv-widget h1 a { \
			color: #fff; \
			text-decoration: none; \
			padding-left: 65px; \
			display: block; \
			background: #555 url('/static/img/usv-logo-green-44x44.png') 10px 0 no-repeat; \
			font-weight: 100; \
			font-style: normal; \
			letter-spacing: normal !important; \
			padding-top: 15px; \
			font-size: 16px; \
			height: 44px; \
		} \
		#usv-widget h1 a:hover { \
			color: #ddd; \
		} \
		#usv-widget ul { \
			padding: 0 10px;	 \		
		} \
		#usv-widget ul#posts li { \
			margin: 0 0 12px; \
			color: #999; \
			padding-left: 50px; \
			position: relative; \
			display: block !important; \
		} \
		#usv-widget ul#posts li.repeat { \
			display:none; \
		} \
		#usv-widget ul#posts .avatar { \
			border:1px solid #DFDFD1; \
			border-radius: 3px; \
			width: 36px; \
			height: 36px; \
			position: absolute; \
			top: 2px; \
			left: 4px; \
		} \
		#usv-widget ul#posts h3 { \
			font-family: 'usv-proximanova-bold'; \
			margin: 0px; \
			line-height: 1.2em; \
		} \
		#usv-widget ul#posts h3 a { \
			color: #000; \
		} \
		#usv-widget ul#posts .comment-count { \
			margin-left: 8px; \
		} \
		#usv-widget .comment-count:before { \
			content: '\e111'; \
			font-family: 'Glyphicons Halflings'; \
			-webkit-font-smoothing: antialiased; \
			font-style: normal; \
			font-weight: normal; \
			font-size: .9em; \
		} \
		#usv-widget ul#nav { \
		} \
		#usv-widget ul#nav li { \
			display: inline; \
		} \
		#usv-widget ul#nav li#more { \
			font-family: 'usv-proximanova-bold' \
		} \
		#usv-widget ul#nav li#tools { \
			float: right; \
		} \
		#usv-widget ul#nav a { \
			color: #628F20; \
		} \
	</style>");
	
	document.write('<div id="usv-widget">');
		document.write('<h1><a href="http://www.usv.com?referer=widget" target="_blank">Conversation</a></h1>');
		document.write('<ul id="posts">');
			{% for post in posts %}
				{% if 'previous_author_username' in locals() and previous_author_username == post.user.username %}
				  {% set repeat = True %}
				{% else %}
				  {% set repeat = False %}
				{% end %}
				var title = RegExp.escape("{{ post.title }}");
				document.write('<li {% if repeat %}class="repeat"{% end %}>');
					document.write('<img class="avatar" src="{{ post.user.profile_image_url }}" />');
					document.write('<h3><a href="{{ post.permalink() }}" target="_blank">' + title + '</a></h3>');
					document.write('by @{{ post.user.username }}');
					{% if post.comment_count > 0 %}
						document.write('<span class="comment-count">');
						document.write('{{ post.comment_count }}');
						document.write('</span>');
					{% end %}
				document.write('</li>');
				{% set previous_author_username = post.user.username %}  
			{% end %}
		document.write('</ul>');
		document.write('<ul id="nav">');
			document.write('<li id="more"><a href="http://www.usv.com?referer=widget" target="_blank">More</a></li>');
			document.write('<li id="tools"><a href="http://www.usv.com/#tools" target="_blank">Add this to your site</a></li>');
		document.write('</ul>');
	document.write('</div>')

/* call it */
})();