<?php get_header(); ?>

    <div id="main" role="main">
        <article class="investments-profile">
            <h1><?php echo get_the_title(); ?></h1>

            <div class="profile-photo">
                <a href="#"><img src="<?php the_field('logo'); ?>" alt="profile photo"></a>
            </div>

            <div class="profile-links">
                <?php if(get_field('twitter_url')): ?>
                    <a href="<?php echo addhttp( get_field('twitter_url') ); ?>" class="sidebar-link">Twitter</a>
                <?php endif; ?>

                <?php if(get_field('blog_url')): ?>
                    <a href="<?php echo addhttp( get_field('blog_url') ); ?>" class="sidebar-link">Blog</a>
                <?php endif; ?>
                
                <?php if(get_field('jobs_url')): ?>
                    <a href="<?php echo addhttp( get_field('jobs_url') ); ?>" class="sidebar-link">Job Openings</a>
                <?php endif; ?>
            </div>

            <div class="intro">
                <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                    <?php the_content(); ?>
                <?php endwhile; else: ?>
                <?php endif; ?>
            </div><!--end of intro-->
            
            <?php if(get_field('blog_feed_shortcode')) { ?>
                <div class="news-feed" id="anchor-news">
                    <h2><?php echo get_the_title(); ?> Blog</h2>
                    <ul>
                        <?php the_field('blog_feed_shortcode'); ?>
                    </ul>
                    <a href="<?php the_field('blog_url'); ?>" class="read-more">More</a>
                </div><!--end of news-feed-->
            <?php } ?>

            <?php if(get_field('jobs_feed_shortcode')) { ?>
                <div class="news-feed" id="anchor-jobs">
                    <h2>Job Openings</h2>
                    <ul>
                        <?php the_field('jobs_feed_shortcode'); ?>
                    </ul>
                    <a href="<?php the_field('jobs_url'); ?>" class="read-more">More</a>
                </div><!--end of news-feed-->
            <?php } ?>

        </article><!--end of investments-profile-->
    </div><!--end of main-->

<?php get_footer(); ?>