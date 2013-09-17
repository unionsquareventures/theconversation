<?php
require_once("libjobs.php");
require_once("jobs-config.php");

// $report: the list of jobs that didn't fit.  these will be sent as an email everytime this script is run. Adjust the regex below to accomodate weird parsing issues.
// $response: the encapsulation of the results that will become all.json
// $jobs: the clean set of post-filtered job listings

$report = array();
$response = array();
$jobs = array();


// grab the US-based jobs for each of the portfolio companies
foreach ($startups as $s) {

$keyword = urlencode(wrapquotes($s));
$val = strtolower(ereg_replace("[^A-Za-z0-9]", "",$s));

$start = 0;
$more = true;

while ($more) {
	  $url = "http://api.indeed.com/ads/apisearch?publisher=$indeed_publisher_id&q=company%3A($keyword)";
	  $url .= "&l=&sort=&radius=&st=&jt=&start=$start&limit=1000&fromage=$indeed_fromage&filter=&co=&latlong=1&chnl=&userip=1.2.3.4&useragent=Mozilla//4.0(Firefox)&v=2&format=json";

// uncomment to see the actual API calls being made
	  echo "$start: $url<br>";

	  $data = get_data($url);

	  if ($data) {
			$json = json_decode($data);

	  $jobs = array_merge($jobs, get_jobs($json->{'results'},$startups));

	  if ($json->totalResults > $json->end) {

	  		$start = $json->end + 1;
	  } else {
	  		 $more = false;
		 }
} else {
  var_dump($data);

}
}
}


// for each of the specified geos, grab all the jobs in that geo
foreach ($geos as $g) {

$start = 1;
$more = true;
while ($more) {
	  $url = "http://api.indeed.com/ads/apisearch?publisher=$indeed_publisher_id&q=company%3A(" . urlencode($indeed_query) . ")";
	  $url .= "&l=&sort=&radius=&st=&jt=&start=$start&limit=1000&fromage=$indeed_fromage&filter=&co=$g&latlong=1&chnl=&userip=1.2.3.4&useragent=Mozilla//4.0(Firefox)&v=2&format=json";

	  echo "$start: $url<br>";
	  $json = json_decode(get_data($url));

	  $jobs = array_merge($jobs, get_jobs($json->{'results'},$startups));

	  if ($json->totalResults > $json->end) {
	  		$start = $json->end + 1;
	  } else {
	  		 $more = false;
		 }

}
}

$response['jobs'] = $jobs;
$response['total'] = count($jobs);

//echo "total: " . $response['total'];
if ($response['total'] > 1) {

// backup the old file
$old = file_get_contents(TEMPPATH . '/' . 'all.json');
$fp2 = fopen(TEMPPATH . '/' .'all.json.bak', 'w');
fwrite($fp2, $old);
fclose($fp2);

// write the results to a file
$fp = fopen(TEMPPATH . '/' . 'all.json', 'w');
fwrite($fp, json_encode($response));
fclose($fp);
}

// email me the companies that got filtered out
sort($report);
$summary = "Total Jobs:\n" . $response['total'] . "\n\nFiltered Out:\n" . implode("\n",$report);

mail($admin_email,"[USV Jobs] Discarded Companies",$summary);

// parse the json resultset that is returned from Indeed, and return the jobs.
function get_jobs($results, $startups) {

// jobs that don't appear to be relevant are stored in report
global $report;
$retval=array();

// loop through all of the results, filter out a bunch of stuff, and save only the fields we are using.
foreach ($results as $r) {

// filter bad results
if (preg_match("/Opportunity|^Art|Assurance/",$job->city)) continue;
if (preg_match("/VERKOOPSTER/",$job->title)) continue;


// LOCATION
if ($r->city == "Germany") {
   $loc = "Berlin, DE";
} elseif ($r->country != "US") {
  if ($r->city != "") {
	 $loc = "$r->city, $r->country";
} else {
  $loc = "$r->formattedLocation, $r->country";
}
} else {
  if ($r->city == "Kingdom") {
  $loc = "London, GB";
  } else {
  $loc = "$r->formattedLocation";
  }
};


// COMPANY
$r->company = ucwords(strtolower($r->company));

// normalize the company name
$r->company = trim(preg_replace("/, Inc\.|Inc\.|Inc|\n\n11|,|Ltd./","",$r->company));
$r->company = trim(preg_replace("/Kickstarter.com|Kickstarter,/","Kickstarter",$r->company));
$r->company = trim(preg_replace("/Covestor\./","Covestor",$r->company));
$r->company = trim(preg_replace("/Foursquare.com/","Foursquare",$r->company));
$r->company = trim(preg_replace("/Foursquare Labs/","Foursquare",$r->company));
$r->company = trim(preg_replace("/Covestor\n\n*9/","Covestor",$r->company));
$r->company = trim(preg_replace("/Getglue\.com/","GetGlue",$r->company));
$r->company = trim(preg_replace("/Boxee\.tv/","Boxee",$r->company));
$r->company = trim(preg_replace("/c2fo \(c2fo\)/","C2FO",$r->company));
$r->company = trim(preg_replace("/Sales Operations Manager /","",$r->company)); //pollenware hack

// properly capitalize some of our non-standard portfolio company names
if ($r->company == "Soundcloud") $r->company = "SoundCloud";
if ($r->company == "Targetspot") $r->company = "TargetSpot";
if ($r->company == "Getglue") $r->company = "GetGlue";
if ($r->company == "Amee") $r->company = "AMEE";
if ($r->company == "Younow") $r->company = "YouNow";
if ($r->company == "Siftscience") $r->company = "SiftScience";
if ($r->company == "C2FO") $r->company = "C2FO";

if (($r->company == "Kik") && (preg_match("/Brussel/",$loc))) continue;

$company = $r->company;

$job = array();
$job['company'] = $company;
$job['location'] = trim($loc);
$job['jobtitle'] = trim($r->jobtitle);
$job['position'] = get_position($job['jobtitle']);
$job['url'] = trim($r->url);

// put together a list of companies that came back as a match from Indeed, but don't exactly match the list of company names in config.php and send them
if (!in_array($company,$startups)) {
$report[] = $job['company'];
$report = array_unique($report);
continue;
}

// add the listing to our list of jobs
$retval[] = $job;

}

return $retval;
}




?>