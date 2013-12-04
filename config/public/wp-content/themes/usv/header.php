<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title><?php if( is_front_page() ) { echo "About | Union Square Ventures"; ?>
	<?php } else { wp_title('|', true, 'right') . bloginfo('name'); } ?>
	</title>

    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?> data-menu-position="closed">
	<div class="shell">
        
        <div id="mobile-header">
            <a id="menu-trigger" href="#">Open Menu</a>
            <a id="mobile-logo" href="<?php the_field('homepage_url', 'option'); ?>">Union Square Ventures</a>
        </div>

        <div class="container">
            
            <header id="site-header">
                <a id="logo" href="<?php the_field('homepage_url', 'option'); ?>">Union Square Ventures</a>
                <ul id="main-nav">
                    <li><a class="<?php if(is_post_type_archive('team')) { echo "current"; } ?>" href="<?php echo get_post_type_archive_link( 'team' ); ?>">Team</a></li><li><a class="<?php if(is_post_type_archive('investments')) { echo "current"; } ?>" href="<?php echo get_post_type_archive_link( 'investments' ); ?>">Investments</a></li><li><a class="<?php if(is_page('10')) { echo "current"; } ?>" href="<?php echo get_permalink('10'); ?>">Network</a></li><li><a class="<?php if(is_page('8')) { echo "current"; } ?>" href="<?php echo get_permalink('8'); ?>">About</a></li><li><a class="<?php if(is_page('12')) { echo "current"; } ?>" href="<?php echo get_permalink('12'); ?>">Jobs</a></li>
                </ul>
            </header><!--end of site-header-->