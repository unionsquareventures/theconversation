jQuery( 'document' ).ready( function( $ ){
jQuery('.nav-toggle').click(function(){
	var collapse_content_selector = $(this).attr('id');	
	
	var toggle_switch = $(this);
	$(collapse_content_selector).toggle(function(){
	  if($(this).css('display')=='none'){
		
      	toggle_switch.attr("src", toggle_switch.attr("src").replace("up", "down"));

	  }else{
 
		toggle_switch.attr("src", toggle_switch.attr("src").replace("down", "up"));
	
	  }
	});
});
});