<?php
	
	
	//  don't mess with this php code 
	foreach($myarray as $items) {

	if ($pag!==1){ 	
		$total = $total +1;
		if ($maxperPage>0 && $total>=$maxperPage) break;
	}

	$idnum=$idnum +1;
	//  END don't mess with this php code 
	
	
	
	
	$readable .= '<div class="wprssmi-cs-items">';
//	$readable .= '<div class="title"><a '.$openWindow.' href='.$items["mylink"].' '.($noFollow==1 ? 'rel=nofollow':'').'>'.$items["mytitle"].'</a>';
	
$readable .= '<div class="title"><a '.$openWindow.' href='.$items["mylink"].' title="'.$items["mytitle"].'" '.($noFollow==1 ? 'rel=nofollow':'').'>'.$items["mytitle"].'</a>';


if(!empty($items["myAuthor"])){
 $readable .=  '<br><span style="font-style:italic; font-size:16px;">from <a '.$openWindow.' href='.$items["mylink"].' '.($noFollow==1 ? 'rel=nofollow':'').'">'.$items["myAuthor"].'</a></span>';  ///this is testing
	}
	
	if ($showmore==1 && $showDesc==1){
		
		$readable .=  ' <a href="javascript:void(0)"><img src="'.$images_url.'/arrow_down.png"/  id="#'.$idnum.'" class="nav-toggle"></a></div>';	
		
	} else{
		
		$readable .=  '</div>';	
	}
		
if (!empty($items["mydesc"]) && $showDesc==1){
	
	
	
	if ($showmore==1 && $showDesc==1){
		$readable .=  '<div id="'.$idnum.'" style="display:none">';
	}else{
		$readable .=  '<div class="body">';		
	}
	
	
$readable .=  showexcerpt($items["mydesc"],$descNum,$openWindow,$stripAll,$items["mylink"],$adjustImageSize,$float,$noFollow,$items["myimage"],$items["mycatid"]);

$readable .=  '</div>';	
	
}
	
	

	
	$readable .= '<div class="wprssmi-cs-source">'.date_i18n("D, M d, Y g:i:s A",$items["mystrdate"]).', Continue reading <a '.$openWindow.' href='.$items["mylink"].' '.($noFollow==1 ? 'rel=nofollow':'').'">at the source</a></div></div>';
	
	
	
	
	

}  	//  don't mess with this php code 

						



?>