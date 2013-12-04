<?php
/*
Template Name: Jobs
*/
?>

<?php

	require_once("libjobs.php");

	// declare our arrays. each array corresponds to a different tab
	$company = array();
	$position = array();
	$location = array();
	$title = array();

	$indeed = json_decode(file_get_contents(TEMPPATH . '/' . 'all.json'));

	$numjobs = $indeed->total;

	foreach ($indeed->jobs as $job) {
	// map this back to the index for each of these so that it appears in the right section on the right tab
	$company[$job->company][] = $job;
	$position[$job->position][] = $job;
	$location[$job->location][] = $job;

	// include this job in a special Interns section (in addition) to where it would normally fall in the taxonomy
	if ((preg_match("/Intern/",$job->jobtitle)) && (!preg_match("/Internet|Internal|International/",$job->jobtitle))) {
		$title['Internships'][] = $job;
	} elseif (preg_match("/CTO|CEO|CFO|CIO|CMO|Chief/",$job->jobtitle)) {
		$title["C-Level"][] = $job;
	} elseif (preg_match("/^VP|Vice President/",$job->jobtitle)) {
		$title["Vice President"][] = $job;
	} elseif (preg_match("/Sr. Director|Senior Director|^Director/",$job->jobtitle)) {
		$title["Director"][] = $job;
	} else {

	}

	}

	// group and sort them
	ksort($company);
	ksort($position);
	ksort($location);
	ksort($title);

	get_header();

?>  

<script>
 $(document).ready(function() {
 
 	// Setup Search Box
	var companies = 'company:("10gen" OR "AMEE" OR "Auxmoney" OR "Boxee" OR "Brewster" OR "C2FO" OR "Canvas" OR "CircleUp" OR "Codecademy" OR "Coinbase" OR "Covestor" OR "Disqus" OR "DuckDuckGo" OR "Duolingo" OR "Dwolla" OR "Edmodo" OR "Etsy" OR "Firebase" OR "Flurry" OR "Foursquare" OR "Funding Circle" OR "GetGlue" OR "Hailo" OR "Heyzap" OR "Kickstarter" OR "Kik" OR "Kitchensurfing" OR "Lending Club" OR "Meetup" OR "Return Path" OR "Science Exchange" OR "Shapeways" OR "SiftScience" OR "SigFig" OR "Simulmedia" OR "Skillshare" OR "SoundCloud" OR "Stack Exchange" OR "TargetSpot" OR "Turntable.fm" OR "Twilio" OR "Twitter" OR "Wattpad" OR "Work Market" OR "YieldMo" OR "YouNow" OR "Zemanta")';

	$('#jobform').submit(function() {
		var query = $('input#q').val();
	$('input#q').val(query+companies);
	});
 
 });
</script>

    <div id="main" role="main">
        <h1 class="mobile-page-headline">Jobs</h1>

        <div class="jobs-container">
        	<header>
        		<ul class="stats">
					<li>
						<span class="stat"><?=$numjobs;?></span>
						<span class="label">jobs</span>
					</li>
					<li>
						<span class="stat"><?=count($company);?></span>
						<span class="label">companies</span>
					</li>
					<li>
						<span class="stat"><?=count($location);?></span>
						<span class="label">cities</span>
					</li>
        		</ul>

        		<div class="job-search">
					<form id="jobform" METHOD='GET' action='http://www.indeed.com/jobs'>
						<div class='form-row'>
							<input type='text' name='q' value='' size='25' id='q' placeholder='Job Title or Keywords'>
						</div>
						<div class='form-row'>
							<input type='text' name='l' value='' size='' id='l' placeholder='City, State or Zip'>
						</div>
						<div class='form-button'>
							<input type='submit' value='Search' name=''>
						</div>
					</form>
        		</div>
        	</header>

			<div id="jobs-content">
				<div class="col-1">
					<div class="job-tabs-container">
						<h2>Sort</h2>
						<ul class="job-tabs">
							<li><a href="#in" rel="in">By Job</a></li>
							<li><a href="#location" rel="location">By Location</a></li>
							<li><a href="#company" rel="company">By Company</a></li>
							<li><a href="#title" rel="title">By Title</a></li>
						</ul>
					</div>

					<div id="jobs-menu">
						<h2>Categories</h2>
						<div id="yo">
							<ul class="side-nav" id="in">
								<?php foreach ($position as $key=>$value) { ?>
									<li><a href="#in,<?=create_slug($key);?>"><?=$key;?></a></li>
								<?php } ?>
							</ul>

							<ul class="side-nav" id="location">
								<?php foreach ($location as $key=>$value) { ?>
									<li><a href="#location,<?=create_slug($key);?>"><?=$key;?></a></li>
								<?php } ?>
							</ul>

							<ul class="side-nav" id="company">
								<?php foreach ($company as $key=>$value) { ?>
									<li><a href="#company,<?=create_slug($key);?>"><?=$key;?></a></li>
								<?php } ?>
							</ul>

							<ul class="side-nav" id="title">
								<?php foreach ($title as $key=>$value) { ?>
									<li><a href="#title,<?=create_slug($key);?>"><?=$key;?></a></li>
								<?php } ?>
							</ul>
						</div>
					</div>
				</div>

				<div class="col-2">
					<div class="tab_container">
						<div id="in" class="tab_content"><?=render_tab($position, "location_cmp", "location", "jobtitle", "company", "in"); ?></div>
						<div id="location" class="tab_content"><?=render_tab($location, "jobtitle_cmp", "location", "jobtitle", "company", "location"); ?></div>
						<div id="company" class="tab_content"><?=render_tab($company, "location_cmp", "location", "jobtitle", "company", "company"); ?></div>
						<div id="title" class="tab_content"><?=render_tab($title, "location_cmp", "location", "jobtitle", "company", "title"); ?></div>
					</div>
				</div>
			</div><!--end of jobs-content-->
        </div><!--end of jobs-container-->

    </div><!--end of main-->

<?php get_footer(); ?>
