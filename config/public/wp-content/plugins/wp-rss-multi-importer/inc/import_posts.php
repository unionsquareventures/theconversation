<?php
$feedID = isset( $_GET[ 'rssmi_feedID' ] ) ? $_GET['rssmi_feedID'] : NULL;
$catID = isset( $_GET[ 'rssmi_catID' ] ) ? $_GET['rssmi_catID'] :  NULL;
if (!IS_NULL($feedID) || !IS_NULL($catID) ){	
	$post_options = get_option('rss_post_options');
	if($post_options['active']==1){
		if (!IS_NULL($feedID)){
			$result=wp_rss_multi_importer_post($feedID);  /// Used for external cron jobs	
	}else{
			$result=wp_rss_multi_importer_post($catID);	
	}
	
		if ($result==True){
			echo "success";
		}
			die();
	}
}

function deleteArticles(){

	
	global $wpdb;

  $mypostids = $wpdb->get_results("select * from $wpdb->postmeta where meta_key LIKE '%rssmi_source_link%");


    foreach( $mypostids as $mypost ) {
	
	//	delete_post_meta($mypost->ID, 'rssmi_source_link');
 

    }
}


function setFeaturedImage($post_id,$url,$featuredImageTitle){  
	
    // Download file to temp location and setup a fake $_FILE handler
    // with a new name based on the post_id
    $tmp_name = download_url( $url );
//								echo $tmp_name;
    $file_array['name'] = $post_id. '-thumb.jpg';  // new filename based on slug
    $file_array['tmp_name'] = $tmp_name;



    // If error storing temporarily, unlink
    if ( is_wp_error( $tmp_name ) ) {
        @unlink($file_array['tmp_name']);
        $file_array['tmp_name'] = '';
    }

    // do validation and storage .  Make a description based on the Post_ID
    $attachment_id = media_handle_sideload( $file_array, $post_id, 'Thumbnail for ' .$post_id);



    // If error storing permanently, unlink
    if ( is_wp_error($attachment_id) ) {
	$error_string = $attachment_id->get_error_message();
        @unlink($file_array['tmp_name']);
        return;
    }


    // Set as the post attachment
   $post_result= add_post_meta( $post_id, '_thumbnail_id', $attachment_id, true );

//					echo $post_result);
		
}






function rssmi_import_feed_post() {
	
	$post_options = get_option('rss_post_options');
	
	if($post_options['active']==1){
		wp_rss_multi_importer_post();
	}
}




add_action('wp_ajax_fetch_now', 'fetch_rss_callback');

function fetch_rss_callback() {

	$post_options = get_option('rss_post_options');

		if($post_options['active']==1){

			wp_rss_multi_importer_post();
	        echo '<h3>The most recent feeds have been put into posts.</h3>';

		}else{
			
	 		echo '<h3>Nothing was done because you have not activated this service.</h3>';
}

	die(); 
}



function rssmi_delete_feed_post_admin() {
rssmi_delete_posts_admin();
}



add_action('wp_ajax_fetch_delete', 'fetch_rss_callback_delete');

function fetch_rss_callback_delete() {

			rssmi_delete_feed_post_admin();


}






function filter_id_callback2($val) {
    if ($val != null && $val !=99999){
	return true;
}
}

function filter_id_callback($val) {
	foreach($val as $thisval){
    if ($thisval != null){
	return true;
	}
}
}




function get_values_for_id_keys($mapping, $keys) {
    foreach($keys as $key) {
        $output_arr[] = $mapping[$key];
    }
    return $output_arr;
}


function strip_qs_var($sourcestr,$url,$key){
	if (strpos($url,$sourcestr)>0){
		return preg_replace( '/('.$key.'=.*?)&/', '', $url );
	}else{
		return $url;
	}		
}

$post_filter_options = get_option('rss_post_options');   // make title of post on listing page clickable
if($post_filter_options['titleFilter']==1){
	add_filter( 'the_title', 'ta_modified_post_title');  
}else{
	remove_filter( 'the_title', 'ta_modified_post_title' );  
}



function ta_modified_post_title ($title) {
	$post_options = get_option('rss_post_options'); 
	$targetWindow=$post_options['targetWindow']; 
	if($targetWindow==0){
		$openWindow='class="colorbox"';
	}elseif ($targetWindow==1){
		$openWindow='target=_self';		
	}else{
		$openWindow='target=_blank ';	
	}
	
  if ( in_the_loop() && !is_page() ) {
	global $wp_query;
	$postID=$wp_query->post->ID;
	$myLink = get_post_meta($postID, 'rssmi_source_link' , true);
		if (!empty($myLink)){
			$myTitle=$wp_query->post->post_title;
			$myLinkTitle='<a href='.$myLink.' '.$openWindow.'>'.$myTitle.'</a>';  // change how the link opens here
		return $myLinkTitle;					
			}
  }
  return $title;
}



