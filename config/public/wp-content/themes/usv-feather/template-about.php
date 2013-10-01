<?php
/*
Template Name: About
*/
?>

<script>
    USV_person_names = [];
</script>

<?php get_header(); ?>

    <div id="main" role="main">
        <h1 class="mobile-page-headline">About</h1>
        <article class="page">
            <?php if(get_field('stats') && false): ?>
               <div class="stats hidden-xs">
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
               <div class="indent">
                   <?php //the_field('about_page_content'); ?>
               </div>
            <?php endif; ?>

            <div class="row">
                <div class="col-sm-12">
                    <div class="deck" style="padding: 0">
                        <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                        <?php the_content(); ?>
                        <?php endwhile; else: ?>
                        <?php endif; ?>
                    </div>

                     <?php /*
                     <!--<h2 class="section-heading" id="approach">Our Approach</h2>-->
                     <div>
                         <p>We founded Union Square Ventures in 2003 to invest in the applications layer of the web. Over the last seven years, we have refined that investment focus. We now invest almost exclusively in Internet services that create large networks. Some might think this focus is narrow. We don't see it that way at all. We believe the irresistible economics of Internet networks will ultimately transform the entire global economy. We continue to be very excited by the opportunity to invest in that transformation.</p>
                         <p>Early on, we recognized that investing in web services was different than investing in chips, routers and enterprise software. The start-ups are more capital efficient. Differentiation is more about user experience than proprietary technology. Defensibility is more about network effects than patents. We have designed our small, collegial, partner driven firm specifically for this new opportunity. Smaller fund sizes allow us to invest only as much as an entrepreneur needs and our successful portfolio companies can have a big impact on the funds' returns.</p>

                     </div>
                     */ ?>

                    <h2 class="section-heading" id="team-heading" style="margin-bottom: 0;">Team</h2>
                    <br />

                    <!-- Divs for bio information when clicking on each person -->
                    <div id="full-bio" style="display:none">
                        <div id="full-bio-content"></div>
                        <div id="close-bio"><a href="" class="btn btn-small">Close</a></div>
                    </div>

                    <div class="row">
                        <!--<div class="col-sm-2">
                            <h2 class="subsection">Partners</h2>
                        </div>-->
                        <div class="col-lg-12 clearfix">
                            <div class="row" id="people">
                                    <?php 
                                        /* Hacking order in manually, since custom post types ordering isn't working */
                                        $order = array(
                                                "brad-burnham",
                                                "fred-wilson",
                                                "albert-wenger",
                                                "john-buttrick",
                                                "andy-weissman",
                                                "kerri-rachlin",
                                                "nick-grossman",
                                                "brian-watson",
                                                "alexander-pease",
                                                "brittany-laughlin",
                                                "gillian-campbell",
                                                "veronica-keaveney"
                                            );
                                    ?>
                                    <?php foreach ($order as $person): ?>
                                        <?php
                                            $args = array( 'post_type' => 'team', 'posts_per_page' => -1, 'name' => $person ); 
                                            $loop = new WP_Query( $args );
                                            //$total_partners = $loop->found_posts;
                                            $count = 0;
                                            while ( $loop->have_posts() ) : $loop->the_post(); 
                                        ?>
                                            <script>
                                                USV_person_names.push('<?php echo $post->post_name; ?>');
                                            </script>

                                                <div class="col-sm-4 col-xs-4 person-container" usv-person="<?php echo $post->post_name; ?>">
                                                    <div class="person">
                                                        <a class="open-bio" usv:person="<?php echo $post->post_name; ?>" href="<?php echo get_permalink(); ?>">
                                                            <img src="<?php the_field('thumbnail_image'); ?>" alt="thumbnail" height="160" width="160">
                                                        </a>
                                                        <p class="bio">
                                                            <b><a class="open-bio" usv:person="<?php echo $post->post_name; ?>" href="<?php echo get_permalink(); ?>"><?php echo get_the_title(); ?></a></b><br /> <?php the_excerpt(); ?> <!-- <br /><a href="<?php echo get_permalink(); ?>" class="more-button">MORE</a>-->
                                                        </p>
                                                        <?php edit_post_link('edit', '<span class="editlink">', '</span>'); ?>
                                                        <div class="full-bio-shim" style="display:none"></div>
                                                        <div class="full-bio" style="display:none">
                                                            <?php the_content(); ?>
                                                            <div class="bio-links">
                                                                <?php if (get_field('blog_url')): ?>
                                                                    <a class="blog" href="<?php the_field('blog_url'); ?>"><?php the_field('blog_url'); ?></a>                                                  
                                                                <?php endif; ?>
                                                                <?php if (get_field('twitter_handle')): ?>
                                                                    <a class="twitter" href="http://twitter.com/<?php the_field('twitter_handle'); ?>">@<?php the_field('twitter_handle'); ?></a>
                                                                <?php endif; ?>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                        <?php $count++; ?>   
                                        <?php endwhile; ?>
                                    <?php endforeach; ?>
                                    <?php wp_reset_postdata(); ?>
                            </div><!-- /row -->
                        </div><!-- /col-10 -->
                    </div><!--end of team-->
                </div><!-- /.col-lg-5 -->
            </div><!-- /.row -->
            <h2 class="section-heading" id="team-heading" style="text-transform:uppercase; font-weight: 300">Our Focus</h2>
            
            [Blog posts, like at <a href="http://www.usv.com/focus/">usv.com/focus</a>]
            
        </article>
    </div><!--end of main-->

<?php get_footer(); ?>