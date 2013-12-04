<?php



//  Categories Page

function wp_rss_multi_importer_category_images_page() {


       ?>
      <div class="wrap">
		 <h2>Category Default Images, Post Tags and Filter Words Admin</h2>
	<div id="poststuff">
  


     <form action="options.php" method="post" class="catform" >  
	
		<div class="postbox">
		<div class="inside">
	<h3><?php _e("Set a Default Feed Category Image, Post Category Tags and Category Word Filters (all are optional) - note: filters work for both shortcode and Feed to Post", 'wp-rss-multi-importer')?></h3>

	
	<?php
	settings_fields( 'wp_rss_multi_importer_categories_images' );


	$options = get_option('rss_import_categories' ); 
	$options_images = get_option('rss_import_categories_images' ); 

	if ( !empty($options) ) {
		
				echo '<div class="default-image-wrapper"><span class="default-image-text">Default Feed Category Image</span><span class="default-tags-text">Post Category Tags</span><span class="default-filter-text">Include Filter Words</span><br>';
				echo '<span class="default-image-text-more">(full URL required)</span><span class="default-tags-text-more">(comma delimited list)</span><span class="default-tags-filter-more">(comma delimited list)</span><span class="default-tags-exclude-more">(check to exclude words)</span></div>';
				
		$size = count($options);


		for ( $i=1; $i<=$size; 	$i++ ) {   
		   
if( $i % 2== 0 ) continue;

				
				   $key = key( $options );

	$j = cat_get_id_number($key);
	$textUpper=strtoupper($options[$key]);
		if ( !empty($options_images) ) {
	$cat_default_image=$options_images[$j]['imageURL'];
	$cat_default_tags=$options_images[$j]['tags'];
	$cat_default_filterwords=$options_images[$j]['filterwords'];
	$cat_default_filterwords_exclude=$options_images[$j]['exclude'];
	if ($cat_default_filterwords_exclude==1) {$checkmsg='checked=checked';}else{$checkmsg='';}
		}
	
echo "<div class='default-list-name'>".$textUpper.":</div>";

	next( $options );

echo "<div class='default-list-image'><input class='default-cat-image'  size='70' name='rss_import_categories_images[$j][imageURL]' type='text' value='$cat_default_image' /></div>";

echo "<div class='default-list-tags'><input id='default-cat-tags' class='default-cat-tags'  size='20' name='rss_import_categories_images[$j][tags]' type='text' value='$cat_default_tags' /></div>";
echo "<div class='default-list-tags'><input id='default-cat-tags' class='default-cat-tags'  size='60' name='rss_import_categories_images[$j][filterwords]' type='text' value='$cat_default_filterwords' /><input type='checkbox' Name='rss_import_categories_images[$j][exclude]' Value='1' $checkmsg></div>";
		next( $options );

}

echo "<br><p class='submit'><input type='submit' value='Save Settings' name='submit' class='button-primary'></p>";		 

}else{
	 _e("<br>Once you add categories (above), you'll be able to add default images and tags here.", 'wp-rss-multi-importer');
	
}
	?>

</div></div>	          
</form>
</div></div>

<?php

}





function catDropDown($thisCatID){

if($thisCatID[1]=="0") {
	$thisCatID[1]=1;
}
	$category_ids = get_all_category_ids();
	echo 	'<OPTION  '.((isset($thisCatID[0]) && is_null($thisCatID[0])) ? 'selected':'').'  VALUE=NULL>Not in Use</OPTION>';	 
	foreach($category_ids as $cat_id) {
	  $cat_name = get_cat_name($cat_id);
	
	echo 	'<OPTION  '.selected(true, in_array($cat_id, $thisCatID), false).'  VALUE="'.$cat_id.'">'.$cat_name.'</OPTION>';
 
	}

}












function wprssmi_convert_key( $key ) { 

     if ( strpos( $key, 'feed_name_' ) === 0 ) { 
	

 $label = str_replace( 'feed_name_', __('Feed Name ','wp-rss-multi-importer') , $key );

     }

     else if ( strpos( $key, 'feed_url_' ) === 0 ) { 

         $label = str_replace( 'feed_url_', __('Feed URL ','wp-rss-multi-importer'), $key );
     }

		else if ( strpos( $key, 'feed_cat_' ) === 0 ) { 

         $label = str_replace( 'feed_url_', __('Feed Category ','wp-rss-multi-importer'), $key );
     }

		else if ( strpos( $key, 'cat_name_' ) === 0 ) { 

         $label = str_replace( 'cat_name_', __('Category ID # ','wp-rss-multi-importer'), $key );
     }


     return $label;
 }

 function wprss_get_id_number($key){
	
	if ( strpos( $key, 'feed_name_' ) === 0 ) { 

     $j = str_replace( 'feed_name_', '', $key );
 }
	return $j;
	
 }


function cat_get_id_number($key){

	if ( strpos( $key, 'cat_name_' ) === 0 ) { 

     $j = str_replace( 'cat_name_', '', $key );
 }
	return $j;

 }


function check_feed($url){
	
		$url=(string)($url);


		while ( stristr($url, 'http') != $url )
			$url = substr($url, 1);

		$url = esc_url_raw(strip_tags($url));


					$feed = fetch_feed($url);

		if (is_wp_error( $feed ) ) {
			return "<span class=chk_feed>".__('This feed has errors', 'wp-rss-multi-importer')."</span>";			

		}
		
}



