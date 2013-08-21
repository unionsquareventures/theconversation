<?php

// where the script is installed

$indeed_publisher_id = "9648379283006957";
$indeed_fromage = 45;

$geos = array(
'ar',
'au',
'at',
'be',
'br',
'ca',
'cn',
'de',
'fr',
'gb',
'hk',
'ie',
'il',
'in',
'it',
'jp',
'kr',
'mx',
'nl',
'ru',
'se',
'sg',
'es',
'tw'
);

// if you are adding a company name that has non-standard capitalization like: SoundCloud or YouNow make sure you add them to line 138 of refresh.php
$startups = array(
'10gen',
'AMEE',
'Auxmoney',
'Boxee',
'Brewster',
'C2FO',
'Canvas',
'CircleUp',
//'CloudFlare',
'Codecademy',
'Coinbase',
'Covestor',
'Disqus',
'DuckDuckGo',
'Duolingo',
'Dwolla',
'Edmodo',
'Etsy',
'Firebase',
'Flurry',
'Foursquare',
'Funding Circle',
'GetGlue',
'Hailo',
'Heyzap',
'Kickstarter',
'Kik',
'Kitchensurfing',
'Lending Club',
'Meetup',
'Return Path',
'Science Exchange',
'Shapeways',
'SiftScience',
'SigFig',
'Simulmedia',
'Skillshare',
'SoundCloud',
'Stack Exchange',
'TargetSpot',
'Turntable.fm',
'Twilio',
'Twitter',
'Wattpad',
'Work Market',
'YieldMo',
'YouNow',
'Zemanta'
);


$indeed_query = implode(' OR ', array_map("wrapquotes",$startups));
$feed_url = "http://rss.indeed.com/rss?q=company%3A%28" . urlencode($indeed_query) . "%29";
$admin_email = "www-bot@usv.com";

?>