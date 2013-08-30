        </div><!--end of container-->

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
</body>
</html>