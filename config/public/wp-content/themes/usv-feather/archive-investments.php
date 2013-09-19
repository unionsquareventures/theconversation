<?php get_header(); ?>

	<h1 class="mobile-page-headline">Investments</h1>

	<div class="row">
		<div class="col-lg-3 col-xs-2 hidden-xs">
			
			
			<div id="portfolio-filter">
				<p class="text-muted" style="margin-top: 0;">by location:</p>
				<ul class="filter-tabs" id="locations">
					<li class="all active"><a href="#" usv-filter="all">All</a></li>
				</ul>
				<p class="text-muted" style="white-space:nowrap">by initial investment:</p>
				<ul class="filter-tabs" id="series">
					<li class="all active"><a href="#" usv-filter="all">All</a></li>
				</ul>
				<p class="text-muted" style="white-space:nowrap">by year:</p>
				<ul class="filter-tabs" id="years">
					<li class="all active"><a href="#" usv-filter="all">All</a></li>
				</ul>
				<p class="text-muted" style="white-space:nowrap">by type:</p>
				<ul class="filter-tabs" id="types">
					<li class="all active"><a href="#" usv-filter="all">All</a></li>
				</ul>
				</div>
			
		</div><!-- /col-lg-2 -->
		
		<div class="col-md-9 col-xs-12">
			<h2 class="subsection section-heading" id="current-portfolio">Current Portfolio<span class="filter-label" style="display:none"></span>
				</h2>
			<div class="row investments-list">
				<?php
					$args = array( 'post_type' => 'investments', 'investment-types' => 'current', 'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC' ); 
					$loop = new WP_Query( $args );
					$count = 0;
					while ( $loop->have_posts() ) : $loop->the_post(); 
				?>

				<div class="col-sm-3 col-xs-6 company-container current" usv:investment_series="<?php the_field('investment_series'); ?>" usv:city="<?php the_field('city'); ?>" usv:investment_date="<?php the_field('investment_date'); ?>" usv:investment_type="<?php the_field('type'); ?>">
					<div class="company">
					<a href="<?php the_permalink(); ?>"><img alt="<?php the_title(); ?>" src="<?php the_field('logo'); ?>"  class="logo mt-image-none <?php if (get_field('white_logo')) : ?>white<?php endif; ?>" style="" width="220" height="150"></a>
					<p class="summary">
						<?php 
							if( $post->post_excerpt ) {
								echo '<a href="'. get_permalink() . '">' . get_the_title() .'</a> ';
								echo get_the_excerpt();
	}                                   else {
								$content = get_the_content();
								$stripped = strip_tags($content, '<a>');
								$trunc_description = substr($stripped, 0, 180);
								echo $trunc_description;
							}
						?>
						<!--<a href="<?php the_permalink(); ?>" class="btn-continue">More</a>-->
					</p>
					<span class="since-date">
						<?php if (get_field('investment_date')) :?><?php the_field('investment_date'); ?><?php else: ?>{year}<?php endif; ?>, <?php if (get_field('investment_series')) : ?><?php the_field('investment_series'); ?><?php else: ?>{series}<?php endif; ?>
					</span>
	
					<?php edit_post_link('edit', '<span class="editlink">', '</span>'); ?>
				</div><!-- /company -->
				</div><!-- /col-lg-4 -->
				<?php endwhile; ?>
				<?php wp_reset_postdata(); ?>
				
			</div><!-- /row -->


			<h2 class="subsection section-heading" id="past-portfolio" style="clear:both">Past Portfolio<span class="filter-label" style="display:none"></span>
				</h2>	

			<div class="row investments-list">
								<?php
									$args = array( 'post_type' => 'investments', 'investment-types' => 'past', 'posts_per_page' => -1, 'orderby' => 'title', 'order' => 'ASC' ); 
									$loop = new WP_Query( $args );
									$count = 0;
									while ( $loop->have_posts() ) : $loop->the_post(); 
								?>
	
				<div class="col-sm-3 col-xs-6 company-container past" usv:investment_series="<?php the_field('investment_series'); ?>" usv:city="<?php the_field('city'); ?>" usv:investment_date="<?php the_field('investment_date'); ?>" usv:investment_type="<?php the_field('type'); ?>">
					<div class="company">
					<a href="<?php the_permalink(); ?>"><img alt="<?php the_title(); ?>" src="<?php the_field('logo'); ?>"  class="logo mt-image-none <?php if (get_field('white_logo')) : ?>white<?php endif; ?>" style="" width="220" height="150"></a>
					<p class="summary">
						<?php 
							if( $post->post_excerpt ) {
								echo '<a href="'. get_permalink() . '">' . get_the_title() .'</a> ';
								echo get_the_excerpt();
	}                                   else {
								$content = get_the_content();
								$stripped = strip_tags($content, '<a>');
								$trunc_description = substr($stripped, 0, 180);
								echo $trunc_description;
							}
						?>
						<!--<a href="<?php the_permalink(); ?>" class="btn-continue">More</a>-->
					</p>
					<span class="since-date">
						<?php if (get_field('investment_date')) :?><?php the_field('investment_date'); ?><?php else: ?>{year}<?php endif; ?>, <?php if (get_field('investment_series')) : ?><?php the_field('investment_series'); ?><?php else: ?>{series}<?php endif; ?>
					</span>
	
					<?php edit_post_link('edit', '<span class="editlink">', '</span>'); ?>
				</div><!-- /company -->
				</div><!-- /col-lg-4 -->
				<?php endwhile; ?>
				<?php wp_reset_postdata(); ?>
				
			</div><!-- /row -->
		</div><!-- /col-lg-10 -->
		
		
	</div><!-- /row -->
	
	
<script>
		/*$(document).ready(function() {
			var min_height = 0;
			$('.investments-list li').each(function(){
				if ($(this).height() > min_height) {
					min_height = $(this).height()
				}
			});
			//$('.investments-list li').height(min_height + 'px');
			//$('.investments-list img').css('margin-top', min_height - 165 + "px");
			//$('.investments-list p.summary').css('margin-top', min_height - 165 + "px");
		});
		*/
</script>

<?php get_footer(); ?>