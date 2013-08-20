<?php



//ON INIT

add_action('admin_init','wp_rss_multi_importer_start');



function wp_rss_multi_importer_start () {
	
register_setting('wp_rss_multi_importer_options', 'rss_import_items');
register_setting('wp_rss_multi_importer_categories', 'rss_import_categories');	
register_setting('wp_rss_multi_importer_item_options', 'rss_import_options');	 
register_setting('wp_rss_multi_importer_template_item', 'rss_template_item');	 
register_setting('wp_rss_multi_importer_feed_options', 'rss_feed_options');	 
register_setting('wp_rss_multi_importer_post_options', 'rss_post_options');	 
register_setting('wp_rss_multi_importer_admin_options', 'rss_admin_options');
register_setting('wp_rss_multi_importer_categories_images', 'rss_import_categories_images');	 
add_settings_section( 'wp_rss_multi_importer_main', '', 'wp_section_text', 'wprssimport' );  


}

add_action('admin_init', 'ilc_farbtastic_script');

function ilc_farbtastic_script() {
  wp_enqueue_style( 'farbtastic' );
  wp_enqueue_script( 'farbtastic' );
}



add_action('init', 'wp_rss_multi_importer_post_to_feed');

function wp_rss_multi_importer_post_to_feed(){
  $post_options = get_option('rss_post_options'); 
	if (!empty($post_options)) {
		if ($post_options['targetWindow']==0 && $post_options['active']==1){
			add_action('wp_footer','colorbox_scripts');
		}
		if ($post_options['noindex']==1){
			add_action('wp_head', 'rssmi_noindex_function');
		}
		
	}
}




function isMobile() {
    return preg_match("/(android|avantgo|blackberry|bolt|boost|cricket|docomo|fone|hiptop|mini|mobi|palm|phone|pie|tablet|up\.browser|up\.link|webos|wos)/i", $_SERVER["HTTP_USER_AGENT"]);
}

function isMobileForWordPress() {
	global $isMobileDevice;
    if(isMobile()){
       $isMobileDevice=1;
		}else{
 			$isMobileDevice=0;
		}
		return $isMobileDevice;
}

add_action('init', 'isMobileForWordPress', 1);



function startSimplePie(){
	if(! class_exists('SimplePie')){
	     		require_once(ABSPATH . WPINC . '/class-simplepie.php');
	}
	class SimplePie_RSSMI extends SimplePie {}	
	
}
add_action('init', 'startSimplePie');



add_action('admin_menu','wp_rss_multi_importer_menu');

function wp_rss_multi_importer_menu () {
add_options_page('WP RSS Multi-Importer','RSS Multi-Importer','manage_options','wp_rss_multi_importer_admin', 'wp_rss_multi_importer_display');
}




add_action( 'widgets_init', 'src_load_widgets');  //load widget

function src_load_widgets() {
register_widget('WP_Multi_Importer_Widget');
}








