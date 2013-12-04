<?php
/*
Plugin Name: Post Types Order
Plugin URI: http://www.nsp-code.com
Description: Posts Order and Post Types Objects Order using a Drag and Drop Sortable javascript capability
Author: Nsp Code
Author URI: http://www.nsp-code.com 
Version: 1.6.2
*/

define('CPTPATH',   plugin_dir_path(__FILE__));
define('CPTURL',    plugins_url('', __FILE__));


register_deactivation_hook(__FILE__, 'CPTO_deactivated');
register_activation_hook(__FILE__, 'CPTO_activated');

function CPTO_activated() 
    {
        //make sure the vars are set as default
        $options = get_option('cpto_options');
        if (!isset($options['autosort']))
            $options['autosort'] = '1';
            
        if (!isset($options['adminsort']))
            $options['adminsort'] = '1';
            
        if (!isset($options['capability']))
            $options['capability'] = 'install_plugins';
            
        update_option('cpto_options', $options);
    }

function CPTO_deactivated() 
    {
        
    }
    
include_once(CPTPATH . '/include/functions.php');

add_filter('pre_get_posts', 'CPTO_pre_get_posts');
function CPTO_pre_get_posts($query)
    {
        //--  lee@cloudswipe.com requirement
        global $post;
        if(is_object($post) && $post->ID < 1) 
            { return $query; }  // Stop running the function if this is a virtual page
        //--
           
        $options = get_option('cpto_options');
        if (is_admin())
            {
                //no need if it's admin interface
                return false;   
            }
        //if auto sort    
        if ($options['autosort'] == "1")
            {
                //remove the supresed filters;
                if (isset($query->query['suppress_filters']))
                    $query->query['suppress_filters'] = FALSE;    
                
     
                if (isset($query->query_vars['suppress_filters']))
                    $query->query_vars['suppress_filters'] = FALSE;
     
            }
            
        return $query;
    }

add_filter('posts_orderby', 'CPTOrderPosts', 99, 2);
function CPTOrderPosts($orderBy, $query) 
    {
        global $wpdb;
        
        $options = get_option('cpto_options');
        
        //ignore the bbpress
        if (isset($query->query_vars['post_type']) && ((is_array($query->query_vars['post_type']) && in_array("reply", $query->query_vars['post_type'])) || ($query->query_vars['post_type'] == "reply")))
            return $orderBy;
        if (isset($query->query_vars['post_type']) && ((is_array($query->query_vars['post_type']) && in_array("topic", $query->query_vars['post_type'])) || ($query->query_vars['post_type'] == "topic")))
            return $orderBy;
        
        if (is_admin())
                {
                    if ($options['adminsort'] == "1")
                        $orderBy = "{$wpdb->posts}.menu_order, {$wpdb->posts}.post_date DESC";
                }
            else
                {
                    //ignore search
                    if($query->is_search())
                        return($orderBy);
                    
                    if ($options['autosort'] == "1")
                        $orderBy = "{$wpdb->posts}.menu_order, " . $orderBy;
                }

        return($orderBy);
    }

$is_configured = get_option('CPT_configured');
if ($is_configured == '')
    add_action( 'admin_notices', 'CPTO_admin_notices');
    
function CPTO_admin_notices()
    {
        if (isset($_POST['form_submit']))
            return;
        ?>
            <div class="error fade">
                <p><strong><?php _e('Post Types Order must be configured. Please go to', 'cpt') ?> <a href="<?php echo get_admin_url() ?>options-general.php?page=cpto-options"><?php _e('Settings Page', 'cpt') ?></a> <?php _e('make the configuration and save', 'cpt') ?></strong></p>
            </div>
        <?php
    }


add_action( 'plugins_loaded', 'cpto_load_textdomain'); 
function cpto_load_textdomain() 
    {
        load_plugin_textdomain('cpt', FALSE, dirname( plugin_basename( __FILE__ ) ) . '/lang');
    }
  
add_action('admin_menu', 'cpto_plugin_menu'); 
function cpto_plugin_menu() 
    {
        include (CPTPATH . '/include/options.php');
        add_options_page('Post Types Order', '<img class="menu_pto" src="'. CPTURL .'/images/menu-icon.gif" alt="" />Post Types Order', 'manage_options', 'cpto-options', 'cpt_plugin_options');
    }

    
add_action('wp_loaded', 'initCPTO' ); 	
function initCPTO() 
    {
	    global $custom_post_type_order, $userdata;

        $options = get_option('cpto_options');

        if (is_admin())
            {
                if(isset($options['capability']) && !empty($options['capability']))
                    {
                        if(current_user_can($options['capability']))
                            $custom_post_type_order = new CPTO(); 
                    }
                else if (is_numeric($options['level']))
                    {
                        if (userdata_get_user_level(true) >= $options['level'])
                            $custom_post_type_order = new CPTO();     
                    }
                    else
                        {
                            $custom_post_type_order = new CPTO();   
                        }
            }        
    }
    
