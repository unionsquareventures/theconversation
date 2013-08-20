<?php


add_action('wp', 'wp_rss_multi_activation');


function wp_rss_multi_activation() {
	
	if ( !wp_next_scheduled( 'wp_rss_multi_event' ) ) {
		wp_schedule_event( time(), 'hourly', 'wp_rss_multi_event');
	}
	
	$post_schedule_options = get_option('rss_post_options');
		if(	$post_schedule_options['active']==1){
			
			if (isset($post_schedule_options['fetch_schedule'])){
					$periodnumber=$post_schedule_options['fetch_schedule'];
				}else{
			   		$periodnumber = 1;
			}

		switch ($periodnumber) {
			case 1: $display_period='hourly'; break;
			case 2: $display_period='tenminutes'; break;
			case 3: $display_period='fifteenminutes'; break;
			case 4: $display_period='twentyminutes'; break;
			case 5: $display_period='thirtyminutes'; break;
			case 12: $display_period='twicedaily'; break;
			case 24: $display_period='daily'; break;
			case 168: $display_period='weekly'; break;
		}	
					
							
	$cronStartTime=time()+60;
	
	if( !wp_next_scheduled( 'wp_rss_multi_event_feedtopost' ) ){
	     wp_schedule_event( $cronStartTime, $display_period, 'wp_rss_multi_event_feedtopost' );
	  }	
	
	}else{
		wp_rss_multi_deactivation();
	}
}

add_action('wp_rss_multi_event', 'wp_rss_multi_cron');

add_action('wp_rss_multi_event_feedtopost', 'wp_rss_multi_cron_feedtopost');

add_filter( 'cron_schedules', 'cron_add_wprssmi_schedule' );

function cron_add_wprssmi_schedule( $schedules ) {  //add a weekly schedule to cron
	
	$period=168*3600;
	$schedules['weekly'] = array(
		'interval' => $period,
		'display' => __( 'Once Weekly' )
	);
	return $schedules;	
}



add_filter( 'cron_schedules', 'cron_add_wprssmi_schedule_10' );

function cron_add_wprssmi_schedule_10( $schedules ) {  //add a 10 min schedule to cron
	
	$period=600;
	$schedules['tenminutes'] = array(
		'interval' => $period,
		'display' => __( 'Once Every 10 Minutes' )
	);
	return $schedules;	
}


add_filter( 'cron_schedules', 'cron_add_wprssmi_schedule_15' );

function cron_add_wprssmi_schedule_15( $schedules ) {  //add a 15 min schedule to cron
	
	$period=900;
	$schedules['fifteenminutes'] = array(
		'interval' => $period,
		'display' => __( 'Once Every 15 Minutes' )
	);
	return $schedules;	
}


add_filter( 'cron_schedules', 'cron_add_wprssmi_schedule_20' );

function cron_add_wprssmi_schedule_20( $schedules ) {  //add a 20 min schedule to cron
	
	$period=1200;
	$schedules['twentyminutes'] = array(
		'interval' => $period,
		'display' => __( 'Once Every 20 Minutes' )
	);
	return $schedules;	
}


add_filter( 'cron_schedules', 'cron_add_wprssmi_schedule_30' );

function cron_add_wprssmi_schedule_30( $schedules ) {  //add a 30 min schedule to cron
	
	$period=1800;
	$schedules['thirtyminutes'] = array(
		'interval' => $period,
		'display' => __( 'Once Every 30 Minutes' )
	);
	return $schedules;	
}







function wp_rss_multi_cron() {
	find_db_transients();
}


function wp_rss_multi_cron_feedtopost() {
	rssmi_import_feed_post();

}



function find_db_transients() {

    global $wpdb;

    $expired = $wpdb->get_col( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE '_transient_wprssmi_%';" );
	if ( $expired ) {
    	foreach( $expired as $transient ) {

        	$key = str_replace('_transient_wprssmi_', '', $transient);
			wp_rss_multi_importer_shortcode(array('category'=>$key));

    	}
	}
}


register_deactivation_hook(__FILE__, 'wp_rss_multi_deactivation');

function wp_rss_multi_deactivation() {
	wp_clear_scheduled_hook('wp_rss_multi_event_feedtopost');
}


?>