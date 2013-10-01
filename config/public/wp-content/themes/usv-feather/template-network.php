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

            <!--<div id="photo-wall">
                <img src="<?php the_field('network_page_photo'); ?>" alt="photo wall">
            </div>-->
            <div class="row">
                <div class="col-sm-6">
                    <?php the_field('network_page_content'); ?>
                </div>
                <div id="slideshow" class="col-sm-6" style="text-align:right; padding-top:20px">
                    <iframe align="center" src="http://www.flickr.com/slideShow/index.gne?group_id=&user_id=83782618@N00&set_id=72157629963182717&text=" frameBorder="0" width="450" height="450" scrolling="no"></iframe> 
                </div>
                
            </div>
                            
        </article>
    </div><!--end of main-->

<?php get_footer(); ?>