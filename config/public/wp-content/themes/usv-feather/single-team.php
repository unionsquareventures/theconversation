<?php get_header(); ?>

    <div id="main" role="main" class="row">
        <div class="col-lg-3">
            <div class="profile-photo">
                <img src="<?php the_field('thumbnail_image'); ?>" alt="profile photo">
            </div>
        </div>
        <div class="col-lg-6">
        <article class="team-profile">
            <h1><?php echo get_the_title(); ?></h1>

            <div class="intro">
                <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                    <?php the_content(); ?>
                    <?php edit_post_link('edit', '<span class="editlink">', '</span>'); ?>
                <?php endwhile; else: ?>
                <?php endif; ?>
            </div><!--end of intro-->

            <?php if(get_field('blog_feed_shortcode')) { ?>
                <div class="news-feed">
                    <h2><?php echo get_the_title(); ?>'s Blog</h2>
                    <ul>
                        <?php the_field('blog_feed_shortcode'); ?>
                    </ul>
                    <a href="<?php the_field('blog_url'); ?>" class="read-more">More</a>
                </div><!--end of news-feed-->
            <?php } ?>

            

            <?php if(get_field('photo_gallery')): ?>
            <div class="photos-feed">
                <h2>Photos</h2>
                <div class="thumbnails">
                    <?php while(has_sub_field('photo_gallery')): ?>
                        <?php 
                            $attachment_id = get_sub_field('photo');
                            $size_full = "full";
                            $size_thumb = "thumbnail";
                            $image_full = wp_get_attachment_image_src( $attachment_id, $size_full );
                            $image_thumb = wp_get_attachment_image_src( $attachment_id, $size_thumb );
                        ?>
                        <a href="<?php echo $image_full[0]; ?>"><img src="<?php echo $image_thumb[0]; ?>" width="80" height="80" alt="photo"></a>
                    <?php endwhile; ?>
                </div>
            </div><!--end of photos-feed-->
            <?php endif; ?>
            
        </article><!--end of team-profile-->
    </div>
    <div class="col-lg-3">
        <div class="profile-links">
            <?php if(get_field('blog_url')): ?>
                <a href="<?php echo addhttp( get_field('blog_url') ); ?>" class="sidebar-link">Blog</a>
            <?php endif; ?>
        
            <?php if(get_field('external_links')): ?>
                <?php while(has_sub_field('external_links')): ?>
                    <a href="<?php echo addhttp( get_sub_field('url') ); ?>" class="sidebar-link"><?php the_sub_field('title'); ?></a>
                <?php endwhile; ?>
            <?php endif; ?>
        </div>
    </div>
    </div><!--end of main-->

<?php get_footer(); ?>