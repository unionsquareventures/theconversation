<?php
// If uninstall not called from WordPress exit
if( !defined( 'WP_UNINSTALL_PLUGIN' ) )
exit ();
// Delete option from options table
if (is_multisite()) {
    global $wpdb;
    $blogs = $wpdb->get_results("SELECT blog_id FROM {$wpdb->blogs}", ARRAY_A);
    if ($blogs) {
        foreach($blogs as $blog) {
            switch_to_blog($blog['blog_id']);
			$post_options_uninstall = get_option('rss_post_options');
			if ($post_options_uninstall['plugindelete']==1){
				rssmi_uninstall_delete_posts_admin();
			}
            delete_option('rss_import_items');
			delete_option('rss_import_options');
            delete_option('rss_import_categories');
			delete_option('rss_template_item');
			delete_option('rss_admin_options');
			delete_option('rss_feed_options');
			delete_option('rss_post_options');
			delete_option('rss_import_categories_images');
			$allposts = get_posts('numberposts=-1&post_type=post&post_status=any');
			foreach( $allposts as $postinfo) {
			    delete_post_meta($postinfo->ID, 'rssmi_source_link');
			    delete_post_meta($postinfo->ID, 'rssmi_source_protect');
			  }
        }
        restore_current_blog();
    }
} else {
	$post_options_uninstall = get_option('rss_post_options');
	if ($post_options_uninstall['plugindelete']==1){
		rssmi_uninstall_delete_posts_admin();
	}
    delete_option('rss_import_items');
    delete_option('rss_import_categories');
	delete_option('rss_template_item');
	delete_option('rss_import_options');
	delete_option('rss_admin_options');
	delete_option('rss_feed_options');
	delete_option('rss_post_options');
	delete_option('rss_import_categories_images');
	
	$allposts = get_posts('numberposts=-1&post_type=post&post_status=any');
	foreach( $allposts as $postinfo) {
	    delete_post_meta($postinfo->ID, 'rssmi_source_link');
	    delete_post_meta($postinfo->ID, 'rssmi_source_protect');
	  }
	
}
//
function rssmi_uninstall_delete_attachment($id_ID){ // DELETE ATTACHMENTS CREATED BY THIS PLUGIN
	$args = array( 'post_type' => 'attachment', 'numberposts' => -1, 'post_status' =>'any', 'post_parent' => $id_ID ); 
	$attachments = get_posts($args);			
	if ($attachments) {
		foreach ( $attachments as $attachment ) {
			 wp_delete_attachment($attachment->ID,true);
		}
	}
}

function rssmi_uninstall_delete_posts_admin(){  // DELETE BLOG POSTS CREATED BY PLUGIN
	
	global $wpdb;
	$expiration=-1;
	$query = "SELECT ID FROM $wpdb->posts WHERE post_status = 'publish' AND post_type = 'post' AND DATEDIFF(NOW(), `post_date`) > ".$expiration;
	$ids = $wpdb->get_results($query);
	
	foreach ($ids as $id){
		$mypostids = $wpdb->get_results("SELECT * FROM $wpdb->postmeta WHERE meta_key = 'rssmi_source_link' AND post_id = ".$id->ID);
		if (!empty($mypostids)){
			rssmi_uninstall_delete_attachment($id->ID);
			wp_delete_post($id->ID, true);
		}
	}
	
}


?>