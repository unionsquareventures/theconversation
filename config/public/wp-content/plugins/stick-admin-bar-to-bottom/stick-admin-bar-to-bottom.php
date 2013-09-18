<?php
/*
Plugin Name: Stick Admin Bar To Bottom
Description: Annoyed by the new Admin Bar that is covering the top 28 pixels of your website, but you don't want it completely gone? This plugin sticks the Admin Bar to the bottom of your screen!
Author: Coen Jacobs
Version: 1.2
Author URI: http://coenjacobs.me
*/

function stick_admin_bar_to_bottom_css() {
	$version = get_bloginfo( 'version' );

	if ( version_compare( $version, '3.3', '<' ) ) {
		$css_file = 'wordpress-3-1.css';
	} else {
		$css_file = 'wordpress-3-3.css';
	}
	wp_enqueue_style( 'stick-admin-bar-to-bottom', plugins_url( 'css/' . $css_file, __FILE__ ) );
}

add_action( 'admin_init', 'stick_admin_bar_to_bottom_css' );
add_action( 'wp_enqueue_scripts', 'stick_admin_bar_to_bottom_css' );

?>