add_filter('get_previous_post_where', 'cpto_get_previous_post_where');
add_filter('get_previous_post_sort', 'cpto_get_previous_post_sort');
add_filter('get_next_post_where', 'cpto_get_next_post_where');
add_filter('get_next_post_sort', 'cpto_get_next_post_sort');
function cpto_get_previous_post_where($where)
    {
        global $post, $wpdb;

        if ( empty( $post ) )
            return $where;

        $current_post_date = $post->post_date;

        $join = '';
        $posts_in_ex_cats_sql = '';
        if (isset($in_same_cat))
        if ( $in_same_cat || !empty($excluded_categories) ) 
            {
                $join = " INNER JOIN $wpdb->term_relationships AS tr ON p.ID = tr.object_id INNER JOIN $wpdb->term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id";

                if ( $in_same_cat ) {
                    $cat_array = wp_get_object_terms($post->ID, 'category', array('fields' => 'ids'));
                    $join .= " AND tt.taxonomy = 'category' AND tt.term_id IN (" . implode(',', $cat_array) . ")";
                }

                $posts_in_ex_cats_sql = "AND tt.taxonomy = 'category'";
                if ( !empty($excluded_categories) ) {
                    $excluded_categories = array_map('intval', explode(' and ', $excluded_categories));
                    if ( !empty($cat_array) ) {
                        $excluded_categories = array_diff($excluded_categories, $cat_array);
                        $posts_in_ex_cats_sql = '';
                    }

                    if ( !empty($excluded_categories) ) {
                        $posts_in_ex_cats_sql = " AND tt.taxonomy = 'category' AND tt.term_id NOT IN (" . implode($excluded_categories, ',') . ')';
                    }
                }
            }
        $current_menu_order = $post->menu_order;
        
        //check if there are more posts with lower menu_order
        $query = "SELECT p.* FROM $wpdb->posts AS p
                    WHERE p.menu_order < '".$current_menu_order."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' $posts_in_ex_cats_sql";
        $results = $wpdb->get_results($query);
                
        if (count($results) > 0)
            {
                $where = "WHERE p.menu_order < '".$current_menu_order."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' $posts_in_ex_cats_sql";
            }
            else
                {
                    $where = "WHERE p.post_date < '".$current_post_date."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' AND p.ID != '". $post->ID ."' $posts_in_ex_cats_sql";
                }
        
        return $where;
    }
    
function cpto_get_previous_post_sort($sort)
    {
        global $post, $wpdb;
        $posts_in_ex_cats_sql = '';
        
        $current_menu_order = $post->menu_order; 
        
        $query = "SELECT p.* FROM $wpdb->posts AS p
                    WHERE p.menu_order < '".$current_menu_order."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' $posts_in_ex_cats_sql";
        $results = $wpdb->get_results($query);
        
        if (count($results) > 0)
                {
                    $sort = 'ORDER BY p.menu_order DESC, p.post_date ASC LIMIT 1';
                }
            else
                {
                    $sort = 'ORDER BY p.post_date DESC LIMIT 1';
                }

        return $sort;
    }

function cpto_get_next_post_where($where)
    {
        global $post, $wpdb;

        if ( empty( $post ) )
            return null;

        $current_post_date = $post->post_date;

        $join = '';
        $posts_in_ex_cats_sql = '';
        if (isset($in_same_cat))
        if ( $in_same_cat || !empty($excluded_categories) ) 
            {
                $join = " INNER JOIN $wpdb->term_relationships AS tr ON p.ID = tr.object_id INNER JOIN $wpdb->term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id";

                if ( $in_same_cat ) {
                    $cat_array = wp_get_object_terms($post->ID, 'category', array('fields' => 'ids'));
                    $join .= " AND tt.taxonomy = 'category' AND tt.term_id IN (" . implode(',', $cat_array) . ")";
                }

                $posts_in_ex_cats_sql = "AND tt.taxonomy = 'category'";
                if ( !empty($excluded_categories) ) {
                    $excluded_categories = array_map('intval', explode(' and ', $excluded_categories));
                    if ( !empty($cat_array) ) {
                        $excluded_categories = array_diff($excluded_categories, $cat_array);
                        $posts_in_ex_cats_sql = '';
                    }

                    if ( !empty($excluded_categories) ) {
                        $posts_in_ex_cats_sql = " AND tt.taxonomy = 'category' AND tt.term_id NOT IN (" . implode($excluded_categories, ',') . ')';
                    }
                }
            }
        
        $current_menu_order = $post->menu_order;
        
        //check if there are more posts with lower menu_order
        $query = "SELECT p.* FROM $wpdb->posts AS p
                    WHERE p.menu_order > '".$current_menu_order."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' $posts_in_ex_cats_sql";
        $results = $wpdb->get_results($query);
        
        if (count($results) > 0)
            {
                $where = "WHERE p.menu_order > '".$current_menu_order."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' $posts_in_ex_cats_sql";
            }
            else
                {
                    $where = "WHERE p.post_date > '".$current_post_date."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' AND p.ID != '". $post->ID ."' $posts_in_ex_cats_sql";
                }
        
        return $where;
    }

