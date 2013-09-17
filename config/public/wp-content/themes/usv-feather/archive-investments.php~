<?php get_header(); ?>

        <div id="main" role="main">
            <h1 class="mobile-page-headline">Investments</h1>
            <div class="investments">
                <h2>Current Portfolio</h2>
                <ul>
                    <?php
                        $args = array( 'post_type' => 'investments', 'investment-types' => 'current', 'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC' ); 
                        $loop = new WP_Query( $args );
                        $count = 0;
                        while ( $loop->have_posts() ) : $loop->the_post(); 
                    ?>
                        <li>
                            <a class="thumbnail" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('logo'); ?>" alt="thumbnail"><span class="green-bar"></span></a>
                            <p class="description">
                                <?php 
                                    if( $post->post_excerpt ) {
                                        echo '<a href="'. get_permalink() . '">' . get_the_title() .'</a> ';
                                        echo get_the_excerpt() . '...';
}                                   else {
                                        $content = get_the_content();
                                        $stripped = strip_tags($content, '<a>');
                                        $trunc_description = substr($stripped, 0, 180);
                                        echo $trunc_description . '...';
                                    }
                                ?>
                                <a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>
                            </p>
                        </li>
                    <?php endwhile; ?>
                    <?php wp_reset_postdata(); ?>
                </ul>
            </div><!--end of team-->
            <div class="investments">
                <h2>Past Investments</h2>
                <ul>
                    <?php
                        $args = array( 'post_type' => 'investments', 'investment-types' => 'past', 'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC' ); 
                        $loop = new WP_Query( $args );
                        $count = 0;
                        while ( $loop->have_posts() ) : $loop->the_post(); 
                    ?>
                        <li>
                            <a class="thumbnail" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('logo'); ?>" alt="thumbnail"><span class="green-bar"></span></a>
                            <p class="description">
                                <?php 
                                    if( $post->post_excerpt ) {
                                        echo '<a href="'. get_permalink() . '">' . get_the_title() .'</a> ';
                                        echo get_the_excerpt() . '...';
}                                   else {
                                        $content = get_the_content();
                                        $stripped = strip_tags($content, '<a>');
                                        $trunc_description = substr($stripped, 0, 180);
                                        echo $trunc_description . '...';
                                    }
                                ?>
                                <a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>
                            </p>
                        </li>
                    <?php endwhile; ?>
                    <?php wp_reset_postdata(); ?>
                </ul>
            </div><!--end of team-->
        </div><!--end of main-->

<?php get_footer(); ?>