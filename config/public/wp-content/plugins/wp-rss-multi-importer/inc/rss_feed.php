<?php




//  RSS FEED FUNCTIONS

function rssmi_feed() {
	

wp_rss_multi_importer_feed();
}



add_action('init', 'rssmi_rss');

function rssmi_rss(){
	$feed_options = get_option('rss_feed_options', 'option not found');

	if (!empty($feed_options) && isset($feed_options['feedslug'])){
		
add_feed($feed_options['feedslug'], 'rssmi_feed');



	}
}


function rss_text_limit($striptags=0,$string, $length, $replacer = '...') {
	if ($striptags==1){
	 $string = strip_tags($string);
	}
	  if(strlen($string) > $length)
	    return (preg_match('/^(.*)\W.*$/', substr($string, 0, $length+1), $matches) ? $matches[1] : substr($string, 0, $length)) . $replacer;  
	  return $string;
	}


function wp_rss_multi_importer_feed(){
header("Content-type: text/xml");	
$catArray=array(0);

if(!function_exists("wprssmi_hourly_feed")) {
function wprssmi_hourly_feed() { return 0; }  // no caching of RSS feed
}






	
  
   	$options = get_option('rss_import_options','option not found');
	$option_items = get_option('rss_import_items','option not found');
	$feed_options = get_option('rss_feed_options', 'option not found');

	if ($option_items==false) return "You need to set up the WP RSS Multi Importer Plugin before any results will show here.  Just go into the <a href='/wp-admin/options-general.php?page=wp_rss_multi_importer_admin'>settings panel</a> and put in some RSS feeds";


$cat_array = preg_grep("^feed_cat_^", array_keys($option_items));

	if (count($cat_array)==0) {  // for backward compatibility
		$noExistCat=1;
	}else{
		$noExistCat=0;	
	}



    
   if(!empty($option_items)){
	
//GET PARAMETERS  
$size = count($option_items);
$sortDir=$options['sortbydate'];  // 1 is ascending
$stripAll=$options['stripAll'];
$todaybefore=$options['todaybefore'];
$adjustImageSize=$options['adjustImageSize'];
$showDesc=$options['showdesc'];  // 1 is show
$descNum=$options['descnum'];
$maxperPage=$options['maxperPage'];


$cacheMin=$options['cacheMin'];
$maxposts=$options['maxfeed'];

if ($thisfeed!='') $maxposts=$thisfeed;


$targetWindow=$options['targetWindow'];  // 0=LB, 1=same, 2=new
$floatType=$options['floatType'];
$noFollow=$options['noFollow'];
$showmore=$options['showmore'];
$cb=$options['cb'];  // 1 if colorbox should not be loaded
$pag=$options['pag'];  // 1 if pagination
$perPage=$options['perPage'];
if(empty($options['sourcename'])){
	$attribution='';
}else{
	$attribution=$options['sourcename'].': ';
}

if ($floatType=='1'){
	$float="left";
}else{
	$float="none";	
}

if ($parmfloat!='') $float=$parmfloat;

	$cacheMin=0;
if ($cacheMin==''){
$cacheMin=0;  //set caching minutes	
}


if (!is_null($cachetime)) {$cacheMin=$cachetime;}  //override caching minutes with shortcode parameter	







	$myarray=get_transient($cachename);  // added  for transient cache
	
	if ($cacheMin==0){
		delete_transient($cachename); 
	}
	
   if (false===$myarray) {   //  added  for transient cache - only get feeds and put into array if the array isn't cached (for a given category set)



   for ($i=1;$i<=$size;$i=$i+1){

	

   			$key =key($option_items);
				if ( !strpos( $key, '_' ) > 0 ) continue; //this makes sure only feeds are included here...everything else are options
				
   			$rssName= $option_items[$key];

   
   			next($option_items);
   			
   			$key =key($option_items);
   			
   			$rssURL=$option_items[$key];



  	next($option_items);
	$key =key($option_items);
	
// $rssCatID=$option_items[$key];  ///this should be the category ID



if (((!in_array(0, $catArray ) && in_array($option_items[$key], $catArray ))) || in_array(0, $catArray ) || $noExistCat==1) {



   $myfeeds[] = array("FeedName"=>$rssName,"FeedURL"=>$rssURL);   
	
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


//SORT DEPENDING ON SETTINGS

	if($sortDir==1){

		for ($i=$maxfeed-1;$i>=$maxfeed-$maxposts;$i--){
			$item = $feed->get_item($i);
			 if (empty($item))	continue;
		
				$myarray[] = array("mystrdate"=>strtotime($item->get_date()),"mytitle"=>$item->get_title(),"mylink"=>$item->get_link(),"myGroup"=>$feeditem["FeedName"],"mydesc"=>$item->get_description());
			}

		}else{	

		for ($i=0;$i<=$maxposts-1;$i++){
				$item = $feed->get_item($i);
				if (empty($item))	continue;	
				
					
					$myarray[] = array("mystrdate"=>strtotime($item->get_date()),"mytitle"=>$item->get_title(),"mylink"=>$item->get_link(),"myGroup"=>$feeditem["FeedName"],"mydesc"=>$item->get_description());
				}	
		}


	}





if ($cacheMin!==0){
set_transient($cachename, $myarray, 60*$cacheMin);  //  added  for transient cache
}

}  //  added  for transient cache

if ($timerstop==1){
 timer_stop(1); echo ' seconds<br>';  //TIMER END for testing purposes
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
header('Content-Type: ' . feed_content_type('rss-http') . '; charset=' . get_option('blog_charset'), true);
?>
<rss version="2.0">
<channel>
<title><?php echo $feed_options['feedtitle'] ?></title>
<link></link>
<description><?php echo $feed_options['feeddesc'] ?></description>
<language>en-us</language>
<?php

	$total=0;	

foreach($myarray as $items) {
		$total = $total +1;
			if ($total>20) break;
	?>	
<item>		
<title><?php echo $items["mytitle"]?></title>	
<link><?php echo $items["mylink"]?></link>

<description><?php echo '<![CDATA['.rss_text_limit($feed_options['striptags'],$items["mydesc"], 500).'<br/><br/>Keep on reading: <a href="'.$items["mylink"].'">'.$items["mytitle"].'</a>'.']]>';  ?></description>
<pubdate><?php echo  date_i18n("D, M d, Y",$items["mystrdate"])?></pubdate>
<guid><?php echo $items["mylink"]?></guid>
</item>	
<?php		
}
?>
</channel></rss>
 <?php   


}



  }

?>