function isAllCat(){
$post_options = get_option('rss_post_options'); 
$catSize=count($post_options['categoryid']);

	for ( $l=1; $l<=$catSize; $l++ ){

		if($post_options['categoryid']['plugcatid'][$l]==0){
			
			$allCats[]= $post_options['categoryid']['wpcatid'][$l];
		}
}
return $allCats;
}




function getAllWPCats(){
	$category_ids = get_all_category_ids();
	foreach($category_ids as $cat_id) {
		if ($cat_id==1) continue;
 		$getAllWPCats[]=$cat_id;
	}
	return $getAllWPCats;
}






function wp_rss_multi_importer_post($feedID=NULL,$catID=NULL){
	
 $postMsg = FALSE; 


	
require_once(ABSPATH . "wp-admin" . '/includes/media.php');
require_once(ABSPATH . "wp-admin" . '/includes/file.php');
require_once(ABSPATH . "wp-admin" . '/includes/image.php');

if(!function_exists("wprssmi_hourly_feed")) {
function wprssmi_hourly_feed() { return 0; }  // no caching of RSS feed
}
add_filter( 'wp_feed_cache_transient_lifetime', 'wprssmi_hourly_feed' );


  
   	$options = get_option('rss_import_options','option not found');
	$option_items = get_option('rss_import_items','option not found');
	$post_options = get_option('rss_post_options', 'option not found');
	$category_tags=get_option('rss_import_categories_images', 'option not found');
	
	global $fopenIsSet;
	$fopenIsSet = ini_get('allow_url_fopen');

	if ($option_items==false) return "You need to set up the WP RSS Multi Importer Plugin before any results will show here.  Just go into the <a href='/wp-admin/options-general.php?page=wp_rss_multi_importer_admin'>settings panel</a> and put in some RSS feeds";


if(!empty($option_items)){
$cat_array = preg_grep("^feed_cat_^", array_keys($option_items));

	if (count($cat_array)==0) {  // for backward compatibility
		$noExistCat=1;
	}else{
		$noExistCat=0;	
	}

}





if(!IS_NULL($feedID)){
	$feedIDArray=explode(",",$feedID);
}
 
   if(!empty($option_items)){

	
//GET PARAMETERS  
$size = count($option_items);
$sortDir=0;  // 1 is ascending
$maxperPage=$options['maxperPage'];
global $setFeaturedImage;
$setFeaturedImage=$post_options['setFeaturedImage'];
$addSource=$post_options['addSource'];
$sourceAnchorText=$post_options['sourceAnchorText'];
$maxposts=$post_options['maxfeed'];
$post_status=$post_options['post_status'];
$addAuthor=$post_options['addAuthor'];
$bloguserid=$post_options['bloguserid'];
$post_format=$post_options['post_format'];
$postTags=$post_options['postTags'];
global $RSSdefaultImage;
$RSSdefaultImage=$post_options['RSSdefaultImage'];   // 0- process normally, 1=use default for category, 2=replace when no image available
$serverTimezone=$post_options['timezone'];
$autoDelete=$post_options['autoDelete'];
$sourceWords=$post_options['sourceWords'];
$readMore=$post_options['readmore'];
$includeExcerpt=$post_options['includeExcerpt'];
global $morestyle;
$morestyle=' ...read more';
$sourceWords_Label=$post_options['sourceWords_Label'];

if (!is_null($readMore) && $readMore!='') {$morestyle=$readMore;} 


switch ($sourceWords) {
    case 1:
        $sourceLable='Source';
        break;
    case 2:
        $sourceLable='Via';
        break;
    case 3:
        $sourceLable='Read more here';
        break;
	case 4:
	    $sourceLable='From';
	    break;
	case 5:
		$sourceLable=$sourceWords_Label;
		break;
    default:
       	$sourceLable='Source';
}

if (isset($serverTimezone) && $serverTimezone!=''){  //set time zone
	date_default_timezone_set($serverTimezone);
	$rightNow=date("Y-m-d H:i:s", time());
}else{
	$rightNow=date("Y-m-d H:i:s", time());
}





if ($post_options['categoryid']['wpcatid'][1]!==NULL){
$wpcatids=array_filter($post_options['categoryid']['wpcatid'],'filter_id_callback'); //array of post blog categories that have been entered
}




if (!empty($wpcatids)){
	$catArray = get_values_for_id_keys($post_options['categoryid']['plugcatid'], array_keys($wpcatids));  //array of plugin categories that have an association with post blog categories
	$catArray=array_diff($catArray, array(''));
	
	


}else{
	$catArray=array(0);
	
}






if(!IS_NULL($catID)){
		$catArray=array($catID);  //  change to category ID if using external CRON
}



$targetWindow=$post_options['targetWindow'];  // 0=LB, 1=same, 2=new

if(empty($options['sourcename'])){
	$attribution='';
}else{
	$attribution=$options['sourcename'].': ';
}
global $ftp;
$ftp=1;  //identify pass to excerpt_functions comes from feed to post
global $anyimage;  // to identify any image in description 
$anyimage=1;

global $maximgwidth;
$maximgwidth=$post_options['maximgwidth'];;
$descNum=$post_options['descnum'];
$stripAll=$post_options['stripAll'];
$stripSome=$post_options['stripSome'];
$maxperfetch=$post_options['maxperfetch'];
$showsocial=$post_options['showsocial'];
$overridedate=$post_options['overridedate'];
$commentStatus=$post_options['commentstatus'];


if ($commentStatus=='1'){
	$comment_status='closed';
}else{
	$comment_status='open';	
}


$adjustImageSize=1;
$noFollow=0;
$floatType=1;

if ($floatType=='1'){
	$float="left";
}else{
	$float="none";	
}




   for ($i=1;$i<=$size;$i=$i+1){

	//  condition here that id number is here

   			$key =key($option_items);
				if ( !strpos( $key, '_' ) > 0 ) continue; //this makes sure only feeds are included here...everything else are options
				
   			$rssName= $option_items[$key];

			$rssID=str_replace('feed_name_','',$key);  //get feed ID number

   			next($option_items);
   			
   			$key =key($option_items);
   			
   			$rssURL=$option_items[$key];



  	next($option_items);
	$key =key($option_items);
	

$rssCatID=$option_items[$key]; 


if (((!in_array(0, $catArray )  && in_array($option_items[$key], $catArray ))) || in_array(0, $catArray )  || $noExistCat==1 || !EMPTY($feedIDArray)) {  //makes sure only desired categories are included


	if (!EMPTY($feedIDArray)){	//only pick up specific feed arrary if indicated in querystring
		if (!in_array($rssID, $feedIDArray )) {
			if (count($cat_array)>0) { // for backward compatibility
		  		next($option_items); //skip feed category
			}
			continue;
	}
}



	$myfeeds[] = array("FeedName"=>$rssName,"FeedURL"=>$rssURL,"FeedCatID"=>$rssCatID); //with Feed Category ID


}
   
$cat_array = preg_grep("^feed_cat_^", array_keys($option_items));  // for backward compatibility

	if (count($cat_array)>0) {

  next($option_items); //skip feed category
}

   }

  if ($maxposts=="") return "One more step...go into the the <a href='/wp-admin/options-general.php?page=wp_rss_multi_importer_admin&tab=setting_options'>Settings Panel and choose Options.</a>";  // check to confirm they set options

if (empty($myfeeds)){
	
	return "You've either entered a category ID that doesn't exist or have no feeds configured for this category.  Edit the shortcode on this page with a category ID that exists, or <a href=".$cat_options_url.">go here and and get an ID</a> that does exist in your admin panel.";
	exit;
}





 
 foreach($myfeeds as $feeditem){


	$url=(string)($feeditem["FeedURL"]);

	
	while ( stristr($url, 'http') != $url )
		$url = substr($url, 1);


				$feed = fetch_feed($url);

	
	

	if (is_wp_error( $feed ) ) {
		
		if ($size<4){
			return "You have one feed and it's not valid.  This is likely a problem with the source of the RSS feed.  Contact our support forum for help.";
			exit;

		}else{
	//echo $feed->get_error_message();	
		continue;
		}
	}

	$maxfeed= $feed->get_item_quantity(0);  
	
	
	if ($feedAuthor = $feed->get_author())
	{
		$feedAuthor=$feed->get_author()->get_name();
	}




	//SORT DEPENDING ON SETTINGS

		if($sortDir==1){

			for ($i=$maxfeed-1;$i>=$maxfeed-$maxposts;$i--){
				$item = $feed->get_item($i);
				 if (empty($item))	continue;

				if(include_post($feeditem["FeedCatID"],$item->get_content(),$item->get_title())==0) continue;   // FILTER 


							if ($enclosure = $item->get_enclosure()){
								if(!IS_NULL($item->get_enclosure()->get_thumbnail())){			
									$mediaImage=$item->get_enclosure()->get_thumbnail();
								}else if (!IS_NULL($item->get_enclosure()->get_link())){
									$mediaImage=$item->get_enclosure()->get_link();	
								}
							}


							if ($itemAuthor = $item->get_author())
							{
								$itemAuthor=$item->get_author()->get_name();
							}else if (!IS_NULL($feedAuthor)){
								$itemAuthor=$feedAuthor;

							}



				$myarray[] = array("mystrdate"=>strtotime($item->get_date()),"mytitle"=>$item->get_title(),"mylink"=>$item->get_permalink(),"myGroup"=>$feeditem["FeedName"],"mydesc"=>$item->get_content(),"myimage"=>$mediaImage,"mycatid"=>$feeditem["FeedCatID"],"myAuthor"=>$itemAuthor,"feedURL"=>$feeditem["FeedURL"]);

							unset($mediaImage);
							unset($itemAuthor);

				}

			}else{	

			for ($i=0;$i<=$maxposts-1;$i++){
					$item = $feed->get_item($i);
					if (empty($item))	continue;
					
					if(include_post($feeditem["FeedCatID"],$item->get_content(),$item->get_title())==0) continue;   // FILTER 


				if ($enclosure = $item->get_enclosure()){

					if(!IS_NULL($item->get_enclosure()->get_thumbnail())){			
						$mediaImage=$item->get_enclosure()->get_thumbnail();
					}else if (!IS_NULL($item->get_enclosure()->get_link())){
						$mediaImage=$item->get_enclosure()->get_link();	
					}	
				}


				if ($itemAuthor = $item->get_author())
				{
					$itemAuthor=$item->get_author()->get_name();
				}else if (!IS_NULL($feedAuthor)){
					$itemAuthor=$feedAuthor;

				}



				$myarray[] = array("mystrdate"=>strtotime($item->get_date()),"mytitle"=>$item->get_title(),"mylink"=>$item->get_permalink(),"myGroup"=>$feeditem["FeedName"],"mydesc"=>$item->get_content(),"myimage"=>$mediaImage,"mycatid"=>$feeditem["FeedCatID"],"myAuthor"=>$itemAuthor,"feedURL"=>$feeditem["FeedURL"]);


							unset($mediaImage);
							unset($itemAuthor);
					}	
			}


		}





//  CHECK $myarray BEFORE DOING ANYTHING ELSE //

if ($dumpthis==1){
	var_dump($myarray);
}
if (!isset($myarray) || empty($myarray)){
	
	return "There is a problem with the feeds you entered.  Go to our <a href='http://www.allenweiss.com/wp_plugin'>support page</a> and we'll help you diagnose the problem.";
		exit;
}

//$myarrary sorted by mystrdate

foreach ($myarray as $key => $row) {
    $dates[$key]  = $row["mystrdate"]; 
}



//SORT, DEPENDING ON SETTINGS

if($sortDir==1){
	array_multisort($dates, SORT_ASC, $myarray);
}else{
	array_multisort($dates, SORT_DESC, $myarray);		
}



if($targetWindow==0){
	$openWindow='class="colorbox"';
}elseif ($targetWindow==1){
	$openWindow='target=_self';		
}else{
	$openWindow='target=_blank ';	
}

	$total=0;



global $wpdb; // get all links that have been previously processed

$wpdb->show_errors = true;



foreach($myarray as $items) {
	
	$total = $total +1;
	if ($total>$maxperfetch) break;
	$thisLink=trim($items["mylink"]);
//	echo $thisLink.'<br>';
	
	
// VIDEO CHECK
if ($targetWindow==0){
	$getVideoArray=rssmi_video($items["mylink"]);
	$openWindow=$getVideoArray[1];
	$items["mylink"]=$getVideoArray[0];
}

	
	
	
	
	
	
	
	
	$thisLink = strip_qs_var('bing.com',$thisLink,'tid');  // clean time based links from Bing
	

	$thisLink=mysql_real_escape_string($thisLink);



			$wpdb->flush();
			$mypostids = $wpdb->get_results("select post_id from $wpdb->postmeta where meta_key = 'rssmi_source_link' and meta_value like '%".$thisLink."%'");
		
			$myposttitle=$wpdb->get_results("select post_title from $wpdb->posts where post_title like '%".mysql_real_escape_string(trim($items["mytitle"]))."%'");
		
		if ((empty( $mypostids ) && $mypostids !== false) && empty($myposttitle)){ 
		
			$thisContent='';
  			$post = array();  

  			$post['post_status'] = $post_status;



	if ($overridedate==1){
		$post['post_date'] = $rightNow;  	
	}else{
  		$post['post_date'] = date('Y-m-d H:i:s',$items['mystrdate']);
	}




	$post['post_title'] = trim($items["mytitle"]);



	$authorPrep="By ";

		if(!empty($items["myAuthor"]) && $addAuthor==1){
		 	$thisContent .=  '<span style="font-style:italic; font-size:16px;">'.$authorPrep.' <a '.$openWindow.' href='.$items["mylink"].' '.($noFollow==1 ? 'rel=nofollow':'').'">'.$items["myAuthor"].'</a></span>  ';  
			}

	
	$thisExcerpt = showexcerpt($items["mydesc"],$descNum,$openWindow,$stripAll,$items["mylink"],$adjustImageSize,$float,$noFollow,$items["myimage"],$items["mycatid"],$stripSome);
	

	$thisContent .= $thisExcerpt;

	if ($addSource==1){
		
		
		switch ($sourceAnchorText) {
		    case 1:
		        $anchorText=$items["myGroup"];
		        break;
		    case 2:
		        $anchorText=$items["mytitle"];
		        break;
		    case 3:
		        $anchorText=$items["mylink"];
		        break;
		    default:
		        $anchorText=$items["myGroup"];
		}	
		
		$thisContent .= ' <p>'.$sourceLable.': <a href='.$items["mylink"].'  '.$openWindow.'  title="'.$items["mytitle"].'">'.$anchorText.'</a></p>';
	}


	
	if ($showsocial==1){
	$thisContent .= '<span style="margin-left:10px;"><a href="http://www.facebook.com/sharer/sharer.php?u='.$items["mylink"].'"><img src="'.WP_RSS_MULTI_IMAGES.'facebook.png"/></a>&nbsp;&nbsp;<a href="http://twitter.com/intent/tweet?text='.rawurlencode($items["mytitle"]).'%20'.$items["mylink"].'"><img src="'.WP_RSS_MULTI_IMAGES.'twitter.png"/></a>&nbsp;&nbsp;<a href="http://plus.google.com/share?url='.rawurlencode($items["mylink"]).'"><img src="'.WP_RSS_MULTI_IMAGES.'gplus.png"/></a></span>';
	}
	
  	$post['post_content'] = $thisContent;

	if ($includeExcerpt==1){
		$post['post_excerpt'] = $thisExcerpt;
	}

	$mycatid=$items["mycatid"];
	
	
	$blogcatid=array();
	
	if (!empty($post_options['categoryid'])){
		$catkey=array_search($mycatid, $post_options['categoryid']['plugcatid']);
		$blogcatid=$post_options['categoryid']['wpcatid'][$catkey];
	}else{
		$blogcatid=0;	
	}
	
	
	if ($post_options['categoryid']['plugcatid'][1]=='0'){   //this gets all the wp categories indicated when All is chosen in the first position
		$allblogcatid=$post_options['categoryid']['wpcatid'][1];
			if (is_array($blogcatid)){
				$blogcatid=array_merge ($blogcatid,$allblogcatid);
				$blogcatid = array_unique($blogcatid);
			}else{
				$blogcatid=$allblogcatid;
			}
	}



	$post['post_category'] =$blogcatid;
	
	
		if (is_null($bloguserid) || empty($bloguserid)){$bloguserid=1;}  //check that userid isn't empty else give it admin status
	
	
	$post['post_author'] =$bloguserid;
	

	
	$post['comment_status'] = $comment_status;
	
	if (!empty($category_tags[$mycatid]['tags'])) {	
		$postTags=$category_tags[$mycatid]['tags'];
	}

	if($postTags!=''){
		$post['tags_input'] =$postTags;
	}
	


 	$post_id = wp_insert_post($post);
	set_post_format( $post_id , $post_format);
	
	if(add_post_meta($post_id, 'rssmi_source_link', $thisLink)!=false){
	
	

	if ($setFeaturedImage==1 || $setFeaturedImage==2){
		global $featuredImage;
			if (isset($featuredImage)){
				$featuredImageTitle=trim($items["mytitle"]);	
				setFeaturedImage($post_id,$featuredImage,$featuredImageTitle);
				unset($featuredImage);
				}
			}
			
	}else{
		
	wp_delete_post($post_id, true);
	unset($post);
	continue;	
		
		
	}

	unset($post);
}

$postMsg = TRUE; 

}

}

if ($autoDelete==1){
	rssmi_delete_posts();
}

return $postMsg;

  }

?>