(function() {
/* begin our anon function */

	RegExp.escape= function(s) {
		//return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
		return s.replace("'", "\'");
	};


	/* Load up CSS -- remember to add "\" to the end of each line */
	document.write("<style type='text/css'> \
@font-face { \
font-family:'usv-proximanova-bold';\
src:url('http://www.usv.com/static/fonts/proximanova-bold-webfont.eot');\
src:local('proximanova-bold'),local('proximanova-bold'),url('http://www.usv.com/static/fonts/proximanova-bold-webfont.otf') format('opentype'),url('http://www.usv.com/static/fonts/proximanova-bold-webfont.svg#font') format('svg');\
}\
@font-face {\
font-family:'usv-proximanova-light';\
src:url('http://www.usv.com/static/fonts/proximanova-light-webfont.eot');\
src:local('proximanova-light'),url('http://www.usv.com/static/fonts/proximanova-light-webfont.otf') format('opentype'),url('http://www.usv.com/static/fonts/proximanova-light-webfont.svg#font') format('svg');\
}\
@font-face {\
font-family:'Glyphicons Halflings';\
src:url('http://www.usv.com/static/fonts/glyphicons-halflings-regular.eot');\
src:url('http://www.usv.com/static/fonts/glyphicons-halflings-regular.eot?#iefix') format('embedded-opentype'),url('http://www.usv.com/static/fonts/glyphicons-halflings-regular.woff') format('woff'),url('http://www.usv.com/static/fonts/glyphicons-halflings-regular.ttf') format('truetype'),url('http://www.usv.com/static/fonts/glyphicons-halflings-regular.svg#glyphicons-halflingsregular') format('svg');\
}\
}\
#usv-widget,#usv-widget * {\
letter-spacing:0 !important;\
}\
#usv-widget {\
font-family:'usv-proximanova-light','Helvetica Neue',Arial,sans-serif;\
font-size:14px;\
text-transform:none !important;\
position: relative;\
}\
#usv-widget a:hover {\
text-decoration:underline !important;\
}\
#usv-widget-sidebar {\
float: left;\
width: 200px;\
display: none;\
}\
#usv-widget-content {\
border-top:none;\
padding: 0px !important;\
}\
#usv-widget h1#usv-title {\
margin:0px !important;\
font-weight:normal !important;\
padding:0 !important;\
background:#333 url('http://www.usv.com/static/themes/usv/img/usv-logo-green-44x44.png') 0 0 no-repeat;\
height:44px !important;\
font-size:16px !important;\
border-radius: 3px 3px 0 0 !important;\
}\
#usv-widget h1#usv-title a {\
color:#fff;\
text-decoration:none;\
padding-left:57px;\
display:block;\
font-weight:100;\
font-style:normal;\
letter-spacing:normal !important;\
padding-top:14px;\
font-size:16px !important;\
line-height:1em !important;\
text-shadow:none !important;\
}\
#usv-widget h1#usv-title a:hover {\
color:#ddd;\
}\
#usv-widget p.usv-intro {\
text-align: left !important;\
margin: 0 0 10px !important;\
font-size: 16px !important;\
}\
#usv-widget p.usv-intro a {\
color: #809831 !important;\
}\
#usv-widget a#usv-submit-post-btn {\
display: inline-block;\
padding: 3px 8px;\
background: #809831;\
color: #fff;\
font-weight: normal;\
position: absolute;\
top: 8px;\
right: 8px;\
border-radius: 3px;\
}\
#usv-widget ul#usv-posts {\
padding:10px 0 0 0;\
margin:0 !important;\
background: #fff !important;\
}\
#usv-widget ul#usv-posts li {\
margin:0 0 12px 0px;\
color:#999;\
padding: 0px 10px 10px 60px;\
position:relative;\
display:block !important;\
line-height:20px !important;\
border-bottom: 1px solid #ddd !important;\
}\
#usv-widget ul#usv-posts li:last-child {\
margin-bottom: 0 !important; \
}\
#usv-widget ul#usv-posts li.repeat {\
display:none;\
}\
#usv-widget ul#usv-posts .usv-avatar {\
border-bottom:1px solid #DFDFD1;\
border-radius:3px;\
width:36px;\
height:36px;\
position:absolute;\
top:1px;\
left:6px;\
}\
#usv-widget ul#usv-posts h3.usv-post-title {\
font-family:'usv-proximanova-bold','Helvetica Neue',Arial,sans-serif;\
font-size:16px !important;\
margin:0px 0 0 0px;\
line-height:1.2em;\
font-weight:normal !important;\
padding-right:60px !important;\
}\
#usv-widget ul#usv-posts h3.usv-post-title a {\
color:#000;\
}\
#usv-widget ul#usv-posts .usv-post-author {\
font-size:14px !important;\
}\
#usv-widget ul#usv-posts a.usv-post-comment-link {\
color:#628F20;\
font-weight:bold;\
margin-left:5px;\
padding-right:5px;\
}\
#usv-widget ul#usv-posts a.usv-post-comment-link:hover {\
border-bottom:1px solid;\
text-decoration:none;\
}\
#usv-widget ul#usv-posts .usv-comment-count {\
background: url('http://www.usv.com/static/img/icon-comment-default.png?v=2') 10px 50% no-repeat;\
padding: 15px 10px 10px 40px;\
position: absolute;\
top: 2px;\
right: 0;\
width: 70px;\
color: #333;\
}\
#usv-widget ul#usv-nav {\
padding:0 0 5px !important;\
text-align:center;\
margin:0 !important;\
}\
#usv-widget ul#usv-nav li {\
display:block;\
margin:0 !important;\
padding:0 !important;\
line-height:20px !important;\
}\
#usv-widget ul#usv-nav li#usv-more {\
font-family:'usv-proximanova-bold','Helvetica Neue',Arial,sans-serif;\
font-size:16px;\
margin-bottom:0px !important;\
margin-top:-8px !important;\
}\
#usv-widget ul#usv-nav li#usv-tools {\
font-size:12px !important;\
}\
#usv-widget ul#usv-nav li#usv-tools a {\
color:#999;\
}\
#usv-widget ul#usv-nav a {\
color: #628F20;\
}\
</style>");

	document.write('<div id="usv-widget">');
		document.write('<h1 id="usv-title"><a href="http://www.usv.com?referer=widget" target="_blank">#usvconversation</a></h1>');
		document.write('<a id="usv-submit-post-btn" href="http://www.usv.com/posts/new">Submit a post</a>');
		document.write('<div id="usv-widget-content">');
		document.write('<ul id="usv-posts">');
			{% for i, post in enumerate(posts) %}
				{% if 'previous_author_username' in locals() and previous_author_username == post['user']['username'] %}
					{% set repeat = True %}
				{% else %}
					{% set repeat = False %}
				{% end %}
				var title = RegExp.escape("{{ post['title'] }}");

				{% if i < num_posts %}
				document.write('<li {% if repeat %}class="repeat"{% end %}>');
					document.write('<img class="usv-avatar" src="{{ post["user"]["profile_image_url"] }}" />');
					document.write('<span class="usv-post-author">@{{ post["user"]["username"] }}</span>');
					document.write('<h3 class="usv-post-title"><a href="http://www.usv.com/posts/{{ post["slug"] }}?referer=widget" target="_blank">' + title + '</a></h3>');
						document.write('<a class="usv-comment-count" href="http://www.usv.com/posts/{{ post["slug"] }}?referer=widget"><span class="">');
					{% if post['comment_count'] > 0 %}
						document.write('{{ post["comment_count"] }}');
					{% else %}
						document.write('&nbsp;');
					{% end %}
						document.write('</span></a>');
				document.write('</li>');
				{% set previous_author_username = post['user']['username'] %}  
				{% end %}
			{% end %}
		document.write('</ul>');
		document.write('</div>');	
	document.write('</div>');

/* call it */
})();