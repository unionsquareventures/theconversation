<?php get_header(); ?>

    <div id="main" role="main">
        <article class="investments-profile">
            <h1><?php echo get_the_title(); ?></h1>

            <div class="profile-photo">
                <a href="#"><img src="<?php the_field('logo'); ?>" alt="profile photo"></a>
            </div>

            <div class="profile-links">
                <?php if(get_field('twitter_url')): ?>
                    <a href="<?php echo addhttp( get_field('twitter_url') ); ?>" class="sidebar-link">Twitter</a>
                <?php endif; ?>

                <?php if(get_field('blog_url')): ?>
                    <a href="<?php echo addhttp( get_field('blog_url') ); ?>" class="sidebar-link">Blog</a>
                <?php endif; ?>
                
                <?php if(get_field('jobs_url')): ?>
                    <a href="<?php echo addhttp( get_field('jobs_url') ); ?>" class="sidebar-link">Job Openings</a>
                <?php endif; ?>
            </div>

            <div class="intro">
                <?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
                    <?php the_content(); ?>
                <?php endwhile; else: ?>
                <?php endif; ?>
            </div><!--end of intro-->
            
<?php if (false) : ?>
            <?php if(get_field('blog_feed_shortcode')) { ?>
                <div class="news-feed" id="anchor-news">
                    <h2><?php echo get_the_title(); ?> Blog</h2>
                    <ul>
                        <?php the_field('blog_feed_shortcode'); ?>	
                    </ul>
                    <a href="<?php the_field('blog_url'); ?>" class="read-more">More</a>
                </div><!--end of news-feed-->
            <?php } ?>

            <?php if(get_field('jobs_feed_shortcode')) { ?>
                <div class="news-feed" id="anchor-jobs">
                    <h2>Job Openings</h2>
                    <ul>
                        <?php the_field('jobs_feed_shortcode'); ?>
                    </ul>
                    <a href="<?php the_field('jobs_url'); ?>" class="read-more">More</a>
                </div><!--end of news-feed-->
            <?php } ?>
	
<?php endif; ?>

	<div class="news-feed" id="blog-feed" style="display:none">
		<h2>Blog Posts</h2>
		<ul></ul>
		<a href="<?php the_field('blog_url'); ?>" class="read-more">More</a>
	</div>

	<div class="news-feed" id="jobs-feed" style="display:none">
		<h2>Jobs</h2>
		<ul></ul>
		<a href="<?php the_field('jobs_url'); ?>" class="read-more">More</a>
	</div>

        </article><!--end of investments-profile-->
    </div><!--end of main-->



<script>
	var blogCallback = function(json) {
			jQuery("#blog-feed").show();
			var items = json.query.results.rss.channel.item;
			for (var i=0; i<5; i++) {
				console.log(items[i]);
				var li = '<li>' + items[i].title + '</li>';
var li = '<li><a class="title" target="_self" href="">'+ items[i].title +'</a><div class="date">'+ items[i].pubDate +'</div></li>';
				jQuery("#blog-feed ul").append(li);
			}
	}

	var jobsCallback = function(json) {
			jQuery("#jobs-feed").show();
			var items = json.query.results.rss.channel.item;
			for (var i=0; i<5; i++) {
				console.log(items[i]);
				var li = '<li>' + items[i].title + '</li>';
var li = '<li><a class="title" target="_self" href="">'+ items[i].title +'</a><div class="date">'+ items[i].pubDate +'</div></li>';
				jQuery("#jobs-feed ul").append(li);
			}
	}

		
	var fetchRSS = function (feedURL, callback) {
            jQuery.ajax({
                url:'http://query.yahooapis.com/v1/public/yql?q=select%20%2a%20from%20xml%20where%20url=%27' + encodeURIComponent(feedURL) + '%27&format=json&callback=' + callback,
                dataType: "jsonp",
                type: 'GET'
	     });
	}

	fetchRSS('<?php the_field('blog_feed_url'); ?>', 'blogCallback');
	fetchRSS('<?php the_field('jobs_feed_url'); ?>', 'jobsCallback');

    </script>

<?php get_footer(); ?>