<?php
/*
Template Name: Network
*/
?>

<?php get_header(); ?>

    <div id="main" role="main">
        <h1 class="mobile-page-headline">Network</h1>
        <article class="page">
            <div class="deck">
                <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                <?php the_content(); ?>
                <?php endwhile; else: ?>
                <?php endif; ?>
            </div>

            <div id="photo-wall">
                <img src="<?php the_field('network_page_photo'); ?>" alt="photo wall">
            </div>
            
            <div class="indent">
                <?php the_field('network_page_content'); ?>
            </div>
        </article>
    </div><!--end of main-->

<?php get_footer(); ?>