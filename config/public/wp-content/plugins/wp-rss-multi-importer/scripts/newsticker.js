(function ($) {
    $.fn.extend({
        vscroller: function (options) {
            var settings = $.extend({ speed: 1800, stay: 2000, newsfeed: '', cache: true }, options);

            return this.each(function () {
                var interval = null;
                var mouseIn = false;
                var totalElements;
                var isScrolling = false;
                var h;
                var t;
                var wrapper = $('.news-wrapper');
                        var newsContents = $('.news-contents');
                      
                        var i = 0;
                        totalElements = $.find('.news').length;
						
                        h = parseFloat($('.news:eq(0)').outerHeight());
                        $('.news', wrapper).each(function () {
                            $(this).css({ top: i++ * h });
                        });
                        t = (totalElements - 1) * h;
                        newsContents.mouseenter(function () {
                            mouseIn = true;
                            if (!isScrolling) {
                                $('.news').stop(true, false);
                                clearTimeout(interval);
                            }
                        });
                        newsContents.mouseleave(function () {
                            mouseIn = false;
                            interval = setTimeout(scroll, settings.stay);
                        });
                        interval = setTimeout(scroll, 1);
                    
                function scroll() {
                    if (!mouseIn && !isScrolling) {
                        isScrolling = true;
                        $('.news:eq(0)').stop(true, false).animate({ top: -h }, settings.speed, function () {

                            clearTimeout(interval);
                            var current = $('.news:eq(0)').clone(true);
                            current.css({ top: t });
                            $('.news-contents').append(current);
                            $('.news:eq(0)').remove();
                            isScrolling = false;
                            interval = setTimeout(scroll, settings.stay);

                        });
                        $('.news:gt(0)').stop(true, false).animate({ top: '-=' + h }, settings.speed);
                    }
                }
              
            });
        }
    });
})(jQuery);
