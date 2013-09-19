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
    
  <link rel="shortcut icon" href="<?php bloginfo('template_directory'); ?>/img/usv-favicon.png" type="image/png" />

    <link rel="stylesheet" href="<?php bloginfo('template_directory'); ?>/css/bootstrap.min.css">
    <link rel="stylesheet" href="<?php the_field('homepage_url', 'option'); ?>/static/css/style.css?<?php echo rand(); ?>">
	<?php wp_head(); ?> 
</head>
<body <?php body_class(); ?> data-menu-position="closed">
    
	<div class="shell">
        
        <div id="mobile-header">
            <a id="menu-trigger" href="#">Open Menu</a>
            <a id="mobile-logo" href="<?php the_field('homepage_url', 'option'); ?>">Union Square Ventures</a>
            <a id="submit-trigger" href="#">Submit Post</a>
        </div>

            <header id="site-header">
               <div class="container">
                <a id="logo" href="<?php the_field('homepage_url', 'option'); ?>">Union Square Ventures</a>
                <ul id="main-nav">
                    <li><a class="<?php if(is_home()) { echo "current"; } ?>" href="<?php the_field('homepage_url', 'option'); ?>">Conversation</a></li>
                    <li><a class="<?php if(is_page('8')) { echo "current"; } ?>" href="<?php echo get_permalink('8'); ?>">About</a></li>
                    <!--<li><a class="<?php if(is_post_type_archive('team')) { echo "current"; } ?>" href="<?php echo get_post_type_archive_link( 'team' ); ?>">Team</a></li>-->
                    <li><a class="<?php if(is_post_type_archive('investments')) { echo "current"; } ?>" href="<?php echo get_post_type_archive_link( 'investments' ); ?>">Investments</a></li>
                    <!--<li><a class="<?php if(is_page('10')) { echo "current"; } ?>" href="<?php echo get_permalink('10'); ?>">Network</a></li>
                    <li><a class="<?php if(is_page('8')) { echo "current"; } ?>" href="<?php echo get_permalink('8'); ?>">About</a></li>-->
                    <?php if ($_SERVER['HTTP_HOST'] == "sandbox.wrkng.net") :?>
                    <li><a href="#" onclick="alert('broken on this server'); return false;">Jobs</a></li>

                    <?php else: ?>
                    <li><a class="<?php if(is_page('12')) { echo "current"; } ?>" href="<?php echo get_permalink('12'); ?>">Jobs</a></li>
                        
                    <?php endif; ?>
                </ul>
                <div id="login">
                    Welcome, @you! <!--&nbsp;[<a href="#">logout</a>]-->
                </div>
                </div>         
            </header><!--end of site-header-->
            <?php if( is_home() && false ): ?>
                <div id="tools">
                    <div class="container">
                <div class="hidden-xs" style=""><b>Welcome!</b>  Grab the the <a href="https://chrome.google.com/webstore/detail/usvcom/ikpfoekojmeibidkolkbbocepjfdmgol" target="_blank" >Chrome extension</a> or the bookmarklet:
                <a href="javascript:var d%3Ddocument,w%3Dwindow,e%3Dw.getSelection,k%3Dd.getSelection,x%3Dd.selection,s%3D(e%3Fe():(k)%3Fk():(x%3Fx.createRange().text:0)),f%3D%27http://beta.usv.com/posts/new%27,l%3Dd.location,e%3DencodeURIComponent,p%3D%27%3Fv%3D3%26url%3D%27%2Be(l.href) %2B%27%26title%3D%27%2Be(d.title) %2B%27%26s%3D%27%2Be(s),u%3Df%2Bp%3Btry%7Bif(!/%5E(.*%5C.)%3Ftumblr%5B%5E.%5D*%24/.test(l.host))throw(0)%3Btstbklt()%3B%7Dcatch(z)%7Ba %3Dfunction()%7Bif(!w.open(u,%27t%27,%27toolbar%3D0,resizable%3D0,status%3D1,width%3D450,height%3D430%27))l.href%3Du%3B%7D%3Bif(/Firefox/.test(navigator.userAgent))setTimeout(a,0)%3Belse a()%3B%7Dvoid(0)">Post to USV.com</a> (&larr; drag to your bookmarks bar).</div>
                
                <div class="visible-xs"><b>Welcome!</b> Get the <a href="https://play.google.com/store/apps/details?id=com.connectedio.usvmobile" target="_blank">Android app</a>.</div></div>
                </div>
            <?php endif; ?>

        <div id="content">   
        <div class="container">
        