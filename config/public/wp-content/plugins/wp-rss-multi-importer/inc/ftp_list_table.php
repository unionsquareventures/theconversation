<?php



if( ! class_exists( 'WP_List_Table' ) ) {
    require_once( ABSPATH . 'wp-admin/includes/class-wp-list-table.php' );
}

class My_List_Table extends WP_List_Table {
	
    
    function __construct(){
    global $status, $page;

        parent::__construct( array(
            'singular'  => __( 'post', 'mylisttable' ),     //singular name of the listed records
            'plural'    => __( 'posts', 'mylisttable' ),   //plural name of the listed records
            'ajax'      => false        //does this table support ajax?

    ) );

    add_action( 'admin_head', array( &$this, 'admin_header' ) );            

    }

  function admin_header() {
    $page = ( isset($_GET['page'] ) ) ? esc_attr( $_GET['page'] ) : false;
    if( 'wp_rss_multi_importer_admin' != $page )

    return;

    echo '<style type="text/css">';
    echo '.wp-list-table .column-id { width: 5%; }';
    echo '.wp-list-table .column-posttitle { width: 60%; font-weight: bold !important; font-size: 14px;}';
	echo '.wp-list-table .column-posttitle .delete {font-weight: normal; font-size: 12px;}';
	echo '.wp-list-table .column-posttitle .view {font-weight: normal; font-size: 12px;}';
	echo '.wp-list-table .column-posttitle .readydelete {font-weight: normal; font-size: 12px;}';
    echo '.wp-list-table .column-postdate { width: 20%; }';
    echo '.wp-list-table .column-postid { width: 10%;}';
 	echo '.wp-list-table .column-postprotect { width: 10%;}';
    echo '</style>';
  }

  function no_items() {
    _e( 'No posts found.' );
  }

  function column_default( $item, $column_name ) {
    switch( $column_name ) { 
        case 'posttitle':
        case 'postdate':
        case 'postid':
		case 'postprotect':
            return $item[ $column_name ];
        default:
            return print_r( $item, true ) ; //Show the whole array for troubleshooting purposes
    }
  }

function get_sortable_columns() {
  $sortable_columns = array(
    'posttitle'  => array('posttitle',false),
    'postdate' => array('postdate',false),
    'postid'   => array('postid',false),
	'postprotect'=> array('postprotect',false)
  );
  return $sortable_columns;
}

function get_columns(){
        $columns = array(
            'cb'        => '<input type="checkbox" />',
            'posttitle' => __( 'Post Title', 'mylisttable' ),
            'postdate'    => __( 'Post Date', 'mylisttable' ),
            'postid'      => __( 'Time Until Deletion', 'mylisttable' ),
 			'postprotect'      => __( 'Do Not Delete', 'mylisttable' )
        );
         return $columns;
    }

function usort_reorder( $a, $b ) {
  // If no sort, default to title
  $orderby = ( ! empty( $_GET['orderby'] ) ) ? $_GET['orderby'] : 'postdate';
  // If no order, default to asc
  $order = ( ! empty($_GET['order'] ) ) ? $_GET['order'] : 'asc';
  // Determine sort order
  $result = strcmp( $a[$orderby], $b[$orderby] );
  // Send final sort direction to usort
  return ( $order === 'asc' ) ? $result : -$result;
}

function column_posttitle($item){
  $actions = array(
            'delete'    => sprintf('<a href="?page=%s&tab=posts_list&action=%s&post=%s&paged=%s">Do Not Delete</a>',$_REQUEST['page'],'preserve',$item['ID'],$_GET['paged']),
			'view'    => sprintf('<a href="%s">View</a>',$item['guid']),
        );

		if($item['postprotect']){ $actions['readydelete'] = sprintf('<a href="?page=%s&tab=posts_list&action=%s&post=%s&paged=%s">Auto Delete</a>',$_REQUEST['page'],'readydelete',$item['ID'],$_GET['paged']); }

  return sprintf('%1$s %2$s', $item['posttitle'], $this->row_actions($actions) );
}

function get_bulk_actions() {
  $actions = array(
    'delete'    => 'Do Not Delete'
  );
  return $actions;
}





function process_bulk_action() {
        if( 'delete'===$this->current_action() ) {
            foreach($_POST['post'] as $post) {
                delete_single_meta_post($post);
           }
		}
    }







function column_cb($item) {
        return sprintf(
            '<input type="checkbox" name="post[]" value="%s" />', $item['ID']
        );    
    }

function prepare_items() {
	$search = trim($_POST['s']);
  	global $wpdb;
  	$columns  = $this->get_columns();
  	$hidden   = array();
  	$sortable = $this->get_sortable_columns();
  	$this->_column_headers = array( $columns, $hidden, $sortable );
  
 	$this->process_bulk_action();

	$post_options_delete = get_option('rss_post_options');
	$expSetting=$post_options_delete['expiration'];
	$autoDelete=$post_options_delete['autoDelete'];
	$serverTimezone=$post_options_delete['timezone'];
	if (isset($serverTimezone) && $serverTimezone!=''){  //set time zone
		date_default_timezone_set($serverTimezone);
		$rightNow=date("Y-m-d H:i:s", time());
	}else{
		$rightNow=date("Y-m-d H:i:s", time());
	}
	
	
	$expiration=-2;  //GET ALL POSTS


	if ($search != NULL){
	
	
		$query = "SELECT ID, post_date, post_title, guid FROM $wpdb->posts WHERE post_status = 'publish' AND post_type = 'post' AND `post_title` LIKE '%$search%' AND DATEDIFF(NOW(), `post_date`) > ".$expiration. " AND ID IN (SELECT post_id FROM $wpdb->postmeta WHERE meta_key = 'rssmi_source_link')";	
		
	
		
	}else{
	
		$query = "SELECT ID, post_date, post_title, guid FROM $wpdb->posts WHERE post_status = 'publish' AND post_type = 'post' AND DATEDIFF(NOW(), `post_date`) > ".$expiration. " AND ID IN (SELECT post_id FROM $wpdb->postmeta WHERE meta_key = 'rssmi_source_link')";
		

		
	}



	$this->items = $wpdb->get_results($query);
		
	$ids = $this->items;
	
	if (empty($ids)) return;

foreach ($ids as $id){
	
	if ($autoDelete==1){
		
			$timeToExpire=getDateUntil(strtotime($id->post_date),$expSetting);

		}else{
			$timeToExpire='n/a';
		}
		
		
	if (get_post_meta($id->ID, 'rssmi_source_protect', true)){$protectThis='<span style="color:green;">TRUE</span>';$timeToExpire='n/a';}else{$protectThis='';}
	
			
			$data[]=array("ID" => $id->ID,"postdate"=>$id->post_date,"posttitle"=>$id->post_title, "postid"=>$timeToExpire,'guid'=>$id->guid,'postprotect'=>$protectThis);
			unset($timeToExpire);		
}
  

 	$this->example_data =$data;
  
  	usort( $this->example_data, array( &$this, 'usort_reorder' ) );
  
  	$per_page = 10;
  	$current_page = $this->get_pagenum();
  	$total_items = count( $this->example_data );

  // only ncessary because we have sample data
  $this->found_data = array_slice( $this->example_data,( ( $current_page-1 )* $per_page ), $per_page );

  $this->set_pagination_args( array(
    'total_items' => $total_items,                  //WE have to calculate the total number of items
    'per_page'    => $per_page                     //WE have to determine how many items to show on a page
  ) );
  $this->items = $this->found_data;
}

} //class