function wp_rss_multi_importer_display( $active_tab = '' ) {

	
		
?>
	
	<div class="wrap">
		<?php
		$wprssmi_admin_options = get_option( 'rss_admin_options' );
		if ( isset( $_GET['page'] ) && $_GET['page'] == 'wp_rss_multi_importer_admin'  && $wprssmi_admin_options['dismiss_slug'] != "true" ) {
		?>
		<div id="message" class="updated fade">
		<h3><?php _e("If you find this plugin helpful, let others know by <a target=\"_blank\" href=\"http://wordpress.org/extend/plugins/wp-rss-multi-importer/\">rating it here</a>. That way, it will help others determine whether or not they should try out the plugin. Thank you.", 'wp-rss-multi-importer')?></h3>
		<form method="post" action="options.php">		
			<?php 
			settings_fields('wp_rss_multi_importer_admin_options');
			?>
			<input type="hidden" name="rss_admin_options[dismiss_slug]" value="true">
			<input type="submit" value="<?php _e("Dismiss This Message", 'wp-rss-multi-importer')?>" name="submit">
			</form>
		
			</div>
	<?php
}
?>
		<div id="icon-themes" class="icon32"></div>
		<h2><?php  _e("WP RSS Multi-Importer Options", 'wp-rss-multi-importer')?></h2>
		<?php //settings_errors(); ?>
		
		<?php if( isset( $_GET[ 'tab' ] ) ) {
			$active_tab = $_GET[ 'tab' ];
		} else if( $active_tab == 'setting_options' ) {
				$active_tab = 'setting_options';
		} else if( $active_tab == 'category_options' ) {
			$active_tab = 'category_options';
		} else if( $active_tab == 'shortcode_parameters' ) {
			$active_tab = 'shortcode_parameters';
		} else if( $active_tab == 'template_options' ){
				$active_tab = 'template_options';
		} else if( $active_tab == 'feed_options' ){
				$active_tab = 'feed_options';
		} else if( $active_tab == 'feed_to_post_options' ){
					$active_tab = 'feed_to_post_options';
		} else if( $active_tab == 'items_list' ){
			$active_tab = 'items_list';
		} else if( $active_tab == 'posts_list' ){
			$active_tab = 'posts_list';
		} else { $active_tab = 'intro';	
			
		} // end if/else ?>
		
		<h2 class="nav-tab-wrapper">
			<a href="?page=wp_rss_multi_importer_admin&tab=intro" class="nav-tab <?php echo $active_tab == 'intro' ? 'nav-tab-active' : ''; ?>"><?php  _e("Overview", 'wp-rss-multi-importer')?></a>
			<a href="?page=wp_rss_multi_importer_admin&tab=items_list" class="nav-tab <?php echo $active_tab == 'items_list' ? 'nav-tab-active' : ''; ?>"><?php  _e("Feeds", 'wp-rss-multi-importer')?></a>
			<a href="?page=wp_rss_multi_importer_admin&tab=category_options" class="nav-tab <?php echo $active_tab == 'category_options' ? 'nav-tab-active' : ''; ?>"><?php  _e("Categories", 'wp-rss-multi-importer')?></a>
				<a href="?page=wp_rss_multi_importer_admin&tab=setting_options" class="nav-tab <?php echo $active_tab == 'setting_options' ? 'nav-tab-active' : ''; ?>"><?php  _e("Shortcode Settings", 'wp-rss-multi-importer')?></a>
				<a href="?page=wp_rss_multi_importer_admin&tab=feed_to_post_options" class="nav-tab <?php echo $active_tab == 'feed_to_post_options' ? 'nav-tab-active' : ''; ?>"><?php  _e("Feed to Post Settings", 'wp-rss-multi-importer')?></a>
			<a href="?page=wp_rss_multi_importer_admin&tab=shortcode_parameters" class="nav-tab <?php echo $active_tab == 'shortcode_parameters' ? 'nav-tab-active' : ''; ?>"><?php  _e("Shortcode Parameters", 'wp-rss-multi-importer')?></a>
				<a href="?page=wp_rss_multi_importer_admin&tab=template_options" class="nav-tab <?php echo $active_tab == 'template_options' ? 'nav-tab-active' : ''; ?>"><?php  _e("Template Options", 'wp-rss-multi-importer')?></a>
				<a href="?page=wp_rss_multi_importer_admin&tab=posts_list" class="nav-tab <?php echo $active_tab == 'posts_list' ? 'nav-tab-active' : ''; ?>"><?php  _e("Manage Posts", 'wp-rss-multi-importer')?></a>
				<a href="?page=wp_rss_multi_importer_admin&tab=feed_options" class="nav-tab <?php echo $active_tab == 'feed_options' ? 'nav-tab-active' : ''; ?>"><?php  _e("Export RSS", 'wp-rss-multi-importer')?></a>
				
				
		</h2>

			<?php
			
				if( $active_tab == 'items_list' ) {
						
			wp_rss_multi_importer_items_page();
			
		} else if ( $active_tab == 'setting_options' ) {

				wp_rss_multi_importer_options_page();
			
		} else if ( $active_tab == 'category_options' ) {
			
			wp_rss_multi_importer_category_page();
		wp_rss_multi_importer_category_images_page();
		
			
		} else if ( $active_tab == 'shortcode_parameters' ) {
			
			wp_rss_multi_importer_style_tags();
			
		} else if ( $active_tab == 'template_options' ) {
				
			wp_rss_multi_importer_template_page();	
			
		} else if ( $active_tab == 'feed_options' ) {
				
			wp_rss_multi_importer_feed_page();	
			
		} else if ( $active_tab == 'feed_to_post_options' ) {
				
			wp_rss_multi_importer_post_page();
		
		} else if ( $active_tab == 'posts_list' ) {
			
			 	global $myListTable;
				my_add_menu_items();
				add_options();
				my_render_list_page();
				$myListTable->admin_header(); 
				
				} else {
			wp_rss_multi_importer_intro_page();
					
				
				} // end if/else  	
				
				
			
			?>
	</div>
	
<?php
} 




?>