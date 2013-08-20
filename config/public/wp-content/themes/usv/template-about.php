<?php
/*
Template Name: About
*/
?>

<?php get_header(); ?>

    <div id="main" role="main">
        <h1 class="mobile-page-headline">About</h1>
        <article class="page">
            <div class="deck">
                <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                <?php the_content(); ?>
                <?php endwhile; else: ?>
                <?php endif; ?>
            </div>
            
            <?php if(get_field('stats')): ?>
                <div class="stats">
                    <?php //count total current and past investments
                        $queryCurrent = new WP_Query( array( 'investment-types' => 'current', 'posts_per_page' => -1 ) );
                        $currentCount = $queryCurrent->post_count;
                        wp_reset_postdata();
                        $queryPast = new WP_Query( array( 'investment-types' => 'past', 'posts_per_page' => -1 ) );
                        $pastCount = $queryPast->post_count;
                    ?>
                    <ul>
                        <li>
                            <span><?php echo $currentCount; ?></span>
                            Current Portfolio
                        </li>
                        <li>
                            <span><?php echo $pastCount; ?></span>
                            Past Investments
                        </li>
                        <?php while(the_repeater_field('stats')): ?>
                        <li>
                            <span><?php the_sub_field('number'); ?></span>
                            <?php the_sub_field('text'); ?>
                        </li>
                        <?php endwhile; ?>
                    </ul>
                </div><!--end of stats-->
             <?php endif; ?>
            
            <div class="indent">
                <?php the_field('about_page_content'); ?>
            </div>
        </article>
    </div><!--end of main-->

<?php get_footer(); ?>