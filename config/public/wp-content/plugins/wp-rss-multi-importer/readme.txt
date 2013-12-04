=== WP RSS Multi Importer ===
Contributors: allenweiss
Donate link: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=M6GC7V8BARAJL
Tags: rss, atom, feeds, aggregation, aggregator, import, syndication, autoblog, widget
Requires at least: 3.1
Tested up to: 3.6
Stable tag: 2.66.3
Imports & merges multiple feeds. Make blog posts or display on a page, excerpts w/ images, 8 templates, categorize and more.

== Description ==

All-In-One solution for importing, merging and displaying RSS and Atom feeds on your Wordpress site.  Using this plugin you can do 3 things (separately or at the same time):


<blockquote>
<ul>
<li>Display the aggregated feed items on a page in one of **8 different templates that you can customize** </li>
<li>**Create blog posts (autoblog)** from the feed items so readers can comment on them</li>
<li>Display the aggregated feed items in a theme widget, in one of 3 different displays</li>
</ul>
</blockquote>


= Newest Features =

Feed to Post has options to make the image into a Featured Image and auto-remove posts.

= See How It Works =

[youtube http://www.youtube.com/watch?v=S-Ixus8Maz0]


= Main Features =

* Templates - choose from 8 different templates, create and style your own and save it
* Import feed items (like Google news) and creates blog posts so readers can comment on them..and put the posts into your own blog categories
* When posting to your blog, have the image be the Featured Image which you can use in the most current themes
* Auto remove posts to your blog based on expiration time

= More Features =

* Set a default image to show for each category
* Pagination option - select number of posts per page
* Select number of posts per feed you want to show
* Select number of posts on a page of your web site (when not in pagination mode)
* Separate out Today from Earlier posts
* Sort by date (ascending or descending) 
* Output feed name as (Source, Sponsor, Via, or Club)
* Show an excerpt (and select the number of words to show)
* Select how you would like the links to open (in a Lightbox, a new window, or the current window)
* Set the links as no-follow or not
* Suppress images in excerpts if you want
* Resize images in excerpts
* Allow users to determine whether to show-hide excerpts
* Set caching time for faster page loading
* Export all the feeds as a single RSS feed
* Add social links (Twitter and Facebook)
* Over 15 shortcode parameters you can use to further customize the output

These features are all available in the admin panel.

= Translation = 

* Turkish - thanks to Hakaner

= Credit = 

[__Allen Weiss__](http://www.allenweiss.com/wp_plugin)

== Installation ==

1. Upload the `wp-rss-multi-importer` folder to the `/wp-content/plugins/` directory
2. Activate the WP RSS Multi Importer plugin through the 'Plugins' menu in WordPress
3. Configure the plugin by going to the `RSS Multi Importer` submenu that appears in your `Settings` admin menu.
3. Use the shortcode in your posts or pages: `[wp_rss_multi_importer]` or use the widget, or use the Feed to Post option.
4. Limit which feeds get shown on a page by using a parameter in the shortcode, like: [wp_rss_multi_importer category="#,#"] or choose the categories in the widget.

You can also use other over 20 other parameters for the DEFAULT template which can be customized in the shortcode.

== Frequently Asked Questions ==
= How can I output the feeds in my theme? =

Use the shortcode in your posts and pages:
[wp_rss_multi_importer]
Make sure the shortcode is entered when the input is set to HTML (versus Visual)

If you want to limit the feeds to those in a given category, make sure to first
assign the feed to a category, then use this shortcode on your page or post:
[wp_rss_multi_importer category="#"]
Assign multiple categories using a comma delimited list:
[wp_rss_multi_importer category="#,#,#"]

Use the Feed to Post option and turn the feed articles into blog posts. 


Use the widget.  If your theme allows for widgets, you'll find the RSS Multi Importer Widget there.
Configure your feeds in the administration panel, then choose the categories, number of posts, sorting method, optional scrolling, and more in the widget admin.

If you want to put this in the code on your theme, you can do it like this:

echo do_shortcode('[wp_rss_multi_importer]'); 

= Can I have the feeds go directly into blog posts? =

Yes.  Just add feeds and then go to the Feed to Posts Options tab in the admin section.

= Can I export my own feed of the aggregated feed? =

Yes.  Just add feeds and then go to the Export Feed Options tab in the admin section.


Go here to find [__more FAQs__](http://www.allenweiss.com/faqs)

== Screenshots ==

1. Adding feeds and assigning categories.

2. Adding new categories.

3. Options panel.

4. User view - with excerpts and images.

== Change Log ==

= Version 2.66.3 =
* Fixed bugs found in earlier version that prohibited some excerpts and video images from showing.
= Version 2.66.2 =
* Feed to Post now can grab featured image when Give Me Everything word length is chosen. Accepts images from Google news feed. Google+ social media link added. Ability to suppress Read More added. Several bugs fixed.
= Version 2.66.1 =
* Fixed RSS export feature and several other bugs.
= Version 2.66 =
* Additional controls to eliminate duplicate entries added.  One-click delete all Feed to Posts entries and associated featured images added.  Turkish translation added.  Added support for Vimeo feeds.  Fixed bugs associated with images that use properties with single quotes.
= Version 2.65 =
* Pagination numbers added, choose to have Feed to Post items set to no index, no follow in the meta tag to make search invisible (if respected by crawlers), images with single quotes around the src tag now recognized, several bug fixes.
= Version 2.64 =
* Choose source anchor text, option to put content into excerpt field and option to eliminate hyperlinks for Feed to Post added.  Several other bugs fixes.
= Version 2.63 =
* Fixed problem with posting Feed to Post to multiple blog categories and several other bugs fixes.
= Version 2.62 =
* Add Feed to Post to multiple blog categories, filter now works with titles, choose which posts to auto remove or save, post format fixed, and several bugs fixes.
= Version 2.61 =
* Category picker added for Feed to Post, improvements to shortcode templates, increased mobile detection to disable lightbox.  Several bugs fixes.
= Version 2.60 =
* Auto remove posts added for Feed to Post option.  Default time zone can now be specified.  Several bugs fixes.
= Version 2.58 =
* Category filters for words added (include or exclude), reworked code to prevent double posting of articles in Feed to Post, other bug fixes.
= Version 2.57 =
* Bug fixes
= Version 2.56 =
* Assign blog tags to each plugin category.  Using an outside cron service, can now update Feed to Post on individual feeds.  Mobile detection for Feed to Post option. Default category image option added to widget. Can change links to titles of feed posts to go directly to source.
= Version 2.55 =
* Added more options to Feed to Post, including ability to preserve all html, stored templates and css file now automatically restored on update, improved cleaning up html in imported feeds, fixed several bugs.
= Version 2.54 =
* Added option to make images in Feed to Post be the featured image.
= Version 2.53 =
* Added default category image option, set post format for Feed to Post option and other options added, preserves more tags in Feed to Post option, added more shortcode parameters and fixed several bugs.
= Version 2.52 =
* Added more options for Feed to Post users including ability to specify user_id and suppress the source. Clearer admin interface. Image recognition improved. Class added to stylize image in Feed to Post. Small bug fixes. 
= Version 2.51 =
* Images are now hyperlinked in excerpts. Images that are on secure servers now work. Feed or item author now available for use in templates and Feed to Post (if the feed has the author).
= Version 2.50 =
* Many features added, including improved image handling, selecting window option and more cron scheduling options when using Feed to Post, fixed problem with custom posts, ability to choose different templates on different pages (via shortcode), more shortcode parameters added, suppress beacon images in feeds, fixed Bing resulting in duplicate entries in Feed to Post, YouTube now opens in lightbox in Feed to Post, and several other bug fixes.
= Version 2.47 =
* Added more options to put Feed to Post entries into your blog categories. Added more shortcode parameters and fixed various bugs.
= Version 2.46 =
* More fixes related to the foreign language character problem.  RSS content tag now used for excerpt so full text available if in the feed.
= Version 2.45 =
* Added option to show images in widget.  Fixed foreign language character problem.  Other smaller bug fixes.
= Version 2.44 =
* Recognizes YouTube video feeds in the default template and puts the video in the lightbox if selected.  Added a Pinterest parameter to the shortcode for size correction.  Bug fixes.
= Version 2.43 =
* Added option to put Feed to Post entries into your selected blog category.  Also, there is now an alert if the feed you enter is going to cause errors.
= Version 2.42 =
* Added social sharing option.  Set default settings for new users.
= Version 2.41 =
* Added more options to the Feed to Post settings.  Prepared files for translation into other languages.
= Version 2.40 =
* Added option to import feed items (like news) and creates blog posts so readers can comment on them.  Category name added as an option to add to templates, plus bug fixes.
= Version 2.37 =
* Bug fixes and added option to have simple list view to the widget.
= Version 2.36 =
* Added ability to pick up images in RSS enclosures and more diagnostic code.
= Version 2.35 =
* Fixed bug due to php short form and added mobile detection to not use lightbox.
= Version 2.34 =
* Added option to re-export all feeds as one single RSS feed.
= Version 2.33 =
* Added open window options to the widget.  Added diagnostic parameter.
= Version 2.32 =
* Added new vertical scroll template. Added cron hourly service.  Cache shortcode parameter added.
= Version 2.31 =
* Fixed option to open widget feeds in lightbox and allow several shortcodes on the same page.
= Version 2.30 =
* Added templates, improved admin interface, fixed several bugs.  Switched caching methods to allow for more real time RSS if desired. Updated colorbox version.
= Version 2.25 =
* Fixed bug that caused feeds to disappear from admin panel when several categories added.  No data was lost by users.
= Version 2.24 =
* Usability improvements added for new users.  Quick start video added.
= Version 2.23 =
* Added a workaround when other plugins did not restrict their javascript to their own admin pages..thus causing problems for some users.
= Version 2.22 =
* Caching made optional. Enhanced the admin section by putting option settings on a separate panel. More options added to the number of words in the excerpt.
= Version 2.21 =
* Performance improvements. Ability to change color of hyperlinked titles added with shortcode parameter.  Also, specify number of posts per feed via shortcode parameter.
= Version 2.20 =
* Pagination option added.
= Version 2.19 =
* Option added to not load colorbox.  Some themes already load colorbox and this causes a conflict.
= Version 2.18 =
* Show-hide option added to excerpts.
= Version 2.17 =
* No follow option added to all links.  Fixed bug with widget when no category selection is made.
= Version 2.16 =
* Date formats are now consistent with international formats. Added ability to optionally float images to the left.  Options to show excerpts in widget and number of post/feed added.
= Version 2.15 =
* Multiple categories can now be used in the shortcode and widget.  Widget now has small footprint option with motion.  Excerpt images can be sized to a certain width. Additional customized parameters added.
= Version 2.11 =
* Fixed bug that kept new window and same window links to not be live
= Version 2.1 =
* Added a widget option for displaying feeds, better image formatting, separate Today from Earlier posts.
= Version 2.01 =
* Fixed bug that caused some users to have problems when they haven't added any categories.
= Version 2.0 =
* Added option to assign feeds to a category and output feeds from a given a given category.  Limit posts on a page.  Uninstall now works for multiuser sites.  Solved problem for some users where the LightBox option was conflicting with other plugins that also relied on Lightbox or Colorbox.
= Version 1.1 =
* Added option to determine where the links should open (Lightbox, new window, current window)
= Version 1.0 =
* Fixed problem where showing text before the shortcode rendered after the shortcode
= Version 0.7 =
* Fixed problem with showing excerpts withe foreign characters
= Version 0.6 =
* Fixed bugs in Lightbox and eliminated error message
= Version 0.5 =
* Added option to include short descriptions - excerpts (if they exist in the RSS feed)

== Upgrade Notice ==

= 2.60 =
This version includes several improvements (e.g. featured image, auto remove, default image, filtering) and bug fixes for the Feed to Post option and added improved flexibility for the shortcode option.