function cpto_get_next_post_sort($sort)
    {
        global $post, $wpdb; 
        $posts_in_ex_cats_sql = '';
        
        $current_menu_order = $post->menu_order; 
        
        $query = "SELECT p.* FROM $wpdb->posts AS p
                    WHERE p.menu_order > '".$current_menu_order."' AND p.post_type = '". $post->post_type ."' AND p.post_status = 'publish' $posts_in_ex_cats_sql";
        $results = $wpdb->get_results($query);
        if (count($results) > 0)
                {
                    $sort = 'ORDER BY p.menu_order ASC, p.post_date DESC LIMIT 1';
                }
            else
                {
                    $sort = 'ORDER BY p.post_date ASC LIMIT 1';
                }
        
        return $sort;    
    }
    
    
class Post_Types_Order_Walker extends Walker 
    {

        var $db_fields = array ('parent' => 'post_parent', 'id' => 'ID');


        function start_lvl(&$output, $depth = 0, $args = array()) {
            $indent = str_repeat("\t", $depth);
            $output .= "\n$indent<ul class='children'>\n";
        }


        function end_lvl(&$output, $depth = 0, $args = array()) {
            $indent = str_repeat("\t", $depth);
            $output .= "$indent</ul>\n";
        }


        function start_el(&$output, $page, $depth = 0, $args = array()) {
            if ( $depth )
                $indent = str_repeat("\t", $depth);
            else
                $indent = '';

            extract($args, EXTR_SKIP);

            $output .= $indent . '<li id="item_'.$page->ID.'"><span>'.apply_filters( 'the_title', $page->post_title, $page->ID ).'</span>';
        }


        function end_el(&$output, $page, $depth = 0, $args = array()) {
            $output .= "</li>\n";
        }

    }


