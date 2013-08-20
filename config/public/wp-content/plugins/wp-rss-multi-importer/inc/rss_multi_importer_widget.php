<?php 

    
class WP_Multi_Importer_Widget extends WP_Widget {

	/**
	 * Register widget with WordPress.
	 */
	public function __construct() {
		parent::__construct(
	 		'rss_multi_importer_widget', // Base ID
			'RSS Multi-Importer', // Name
			array( 'description' => __( 'Use this to put RSS feeds on your site', 'text_domain' , 'wp-rss-multi-importer'), ) // Args
		);
	}

	/**
	 * Front-end display of widget.
	 *
	 * @see WP_Widget::widget()
	 *
	 * @param array $args     Widget arguments.
	 * @param array $instance Saved values from database.
	 */
	public function widget( $args, $instance ) {
		add_action('wp_footer','footer_scripts');
		
		/* Load the excerpt functions file. */
		
		global $maximgwidth;
		$maximgwidth=100;
		global $anyimage;  // to identify any image in description 
		$anyimage=1;
		require_once ( WP_RSS_MULTI_INC . 'excerpt_functions.php' );
		
		extract( $args );
		
		$siteurl= get_site_url();

			$widget_images_url = $siteurl . '/wp-content/plugins/wp-rss-multi-importer/images';
			
			
		$title = apply_filters( 'widget_title', $instance['title'] );
		$count = $instance['numoption'];

	(array) $catArray = $instance['category'];
	
		if (empty($catArray)) {
			$catArray=array("0");	
		}
	
		$sortDir = $instance['checkbox'];
		$showdate = $instance['showdate'];
		$showicon = $instance['showicon'];
		$linktitle = $instance['linktitle'];
		$showdesc = $instance['showdesc'];
		$maxposts = $instance['maxposts'];
		$targetwindow= $instance['targetwindow'];
		$simplelist= $instance['simplelist'];
		$showimage= $instance['showimage'];
		$showsource=$instance['showsource'];
		$descNum=$instance['descnum'];
		
		global $anyimage;
		$anyimage=1;
		
		global $RSSdefaultImage;
		$RSSdefaultImage=$instance['rssdefaultimage'];   // 0- process normally, 1=use default for category, 2=replace when no image available
		//$RSSdefaultImage=1;
		
		

		global $isMobileDevice;
		if (isset($isMobileDevice) && $isMobileDevice==1){  //open mobile device windows in new tab
			$targetwindow=2;

			}
		
		
		if (!empty($linktitle)){
			$title = '<a href="'.$linktitle.'">'.$title.'</a>';	
		}
		
		
		
		if ($showicon==1){
			$title=	'<img src="'.$widget_images_url.'/rss.png" width="14" height="14" style="border:0;margin-right:5px;">'.$title;
		}
		
		$addmotion = $instance['addmotion'];
		$background = $instance['background'];
		
		if($addmotion==1){
			add_action('wp_footer','widget_footer_scripts');		
		}
		
		if(!function_exists("wprssmi_hourly_feed")) {
		function wprssmi_hourly_feed() { return 3600; }
		}
	    add_filter( 'wp_feed_cache_transient_lifetime', 'wprssmi_hourly_feed' );
		
			
		if ($cb!=='1' && $targetwindow==0 ){
		add_action('wp_footer','colorbox_scripts');  // load colorbox only if not indicated as conflict
		   }
		
		if (empty( $sortDir ) ){$sortDir=0;}
	
		echo $before_widget;
		if ( ! empty( $title ) )
			echo $before_title . $title . $after_title;
	
		
		$readable = '';
	   	$options = get_option('rss_import_items','option not found');
	
	
	
		$cat_array = preg_grep("^feed_cat_^", array_keys($options));
		
	
		

			if (count($cat_array)==0) {  //for backward compatibility
				$noExistCat=1;
			}else{
				$noExistCat=0;	
			}
	
	
		$size = count($options);
		$targetWindow=$options['targetWindow']; 
		
	
	//	$sortDir=$options['sortbydate'];
		//$sortDir=0;
		
		for ($i=1;$i<=$size;$i=$i+1){



		   			$key =key($options);
						if ( !strpos( $key, '_' ) > 0 ) continue; //this makes sure only feeds are included here...everything else are options

		   			$rssName= $options[$key];


		   			next($options);

		   			$key =key($options);

		   			$rssURL=$options[$key];



		  	next($options);
			$key =key($options);


 $rssCatID=$options[$key]; 


	
	if (((!in_array(0, $catArray ) && in_array($options[$key], $catArray ))) || in_array(0, $catArray ) || $noExistCat==1) {


		   $myfeeds[] = array("FeedName"=>$rssName,"FeedURL"=>$rssURL,"FeedCatID"=>$rssCatID);   

		}

		$cat_array = preg_grep("^feed_cat_^", array_keys($options));  // for backward compatibility

			if (count($cat_array)>0) {

		  next($options); //skip feed category
		}

		   }


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

				continue;

			}

