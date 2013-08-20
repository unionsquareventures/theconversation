/*

  JQuery code to add or remove option fields

*/



jQuery(function() { // when document has loaded


//get last feed number, if one exists, else set to 0

	var z=jQuery('div.wprss-input').size();
		if (z==0){
			var  i=0;
		}else{
			var i = (jQuery('div.wprss-input').get(-1).id);
		}
	i=parseInt(i)+1;
	var delstr=add_remove_parms;

	jQuery('a#add').click(function() { // when you click the add link				

		jQuery( "<div class='wprss-input'"+i+"'  id="+i+"><p><label class='textinput' for='feed_name_" + i + "'>Feed Name " + i + "</label>" +

		        "<input id='feed_name_" + i + "' class='wprss-input' size='100' name='rss_import_items[feed_name_" + i + "]' type='text' value='' /> <a href='#' class='btnDeleteNew' id='"+i+"'>"+delstr.delfeed+"</a></p>" +

			"<p><label class='textinput' for='feed_url_" + i + "'>Feed URL " + i + "</label>" +
			
			"<input id='urlid' class='url-item' size='100' name='rss_import_items[feed_url_" + i + "]' type='text' value='' />"+
			
			"<input id=''feed_cat_" + i + "' class='url-item' size='100' name='rss_import_items[feed_cat_" + i + "]' type='hidden' value='0' />"+			
			
			"<span id='errormsg'></span></p></div>")

			.fadeIn('slow').insertBefore('div#buttons');

		// append (add) a new input to the document.

		i++; //after the click i will increment up		

	});
	
	
	jQuery('a#addCat').click(function() { 
	//	alert('hello');
		
		var z=jQuery('div.cat-input').size();
			if (z==0){
				var  i=0;
			}else{
				var i = (jQuery('div.cat-input').get(-1).id);
			}
		i=parseInt(i)+1;
		
		
	
		
		jQuery( "<div class='cat-input'"+i+"'  id="+i+"><p><label class='textinput' for='cat_name_" + i + "'>Category Name</label>" +

		        "<input id='cat_name_" + i + "' class='cat-input' size='25' name='rss_import_categories[cat_name_" + i + "]' type='text' value='' /> <input id='cat_name_" + i + "' class='cat-input' size='25' name='rss_import_categories[id_" + i + "]' type='hidden' value="+ i+" /><a href='#' class='btnDeleteNew' id='"+i+"'>"+delstr.delcat+"</a></p>" +


			
			"</div>")

			.fadeIn('slow').insertBefore('div#category');

		// append (add) a new input to the document.

		i++; //after the click i will increment up
		
	
	});
	
	
	jQuery(".btnDelete").click(function() {
        var $id =this.id;
        jQuery('div').remove('#'+$id); 
    });


});

    jQuery(document).on('change', '.url-item', function() {
       //alert(isvalidurl(jQuery(this).val()));  //for testing
        var $messageDiv = jQuery('#errormsg');
		var urlprob=add_remove_parms;
        if (isvalidurl(jQuery(this).val())) { 
        	jQuery(this).removeClass("errorfld");
        	$messageDiv.hide().html('');
        }
        else 
       	 {
       	 	jQuery(this).addClass("errorfld") ;
			$messageDiv.show().html(urlprob.urlcheck);
        };
    });

    function isvalidurl(url) {
        var regexp = /(ftp|http|https|Http|Https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
        return regexp.test(url);
    }










 jQuery(document).on('change', '.default-cat-image', function() {


this.value = jQuery.trim(this.value);

//alert(isValidImage(jQuery(this).val()));

  });

	function isValidImage(url) {
      var regexp = /^(http|https):\/\/(.*)\.(gif|png|jpg|jpeg)?/;
      return regexp.test(url);
  }








	jQuery(document).on('click', '.btnDeleteNew', function() {  //this removes any new feeds not saved
	var $id =this.id;
       jQuery('div').remove('#'+$id); 
    });



   jQuery(document).on('change', '#showdesc', function() {       
    if(jQuery(this).val() == 1){
		jQuery('span#secret').show();
	}else{
		jQuery('span#secret').hide()};
 });


   jQuery(document).on('change', '#stripAll', function() {       
    if(jQuery(this).val() == 1){
		jQuery('span#stripAllsecret').hide();
	}else{
		jQuery('span#stripAllsecret').show()};
 });




  jQuery(document).on('change', '#pagination', function() {       
     if(jQuery('#pagination').val() == 1){
//alert("hello");
		jQuery('span#pag_options').show();
	}else{
		jQuery('span#pag_options').hide()};
    });




   jQuery(document).on('change', '.cat-input', function() {
	 this.value = this.value.toUpperCase();
	    });
	
	
	jQuery(document).on('change', '#feedslug',function() {
		this.value = this.value.replace(/ /g,'');
				
	});
	
	
	jQuery(document).on('change', '#wpcategory',function() {
		var chkstr=add_remove_parms;
		var intRegex = /^\d+$/;
		this.value = this.value.replace(/ /g,'');
		if(!intRegex.test(this.value)&& this.value!=''){
		alert(chkstr.intcheck);
		jQuery("#wpcategory").val('');
		} 		
	});
	
	
	jQuery(document).on('change', '#bloguserid',function() {
		var chkstr=add_remove_parms;
		var intRegex = /^\d+$/;
		this.value = this.value.replace(/ /g,'');
		if(!intRegex.test(this.value)&& this.value!=''){
		alert(chkstr.intcheck);
		jQuery("#bloguserid").val('');
		} 		
	});
	
	
	
	jQuery(document).ready( function( $ ){		
		jQuery(".add_cat_id").click(function() {
			
		//	var p= $('div.category_id_options:not([style*="display:none"])').length;
	      //  var $id =p+1;
	
	var $id = $('div.category_id_options[style*="display:none"]').first().attr('id');
	if ($id ==undefined)
		{
	alert("You need to add another plugin category before you can associate it with a blog post category.");
		}	
	
			jQuery('#'+$id).show("slow");	
	    });
			});
	
	
	
	jQuery(document).on('click', '#autoRemoveCB',function() {
		if (jQuery('#autoRemoveCB').is(':checked')) {
			jQuery('#autoremoveposts').show();
				}else{
			jQuery('#autoremoveposts').hide();
				}	
		});
	
	
