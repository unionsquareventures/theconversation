<?php get_header(); ?>

        <div id="main" role="main">
            <h1 class="mobile-page-headline">Team</h1>
            <div class="team">
                <h2>Partners</h2>
                <ul>
                    <?php
                        $args = array( 'post_type' => 'team', 'types' => 'partner', 'posts_per_page' => -1, 'orderby' => 'date', 'order' => 'ASC' ); 
                        $loop = new WP_Query( $args );
                        //$total_partners = $loop->found_posts;
                        $count = 0;
                        while ( $loop->have_posts() ) : $loop->the_post(); 
                    ?>
                        <?php if($count == 3) { ?>
                            <li class="blank"></li>
                            <li>
                                <a class="thumbnail" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('thumbnail_image'); ?>" alt="thumbnail"><span class="green-bar"></span></a>
                                <p class="description">
                                    <a href="<?php echo get_permalink(); ?>"><?php echo get_the_title(); ?></a> <?php the_excerpt(); ?>... <a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>
                                </p>
                            </li>
                            <?php $count++; ?>
                        <?php } else { ?>
                            <li>
                                <a class="thumbnail" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('thumbnail_image'); ?>" alt="thumbnail"><span class="green-bar"></span></a>
                                <p class="description">
                                    <a href="<?php echo get_permalink(); ?>"><?php echo get_the_title(); ?></a> <?php the_excerpt(); ?>... <a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>
                                </p>
                            </li>
                            <?php $count++; ?>
                        <?php } ?>
                    <?php endwhile; ?>
                    <?php wp_reset_postdata(); ?>
                </ul>
            </div><!--end of team-->
            <div class="team">
                <h2>Staff</h2>
                <ul>
                    <?php 
                        $args = array( 'post_type' => 'team', 'types' => 'staff', 'posts_per_page' => -1, 'orderby' => 'date', 'order' => 'ASC' ); 
                        $loop = new WP_Query( $args );
                        while ( $loop->have_posts() ) : $loop->the_post(); 
                    ?>
                        <li>
                            <a class="thumbnail" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('thumbnail_image'); ?>" alt="thumbnail"><span class="green-bar"></span></a>
                            <p class="description">
                                <a href="<?php echo get_permalink(); ?>"><?php echo get_the_title(); ?></a> <?php the_excerpt(); ?>... <a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>
                            </p>
                        </li>
                    <?php endwhile; ?>
                    <?php wp_reset_postdata(); ?>
                </ul>
            </div><!--end of team-->
        </div><!--end of main-->

<?php get_footer(); ?>