<?
	require_once("jobs-config.php");

	// If the company name has a space, we wrap it in quotes
	function wrapquotes($x) {
		//if (strrpos($x,' ')) return "\"$x\""; else return $x;
		return "\"$x\"";
	}

	// take the name of something and convert it into something I can use in a URL
	function create_slug($v) {
		$retval = preg_replace("/[\/\\&:@\'\"\?\(\)\,\.\!\+]/"," ",strtolower(trim($v)));
		$retval = preg_replace("/\s\s+/"," ",$retval);
		$retval = preg_replace("/\s-\s|\s/","-",$retval);
		return $retval;
	}

	// create the markup for each tab that lists jobs
	function render_tab($jobs, $sortcmp, $first, $main, $second, $prefix) {

		$retval = "";

		foreach($jobs as $key=>$value) {
			$count = count($value);
			$retval .= "<a name=\"$prefix," . create_slug($key) . "\"></a>";
			$retval .= "<div class=\"cat\">";
			$retval .= "<h3 class=\"heading\">$key <span class=\"count\">($count)</span></h3>";
			$retval .= "<div class=\"jobs\">";

			usort($value, $sortcmp);

			foreach($value as $job) {
				$retval .= "<div class=\"job\">";
				$thing = $job->$second . ":" . $job->$main;
				$retval .= "<div class=\"col-a\">" . $job->$first . "</div>";
				$retval .= "<div class=\"col-b\"><a href=\"" . $job->url . "\"" ." onclick=\"recordOutboundLink(this, '$key', '$thing' );return true;\"" .">" . $job->$main . "</a> <span>(" . $job->$second . ")</span></div>";
				$retval .= "</div>";
			}
			$retval .= "</div>";
			$retval .= "</div>";
		}

		return $retval;
	}

	function get_data($url) {
		$ch = curl_init();
		$timeout = 5;
		curl_setopt($ch,CURLOPT_URL,$url);
		curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
		curl_setopt($ch,CURLOPT_CONNECTTIMEOUT,$timeout);
		$data = curl_exec($ch);
		curl_close($ch);
		return $data;
	}

	function get_position($title) {
		// parse the titles to try and determine what category the job belongs in
		if (preg_match("/QA|Quality Assurance/",$title)) {
			$position = "Engineering - QA";
		} elseif (preg_match("/Operations Associate|Procurement|Office Admin|Office Manager|Administrative Assistant|Executive Assistant|Chief of Staff|Office Administrator|Office Assistant/",$title)) {
			$position = "Administrative";
		} elseif (preg_match("/DBA|MySQL|Database|Data Operations/",$title)) {
			$position = "Database Administration";
		} elseif (preg_match("/Finance|Financial Analyst|Treasury|Controller|Tax Senior|Accountant|Accounts Payable|Payroll|Contracts Administrator|Contract Administrator|FP\&A|Legal|Counsel|Paralegal|General Ledger|Tax Manager/",$title)) {
			$position = "Legal & Finance";
		} elseif (preg_match("/Technical Sourcer|University Relations|Startup Talent Manager|Recruit|HR|Human Resources|Talent Acquisition/",$title)) {
			$position = "HR & Recruiting";
		} elseif (preg_match("/Community|Customer|Fanatic|Moderator|Evangelist|Contact Center Operations|Service Desk Manager/",$title)) {
			$position = "Community Management & Support";
		} elseif (preg_match("/Support|Trust and Safety/",$title)) {
			$position = "Customer Support";
		} elseif (preg_match("/Datacenter|Hardware Engineer|Datacenter Manager|Network Security|Network Engineer|DevOps|Dev Ops|Site Reliability|Tech Ops|Sysadmin|Release|IT Sys Admin|Operations Engineer|Systems Engineer|Systems Engineering|System Administrator|Data Center|System Admin|IT Administrator|Infrastructure|Online Operations|Systems Administrator|Systems Administator/",$title)) {
			$position = "Engineering - Operations";
		} elseif (preg_match("/Prototyper|Frontend|Front-End|Front End|jQuery|UI Engineer|UI Developer|User Interface Engineer|Front-end|Javascript|Flash/",$title)) {
			$position = "Engineering - Front End";
		} elseif (preg_match("/Visual|Artist|Graphic Designer|Art Director/i",$title)) {
			$position = "Design - Visual/Artist";
		} elseif (preg_match("/Interaction Design|Information Architect|UX|User Research|User Experience|Product Designer|Information Designer|UI Designer|User Interface Design/i",$title)) {
			$position = "Design - Interaction/UX";
		} elseif (preg_match("/Design/i",$title)) {
			$position = "Design";
		} elseif (preg_match("/iOS|Android|Blackberry|Mobile|Symbian|iPhone/",$title)) {
			$position = "Engineering - Mobile";
		} elseif ((preg_match("/^Architect|Software Architect|Development Manager|SDET|Engineer|ENGINEER|Technology|Developer|Security Architect|[^Information ]Architect|Ops|Release Manager/i",$title)) && (!preg_match("/Sales Engineer|Business/",$title))) {
		if (preg_match("/Senior|Sr|Lead/", $title)) {
		   $position = "Engineering - Senior";
		} elseif (preg_match("/VP|Manager|Chief|Director/", $title)) {
		  $position = "Engineering - Management";
		} else {
			$position = "Engineering";
		}
		} elseif  (preg_match("/Communications|Corporate Communications|Communications Manager|Marketing|Social Media|PR Coordinator|Events Coordinator|Events Program|Brand Manager|Public Relations|Market Research/",$title)) {
			$position = "Marketing";
		} elseif (preg_match("/Production|Operations|Supply Chain/",$title)) {
			$position = "Operations";
		} elseif (preg_match("/Product/",$title)) {
			$position = "Product Management";
		} elseif (preg_match("/Project|Program Manager|Producer|Netsuite|PMO|CRM Administrator/",$title)) {
			$position = "Project Management";
		}  elseif (preg_match("/Account |Agency and Brand|Sales|Business Develop|Partner Relations|Channel|Revenue|Relationship|Lead Gen|Client|Online Digital Media SALES|Partnerships|Sponsorship Development/",$title)) {
			$position = "Sales & Business Development";
		} elseif (preg_match("/Editor|Copywriter|Technical Writer|Writer|Content/",$title)) {
			$position = "Content & Editorial";
		} elseif (preg_match("/Insight|User Researcher|Chief Scientist|Data Engineer|Data Scientist|Data Analyst|Crime Analyst|Capacity Planning Analyst|Fraud Analyst|Optimization Analyst|Data Researcher|Research Analyst|BI Analyst|Business Intelligence|Reporting Analyst|Analytics|Data Warehouse|Statistical Analyst|Data Mining|Scientist|Research Assistant|Insights/", $title)) {
			$position = "Data & Analytics";
		} elseif (preg_match("/General Manager|Managing Director|Regional Director|Head of/", $title)) {
			$position = "General Management";
		} elseif (preg_match("/Country Lead|Global|Multinational|International|Territory|/", $title)) {
			$position = "International";
		} else  {
			$position = "Other";
		}

		return $position;
	}

	function location_cmp($a, $b) { return strcmp($a->location, $b->location); }
	function jobtitle_cmp($a, $b) { return strcmp($a->jobtitle, $b->jobtitle); }
	function company_cmp($a, $b) { return strcmp($a->company, $b->company); }
	function position_cmp($a, $b) { return strcmp($a->position, $b->position); }

?>