       </div><!--end of container-->
    </div><!-- #content -->
    
        <footer id="site-footer">
            <div class="container">
                <div class="footer-search">
                    <h4>Search Posts Archive</h4>
                    <div class="footer-search-container">
                        <input type="search" placeholder="Enter Keywords" />
                        <a class="submit-button" href="#"></a>
                    </div>
                </div>

                <div class="footer-content">
                    
                    <div class="col-a">
                        <h4>Contact Us</h4>
                        <p>If you would like to share your ideas, business, or feedback with us, please send us email at <a href="mailto:info@usv.com">info@usv.com</a>. All business plan submissions must include a clear description of your operations and current progress.</p>
                    </div>
                    <div class="col-b">
                        <h4>Union Square Ventures</h4>
                        <p class="address">
                            915 Broadway, 19th Floor<br>
                            New York, NY 10010
                        </p>
                        <p class="telephone">
                            <strong>Tel</strong> &nbsp;&nbsp;(212) 914-7880<br>
                            <strong>Fax</strong> &nbsp;&nbsp;(212) 914-7399<br>
                        </p>
                    </div>
                </div>
            </div>
        </footer><!--end of footer-->

    </div><!--end of shell-->

    <nav id="mobile-menu">
        <ul>
            <li class="heading">News</li>
            <li><a href="<?php the_field('newest_news_page_url', 'option'); ?>">Hot</a></li>
            <li><a href="<?php the_field('hottest_news_page_url', 'option'); ?>">Newest</a></li>
            <li><a href="<?php the_field('featured_news_archive_url', 'option'); ?>">Featured</a></li>
            <li class="heading">UNION SQUARE VENTURES</li>
            <li><a href="<?php echo get_post_type_archive_link( 'team' ); ?>">Team</a></li>
            <li><a href="<?php echo get_post_type_archive_link( 'investments' ); ?>">Investments</a></li>
            <li><a href="<?php echo get_permalink('10'); ?>">Network</a></li>
            <li><a href="<?php echo get_permalink('8'); ?>">About</a></li>
            <li><a href="<?php echo get_permalink('12'); ?>">Jobs</a></li>
        </ul>
    </nav>

    <?php wp_footer(); ?>
    <script>
        $(document).ready(function() {
        
            var series_options = [];
            $('.company').each(function() {
                var series = $(this).parent().attr('usv:investment_series');
                if ($.inArray(series, series_options) == -1) {
                    // we haven't seen this one yet
                    if (series != "" && typeof(series) != "undefined") {
                        series_options.push(series);
                    }
                }
            });
            series_options.sort();
            series_options.reverse();
        
            var city_options = [];
            $('.company').each(function() {
                var city = $(this).parent().attr('usv:city');
                if ($.inArray(city, city_options) == -1) {
                    // we haven't seen this one yet
                    if (city != "" && typeof(city) != "undefined") {
                        city_options.push(city);
                    }
                }
            });
            city_options.sort();
            city_options.reverse();
            
            var year_options = [];
            $('.company').each(function() {
                var year = $(this).parent().attr('usv:investment_date');
                if ($.inArray(year, year_options) == -1) {
                    // we haven't seen this one yet
                    if (year != "" && typeof(year) != "undefined") {
                        year_options.push(year);
                    }
                }
            });
            year_options.sort();
            
            var type_options = [];
            $('.company').each(function() {
                var type = $(this).parent().attr('usv:investment_type');
                if ($.inArray(type, type_options) == -1) {
                    // we haven't seen this one yet
                    if (type != "" && typeof(type) != "undefined") {
                        type_options.push(type);
                    }
                }
            });
            type_options.sort();
            type_options.reverse();
            
            var all_options = series_options.concat(city_options).concat(year_options).concat(type_options);        
        
            for (var i = 0; i < series_options.length; i++ ) {
                $("#series li:first").after('<li><a href="#" usv-filter="' + series_options[i] + '">' + series_options[i] + '</a></li>');
            }
        
            for (var i = 0; i < city_options.length; i++ ) {
                $("#locations li:first").after('<li><a href="#" usv-filter="' + city_options[i] + '">' + city_options[i] + '</a></li>');
            }
            
            for (var i = 0; i < year_options.length; i++ ) {
                $("#years li:first").after('<li><a href="#" usv-filter="' + year_options[i] + '">' + year_options[i] + '</a></li>');
            }
            
            for (var i = 0; i < type_options.length; i++ ) {
                $("#types li:first").after('<li><a href="#" usv-filter="' + type_options[i] + '">' + type_options[i] + '</a></li>');
            }
        
        
        
            $(".filter-tabs a").click(function(e) {
                e.preventDefault()
                var query = $(this).attr("usv-filter");
                filter_portfolio(this, query);
            });
            
            if (window.location.hash) {
                var query = window.location.hash.split("#")[1];
                filter_button = $( "a[usv-filter='" + query + "']" );
                if(filter_button.length > 0) {
                     filter_portfolio(filter_button, query);                   
                }
            }
        
            function filter_portfolio(filter_button, query) {

                // deactivate all other tabs
                $('.filter-tabs li').removeClass('active');
                
                // make all the "alls" active, just in case
                $('.all').addClass('active');
                
                // make this active.
                $(filter_button).parent().addClass('active');
                
                // deactivate this one's parent all
                $(filter_button).parent().parent().find('.all').removeClass('active');
                                
                // hide or show all the companies
                $('.company').parent().each(function(){
                    if ($(this).attr("usv:city") == query || $(this).attr("usv:investment_series") == query || $(this).attr("usv:investment_date") == query || $(this).attr("usv:investment_type") == query) {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                });
                
                if (query == "all") {
                    $('.company').parent().show();
                    $('.filter-tabs li').removeClass('active');
                    // make all the "alls" active
                    $('.all').addClass('active');
                    $('body').ScrollTo();
                    window.location.hash = '';
                } else {
                    window.location.hash = query;
                    $('body').ScrollTo();
                }
                
                // hide & show section headings
                if ($('.company-container.current:visible').length == 0) {
                    $('#current-portfolio').hide();
                } else {
                    $('#current-portfolio').show();
                    if (query != 'all') {
                        $('#current-portfolio .filter-label').text(', tagged "' + query + '"').show();
                    } else {
                        $('#current-portfolio .filter-label').hide()
                    }
                }
                if ($('.company-container.past:visible').length == 0) {
                    $('#past-portfolio').hide();
                } else {
                    $('#past-portfolio').show();
                    if (query != "all") {
                        $('#past-portfolio .filter-label').text(', tagged "' + query + '"').show();
                    } else {
                        $('#past-portfolio .filter-label').hide();
                    }
                }   

            }
        
            var min_height = 0;
            $('.company').each(function(){
                if ($(this).height() > min_height) {
                    min_height = $(this).height()
                }
            });
            //$('.company').height(min_height + 'px');
        
            var min_height = 0;
            $('.partner').each(function(){
                if ($(this).height() > min_height) {
                    min_height = $(this).height()
                }
            });
            $('.partner').height(min_height + 'px');
        
            var min_height = 0;
            $('.staff').each(function(){
                if ($(this).height() > min_height) {
                    min_height = $(this).height()
                }
            });
            $('.staff').height(min_height + 'px');
            //$('.investments-list img').css('margin-top', min_height - 165 + "px");
            //$('.investments-list p.summary').css('margin-top', min_height - 165 + "px");
        
        
        });
    </script>
</body>
</html>