			$maxfeed= $feed->get_item_quantity(0);


		//SORT DEPENDING ON SETTINGS

			if($sortDir==1){

				for ($i=$maxfeed;$i>=$maxfeed-$maxposts;$i--){
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
					

						$myarray[] = array("mystrdate"=>strtotime($item->get_date()),"mytitle"=>$item->get_title(),"mylink"=>$item->get_link(),"myGroup"=>$feeditem["FeedName"],"mydesc"=>$item->get_content(),"myimage"=>$mediaImage,"mycatid"=>$feeditem["FeedCatID"]);
						
							unset($mediaImage);
						
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


							$myarray[] = array("mystrdate"=>strtotime($item->get_date()),"mytitle"=>$item->get_title(),"mylink"=>$item->get_link(),"myGroup"=>$feeditem["FeedName"],"mydesc"=>$item->get_content(),"myimage"=>$mediaImage,"mycatid"=>$feeditem["FeedCatID"]);
							
								unset($mediaImage);
							
						}	
				}


			}

			if (!isset($myarray) || empty($myarray)){

				return _e("There is a problem with the feeds you entered.  Go to our <a href='http://www.allenweiss.com/wp_plugin'>support page</a> and we'll help you diagnose the problem.", 'wp-rss-multi-importer');
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

		// HOW THE LINK OPENS
		
		
		global $isMobileDevice;
			if (isset($isMobileDevice) && $isMobileDevice==1){  //open mobile device windows in new tab
				$targetWindow=2;
				}

		if($targetwindow==0){
			$openWindow='class="colorbox"';
		}elseif ($targetwindow==1){
			$openWindow='target=_self';		
		}else{
			$openWindow='target=_blank';	
		}
		
		


$total = -1;





if ($simplelist==1){

	echo '<ul class="wprssmi_widget_list">';
	

	
		foreach($myarray as $items) {

		$total = $total +1;
			
		if ($count>0 && $total>=$count) break;
	
		echo '<li class="title"><a '.$openWindow.' href="'.$items["mylink"].'" '.($noFollow==1 ? 'rel=nofollow':'').'>'.$items["mytitle"].'</a>';
		if (!empty($items["mystrdate"])  && $showdate==1){
		echo '<span class="date">'. date_i18n("D, M d, Y",$items["mystrdate"]).'</span>';
	}
		
		echo '</li>';

	}  	//  don't mess with this php code
	
	
	
	
	
	
	echo '</ul>';	
	
	
} else{




echo ' <div class="news-wrapper" id="newsticker" style="10px;background-color:'.$background.';">';
echo '	<div class="news-contents">';

		foreach($myarray as $items) {


		
			$total = $total +1;
			if ($count>0 && $total>=$count) break;




			echo '<div style="top: 101px;margin-left:5px;" class="news">';
			echo '<p class="widget-rss-output" style="margin-right:5px">';
			
			
			
			
			if($showimage==1 && $addmotion!=1){
							
	
				echo showexcerpt($items["mydesc"],0,$openWindow,0,$items["mylink"],1,"left",0,$items["myimage"],$items["mycatid"]);
			
			}
			
			echo '<a '.$openWindow.' href="'.$items["mylink"].'">'.$items["mytitle"].'</a><br />';
			
		
				
			
			
			
			if ($showdesc==1 && $addmotion!=1){

							
						$desc= esc_attr(strip_tags(@html_entity_decode($items["mydesc"], ENT_QUOTES, get_option('blog_charset'))));	
						$desc= str_replace('[...]','',$desc);
						
					    $words = explode(" ",trim($desc));
						
						
					   	$desc= implode(" ",array_splice($words,0,$descNum));	
						
								
						$desc .= ' <a '.$openWindow.' href="'.$items["mylink"].'">[&hellip;]</a>';
			
							
			echo $desc.'<br/>';
			}
			
			
			
			
			
			

			if (!empty($items["mystrdate"])  && $showdate==1){
			 echo  date_i18n("D, M d, Y",$items["mystrdate"]).'<br />';
		
			
			}
				if (!empty($items["myGroup"]) && $showsource==1){
		    echo '<span style="font-style:italic;">'.$attribution.''.$items["myGroup"].'</span>';
			}
			 echo '</p>';
			echo '</div>';

		}

	echo '</div></div>';
		
	
	
	
	
	}
	
	
	

	
	
	
	
		
		

		echo $after_widget;	
	}

	/**
	 * Sanitize widget form values as they are saved.
	 *
	 * @see WP_Widget::update()
	 *
	 * @param array $new_instance Values just sent to be saved.
	 * @param array $old_instance Previously saved values from database.
	 *
	 * @return array Updated safe values to be saved.
	 */
	public function update( $new_instance, $old_instance ) {
		//$instance = array();
			$instance = $new_instance;
		
		$instance['title'] = strip_tags( $new_instance['title'] );
		$instance['checkbox'] = strip_tags($new_instance['checkbox']);
		$instance['numoption'] = strip_tags($new_instance['numoption']);
		$instance['addmotion'] = strip_tags($new_instance['addmotion']);
		$instance['background'] = strip_tags($new_instance['background']);
		$instance['showdate'] = strip_tags($new_instance['showdate']);
		$instance['showicon'] = strip_tags($new_instance['showicon']);
		$instance['linktitle'] = strip_tags($new_instance['linktitle']);
		$instance['showdesc'] = strip_tags($new_instance['showdesc']);		
		$instance['maxposts'] = strip_tags($new_instance['maxposts']);	
		$instance['targetwindow'] = strip_tags($new_instance['targetwindow']);
		$instance['simplelist'] = strip_tags($new_instance['simplelist']);	
		$instance['showimage'] = strip_tags($new_instance['showimage']);	
		$instance['rssdefaultimage'] = strip_tags($new_instance['rssdefaultimage']);
		$instance['showsource'] = strip_tags($new_instance['showsource']);
		$instance['descnum'] = strip_tags($new_instance['descnum']);
		return $instance;
	}

	/**
	 * Back-end widget form.
	 *
	 * @see WP_Widget::form()
	 *
	 * @param array $instance Previously saved values from database.
	 */
	public function form( $instance ) {
		
		
		//Defaults
		$defaults = array(
			'title' => __( 'RSS Feeds', $this->textdomain, 'wp-rss-multi-importer'),
			'checkbox' => 0,
			'category' => array(),
			'exclude' => array(),
			'numoption' => 2,
			'maxposts' =>1,
			'addmotion' => 0,
			'showdate' => 1,
			'simplelist'=>0,
			'showicon' => 0,
			'linktitle' => '',
			'targetwindow' => 0,
			'showdesc' => 0,
			'showsource'=>1,
			'rssdefaultimage' =>0,
			'showimage' => 0,
			'descnum' =>10,
			'background' => '#ffffff',
		);
		

			$instance = wp_parse_args( (array) $instance, $defaults );
		
		$rssdefaultimage=esc_attr($instance['rssdefaultimage']);
	    $title = esc_attr($instance['title']);
		$checkbox = esc_attr($instance['checkbox']);
		$numoption = esc_attr($instance['numoption']);	
		$addmotion = esc_attr($instance['addmotion']);	
		$background = esc_attr($instance['background']);
		$showdate = esc_attr($instance['showdate']);
		$showicon = esc_attr($instance['showicon']);
		$linktitle = esc_attr($instance['linktitle']);
		$showdesc = esc_attr($instance['showdesc']);
		$maxposts = esc_attr($instance['maxposts']);
		$targetwindow = esc_attr($instance['targetwindow']);
		$simplelist= esc_attr($instance['simplelist']);
		$showimage= esc_attr($instance['showimage']);
		$showsource=esc_attr($instance['showsource']);
		$descnum=esc_attr($instance['descnum']);
		settings_fields( 'wp_rss_multi_importer_categories' );
		$options = get_option('rss_import_categories' );
		
	    ?>

		 <p>
	      	<label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Widget Title', 'wp-rss-multi-importer'); ?></label>
	      	<input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo $title; ?>" />
	    </p>
	
			<p>
		      	<input id="<?php echo $this->get_field_id('showicon'); ?>" name="<?php echo $this->get_field_name('showicon'); ?>" type="checkbox" value="1" <?php checked( '1', $showicon ); ?>/>
		    	<label for="<?php echo $this->get_field_id('showicon'); ?>"><?php _e('Show RSS icon', 'wp-rss-multi-importer'); ?></label>
		    </p>

			 <p>
		      	<label for="<?php echo $this->get_field_id('linktitle'); ?>"><?php _e('URL to link title to another page (optional)', 'wp-rss-multi-importer'); ?></label>
		      	<input class="widefat" id="<?php echo $this->get_field_id('linktitle'); ?>" name="<?php echo $this->get_field_name('linktitle'); ?>" type="text" value="<?php echo $linktitle; ?>" />
		    </p>
			
		
			
		<p>
				
					<label for="<?php echo $this->get_field_id('targetwindow'); ?>"><?php _e('Target Window', 'wp-rss-multi-importer'); ?></label>
					
					
						
				
				<select name="<?php echo $this->get_field_name('targetwindow'); ?>">

			
			<OPTION ID="0" VALUE="0" <?php if($targetwindow==0){echo 'selected="selected"';} ?>>Use LightBox</OPTION>
				<OPTION ID="1" VALUE="1" <?php if($targetwindow==1){echo 'selected="selected"';} ?>>Open in Same Window</OPTION>
				<OPTION ID="2" VALUE="2" <?php if($targetwindow==2){echo 'selected="selected"';} ?>>Open in New Window</OPTION>
				</SELECT>	
			</p>
			
		

		<p>
	      	<input id="<?php echo $this->get_field_id('checkbox'); ?>" name="<?php echo $this->get_field_name('checkbox'); ?>" type="checkbox" value="1" <?php checked( '1', $checkbox ); ?>/>
	    	<label for="<?php echo $this->get_field_id('checkbox'); ?>"><?php _e('Check to sort ascending', 'wp-rss-multi-importer'); ?></label>
	    </p>
	
		<p>
	      	<input id="<?php echo $this->get_field_id('showdate'); ?>" name="<?php echo $this->get_field_name('showdate'); ?>" type="checkbox" value="1" <?php checked( '1', $showdate ); ?>/>
	    	<label for="<?php echo $this->get_field_id('showdate'); ?>"><?php _e('Show date', 'wp-rss-multi-importer'); ?></label>
	    </p>

		<p>
	      	<input id="<?php echo $this->get_field_id('showdesc'); ?>" name="<?php echo $this->get_field_name('showdesc'); ?>" type="checkbox" value="1" <?php checked( '1', $showdesc ); ?>/>
	    	<label for="<?php echo $this->get_field_id('showdesc'); ?>"><?php _e('Show excerpt (will not show if scrolling)', 'wp-rss-multi-importer'); ?></label>
	    </p>
		
		
		<p>
	      	<input id="<?php echo $this->get_field_id('showimage'); ?>" name="<?php echo $this->get_field_name('showimage'); ?>" type="checkbox" value="1" <?php checked( '1', $showimage ); ?>/>
	    	<label for="<?php echo $this->get_field_id('showimage'); ?>"><?php _e('Show image (will not show if scrolling)', 'wp-rss-multi-importer'); ?></label>
	    </p>
		
		
		<p>
	      	<input id="<?php echo $this->get_field_id('showsource'); ?>" name="<?php echo $this->get_field_name('showsource'); ?>" type="checkbox" value="1" <?php checked( '1', $showsource ); ?>/>
	    	<label for="<?php echo $this->get_field_id('showsource'); ?>"><?php _e('Show feed source)', 'wp-rss-multi-importer'); ?></label>
	    </p>


		<p >	<label for="<?php echo $this->get_field_id('rssdefaultimage'); ?>"><?php _e('Default category image setting', 'wp-rss-multi-importer'); ?></label>
		<select name="<?php echo $this->get_field_name('rssdefaultimage'); ?>">	
			
		<OPTION VALUE="0" <?php if ($rssdefaultimage==0){echo 'selected';} ?>>Process normally</OPTION>
		<OPTION VALUE="1" <?php if ($rssdefaultimage==1){echo 'selected';} ?>>Only use default image</OPTION>
		<OPTION VALUE="2" <?php if ($rssdefaultimage==2){echo 'selected';} ?>>When no image, use default</OPTION>

		</SELECT></p>


		<p >	<label for="<?php echo $this->get_field_id('descnum'); ?>"><?php _e('Words in excerpt', 'wp-rss-multi-importer'); ?></label>
		<select name="<?php echo $this->get_field_name('descnum'); ?>">	
			
		<OPTION VALUE="0" <?php if ($descnum==0){echo 'selected';} ?>>None</OPTION>
		<OPTION VALUE="10" <?php if ($descnum==10){echo 'selected';} ?>>10</OPTION>
		<OPTION VALUE="20" <?php if ($descnum==20){echo 'selected';} ?>>20</OPTION>
		<OPTION VALUE="30" <?php if ($descnum==30){echo 'selected';} ?>>30</OPTION>
		<OPTION VALUE="40" <?php if ($descnum==40){echo 'selected';} ?>>40</OPTION>
		<OPTION VALUE="50" <?php if ($descnum==50){echo 'selected';} ?>>50</OPTION>
		</SELECT></p>





	
		<p>
	      	<input id="<?php echo $this->get_field_id('addmotion'); ?>" name="<?php echo $this->get_field_name('addmotion'); ?>" type="checkbox" value="1" <?php checked( '1', $addmotion ); ?>/>
	    	<label for="<?php echo $this->get_field_id('addmotion'); ?>"><?php _e('Check to add scrolling motion', 'wp-rss-multi-importer'); ?></label>
	    </p>
	
			<p>
		      	<input id="<?php echo $this->get_field_id('simplelist'); ?>" name="<?php echo $this->get_field_name('simplelist'); ?>" type="checkbox" value="1" <?php checked( '1', $simplelist ); ?>/>
		    	<label for="<?php echo $this->get_field_id('simplelist'); ?>"><?php _e('Check to get just a simple unordered list', 'wp-rss-multi-importer'); ?></label>
		    </p>
		
		
		<p>
			<label for="<?php echo $this->get_field_id('category'); ?>"><?php _e('Which category do you want displayed?', 'wp-rss-multi-importer'); ?></label>
			<select name="<?php echo $this->get_field_name('category'); ?>[]" id="<?php echo $this->get_field_id('category'); ?>" class="widefat" multiple="multiple">
				<option id="All" value="0" <?php echo in_array(0, (array) $instance['category'] ) ? ' selected="selected"' : ''?>>ALL CATEGORIES</option>
				<?php
					if ( !empty($options) ) {
						$size = count($options);
			
							for ( $i=1; $i<=$size; $i++ ) {   
									if( $i % 2== 0 ) continue;
										$key = key( $options );
											if ( strpos( $key, 'cat_name_' ) === 0 ) { $j = str_replace( 'cat_name_', '', $key );}
				
				$optionName=$options[$key];
				next( $options );
				 $key = key( $options );
				$optionValue=$options[$key];				
					
					echo '<option value="' . $optionValue . '" id="' . $optionName . '"', in_array( $optionValue, (array) $instance['category'] ) ? ' selected="selected"' : '', '>', $optionName, '</option>';
					
					
					
						next( $options );
				}
			}
				?>
			</select>
			<p>
					<label for="<?php echo $this->get_field_id('numoption'); ?>"><?php _e('How many total results displayed?', 'wp-rss-multi-importer'); ?></label>
					<select name="<?php echo $this->get_field_name('numoption'); ?>" id="<?php echo $this->get_field_id('numoption'); ?>" class="widefat">
						<?php
						$myoptions = array('2','5','6','7', '8', '10', '15','20','50');
						foreach ($myoptions as $myoption) {
							echo '<option value="' . $myoption . '" id="' . $myoption . '"', $numoption == $myoption ? ' selected="selected"' : '', '>', $myoption, '</option>';
						}
						?>
					</select>
				</p>
				
				
				
				<p>
						<label for="<?php echo $this->get_field_id('maxposts'); ?>"><?php _e('How many posts per feed?', 'wp-rss-multi-importer'); ?></label>
						<select name="<?php echo $this->get_field_name('maxposts'); ?>" id="<?php echo $this->get_field_id('maxposts'); ?>" class="widefat">
							<?php
							$postoptions = array('1','2', '3', '4', '5','6');
							foreach ($postoptions as $postoption) {
								echo '<option value="' . $postoption . '" id="' . $postoption . '"', $maxposts == $postoption ? ' selected="selected"' : '', '>', $postoption, '</option>';
							}
							?>
						</select>
					</p>
					<script type="text/javascript">
								//<![CDATA[
									jQuery(document).ready(function()
									{
										// colorpicker field
										jQuery('.cw-color-picker').each(function(){
											var $this = jQuery(this),
												id = $this.attr('rel');

											$this.farbtastic('#' + id);
										});

									});
								//]]>   
							  </script>
				<p>
					 <label for="<?php echo $this->get_field_id('background'); ?>"><?php _e('Background Color:', 'wp-rss-multi-importer'); ?></label> 
					 <input class="widefat" id="<?php echo $this->get_field_id('background'); ?>" name="<?php echo $this->get_field_name('background'); ?>" type="text" value="<?php if($background) { echo $background; } else { echo '#cccccc'; } ?>" />
					<div class="cw-color-picker" rel="<?php echo $this->get_field_id('background'); ?>"></div>
							
					        </p>
					  
			
				
			
		<?php 
	}

} // class WP_Multi_Importer_Widget


?>