<?php

// Only load scripts and CSS if we are on this plugin's options page (admin)

if ( isset( $_GET['page'] ) && $_GET['page'] == 'wp_rss_multi_importer_admin' ) {

    add_action( 'init', 'wprssmi_register_scripts' );

   	add_action( 'admin_print_styles', 'wprssmi_header' );

	add_action('wp_print_scripts', 'wprssmi_ajax_load_scripts');
	

}



function rssmi_noindex_function()
{
	global $wp_query;
	$postID=$wp_query->post->ID;
	$myLink = get_post_meta($postID, 'rssmi_source_link' , true);
		if (!empty($myLink) && !is_front_page()  ){
echo '<meta name="robots" content="noindex, nofollow">';
}
}





/**
    * Load scripts for admin, including check for version since new method (.on) used available in jquery 1.7.1
    */


function wprssmi_register_scripts() {

 global $wp_version;

if ( version_compare($wp_version, "3.3.1", ">" ) ) {  
 	wp_enqueue_script( 'jquery' );
} else {	
	wp_deregister_script( 'jquery' );
    wp_register_script( 'jquery', 'http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js');
    wp_enqueue_script( 'jquery' );	
}
  wp_enqueue_script( 'add-remove', plugins_url('scripts/add-remove.js',dirname(__FILE__)),array('jquery'));
  wp_localize_script( 'add-remove', 'add_remove_parms', wprssmi_localize_vars());
 //wp_enqueue_script( 'bpopup', plugins_url('scripts/jquery.bpopup-0.7.0.min.js',dirname(__FILE__)),array('jquery'));  //adds pop-up ability

}



function wprssmi_localize_vars() {
    return array(
        'delcat' => __('Delete this category', 'wp-rss-multi-importer'),
		'delfeed' => __('Delete this feed', 'wp-rss-multi-importer'),
		'intcheck' => __('This must be an integer', 'wp-rss-multi-importer'),
		'urlcheck' => __('Bad URL- feeds start with http', 'wp-rss-multi-importer')
    );
} 






function wprssmi_ajax_load_scripts() {
	wp_enqueue_script( 'ajax-template', plugins_url('scripts/ajax.js',dirname(__FILE__)),array('jquery'));
	wp_localize_script( 'ajax-template', 'the_ajax_script', array( 'ajaxurl' => admin_url( 'admin-ajax.php' ) ) );	

}






 
   
  add_action( 'wp_enqueue_scripts', 'wprssmi_frontend_scripts' );
   
   function wprssmi_frontend_scripts() {
		wp_enqueue_script( 'jquery' );  
   }



add_action( 'wp_enqueue_scripts', 'wprssmi_tempate_header' );

function wprssmi_tempate_header(){

		wp_enqueue_style( 'wprssmi_template_styles', plugins_url( 'templates/templates.css', dirname(__FILE__)) );
	
}




/**
 * Include CSS in plugin page header
 */


    function wprssmi_header() {        
        wp_enqueue_style( 'wprssmi_styles', plugins_url( 'css/styles.css', dirname(__FILE__)) );

    }



/**
    * Include Colorbox-related script and CSS in WordPress in footer
    */



function footer_scripts(){
	wp_enqueue_style( 'frontend', plugins_url( 'css/frontend.css', dirname(__FILE__)) );
	wp_enqueue_script( 'showexcerpt', plugins_url('scripts/show-excerpt.js', dirname(__FILE__)) );  	
}

function colorbox_scripts(){
	wp_enqueue_style( 'wprssmi_colorbox', plugins_url( 'css/colorbox.css', dirname(__FILE__)) );
    wp_enqueue_script( 'jquery.colorbox-min', plugins_url( 'scripts/jquery.colorbox-min.js', dirname(__FILE__)) );
 wp_enqueue_script( 'wprssmi_detect_mobile', plugins_url( 'scripts/detect-mobile.js', dirname(__FILE__)) );
	//echo "<script type='text/javascript'>jQuery(document).ready(function(){ jQuery('a.colorbox').colorbox({iframe:true, width:'80%', height:'80%'})});</script>";	
	echo "<script type='text/javascript'>jQuery(document).ready(function(){ jQuery('a.colorbox').colorbox({iframe:true, width:'80%', height:'80%'});jQuery('a.rssmi_youtube').colorbox({iframe:true, innerWidth:425, innerHeight:344});jQuery('a.rssmi_vimeo').colorbox({iframe:true, innerWidth:500, innerHeight:409})});</script>";	
	
}









function widget_footer_scripts(){
	wp_enqueue_style( 'newstickercss', plugins_url( 'css/newsticker.css', dirname(__FILE__)) );
	wp_enqueue_script( 'newsticker', plugins_url( 'scripts/newsticker.js', dirname(__FILE__)) );  	
	echo "<script type='text/javascript'>jQuery(document).ready(function () {jQuery('#newsticker').vscroller();});</script>";  
}


/*  Template functions */



function vertical_scroll_footer_scripts(){
		wp_enqueue_script( 'vertical_scroll', plugins_url( 'scripts/jquery.vticker.js', dirname(__FILE__)) );  
	
}



	function smooth_scroll_scripts(){
		wp_enqueue_script( 'jquery_custom_ui', plugins_url( 'scripts/scroll/jquery-ui-1.8.23.custom.js', dirname(__FILE__)) , array('jquery'));  	
			wp_enqueue_script( 'mousewheel', plugins_url( 'scripts/scroll/jquery.mousewheel.min.js', dirname(__FILE__)) , array('jquery'));  
				wp_enqueue_script( 'kinetic', plugins_url( 'scripts/scroll/jquery.kinetic.js', dirname(__FILE__)) , array('jquery'));  	
					wp_enqueue_script( 'smoothscroll', plugins_url( 'scripts/scroll/jquery.smoothdivscroll-1.3-min.js', dirname(__FILE__)) , array('jquery'));

 }


function cluetip_scripts(){
		wp_enqueue_script( 'cluetip', plugins_url( 'scripts/jquery.cluetip.js', dirname(__FILE__)) , array('jquery'));  	
}



?>