<?php
/*
Template Name: Network
*/
?>

<?php get_header(); ?>

    <div id="main" role="main">
        <h1 class="mobile-page-headline">Network</h1>
        
        <article class="page">
            <div class="deck" style="margin-bottom: 30px;">
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
                </div><!-- /.col-sm-6 -->
                <div id="slideshow" class="col-sm-6" style="padding-top:20px">
                    <iframe align="center" src="http://www.flickr.com/slideShow/index.gne?group_id=&user_id=83782618@N00&set_id=72157629963182717&text=" frameBorder="0" width="500" height="500" scrolling="no"></iframe> <br /><br />
                    
                    
                
                </div><!-- /col-sm-6 -->
                
            </div><!-- /.row -->
            <!--
            <h2 class="section-heading">Network Updates</h2>
            <div class="row">
                <?php for ($i = 0; $i < 6; $i++) : ?>
                    <div class="col-sm-4">
                        <div class="post" style="background: #eee; border-bottom: 1px solid #ddd; margin-bottom: 40px; padding: 20px;">
                            <h3>This is a post</h3>
                            <p>With some stuff</p>
                        </div>
                    </div>
                <?php endfor; ?>
                </div>
            --><!-- /row -->
                            
        </article>
    </div><!--end of main-->

<?php get_footer(); ?>