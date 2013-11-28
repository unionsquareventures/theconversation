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
      src: url('{{ settings.get('base_url') }}/static/fonts/proximanova-bold-webfont.eot'); \
      src: local('proximanova-bold'),  \
         local('proximanova-bold'),  \
         url('{{ settings.get('base_url') }}/static/fonts/proximanova-bold-webfont.otf') format('opentype'), \
         url('{{ settings.get('base_url') }}/static/fonts/proximanova-bold-webfont.svg#font') format('svg');  \
    } \
    @font-face { \
      font-family: 'usv-proximanova-light'; \
      src: url('{{ settings.get('base_url') }}/static/fonts/proximanova-light-webfont.eot'); \
      src: local('proximanova-light'),  \
         local('proximanova-light'),  \
         url('{{ settings.get('base_url') }}/static/fonts/proximanova-light-webfont.otf') format('opentype'), \
         url('{{ settings.get('base_url') }}/static/fonts/proximanova-light-webfont.svg#font') format('svg');  \
    } \
    @font-face{ \
      font-family:'Glyphicons Halflings'; \
      src:url('{{ settings.get('base_url') }}/static/fonts/glyphicons-halflings-regular.eot'); \
      src:url('{{ settings.get('base_url') }}/static/fonts/glyphicons-halflings-regular.eot?#iefix')  \
      format('embedded-opentype'), \
        url('{{ settings.get('base_url') }}/static/fonts/glyphicons-halflings-regular.woff')  \
      format('woff'), \
        url('{{ settings.get('base_url') }}/static/fonts/glyphicons-halflings-regular.ttf')  \
      format('truetype'), \
        url('{{ settings.get('base_url') }}/static/fonts/glyphicons-halflings-regular.svg#glyphicons-halflingsregular') format('svg') \
      } \
    } \
    #usv-widget, \
    #usv-widget * { \
      letter-spacing: 0 !important; \
    } \
    #usv-widget { \
      font-family: 'usv-proximanova-light', 'Helvetica Neue', Arial, sans-serif; \
      font-size: 14px; \
      background: #fff !important; \
      text-transform: none !important; \
    } \
    #usv-widget a:hover { \
      text-decoration: underline !important; \
    } \
    #usv-widget h1#usv-title { \
      margin: 0 !important; \
      font-weight: normal !important; \
      padding: 0 !important; \
      background: #555 url('{{ settings.get('base_url') }}/static/themes/usv/img/usv-logo-green-50x50.png') 0 0 no-repeat; \
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
      text-shadow: none !important; \
    } \
    #usv-widget h1#usv-title a:hover { \
      color: #ddd; \
    } \
    #usv-widget-content { \
      border: 1px solid #ddd; \
      border-top: none; \
      padding: 10px 7px 0 !important; \
    } \
    #usv-widget ul#usv-posts { \
      padding: 0;	 \		
      margin: 0 !important; \
    } \
    #usv-widget ul#usv-posts li { \
      margin: 0 0 12px; \
      color: #999; \
      padding-left: 50px; \
      position: relative; \
      display: block !important; \
      line-height: 20px !important; \
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
      font-family: 'usv-proximanova-bold','Helvetica Neue', Arial, sans-serif;; \
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
    #usv-widget ul#usv-posts a.usv-post-comment-link { \
      color: #628F20; \
      font-weight: bold; \
      margin-left: 5px; \
      padding-right: 5px; \
    }\
    #usv-widget ul#usv-posts a.usv-post-comment-link:hover { \
      border-bottom: 1px solid; \
      text-decoration: none; \
    } \
    #usv-widget ul#usv-posts .usv-post-comment-count { \
      margin-left: 8px; \
      background: url('{{ settings.get('base_url') }}/static/img/comment-icon-green.png') left center no-repeat; \
      padding-left: 18px; \
    } \
    #usv-widget ul#usv-nav { \
      padding: 0 0 5px !important; \
      text-align: center; \
      margin: 0 !important; \
    } \
    #usv-widget ul#usv-nav li { \
      display: block; \
      margin: 0 !important; \
      padding: 0 !important; \
      line-height: 20px !important; \
    } \
    #usv-widget ul#usv-nav li#usv-more { \
      font-family: 'usv-proximanova-bold', 'Helvetica Neue', Arial, sans-serif; \
      font-size: 16px; \
      margin-bottom: 0px !important; \
      margin-top: -8px !important; \
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
    document.write('<h1 id="usv-title"><a href="http://www.usv.com?referer=widget" target="_blank">#usvconversation</a></h1>');
    document.write('<div id="usv-widget-content">');
    document.write('<ul id="usv-posts">');
      {% for post in posts %}
        {% if 'previous_author_username' in locals() and previous_author_username == post['user']['username'] %}
          {% set repeat = True %}
        {% else %}
          {% set repeat = False %}
        {% end %}
        var title = RegExp.escape("{{ post['title'] }}");
        document.write('<li {% if repeat %}class="repeat"{% end %}>');
          document.write('<img class="avatar" src="{{ post["user"]["profile_image_url"] }}" />');
          document.write('<h3 class="usv-post-title"><a href="http://www.usv.com/posts/{{ post["slug"] }}?referer=widget" target="_blank">' + title + '</a></h3>');
          document.write('<span class="usv-post-author">@{{ post["user"]["username"] }}</span>');
          {% if post['comment_count'] > 0 %}
            document.write('<a class="usv-post-comment-link" href="http://www.usv.com/posts/{{ post["slug"] }}?referer=widget"><span class="usv-post-comment-count">');
            document.write('{{ post["comment_count"] }}');
            document.write('</span></a>');
          {% end %}
        document.write('</li>');
        {% set previous_author_username = post['user']['username'] %}  
      {% end %}
    document.write('</ul>');
    document.write('<ul id="usv-nav">');
      document.write('<li id="usv-more"><a href="http://www.usv.com?referer=widget" target="_blank">More &rarr;</a></li>');
      document.write('<li id="usv-tools"><a href="http://www.usv.com/#tools" target="_blank">Add this to your site</a></li>');
    document.write('</ul>');
    document.write('</div>');	
  document.write('</div>');

/* call it */
})();