class CPTO 
    {
	    var $current_post_type = null;
	    
	    function CPTO() 
            {
		        add_action( 'admin_init', array(&$this, 'registerFiles'), 11 );
                add_action( 'admin_init', array(&$this, 'checkPost'), 10 );
		        add_action( 'admin_menu', array(&$this, 'addMenu') );
                
                
		        
		        add_action( 'wp_ajax_update-custom-type-order', array(&$this, 'saveAjaxOrder') );
	        }

	    function registerFiles() 
            {
		        if ( $this->current_post_type != null ) 
                    {
                        wp_enqueue_script('jQuery');
                        wp_enqueue_script('jquery-ui-sortable');
		            }
                    
                wp_register_style('CPTStyleSheets', CPTURL . '/css/cpt.css');
                wp_enqueue_style( 'CPTStyleSheets');
	        }
	    
	    function checkPost() 
            {
		        if ( isset($_GET['page']) && substr($_GET['page'], 0, 17) == 'order-post-types-' ) 
                    {
			            $this->current_post_type = get_post_type_object(str_replace( 'order-post-types-', '', $_GET['page'] ));
			            if ( $this->current_post_type == null) 
                            {
				                wp_die('Invalid post type');
			                }
		            }
	        }
	    
	    function saveAjaxOrder() 
            {
		        global $wpdb;
		        
		        parse_str($_POST['order'], $data);
		        
		        if (is_array($data))
                foreach($data as $key => $values ) 
                    {
			            if ( $key == 'item' ) 
                            {
				                foreach( $values as $position => $id ) 
                                    {
					                    $wpdb->update( $wpdb->posts, array('menu_order' => $position, 'post_parent' => 0), array('ID' => $id) );
				                    } 
			                } 
                        else 
                            {
				                foreach( $values as $position => $id ) 
                                    {
					                    $wpdb->update( $wpdb->posts, array('menu_order' => $position, 'post_parent' => str_replace('item_', '', $key)), array('ID' => $id) );
				                    }
			                }
		            }
	        }
	    

	    function addMenu() 
            {
		        global $userdata;
                //put a menu for all custom_type
                $post_types = get_post_types();
                
                $options = get_option('cpto_options'); 
                //get the required user capability
                $capability = '';
                if(isset($options['capability']) && !empty($options['capability']))
                    {
                        $capability = $options['capability'];
                    }
                else if (is_numeric($options['level']))
                    {
                        $capability = userdata_get_user_level();
                    }
                    else
                        {
                            $capability = 'install_plugins';  
                        }
                
                foreach( $post_types as $post_type_name ) 
                    {
                        if ($post_type_name == 'page')
                            continue;
                            
                        //ignore bbpress
                        if ($post_type_name == 'reply' || $post_type_name == 'topic')
                            continue; 
                        
                        if ($post_type_name == 'post')
                            add_submenu_page('edit.php', __('Re-Order', 'cpt'), __('Re-Order', 'cpt'), $capability, 'order-post-types-'.$post_type_name, array(&$this, 'SortPage') );
                        else
                            {
                                if (!is_post_type_hierarchical($post_type_name))
                                    add_submenu_page('edit.php?post_type='.$post_type_name, 'Re-Order', 'Re-Order', $capability, 'order-post-types-'.$post_type_name, array(&$this, 'SortPage') );
                            }
		            }
	        }
	    

	    function SortPage() 
            {
		        ?>
		        <div class="wrap">
			        <div class="icon32" id="icon-edit"><br></div>
                    <h2><?php echo $this->current_post_type->labels->singular_name . ' -  '. __('Re-Order', 'cpt') ?></h2>

                    <?php cpt_info_box(); ?>  
                    
			        <div id="ajax-response"></div>
			        
			        <noscript>
				        <div class="error message">
					        <p><?php _e('This plugin can\'t work without javascript, because it\'s use drag and drop and AJAX.', 'cpt') ?></p>
				        </div>
			        </noscript>
			        
			        <div id="order-post-type">
				        <ul id="sortable">
					        <?php $this->listPages('hide_empty=0&title_li=&post_type='.$this->current_post_type->name); ?>
				        </ul>
				        
				        <div class="clear"></div>
			        </div>
			        
			        <p class="submit">
				        <a href="#" id="save-order" class="button-primary"><?php _e('Update', 'cpt' ) ?></a>
			        </p>
			        
			        <script type="text/javascript">
				        jQuery(document).ready(function() {
					        jQuery("#sortable").sortable({
						        'tolerance':'intersect',
						        'cursor':'pointer',
						        'items':'li',
						        'placeholder':'placeholder',
						        'nested': 'ul'
					        });
					        
					        jQuery("#sortable").disableSelection();
					        jQuery("#save-order").bind( "click", function() {
						        jQuery.post( ajaxurl, { action:'update-custom-type-order', order:jQuery("#sortable").sortable("serialize") }, function() {
							        jQuery("#ajax-response").html('<div class="message updated fade"><p><?php _e('Items Order Updated', 'cpt') ?></p></div>');
							        jQuery("#ajax-response div").delay(3000).hide("slow");
						        });
					        });
				        });
			        </script>
                    
		        </div>
		        <?php
	        }

	    function listPages($args = '') 
            {
		        $defaults = array(
			        'depth' => 0, 'show_date' => '',
			        'date_format' => get_option('date_format'),
			        'child_of' => 0, 'exclude' => '',
			        'title_li' => __('Pages'), 'echo' => 1,
			        'authors' => '', 'sort_column' => 'menu_order',
			        'link_before' => '', 'link_after' => '', 'walker' => ''
		        );

		        $r = wp_parse_args( $args, $defaults );
		        extract( $r, EXTR_SKIP );

		        $output = '';
	        
		        $r['exclude'] = preg_replace('/[^0-9,]/', '', $r['exclude']);
		        $exclude_array = ( $r['exclude'] ) ? explode(',', $r['exclude']) : array();
		        $r['exclude'] = implode( ',', apply_filters('wp_list_pages_excludes', $exclude_array) );

		        // Query pages.
		        $r['hierarchical'] = 0;
                $args = array(
                            'sort_column'   =>  'menu_order',
                            'post_type'     =>  $post_type,
                            'posts_per_page' => -1,
                            'orderby'        => 'menu_order',
                            'order'         => 'ASC'
                );
                
                $the_query = new WP_Query($args);
                $pages = $the_query->posts;

		        if ( !empty($pages) ) {
			        if ( $r['title_li'] )
				        $output .= '<li class="pagenav intersect">' . $r['title_li'] . '<ul>';
				        
			        $output .= $this->walkTree($pages, $r['depth'], $r);

			        if ( $r['title_li'] )
				        $output .= '</ul></li>';
		        }

		        $output = apply_filters('wp_list_pages', $output, $r);

		        if ( $r['echo'] )
			        echo $output;
		        else
			        return $output;
	        }
	    
	    function walkTree($pages, $depth, $r) 
            {
		        if ( empty($r['walker']) )
			        $walker = new Post_Types_Order_Walker;
		        else
			        $walker = $r['walker'];

		        $args = array($pages, $depth, $r);
		        return call_user_func_array(array(&$walker, 'walk'), $args);
	        }
    }
   

?>