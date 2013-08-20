<?php
	
		$readable.="<ul class='wprssmi_bullet_list'>";
	//  don't mess with this php code 
	foreach($myarray as $items) {

	if ($pag!==1){ 	
		$total = $total +1;
		if ($maxperPage>0 && $total>=$maxperPage) break;
	}

	$idnum=$idnum +1;
	//  END don't mess with this php code 
	
	

	$readable .= '<li class="title"><a '.$openWindow.' href='.$items["mylink"].' '.($noFollow==1 ? 'rel=nofollow':'').'">'.$items["mytitle"].'</a>  <span class="date">'. date_i18n("D, M d, Y",$items["mystrdate"]).'</span></li>';

	
	

}  	//  don't mess with this php code 

		$readable.="</ul>";					



?>