function wp_rss_multi_importer_intro_page() {
		$feed = fetch_feed("http://rss.marketingprofs.com/marketingprofs");
	
	?>
	
	<div class="wrap">
						
			
	                                <div class="postbox-container" style="min-width:400px; max-width:600px; padding: 0 20px 0 0;">	<h2>Instructions: Get Up and Running Quickly</h2>
					<div class="metabox-holder">	
						<div class="postbox-container">
							<H3 class="info_titles">Add the RSS feeds and optionally assign them to categories</H3>
							<p class="info_text"><?php _e("Start by adding feeds (Add a Feed or Upload RSS Feeds tabs).  Then, if you want, you can add Categories (Categories tab).  If you add categories, you can then go back and assign each feed to a category.", 'wp-rss-multi-importer')?></p>
							<H3 class="info_titles">Decide how you want to present the items from the RSS feeds on your web site</H3>
							<p class="info_text"><?php _e("You can present them on any page using Shortcode, which looks like this - [wp_rss_multi_importer], and display them using one of the 8 templates provided.  Or, you can have the items from RSS feeds become blog posts, and then let the settings of your Wordpress theme determine how they will look.  Finally, you might simply want the feeds in the side bar - and here a widget would work best.<br><br>You don't have to choose one way or another to present the feeds.  You can do all 3 at the same time.", 'wp-rss-multi-importer')?></p>	
		
							<H3 class="info_titles">1. Using the shortcode to display the feed items</H3>
							<p class="info_text"><?php _e("Go to the Shortcode Settings tab and select the template you want to use and set the settings. Make sure this feature is activated. Add the shortcode to your Wordpress page. Use shortcode parameters (Shortcode Parameters tab) to put more customization onto your feed presentation.  If you put your feeds into categories, you can restrict which shows on a page to whatever categories you want.", 'wp-rss-multi-importer')?></p>
							<H3 class="info_titles">2. Create blog posts from the feed items (Feed to Post)</H3>
							<p class="info_text"><?php _e("Click on the Feed to Post Settings tab and set the options.  Make sure this feature is activated. At the bottom of that page you can assign the plugin categories to your WP blog categories", 'wp-rss-multi-importer')?></p>
							<H3 class="info_titles">3. Display the aggregated feed items in a widget</H3>
							<p class="info_text"><?php _e("If your theme supports widgets, go to Appearance->Widgets, add the RSS Multi-Importer widget, configure the options and then click Save.", 'wp-rss-multi-importer')?></p>
							
						</div>
					</div>
				</div>
					<div class="postbox-container" style="width:25%;min-width:200px;max-width:350px;">
			<div id="sidebar" class="MP_box">
					<div >
			<h2 class="MP_title">Cutting Edge Marketing Know-How</h2>
		</div>
		
		
											
												
													<div class="txtorange">Join MarketingProfs.com</div>
														<div class="txtwhite">Over 600,000 have already</div>
													<div class="txtorange">Your Free Membership Includes:</div>
													<ul class="padding_nomargin txtleft" style="margin-left:30px;padding-top:5px;padding-bottom:5px;margin-top:0px;">
														<li style="margin:3px;"><b>FREE</b> access to all marketing articles</li>
														<li style="margin:3px;"><b>FREE</b> community forum use</li>
													</ul>
													<form style="padding-bottom:4px;" onsubmit="validateEmail(document.getElementById('e'));" action="https://www.marketingprofs.com/login/signup.asp" method="POST">
																				<div class="center width_full"><input type="text" onfocus="this.value=''" value="you@company.com" style="width:225px;color:#444;" id="e" name="e"></div>
																				<div class="center width_full"><input type="image" style="margin-top:4px;" src="http://www.mpdailyfix.com/wp-content/themes/mpdailyfix/images/signup_blue.gif" id="btnsignup" name="btnsignup"></div>
																				<input type="hidden" value="amwplugin" name="adref">
																				<script type="text/javascript">
																					function validateEmail(emailField){
																							var re = /^(([^&lt;&gt;()[\]\\.,;:\s@\"]+(\.[^&lt;&gt;()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
																							if (re.test(emailField.value) == false) 
																							{
																								alert('Oops! That email address doesn\'t look quite right.\n\nPlease make sure it was typed correctly and try again.');
																								return false;
																							}
																							return true;
																					}				
																				</script>
																			</form>
																		<span class="MP_title">	<a class="button-primary" style="text-align:center" href="https://www.marketingprofs.com/login/join?adref=amwplugin" target="_blank">Learn more »</a></span>
																
							
			
			
			
			</div>
			
			
			<?php
				if (!is_wp_error( $feed ) ){
		?>
			
			<h3 style="text-align:center;"><?php print 'Latest '.$feed->get_title(); ?></h3>
			<ul>
			<?php foreach ($feed->get_items(0, 5) as $item): ?>
			    <li>
			        <a href="<?php print $item->get_permalink(); ?>" target="_blank">
			        <?php print $item->get_title(); ?></a>
			    </li>
			<?php endforeach; ?>
			</ul>
			<?php	
			}
			
			?>
			
	
			
			
			<div id="sidebar" class="MP_box">
				<div >
		<h2 class="MP_title">Need Plugin Help?</h2>
	</div>
	
	<p><a href="http://www.allenweiss.com/faqs/" target="_blank" style="color:white">Go here</a> to find FAQs, our discussion board, template examples, and more.</p>
	<p><a href="http://www.allenweiss.com/faqs/im-told-the-feed-isnt-valid-or-working/" target="_blank" style="color:white">Go here if you have a feed that isn't working</a><p>			
				
				</div>
			
			
		</div>
				
				</div>
	
	
	<?php
	
}








function wp_rss_multi_importer_options_page() {


delete_db_transients();


       ?>

       <div class="wrap">
	<h2><?php _e("Settings for Displaying Feed Items Using Shortcode", 'wp-rss-multi-importer')?></h2>
	<div id="poststuff">

       <?php screen_icon(); 

//do_settings_sections( 'wprssimport' );

?>

    

       <div id="options">
	

       <form action="options.php" method="post"  >            

       <?php
		$siteurl= get_site_url();
        $images_url = $siteurl . '/wp-content/plugins/' . basename(dirname(__FILE__)) . '/images';

      settings_fields( 'wp_rss_multi_importer_item_options' );


       $options = get_option( 'rss_import_options' ); 


    	




  

    

       ?>

      
      

<div class="postbox"><h3><label for="title"><?php _e("Options Settings for Displaying the Feed Items", 'wp-rss-multi-importer')?></label></h3>
	<p style="margin-left:20px">These are settings for the option to display the feed items on your site.  If you want the settings for the Feed to Post option, use that tab instead.</p>
<div class="inside">

<h3><?php _e("Template", 'wp-rss-multi-importer')?></h3>


<?php
$thistemplate=$options['template'];
	get_template_function($thistemplate);
?>

<?php
if ($options['maxperPage']=='' || $options['maxperPage']=='NULL') {
?>
<H2 class="save_warning"><?php _e("You must choose and then click Save Settings for the plugin to function correctly.  If not sure which options to choose right now, don't worry - the most common settings have been set for you - just click Save Settings.", 'wp-rss-multi-importer')?></H2>
<?php
}
?>


<h3><?php _e("Sorting and Separating Posts", 'wp-rss-multi-importer')?></h3>
 
      <p><label class='o_textinput' for='sortbydate'><?php _e("Sort Output by Date (Descending = Closest Date First", 'wp-rss-multi-importer')?></label>
	
		<SELECT NAME="rss_import_options[sortbydate]">
		<OPTION VALUE="1" <?php if($options['sortbydate']==1){echo 'selected';} ?>><?php _e("Ascending", 'wp-rss-multi-importer')?></OPTION>
		<OPTION VALUE="0" <?php if($options['sortbydate']==0){echo 'selected';} ?>><?php _e("Descending", 'wp-rss-multi-importer')?></OPTION>
		<OPTION VALUE="2" <?php if($options['sortbydate']==2){echo 'selected';} ?>><?php _e("No sorting", 'wp-rss-multi-importer')?></OPTION>
		
		</SELECT></p>  
		
		
		<p><label class='o_textinput' for='todaybefore'><?php _e("Separate Today and Earlier Posts", 'wp-rss-multi-importer')?></label>

		<SELECT NAME="rss_import_options[todaybefore]">
		<OPTION VALUE="1" <?php if($options['todaybefore']==1){echo 'selected';} ?>><?php _e("Yes", 'wp-rss-multi-importer')?></OPTION>
		<OPTION VALUE="0" <?php if($options['todaybefore']==0){echo 'selected';} ?>><?php _e("No", 'wp-rss-multi-importer')?></OPTION>

		</SELECT></p>
	
<h3><?php _e("Number of Posts and Pagination", 'wp-rss-multi-importer')?></h3>
<p><label class='o_textinput' for='maxfeed'><?php _e("Number of Entries per Feed", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[maxfeed]">
<OPTION VALUE="1" <?php if($options['maxfeed']==1){echo 'selected';} ?>>1</OPTION>
<OPTION VALUE="2" <?php if($options['maxfeed']==2){echo 'selected';} ?>>2</OPTION>
<OPTION VALUE="3" <?php if($options['maxfeed']==3){echo 'selected';} ?>>3</OPTION>
<OPTION VALUE="4" <?php if($options['maxfeed']==4){echo 'selected';} ?>>4</OPTION>
<OPTION VALUE="5" <?php if($options['maxfeed']==5){echo 'selected';} ?>>5</OPTION>
<OPTION VALUE="10" <?php if($options['maxfeed']==10){echo 'selected';} ?>>10</OPTION>
<OPTION VALUE="15" <?php if($options['maxfeed']==15){echo 'selected';} ?>>15</OPTION>
<OPTION VALUE="20" <?php if($options['maxfeed']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($options['maxfeed']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="40" <?php if($options['maxfeed']==40){echo 'selected';} ?>>40</OPTION>
<OPTION VALUE="50" <?php if($options['maxfeed']==50){echo 'selected';} ?>>50</OPTION>
<OPTION VALUE="60" <?php if($options['maxfeed']==60){echo 'selected';} ?>>60</OPTION>
<OPTION VALUE="70" <?php if($options['maxfeed']==70){echo 'selected';} ?>>70</OPTION>
<OPTION VALUE="80" <?php if($options['maxfeed']==80){echo 'selected';} ?>>80</OPTION>
</SELECT></p>


<p><label class='o_textinput' for='maxperPage'><?php _e("Number of Entries per Page of Output (<a href=\"http://www.allenweiss.com/faqs/how-does-the-number-of-entries-per-feed-and-page-or-fetch-work//\" target=\"_blank\">Go here to see how to set this option</a>)", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[maxperPage]">
<OPTION VALUE="5" <?php if($options['maxperPage']==5){echo 'selected';} ?>>5</OPTION>
<OPTION VALUE="10" <?php if($options['maxperPage']==10){echo 'selected';} ?>>10</OPTION>
<OPTION VALUE="20" <?php if($options['maxperPage']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($options['maxperPage']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="40" <?php if($options['maxperPage']==40){echo 'selected';} ?>>40</OPTION>
<OPTION VALUE="50" <?php if($options['maxperPage']==50){echo 'selected';} ?>>50</OPTION>
</SELECT></p>




<p><label class='o_textinput' for='pag'><?php _e("Do you want pagination?", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[pag]" id="pagination">
<OPTION VALUE="1" <?php if($options['pag']==1){echo 'selected';} ?>><?php _e("Yes", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="0" <?php if($options['pag']==0){echo 'selected';} ?>><?php _e("No", 'wp-rss-multi-importer')?></OPTION>
</SELECT>  <?php _e("(Note: this will override the Number of Entries per Page of Output)", 'wp-rss-multi-importer')?></p>



<span id="pag_options" <?php if($options['pag']==0){echo 'style="display:none"';}?>>
	
	<p style="padding-left:15px"><label class='o_textinput' for='perPage'><?php _e("Number of Posts per Page for Pagination", 'wp-rss-multi-importer')?></label>
	<SELECT NAME="rss_import_options[perPage]">
	<OPTION VALUE="6" <?php if($options['perPage']==6){echo 'selected';} ?>>6</OPTION>
	<OPTION VALUE="12" <?php if($options['perPage']==12){echo 'selected';} ?>>12</OPTION>
	<OPTION VALUE="15" <?php if($options['perPage']==15){echo 'selected';} ?>>15</OPTION>
	<OPTION VALUE="20" <?php if($options['perPage']==20){echo 'selected';} ?>>20</OPTION>
	</SELECT></p>	
	
</span>



<h3><?php _e("How Links Open and No Follow Option", 'wp-rss-multi-importer')?></h3>

<p><label class='o_textinput' for='targetWindow'><?php _e("Target Window (when link clicked, where should it open?)", 'wp-rss-multi-importer')?></label>
	<SELECT NAME="rss_import_options[targetWindow]" id="targetWindow">
	<OPTION VALUE="0" <?php if($options['targetWindow']==0){echo 'selected';} ?>><?php _e("Use LightBox", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="1" <?php if($options['targetWindow']==1){echo 'selected';} ?>><?php _e("Open in Same Window", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="2" <?php if($options['targetWindow']==2){echo 'selected';} ?>><?php _e("Open in New Window", 'wp-rss-multi-importer')?></OPTION>
	</SELECT>	
</p>
<p style="padding-left:15px"><label class='o_textinput' for='noFollow'>Set links as No Follow.  <input type="checkbox" Name="rss_import_options[noFollow]" Value="1" <?php if ($options['noFollow']==1){echo 'checked="checked"';} ?></label></p>





<h3><?php _e("What Shows - Attribution", 'wp-rss-multi-importer')?></h3>



<p><label class='o_textinput' for='sourcename'><?php _e("Feed Source Attribution Label", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[sourcename]">
<OPTION VALUE="Source" <?php if($options['sourcename']=='Source'){echo 'selected';} ?>><?php _e("Source", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="Via" <?php if($options['sourcename']=='Via'){echo 'selected';} ?>><?php _e("Via", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="Club" <?php if($options['sourcename']=='Club'){echo 'selected';} ?>><?php _e("Club", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="Sponsor" <?php if($options['sourcename']=='Sponsor'){echo 'selected';} ?>><?php _e("Sponsor", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="" <?php if($options['sourcename']==''){echo 'selected';} ?>><?php _e("No Attribution", 'wp-rss-multi-importer')?></OPTION>
</SELECT></p>

<p ><label class='o_textinput' for='addAuthor'><?php _e("Show Feed or Author Name (if available)", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_import_options[addAuthor]" Value="1" <?php if ($options['addAuthor']==1){echo 'checked="checked"';} ?></label></p>



<h3><?php _e("What Shows - EXCERPTS", 'wp-rss-multi-importer')?></h3>

<p><label class='o_textinput' for='showdesc'><?php _e("<b>Show Excerpt</b>", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[showdesc]" id="showdesc">
<OPTION VALUE="1" <?php if($options['showdesc']==1){echo 'selected';} ?>><?php _e("Yes", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="0" <?php if($options['showdesc']==0){echo 'selected';} ?>><?php _e("No", 'wp-rss-multi-importer')?></OPTION>
</SELECT></p>

<p style="padding-left:15px"><label class='o_textinput' for='showcategory'><?php _e("Show Category Name", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_import_options[showcategory]" Value="1" <?php if ($options['showcategory']==1){echo 'checked="checked"';} ?></label></p>


<span id="secret" <?php if($options['showdesc']==0){echo 'style="display:none"';}?>>
	
	
	<p style="padding-left:15px"><label class='o_textinput' for='showmore'><?php _e("Let your readers determine if they want to see the excerpt with a show-hide option. ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_import_options[showmore]" Value="1" <?php if ($options['showmore']==1){echo 'checked="checked"';} ?></label>
	</p>	
	
	
<p style="padding-left:15px"><label class='o_textinput' for='descnum'><?php _e("Excerpt length (number of words)", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[descnum]" id="descnum">
<OPTION VALUE="20" <?php if($options['descnum']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($options['descnum']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="50" <?php if($options['descnum']==50){echo 'selected';} ?>>50</OPTION>
<OPTION VALUE="75" <?php if($options['descnum']==75){echo 'selected';} ?>>75</OPTION>
<OPTION VALUE="100" <?php if($options['descnum']==100){echo 'selected';} ?>>100</OPTION>
<OPTION VALUE="200" <?php if($options['descnum']==200){echo 'selected';} ?>>200</OPTION>
<OPTION VALUE="300" <?php if($options['descnum']==300){echo 'selected';} ?>>300</OPTION>
<OPTION VALUE="400" <?php if($options['descnum']==400){echo 'selected';} ?>>400</OPTION>
<OPTION VALUE="500" <?php if($options['descnum']==500){echo 'selected';} ?>>500</OPTION>
<OPTION VALUE="1000" <?php if($options['descnum']==1000){echo 'selected';} ?>>1000</OPTION>
<OPTION VALUE="99" <?php if($options['descnum']==99){echo 'selected';} ?>><?php _e("Give me everything", 'wp-rss-multi-importer')?></OPTION>
</SELECT><?php _e("  Note: Choosing Give me everything will just be a pure extract of the content without any image processsing, etc.", 'wp-rss-multi-importer')?></p>


<h3><?php _e("Image Handling", 'wp-rss-multi-importer')?></h3>

<?php

if (ini_get('allow_url_fopen')==0){
echo 'You server is not configured to accept images from outside sources.  Please contact your web host to set allow_url_fopen to ON.  You might be able to do this for yourself if your host gives you a way to edit the php.ini file.';	
}
?>

<p><?php _e("An attempt will be made to select an image for your post.  Usually this is the first image in the content or in a feed enclosure, but you have the option - if those are not available - to get the first image in the content.", 'wp-rss-multi-importer')?>
<p><label class='o_textinput' for='stripAll'><?php _e("Check to get rid of all images in the excerpt.", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_import_options[stripAll]" Value="1" <?php if ($options['stripAll']==1){echo 'checked="checked"';} ?></label>
</p>
<p><label class='o_textinput' for='anyimage'><?php _e("Check to use any image in the content if possible", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_import_options[anyimage]" Value="1" <?php if ($options['anyimage']==1){echo 'checked="checked"';} ?></label>
</p>

<p><?php _e("You can adjust the image, if it exists.  Note that including images in your feed may slow down how quickly it renders on your site, so you'll need to experiment with these settings.", 'wp-rss-multi-importer')?></p>
<p style="padding-left:15px"><label class='o_textinput' for='adjustImageSize'><?php _e("If you want excerpt images, check to fix their width at 150 (can be over-written in shortcode).", 'wp-rss-multi-importer')?>  <input type="checkbox" Name="rss_import_options[adjustImageSize]" Value="1" <?php if ($options['adjustImageSize']==1){echo 'checked="checked"';} ?></label></p>
	
<p style="padding-left:15px"><label class='o_textinput' for='floatType'><?php _e("Float images to the left (can be over-written in shortcode).", 'wp-rss-multi-importer')?>  <input type="checkbox" Name="rss_import_options[floatType]" Value="1" <?php if ($options['floatType']==1){echo 'checked="checked"';} ?></label></p>
</span>


	<p style="padding-left:15px"><label class='o_textinput' for='RSSdefaultImage'><?php _e("Default category image setting", 'wp-rss-multi-importer')?></label>
	<SELECT NAME="rss_import_options[RSSdefaultImage]" id="RSSdefaultImage">
	<OPTION VALUE="0" <?php if($options['RSSdefaultImage']==0){echo 'selected';} ?>>Process normally</OPTION>
	<OPTION VALUE="1" <?php if($options['RSSdefaultImage']==1){echo 'selected';} ?>>Use default image for category</OPTION>
	<OPTION VALUE="2" <?php if($options['RSSdefaultImage']==2){echo 'selected';} ?>>Replace articles with no image with default category image</OPTION>

	</SELECT></p>




<h3><?php _e("Get Social", 'wp-rss-multi-importer')?></h3>
<p ><label class='o_textinput' for='showsocial'><?php _e("Add social icons (Twitter and Facebook) to each post. ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_import_options[showsocial]" Value="1" <?php if ($options['showsocial']==1){echo 'checked="checked"';} ?></label>
</p>


<h3><?php _e("Cache and Conflict Handling", 'wp-rss-multi-importer')?></h3>

<p><label class='o_textinput' for='cacheMin'><?php _e("Number of minutes you want the post data held in cache (match to how often your feeds are updated)", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_import_options[cacheMin]" id="cacheMin">
<OPTION VALUE="0" <?php if($options['cacheMin']==0){echo 'selected';} ?>>Turn off caching</OPTION>
<OPTION VALUE="1" <?php if($options['cacheMin']==1){echo 'selected';} ?>>1</OPTION>
<OPTION VALUE="5" <?php if($options['cacheMin']==5){echo 'selected';} ?>>5</OPTION>
<OPTION VALUE="10" <?php if($options['cacheMin']==10){echo 'selected';} ?>>10</OPTION>
<OPTION VALUE="20" <?php if($options['cacheMin']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($options['cacheMin']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="40" <?php if($options['cacheMin']==40){echo 'selected';} ?>>40</OPTION>
<OPTION VALUE="60" <?php if($options['cacheMin']==60){echo 'selected';} ?>>60</OPTION>
<OPTION VALUE="120" <?php if($options['cacheMin']==120){echo 'selected';} ?>>120</OPTION>
<OPTION VALUE="180" <?php if($options['cacheMin']==180){echo 'selected';} ?>>180</OPTION>
<OPTION VALUE="240" <?php if($options['cacheMin']==240){echo 'selected';} ?>>240</OPTION>
<OPTION VALUE="300" <?php if($options['cacheMin']==300){echo 'selected';} ?>>300</OPTION>
</SELECT></p>




<p ><label class='o_textinput' for='cb'><?php _e("Check if you are having colorbox conflict problems.", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_import_options[cb]" Value="1" <?php if ($options['cb']==1){echo 'checked="checked"';} ?></label></p>


<p ><label class='o_textinput' for='warnmsg'><?php _e("Check if you want to suppress warning messages.", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_import_options[warnmsg]" Value="1" <?php if ($options['warnmsg']==1){echo 'checked="checked"';} ?></label></p>

<p ><label class='o_textinput' for='directFetch'><?php _e("Check if you are having simplepie conflict problems.", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_import_options[directFetch]" Value="1" <?php if ($options['directFetch']==1){echo 'checked="checked"';} ?></label></p>


<input   size='10' name='rss_import_options[plugin_version]' type='hidden' value='<?php echo WP_RSS_MULTI_VERSION ?>' />

</div></div>

       <p class="submit"><input type="submit" value="Save Settings" name="submit" class="button-primary"></p>



       </form>

      <div class="postbox"><h3><label for="title"><?php _e("Help Others", 'wp-rss-multi-importer')?></label></h3><div class="inside"><?php _e("If you find this plugin helpful, let others know by <a href=\"http://wordpress.org/extend/plugins/wp-rss-multi-importer/\" target=\"_blank\">rating it here</a>.  That way, it will help others determine whether or not they should try out the plugin.  Thank you.", 'wp-rss-multi-importer')?></div></div> 


       </div>
</div>
       </div>

       <?php 

  }




function wp_rss_multi_importer_items_page() {


	delete_db_transients();

       ?>

       <div class="wrap">
	 <h2>RSS Feeds Admin</h2>
	<div id="poststuff">
 
       <?php screen_icon(); 

do_settings_sections( 'wprssimport' );

?>



       <div id="options">


       <form action="options.php" method="post"  >            

       <?php

	$removeurl=WP_RSS_MULTI_IMAGES."remove.png";

      settings_fields( 'wp_rss_multi_importer_options' );


       $options = get_option( 'rss_import_items' ); 

       $catOptions_exist= get_option( 'rss_import_categories' ); 

//this included for backward compatibility
  if ( !empty($options) ) {
$cat_array = preg_grep("^feed_cat_^", array_keys($options));

	if (count($cat_array)==0) {
	   //echo "category was not found\n";
		$catExists=0;
		$modnumber=2;
	}else{
		$catExists=1;
		$modnumber=3;	
	}
}


       if ( !empty($options) ) {

           $size = count($options);  

           for ( $i=1; $i<=$size; $i++) {            

               //if( $i % $modnumber == 0 ) continue;


               $key = key( $options );


            if ( !strpos( $key, '_' ) > 0 ) continue; //this makes sure only feeds are included here...everything else are options

				$j = wprss_get_id_number($key);
			

             echo "<div class='wprss-input' id='$j'>";

               echo "<p><label class='textinput' for='$key'>" . wprssmi_convert_key( $key ) . "</label>

               <input  class='wprss-input' size='75' name='rss_import_items[$key]' type='text' value='$options[$key]' />  <a href='javascript:void(0)' class='btnDelete' id='$j'><img src='$removeurl'/></a></p>";


               next( $options );


               $key = key( $options );

$url_esc=esc_url($options[$key]);
               echo "<p><label class='textinput' for='$key'>" . wprssmi_convert_key( $key ) . "</label>

               <input id='$j' class='wprss-input' size='75' name='rss_import_items[$key]' type='text' value='$url_esc' />" ; 


			if (empty($catOptions_exist)){
				echo " <input id='$j' class='wprss-input' size='10' name='rss_import_items[feed_cat_$j]' type='hidden' value='0' />" ; 	

			}



	if ($catExists==1){
		    next( $options );
            $key = key( $options );	
			$selectName="rss_import_items[feed_cat_$j]";
	}else{
		$selectName="rss_import_items[feed_cat_$j]";		
	}


$catOptions= get_option( 'rss_import_categories' ); 

	if ( !empty($catOptions) ) {
		echo "<span class=category_list>Category ";
echo "<SELECT NAME=".$selectName." id='feed_cat'>";
echo "<OPTION VALUE='0'>NONE</OPTION>";
	$catsize = count($catOptions);

//echo $options[$key];

	for ( $k=1; $k<=$catsize; $k++ ) {   

if( $k % 2== 0 ) continue;

 	$catkey = key( $catOptions );
 	$nameValue=$catOptions[$catkey];
next( $catOptions );
 	$catkey = key( $catOptions );
	$IDValue=$catOptions[$catkey];


	 if($options[$key]==$IDValue){
		$sel='selected  ';

		} else {
		$sel='';

		}

echo "<OPTION " .$sel.  "VALUE=".$IDValue.">".$nameValue."</OPTION>";
next( $catOptions );

}
echo "</SELECT></span>";
}
//echo check_feed($url_esc);  // needs style

              echo " </p>";



               next( $options );

               echo "</div>"; 



           }

       }







       ?>

       <div id="buttons"><a href="javascript:void(0)" id="add" class="addbutton"><img src="<?php echo WP_RSS_MULTI_IMAGES; ?>add.png"></a>  



       <p class="submit"><input type="submit" value="Save Settings" name="submit" class="button-primary"></p>



       </form>

	



      <div class="postbox"><h3><label for="title">   <?php _e("Help Others", 'wp-rss-multi-importer')?></label></h3><div class="inside"><?php _e("If you find this plugin helpful, let others know by <a href=\"http://wordpress.org/extend/plugins/wp-rss-multi-importer/\" target=\"_blank\">rating it here</a>.  That way, it will help others determine whether or not they should try out the plugin.  Thank you.", 'wp-rss-multi-importer')?></div></div> 

       </div>

</div>
       </div>

       <?php 

  }



















//  Categories Page

function wp_rss_multi_importer_category_page() {


       ?>
      <div class="wrap">
	 <h2>Categories Admin</h2>	
	

	<div id="poststuff">



     <form action="options.php" method="post"  >  

		<div class="postbox">
		<div class="inside">
	<h3><?php _e("RSS Multi-Importer Categories (and their shortcodes)", 'wp-rss-multi-importer')?></h3>
	
	
	<?php

	settings_fields( 'wp_rss_multi_importer_categories' );

	$options = get_option('rss_import_categories' ); 


	if ( !empty($options) ) {
		$size = count($options);


		for ( $i=1; $i<=$size; $i++ ) {   

if( $i % 2== 0 ) continue;



				   $key = key( $options );

	$j = cat_get_id_number($key);
		$textUpper=strtoupper($options[$key]);
 			echo "<div class='cat-input' id='$j'>";
	echo "<p><label class='textinput' for='Category ID'>" . wprssmi_convert_key( $key ) . "</label>



       <input id='5' class='cat-input' size='20' name='rss_import_categories[$key]' type='text' value='$textUpper' />  [wp_rss_multi_importer category=\"".$j."\"]";
next( $options );
   $key = key( $options );

     echo"  <input id='5'  size='20' name='rss_import_categories[$key]' type='hidden' value='$options[$key]' />" ; 
	echo "</div>";
	next( $options );	
}



}
	?>
  <div id="category"><a href="javascript:void(0)" id="addCat" class="addCategory"><img src="<?php echo WP_RSS_MULTI_IMAGES; ?>addCat.png"></a>  	
<p class="submit"><input type="submit" value="Save Settings" name="submit" class="button-primary"></p>
</div></div>	          
</form>
</div></div>

<?php

}



function wp_rss_multi_importer_feed_page() {

       ?>

       <div class="wrap">
	  <h2><?php _e("Export Your RSS Feed", 'wp-rss-multi-importer')?></h2>
	<div id="poststuff">

  
<p><?php _e("You can re-export your feeds as an RSS feed for your readers.  You configure some options for this feed here.", 'wp-rss-multi-importer')?></p>


       <div id="options">

       <form action="options.php" method="post"  >            

       <?php

      settings_fields('wp_rss_multi_importer_feed_options');
      $options = get_option('rss_feed_options');    

       ?>


<div class="postbox">
	
<div class="inside">



<h3><?php _e("Export Feed Options Settings", 'wp-rss-multi-importer')?></h3>


<p><label class='o_textinput' for='feedtitle'><?php _e("Feed Title", 'wp-rss-multi-importer')?></label>

<input id="feedtitle" type="text" value="<?php echo $options['feedtitle']?>" name="rss_feed_options[feedtitle]"></p>

<p><label class='o_textinput' for='feedslug'><?php _e("Feed Slug", 'wp-rss-multi-importer')?></label>

<input id="feedslug" size="10" type="text" value="<?php echo $options['feedslug']?>" name="rss_feed_options[feedslug]"> <?php _e("(no spaces are allowed!  See what a slug is below)", 'wp-rss-multi-importer')?></p>

<p><label class='o_textinput' for='feeddesc'><?php _e("Feed Description", 'wp-rss-multi-importer')?></label>

<input id="feeddesc" type="text" value="<?php echo $options['feeddesc']?>" name="rss_feed_options[feeddesc]" size="50"></p>

<p><label class='o_textinput' for='striptags'><?php _e("Check to get rid of all images in the feed output.", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_feed_options[striptags]" Value="1" <?php if ($options['striptags']==1){echo 'checked="checked"';} ?></label>
</p>

</div></div>

       <p class="submit"><input type="submit" value="Save Settings" name="submit" class="button-primary"></p>



       </form>

	<?php
	$url=site_url();
	if (!empty($options['feedslug'])){

		echo "<h3>". __("Your RSS feed is here:", 'wp-rss-multi-importer'). "<br><br><a href=".$url."?feed=".$options['feedslug']." target='_blank'>".$url."?feed=".$options['feedslug']."</a></h3>";
		echo "<p>". __("To activate this feature, you may need to save your permalinks again by going to Settings -> Permalinks and clicking Save Changes.", 'wp-rss-multi-importer'). "</p>";
	}else{
		
		echo "<h3>". __("Your RSS feed is here:", 'wp-rss-multi-importer')." <br><br>".$url."?feed=[this is your slug]</h3>";
	}

	?>

</div></div></div>
<?php
}




function wp_rss_multi_importer_post_page() {

       ?>

       <div class="wrap">
	 <h2><?php _e("Put Your RSS Feed Into Blog Posts", 'wp-rss-multi-importer')?></h2>
	<div id="poststuff">


       <div id="options">

       <form action="options.php" method="post"  >            

       <?php

      settings_fields('wp_rss_multi_importer_post_options');
      $post_options = get_option('rss_post_options');    

       ?>


<div class="postbox">
<h3><label for="title"><?php _e("Feed to Post Options Settings", 'wp-rss-multi-importer')?></label></h3>

<div class="inside">

<h3><?php _e("Activation and Post Type Settings", 'wp-rss-multi-importer')?></h3>



<p><label class='o_textinput' for='active'><?php _e("Check to Activate this Feature", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[active]" Value="1" <?php if ($post_options['active']==1){echo 'checked="checked"';} ?></label><?php if ($post_options['active']!=1){echo "   <span style=\"color:red\">This feature is not active</span>";}?>
</p>
<?php
if ($post_options['active']==1){
wp_rss_multi_deactivation();
wp_rss_multi_activation();
}else{	
wp_rss_multi_deactivation();
}
?>

<p><label class='o_textinput' for='fetch_schedule'><?php _e("How often to import feeds (<a href=\"http://www.allenweiss.com/faqs/how-to-have-more-control-over-scheduling-of-feteching-feeds//\" target=\"_blank\">click here to learn how to have more control over this</a>)", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[fetch_schedule]" id="post_status">
<OPTION VALUE="2" <?php if($post_options['fetch_schedule']=="2"){echo 'selected';} ?>>Every 10 Min.</OPTION>
<OPTION VALUE="3" <?php if($post_options['fetch_schedule']=="3"){echo 'selected';} ?>>Every 15 Min.</OPTION>
<OPTION VALUE="4" <?php if($post_options['fetch_schedule']=="4"){echo 'selected';} ?>>Every 20 Min.</OPTION>
<OPTION VALUE="5" <?php if($post_options['fetch_schedule']=="5"){echo 'selected';} ?>>Every 30 Min.</OPTION>
<OPTION VALUE="1" <?php if($post_options['fetch_schedule']=="1"){echo 'selected';} ?>>Hourly</OPTION>
<OPTION VALUE="12" <?php if($post_options['fetch_schedule']=="12"){echo 'selected';} ?>>Twice Daily</OPTION>
<OPTION VALUE="24" <?php if($post_options['fetch_schedule']=="24"){echo 'selected';} ?>>Daily</OPTION>
<OPTION VALUE="168" <?php if($post_options['fetch_schedule']=="168"){echo 'selected';} ?>>Weekly</OPTION>
</SELECT></p>



<p><label class='o_textinput' for='post_status'><?php _e("Default status of posts", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[post_status]" id="post_status">
<OPTION VALUE="draft" <?php if($post_options['post_status']=="draft"){echo 'selected';} ?>>draft</OPTION>
<OPTION VALUE="publish" <?php if($post_options['post_status']=="publish"){echo 'selected';} ?>>publish</OPTION>
<OPTION VALUE="pending" <?php if($post_options['post_status']=="pending"){echo 'selected';} ?>>pending</OPTION>
<OPTION VALUE="future" <?php if($post_options['post_status']=="future"){echo 'selected';} ?>>future</OPTION>
<OPTION VALUE="private" <?php if($post_options['post_status']=="private"){echo 'selected';} ?>>private</OPTION>
</SELECT></p>


<p><label class='o_textinput' for='post_format'><?php _e("Default post format", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[post_format]" id="post_format">
<OPTION VALUE="standard" <?php if($post_options['post_format']=="standard"){echo 'selected';} ?>>Standard</OPTION>
<OPTION VALUE="aside" <?php if($post_options['post_format']=="aside"){echo 'selected';} ?>>Aside</OPTION>
<OPTION VALUE="gallery" <?php if($post_options['post_format']=="gallery"){echo 'selected';} ?>>Gallery</OPTION>
<OPTION VALUE="link" <?php if($post_options['post_format']=="link"){echo 'selected';} ?>>Link</OPTION>
<OPTION VALUE="image" <?php if($post_options['post_format']=="image"){echo 'selected';} ?>>Image</OPTION>
<OPTION VALUE="quote" <?php if($post_options['post_format']=="quote"){echo 'selected';} ?>>Quote</OPTION>
<OPTION VALUE="status" <?php if($post_options['post_format']=="status"){echo 'selected';} ?>>Status</OPTION>
</SELECT></p>



<p ><label class='o_textinput' for='bloguserid'><?php _e("Post to blog user_id", 'wp-rss-multi-importer')?>   <input  id='bloguserid' type="text" size='4' maxlength='4' Name="rss_post_options[bloguserid]" Value="<?php echo $post_options['bloguserid'] ?>">(if left blank, the admin will be the user)</label></p>


<p ><label class='o_textinput' for='plugindelete'><span style="color:red"><?php _e("IMPORTANT: Check to delete all posts and featured images created by this plugin if this plugin is deleted  ", 'wp-rss-multi-importer')?></span><input type="checkbox" Name="rss_post_options[plugindelete]" Value="1" <?php if ($post_options['plugindelete']==1){echo 'checked="checked"';} ?></label>
</p>


<h3><?php _e("Post Time Settings", 'wp-rss-multi-importer')?></h3>
<p><label class='o_textinput' for='overridedate'><?php _e("Check to over-ride the posts date/time with the current date and time   ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[overridedate]" Value="1" <?php if ($post_options['overridedate']==1){echo 'checked="checked"';} ?></label>
</p>

<p ><label class='o_textinput' for='timezone'><?php _e("Server Time Zone", 'wp-rss-multi-importer')?>   <input  id='timezone' type="text" size='40'  Name="rss_post_options[timezone]" Value="<?php echo $post_options['timezone'] ?>"> - <?php _e("Only fill this if your posts are showing up at the wrong time, even if the override box is checked - (<a href=\"http://www.allenweiss.com/faqs/my-posts-are-showing-up-with-the-wrong-time//\" target=\"_blank\">Read this for what to do here</a>).", 'wp-rss-multi-importer')?> </label></p>

<h3><?php _e("Fetch Quantity Settings", 'wp-rss-multi-importer')?></h3>


<p><label class='o_textinput' for='maxfeed'><?php _e("Number of Entries per Feed to Fetch", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[maxfeed]">
<OPTION VALUE="1" <?php if($post_options['maxfeed']==1){echo 'selected';} ?>>1</OPTION>
<OPTION VALUE="2" <?php if($post_options['maxfeed']==2){echo 'selected';} ?>>2</OPTION>
<OPTION VALUE="3" <?php if($post_options['maxfeed']==3){echo 'selected';} ?>>3</OPTION>
<OPTION VALUE="4" <?php if($post_options['maxfeed']==4){echo 'selected';} ?>>4</OPTION>
<OPTION VALUE="5" <?php if($post_options['maxfeed']==5){echo 'selected';} ?>>5</OPTION>
<OPTION VALUE="10" <?php if($post_options['maxfeed']==10){echo 'selected';} ?>>10</OPTION>
<OPTION VALUE="15" <?php if($post_options['maxfeed']==15){echo 'selected';} ?>>15</OPTION>
<OPTION VALUE="20" <?php if($post_options['maxfeed']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($post_options['maxfeed']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="40" <?php if($post_options['maxfeed']==40){echo 'selected';} ?>>40</OPTION>
<OPTION VALUE="50" <?php if($post_options['maxfeed']==50){echo 'selected';} ?>>50</OPTION>
<OPTION VALUE="60" <?php if($post_options['maxfeed']==60){echo 'selected';} ?>>60</OPTION>
<OPTION VALUE="70" <?php if($post_options['maxfeed']==70){echo 'selected';} ?>>70</OPTION>
<OPTION VALUE="80" <?php if($post_options['maxfeed']==80){echo 'selected';} ?>>80</OPTION>
<OPTION VALUE="100" <?php if($post_options['maxfeed']==100){echo 'selected';} ?>>100</OPTION>
</SELECT></p>



<p><label class='o_textinput' for='maxperfetch'><?php _e("Number of Total Post Entries per Fetch (<a href=\"http://www.allenweiss.com/faqs/how-does-the-number-of-entries-per-feed-and-page-or-fetch-work//\" target=\"_blank\">Go here to see how to set this option</a>)", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[maxperfetch]">
<OPTION VALUE="1" <?php if($post_options['maxperfetch']==1){echo 'selected';} ?>>1</OPTION>
<OPTION VALUE="2" <?php if($post_options['maxperfetch']==2){echo 'selected';} ?>>2</OPTION>
<OPTION VALUE="3" <?php if($post_options['maxperfetch']==3){echo 'selected';} ?>>3</OPTION>
<OPTION VALUE="4" <?php if($post_options['maxperfetch']==4){echo 'selected';} ?>>4</OPTION>
<OPTION VALUE="5" <?php if($post_options['maxperfetch']==5){echo 'selected';} ?>>5</OPTION>
<OPTION VALUE="10" <?php if($post_options['maxperfetch']==10){echo 'selected';} ?>>10</OPTION>
<OPTION VALUE="15" <?php if($post_options['maxperfetch']==15){echo 'selected';} ?>>15</OPTION>
<OPTION VALUE="20" <?php if($post_options['maxperfetch']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($post_options['maxperfetch']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="40" <?php if($post_options['maxperfetch']==40){echo 'selected';} ?>>40</OPTION>
<OPTION VALUE="50" <?php if($post_options['maxperfetch']==50){echo 'selected';} ?>>50</OPTION>
<OPTION VALUE="100" <?php if($post_options['maxperfetch']==100){echo 'selected';} ?>>100</OPTION>
<OPTION VALUE="200" <?php if($post_options['maxperfetch']==200){echo 'selected';} ?>>200</OPTION>
<OPTION VALUE="300" <?php if($post_options['maxperfetch']==300){echo 'selected';} ?>>300</OPTION>
</SELECT></p>


<h3><?php _e("Link Settings", 'wp-rss-multi-importer')?></h3>


<p><label class='o_textinput' for='targetWindow'><?php _e("Target Window (when link clicked, where should it open?)", 'wp-rss-multi-importer')?></label>
	<SELECT NAME="rss_post_options[targetWindow]" id="targetWindow">
	<OPTION VALUE="0" <?php if($post_options['targetWindow']==0){echo 'selected';} ?>><?php _e("Use LightBox", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="1" <?php if($post_options['targetWindow']==1){echo 'selected';} ?>><?php _e("Open in Same Window", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="2" <?php if($post_options['targetWindow']==2){echo 'selected';} ?>><?php _e("Open in New Window", 'wp-rss-multi-importer')?></OPTION>
	</SELECT></p>
	
		<p ><label class='o_textinput' for='titleFilter'><?php _e("Make title clickable on listing page with same settings as above", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_post_options[titleFilter]" Value="1" <?php if ($post_options['titleFilter']==1){echo 'checked="checked"';} ?></label></p>
	
	<p ><label class='o_textinput' for='readmore'><?php _e("Text to use for Read More (default is ...Read More)", 'wp-rss-multi-importer')?>   <input  id='readmore' type="text" size='18' Name="rss_post_options[readmore]" Value="<?php echo $post_options['readmore'] ?>"></label></p>
	
	

<h3><?php _e("Word Output Setting", 'wp-rss-multi-importer')?></h3>
<p><label class='o_textinput' for='descnum'><?php _e("Excerpt length (number of words)", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[descnum]" id="descnum">
<OPTION VALUE="0" <?php if($post_options['descnum']==0){echo 'selected';} ?>>0</OPTION>
<OPTION VALUE="20" <?php if($post_options['descnum']==20){echo 'selected';} ?>>20</OPTION>
<OPTION VALUE="30" <?php if($post_options['descnum']==30){echo 'selected';} ?>>30</OPTION>
<OPTION VALUE="50" <?php if($post_options['descnum']==50){echo 'selected';} ?>>50</OPTION>
<OPTION VALUE="100" <?php if($post_options['descnum']==100){echo 'selected';} ?>>100</OPTION>
<OPTION VALUE="200" <?php if($post_options['descnum']==200){echo 'selected';} ?>>200</OPTION>
<OPTION VALUE="300" <?php if($post_options['descnum']==300){echo 'selected';} ?>>300</OPTION>
<OPTION VALUE="400" <?php if($post_options['descnum']==400){echo 'selected';} ?>>400</OPTION>
<OPTION VALUE="500" <?php if($post_options['descnum']==500){echo 'selected';} ?>>500</OPTION>
<OPTION VALUE="1000" <?php if($post_options['descnum']==1000){echo 'selected';} ?>>1000</OPTION>
<OPTION VALUE="99" <?php if($post_options['descnum']==99){echo 'selected';} ?>><?php _e("Give me everything", 'wp-rss-multi-importer')?></OPTION>
</SELECT></p>

<h3><?php _e("Author and Source Settings", 'wp-rss-multi-importer')?></h3>
<p ><label class='o_textinput' for='addAuthor'><?php _e("Show Feed or Author Name (if available)", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_post_options[addAuthor]" Value="1" <?php if ($post_options['addAuthor']==1){echo 'checked="checked"';} ?></label></p>


<p ><label class='o_textinput' for='addSource'><?php _e("Show Feed Source", 'wp-rss-multi-importer')?>   <input type="checkbox" Name="rss_post_options[addSource]" Value="1" <?php if ($post_options['addSource']==1){echo 'checked="checked"';} ?></label></p>


<p style="padding-left:15px"><label class='o_textinput' for='sourceWords'><?php _e("Feed Source Attribution Label", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[sourceWords]">
<OPTION VALUE="1" <?php if($post_options['sourceWords']==1){echo 'selected';} ?>><?php _e("Source", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="2" <?php if($post_options['sourceWords']==2){echo 'selected';} ?>><?php _e("Via", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="3" <?php if($post_options['sourceWords']==3){echo 'selected';} ?>><?php _e("Read more here", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="4" <?php if($post_options['sourceWords']==4){echo 'selected';} ?>><?php _e("From", 'wp-rss-multi-importer')?></OPTION>
<OPTION VALUE="5" <?php if($post_options['sourceWords']==5){echo 'selected';} ?>><?php _e("Other (fill in below)", 'wp-rss-multi-importer')?></OPTION>
</SELECT></p>

<p style="padding-left:15px"><label class='o_textinput' for='sourceWords_Label'><?php _e("Your own attribution label", 'wp-rss-multi-importer')?>   <input  id='sourceWords_Label' type="text" size='12'  Name="rss_post_options[sourceWords_Label]" Value="<?php echo $post_options['sourceWords_Label'] ?>">(make sure to choose Other in drop down list)</label></p>

<p><label class='o_textinput' for='sourceAnchorText'><?php _e("Read More anchor text", 'wp-rss-multi-importer')?></label>
	<SELECT NAME="rss_post_options[sourceAnchorText]" id="sourceAnchorText">
	<OPTION VALUE="1" <?php if($post_options['sourceAnchorText']==1){echo 'selected';} ?>><?php _e("Feed Name", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="2" <?php if($post_options['sourceAnchorText']==2){echo 'selected';} ?>><?php _e("Title", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="3" <?php if($post_options['sourceAnchorText']==3){echo 'selected';} ?>><?php _e("Link", 'wp-rss-multi-importer')?></OPTION>
	</SELECT></p>


<h3><?php _e("HTML and Image Handling", 'wp-rss-multi-importer')?></h3>


<p><label class='o_textinput' for='stripAll'><?php _e("Check to get rid of all html and images in the excerpt", 'wp-rss-multi-importer')?>
	<SELECT NAME="rss_post_options[stripAll]" id="stripAll">
	<OPTION VALUE="1" <?php if($post_options['stripAll']==1){echo 'selected';} ?>><?php _e("Yes", 'wp-rss-multi-importer')?></OPTION>
	<OPTION VALUE="0" <?php if($post_options['stripAll']==0){echo 'selected';} ?>><?php _e("No", 'wp-rss-multi-importer')?></OPTION>
	</SELECT>
</p>







<span id="stripAllsecret" <?php if($post_options['stripAll']==1){echo 'style="display:none"';}?>>
	
	
	<p ><label class='o_textinput' for='stripSome'><?php _e("Eliminate all hyperlinks   ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[stripSome]" Value="1" <?php if ($post_options['stripSome']==1){echo 'checked="checked"';} ?></label> </p>

<p><label class='o_textinput' for='maximgwidth'><?php _e("Maximum width size of images", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[maximgwidth]">
<OPTION VALUE="100" <?php if($post_options['maximgwidth']==100){echo 'selected';} ?>>100px</OPTION>
<OPTION VALUE="150" <?php if($post_options['maximgwidth']==150){echo 'selected';} ?>>150px</OPTION>
<OPTION VALUE="250" <?php if($post_options['maximgwidth']==250){echo 'selected';} ?>>250px</OPTION>
<OPTION VALUE="350" <?php if($post_options['maximgwidth']==350){echo 'selected';} ?>>350px</OPTION>
<OPTION VALUE="500" <?php if($post_options['maximgwidth']==500){echo 'selected';} ?>>500px</OPTION>
<OPTION VALUE="999" <?php if($post_options['maximgwidth']==999){echo 'selected';} ?>><?php _e("unrestricted", 'wp-rss-multi-importer')?></OPTION>
</SELECT></p>

<p ><label class='o_textinput' for='RSSdefaultImage'><?php _e("Default category image setting", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[RSSdefaultImage]" id="RSSdefaultImage">
<OPTION VALUE="0" <?php if($post_options['RSSdefaultImage']==0){echo 'selected';} ?>>Process normally</OPTION>
<OPTION VALUE="1" <?php if($post_options['RSSdefaultImage']==1){echo 'selected';} ?>>Use default image for category</OPTION>
<OPTION VALUE="2" <?php if($post_options['RSSdefaultImage']==2){echo 'selected';} ?>>Replace articles with no image with default category image</OPTION>

</SELECT></p>




<p ><label class='o_textinput' for='setFeaturedImage'><?php _e("Select how to use the image (in excerpt and/or as the Featured Image).", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[setFeaturedImage]" id="setFeaturedImage">
<OPTION VALUE="0" <?php if($post_options['setFeaturedImage']==0){echo 'selected';} ?>>Excerpt Only</OPTION>
<OPTION VALUE="1" <?php if($post_options['setFeaturedImage']==1){echo 'selected';} ?>>Excerpt and Featured Image</OPTION>
<OPTION VALUE="2" <?php if($post_options['setFeaturedImage']==2){echo 'selected';} ?>>Featured Image Only</OPTION>
</SELECT></p>


</span>


<h3><?php _e("Get Social", 'wp-rss-multi-importer')?></h3>
<p ><label class='o_textinput' for='showsocial'><?php _e("Add social icons (Twitter and Facebook) to each post ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[showsocial]" Value="1" <?php if ($post_options['showsocial']==1){echo 'checked="checked"';} ?></label>
</p>

<h3><?php _e("Comment Status", 'wp-rss-multi-importer')?></h3>
<p ><label class='o_textinput' for='showsocial'><?php _e("Turn off comments on posts made by this plugin ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[commentstatus]" Value="1" <?php if ($post_options['commentstatus']==1){echo 'checked="checked"';} ?></label>
</p>

<h3><?php _e("Excerpt Handling", 'wp-rss-multi-importer')?></h3>
<p ><label class='o_textinput' for='includeExcerpt'><?php _e("Put the contents also in the excerpts field. ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[includeExcerpt]" Value="1" <?php if ($post_options['includeExcerpt']==1){echo 'checked="checked"';} ?></label>
</p>


<h3><?php _e("No Index, No Follow ", 'wp-rss-multi-importer')?></h3>
<p ><label class='o_textinput' for='noindex'><?php _e("Make the Feed to Post items not search engine visible (It is up to search engines to honor this request.). ", 'wp-rss-multi-importer')?><input type="checkbox" Name="rss_post_options[noindex]" Value="1" <?php if ($post_options['noindex']==1){echo 'checked="checked"';} ?></label>
</p>



<h3><?php _e("Auto Remove Posts", 'wp-rss-multi-importer')?></h3>

<p ><label class='o_textinput' for='autoDelete'><?php _e("Check to Auto Remove Posts Created by this Plugin", 'wp-rss-multi-importer')?>   <input type="checkbox" id="autoRemoveCB" Name="rss_post_options[autoDelete]" Value="1" <?php if ($post_options['autoDelete']==1){echo 'checked="checked"';} ?></label>   (<a href="/wp-admin/options-general.php?page=wp_rss_multi_importer_admin&tab=posts_list">Manage what posts to keep here.</a>)</p>

<span id="autoremoveposts" <?php if($post_options['autoDelete']!=1){echo 'style="display:none"';}?>>

<p ><label class='o_textinput' for='expiration'><?php _e("Select the expiration time (number of days, weeks, etc.) before removing posts", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[expiration]" id="expiration">
<OPTION VALUE="1" <?php if($post_options['expiration']==1){echo 'selected';} ?>>1 Day</OPTION>
<OPTION VALUE="2" <?php if($post_options['expiration']==2){echo 'selected';} ?>>2 Days</OPTION>
<OPTION VALUE="3" <?php if($post_options['expiration']==3){echo 'selected';} ?>>3 Days</OPTION>
<OPTION VALUE="4" <?php if($post_options['expiration']==4){echo 'selected';} ?>>4 Days</OPTION>
<OPTION VALUE="5" <?php if($post_options['expiration']==5){echo 'selected';} ?>>5 Days</OPTION>
<OPTION VALUE="6" <?php if($post_options['expiration']==6){echo 'selected';} ?>>6 Days</OPTION>
<OPTION VALUE="7" <?php if($post_options['expiration']==7){echo 'selected';} ?>>7 Days</OPTION>
<OPTION VALUE="14" <?php if($post_options['expiration']==14){echo 'selected';} ?>>2 Weeks</OPTION>
<OPTION VALUE="21" <?php if($post_options['expiration']==21){echo 'selected';} ?>>3 Weeks</OPTION>
<OPTION VALUE="28" <?php if($post_options['expiration']==28){echo 'selected';} ?>>4 Weeks</OPTION>
<OPTION VALUE="56" <?php if($post_options['expiration']==56){echo 'selected';} ?>>2 Months</OPTION>
</SELECT></p>

<p ><label class='o_textinput' for='oldPostStatus'><?php _e("Move posts to what status?", 'wp-rss-multi-importer')?></label>
<SELECT NAME="rss_post_options[oldPostStatus]" id="setFeaturedImage">
<OPTION VALUE="0" <?php if($post_options['oldPostStatus']==0){echo 'selected';} ?>>Permanently Delete</OPTION>
<OPTION VALUE="1" <?php if($post_options['oldPostStatus']==1){echo 'selected';} ?>>Trash (but don't permanently delete)</OPTION>
<OPTION VALUE="2" <?php if($post_options['oldPostStatus']==2){echo 'selected';} ?>>Pending</OPTION>
</SELECT><?php _e("  NOTE: Choosing Permanently Delete may result in posts being imported again", 'wp-rss-multi-importer')?></p>

</span>
<?php



$catOptions= get_option( 'rss_import_categories' ); 


	if ( !empty($catOptions) ) {
		echo "<h3><label class='o_textinput' for='category'>".__('Restrict feeds to one of your defined RSS Multi Importer categories and place them in your blog categories', 'wp-rss-multi-importer')."</label></h3>";
			echo "<p>".__('Choose a plugin category and associate it with one of your blog post categories.', 'wp-rss-multi-importer')."</p>";
				
	

echo '<div class="ftpost_head">Plugin Category --></div><div class="ftpost_head">Blog Post Category</div><div style="clear:both;"></div>';	
		$catsize = count($catOptions);
		$postoptionsize= $catsize/2;






		for ( $q=1; $q<=$postoptionsize; $q++ ){
			


		if ((isEmpty($post_options['categoryid']['wpcatid'][$q])==0) || $q==1){
		
		
			echo "<div class='category_id_options' id='$q'>";
			$selclear=0; // added
			}else{	
			echo "<div class='category_id_options' id='$q' style='display:none'>";
			$selclear=1; // added
			}
?>



<p><span class="ftpost_l"><SELECT NAME="rss_post_options[categoryid][plugcatid][<?php echo $q ?>]">
	<?php if ($selclear==1){  // added
	?>
	<OPTION selected VALUE=''>None</OPTION>
	<?php
}
if($q==1){
	?>
<OPTION VALUE='0' <?php if($post_options['categoryid']['plugcatid'][$q]==0){echo 'selected="selected"';} ?>>ALL</OPTION>
<?php
}

	for ( $k=1; $k<=$catsize; $k++) {   

if( $k % 2== 0 ) continue;

 	$catkey = key( $catOptions );
 	$nameValue=$catOptions[$catkey];
next( $catOptions );
 	$catkey = key( $catOptions );
	$IDValue=$catOptions[$catkey];


	 if($post_options['categoryid']['plugcatid'][$q]==$IDValue && $selclear==0){  // selclear added
		$sel='selected  ';

		} else {
		$sel='';

		}

echo "<OPTION " .$sel.  "VALUE=".$IDValue.">".$nameValue."</OPTION>";
next( $catOptions );

}
echo "</SELECT></span><span class='ftpost_r'>";




echo "<SELECT multiple='multiple' size='4' id='wpcategory2' NAME='rss_post_options[categoryid][wpcatid][$q][]'>";


catDropDown($post_options['categoryid']['wpcatid'][$q]);


echo "</SELECT></span></p></div>";






reset($catOptions);

}


echo "<a href='javascript:void(0)' class='add_cat_id'>Add another plugin to blog post category association</a>";



}else{
	
	echo __("<b>NOTE: If you set up categories (in Category Options) you can restrict only feeds in that category to go into blog posts.</b> ", 'wp-rss-multi-importer');
}

?>


</div></div>

       <p class="submit"><input type="submit" value="Save Settings" name="submit" class="button-primary"></p>



       </form>

<button type="button" name="fetchnow" id="fetch-now" value=""><?php _e("CLICK TO FETCH FEEDS NOW", 'wp-rss-multi-importer')?></button>	
<div id="note"></div>
	
</div></div>



</div>
<?php
}


function chk_zero_callback($val) {
    if ($val != null){
	return true;
}
}


function isEmpty_old($arr) {
	if(empty($arr)) return 1;
  foreach ($arr as $k => $v) {
    if ($v === '') {
      return 1;
    }
  }
  return 0;
}

function isEmpty($arr) {
	if(empty($arr)) return 1;
  foreach ($arr as $k => $v) {
    if ($v != '' && $v !='NULL') {
      return 0;
    }
  }
  return 1;
}

?>