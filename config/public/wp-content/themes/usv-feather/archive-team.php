<?php get_header(); ?>

            <h1 class="mobile-page-headline">Team</h1>
            
            <div class="jumbotron">Union Square Ventures is a venture capital firm based in New York City. We are a small collegial partnership that manages $450,000,000 across three funds. Our portfolio companies create services that have the potential to fundamentally transform important markets.</div>

            <h2 class="section-heading">Team</h2>
            
            <div class="row">
                <!--<div class="col-sm-2">
                    <h2 class="subsection">Partners</h2>
                </div>-->
                <div class="col-lg-12 clearfix">
                    <div class="row">
                            <?php
                                $args = array( 'post_type' => 'team', 'posts_per_page' => -1 ); 
                                $loop = new WP_Query( $args );
                                //$total_partners = $loop->found_posts;
                                $count = 0;
                                while ( $loop->have_posts() ) : $loop->the_post(); 
                            ?>

                                    <div class="col-sm-3 col-xs-6 person-container">
                                        <div class="person partner">
                                        <a class="" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('thumbnail_image'); ?>" alt="thumbnail" height="160" width="160"><span class="green-bar"></span></a>
                                        <p class="bio">
                                            <b><a href="<?php echo get_permalink(); ?>"><?php echo get_the_title(); ?></a></b><br /> <?php the_excerpt(); ?> <!-- <br /><a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>-->
                                        </p>
                                        <?php edit_post_link('edit', '<span class="editlink">', '</span>'); ?>
                                        </div>
                                    </div>

                            <?php endwhile; ?>
                            <?php wp_reset_postdata(); ?>
                    </div><!-- /row -->
                </div><!-- /col-10 -->
            </div><!--end of team-->
            
            <?php /*
            <div class="row">
                <div class="col-lg-2">
                    <h2 class="subsection">Staff</h2>
                </div>
                <div class="col-lg-10">
                    <div class="row">
                    <?php 
                        $args = array( 'post_type' => 'team', 'types' => 'staff', 'posts_per_page' => -1, 'orderby' => 'date', 'order' => 'ASC' ); 
                        $loop = new WP_Query( $args );
                        while ( $loop->have_posts() ) : $loop->the_post(); 
                    ?>
                        <div class="col-sm-4 col-xs-6">
                            <div class="person staff">
                            <a class="" href="<?php echo get_permalink(); ?>"><img src="<?php the_field('thumbnail_image'); ?>" alt="thumbnail" height="220" width="220"><span class="green-bar"></span></a>
                            <p class="bio">
                                <b><a href="<?php echo get_permalink(); ?>"><?php echo get_the_title(); ?></a></b><br /> <?php the_excerpt(); ?> <!--<br /><a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>-->
                            </p>
                            <?php edit_post_link('edit', '<span class="editlink">', '</span>'); ?>
                            </div>
                        </div>
                    <?php endwhile; ?>
                    <?php wp_reset_postdata(); ?>
                </div>
            </div>
            <? */ ?>
            </div><!--end of team-->

<?php get_footer(); ?>