function getDateUntil($postDate,$expSetting){
	$originalPost=$postDate;
	$deleteDate=$originalPost+($expSetting*60*60*24);
	$rightNow=time();
	$dateDiff    = $deleteDate-$rightNow;
	$fullDays    = floor($dateDiff/(60*60*24));
	$fullHours   = floor(($dateDiff-($fullDays*60*60*24))/(60*60));
	$fullMinutes = floor(($dateDiff-($fullDays*60*60*24)-($fullHours*60*60))/60);
	
	if($fullDays>0){
		$timeSince.=$fullDays." days ";
	}
	if($fullHours>0){
		if ($fullHours==1){
		$timeSince.=$fullHours." hour ";	
		}else{
		$timeSince.=$fullHours." hours ";
	}
	}
	if($fullMinutes>0){
		$timeSince.=$fullMinutes." min ";
	}
	return $timeSince;
}





function my_add_menu_items(){
  $hook = add_menu_page( 'My Plugin List Table', 'My List Table Example', 'activate_plugins', 'my_list_test', 'my_render_list_page' );
  add_action( "load-$hook", 'add_options' );
}

function add_options() {
  global $myListTable;
  $option = 'per_page';
  $args = array(
         'label' => 'Post Title',
         'default' => 10,
         'option' => 'posts_per_page'
         );
  add_screen_option( $option, $args );
  $myListTable = new My_List_Table();
}
//add_action( 'admin_menu', 'my_add_menu_items' );







if ( isset($_GET['action']) && $_GET['action']=='preserve' ){
	$mypostid=$_GET['post'];
	delete_single_meta_post($mypostid);
}


if ( isset($_GET['action']) && $_GET['action']=='readydelete' ){
	$mypostid=$_GET['post'];
	undelete_single_meta_post($mypostid);
}


function delete_single_meta_post($mypostid){			//  DELETE META POST DATA FUNCTION
	add_post_meta($mypostid, 'rssmi_source_protect', 1);
}

function undelete_single_meta_post($mypostid){			//  DELETE META POST DATA FUNCTION
	delete_post_meta($mypostid, 'rssmi_source_protect', 1);
}


   

function my_render_list_page(){
  global $myListTable;
  echo '</pre><div class="wrap"><h2>Manage Feed to Post Auto Delete Actions</h2>'; 


	if( isset($_POST['s']) ){
                $myListTable->prepare_items($_POST['s']);
        } else {
               $myListTable->prepare_items(); 
        }

?>

    <div style="background:#ECECEC;border:1px solid #CCC;padding:0 10px;margin-top:5px;border-radius:5px;-moz-border-radius:5px;-webkit-border-radius:5px;">
        <p>This page lists all the articles you have imported using the plugin using Feed to Post.  If the articles are set to be deleted, you'll see the time until deletion in the last column (otherwise it is marked with n/a).</p> 
        <p>If you've set the plugin to automatically delete imported articles but want one or more imported articles NOT to be deleted, you can do this using the page.  Click Do Not Delete for any single article you don't want automatically deleted or check off all the articles you want to be preserved and choose Do Not Delete from the drop down menu and click Apply.</p>
		<p style="color:red">If at any time you want to delete all the post created by this plugin and all the featured images associated with these posts, click this button once (then wait a minute or so and refresh this page) - NOTE:  This will delete only the posts created by this plugin.<button type="button" name="fetchdelete" id="fetch-delete" value=""><?php _e("CLICK TO DELETE ALL PLUGIN POSTS NOW", 'wp-rss-multi-importer')?></button> </p>
    </div>


  <form method="post">
    <input type="hidden" name="page" value="wp_rss_multi_importer_admin&tab=posts_list&paged=<?php echo $_GET['paged'];?>>
    <?php
    $myListTable->search_box( 'search', 'search_id' );

  $myListTable->display(); 
  echo '</form></div>'; 
}

