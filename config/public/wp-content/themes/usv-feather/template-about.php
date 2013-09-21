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
                <br />
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
                <?php //the_field('about_page_content'); ?>
            </div>
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
                             <?php $count++; ?>   
                            <?php endwhile; ?>
                            <?php wp_reset_postdata(); ?>
                    </div><!-- /row -->
                </div><!-- /col-10 -->
            </div><!--end of team-->
            
            <h2 class="section-heading" id="approach">Approach</h2>
            <div>
                <p>We founded Union Square Ventures in 2003 to invest in the applications layer of the web. Over the last seven years, we have refined that investment focus. We now invest almost exclusively in Internet services that create large networks. Some might think this focus is narrow. We don't see it that way at all. We believe the irresistible economics of Internet networks will ultimately transform the entire global economy. We continue to be very excited by the opportunity to invest in that transformation.</p>
                <p>Early on, we recognized that investing in web services was different than investing in chips, routers and enterprise software. The start-ups are more capital efficient. Differentiation is more about user experience than proprietary technology. Defensibility is more about network effects than patents. We have designed our small, collegial, partner driven firm specifically for this new opportunity. Smaller fund sizes allow us to invest only as much as an entrepreneur needs and our successful portfolio companies can have a big impact on the funds' returns.</p>

            </div>
        </article>
    </div><!--end of main-->

<?php get_footer(); ?>