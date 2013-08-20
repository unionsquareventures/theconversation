<script type="text/javascript">
jQuery(function(){
	jQuery('#news-container').vTicker({ 
		speed: 700,  //speed
		pause: 4000,
		animation: 'fade',
		mousePause: false,
		direction: 'down',
		showItems: 3  //number of items
	});
});
</script>



<?php

$charstoshow=50;  //  This number can be changed..indicates how many characters of the excerpt to show

	
			add_action('wp_footer','footer_scripts');  //  Don't mess with this
			add_action('wp_footer','vertical_scroll_footer_scripts'); //  Don't mess with this
		
		
			$readable .=  '	<div  id="news-container" class="v_scroller"><ul class="wprssmi_rss_vs">';
			
			
				
	//  don't mess with this php code 
	$addmotion=1;			
	$showdesc=1;
	foreach($myarray as $items) {

	if ($pag!==1){ 	
		$total = $total +1;
		if ($maxperPage>0 && $total>=$maxperPage) break;
	}

	$idnum=$idnum +1;
	//  END don't mess with this php code 
	
	
	
	
	
				$readable .=  '<li><div>';
				$readable .=  '<div class="title"><a '.$openWindow.' href='.$items["mylink"].'>'.$items["mytitle"].'</a></div>';
			
			if ($showdesc==1){
			
						$desc= esc_attr(strip_tags(@html_entity_decode($items["mydesc"], ENT_QUOTES, get_option('blog_charset'))));
						$desc = wp_html_excerpt( $desc, $charstoshow );
						if ( '[...]' == substr( $desc, -5 ) )
							$desc = substr( $desc, 0, -5 ) . '[&hellip;]';
							elseif ( '[&hellip;]' != substr( $desc, -10 ) )
								$desc .= ' [&hellip;]';
							$desc = esc_html( $desc );
				$readable .=  $desc.'<br/>';
			}

			if (!empty($items["mystrdate"])  && $showdate==1){
			 	$readable .=   date_i18n("D, M d, Y",$items["mystrdate"]).'<br />';
			}
				if (!empty($items["myGroup"])){
		    	$readable .=  '<span style="font-style:italic;">'.$attribution.''.$items["myGroup"].'</span>';
			}
			 
				$readable .=  '</div></li>';

		}

		$readable .=  '</ul></div>';
	
	
	


						



?>