<?php get_header(); ?>

  <script>
		$(document).ready(function() {
			$.ajax(
				"http://0.0.0.0:5000",
				{
					crossDomain: true,
					dataType: "jsonp",
					jsonpCallback: 'handlePosts'
				}
			);

			$(".coming-soon").click(function(e){
				e.preventDefault();
				$("#alert").slideDown();
			});

			$("#close-alert").click(function(e) {
  	  		e.preventDefault();
  	  		$("#alert").slideUp();
			});
		});

		var handlePosts = function(html) {
			$("#posts-stream").html(html);
		}

	</script>
	
	<div id="main" role="main">
	<section class="featured-feed clearfix">
	<!--<h3 class="featured-title">Featured Posts</h3>-->
	
	<ul class="feed">
	
	<li>
	<div class="content">
	<a class="title" href="/posts/a-vc-some-thoughts-on-the-secs-rulemaking-on-general-solicitation" target="_blank">A VC: Some Thoughts On The SEC's Rulemaking On General Solicitation</a>
	
	<a href="http://www.avc.com/a_vc/2013/08/some-thoughts-on-the-secs-rulemaking-on-general-solicitation.html" class="source" target="_blank">www.avc.com</a>
	
	<div class="excerpt">It would be cool if one could tag a post with #secpubliccomment and have the post submitted to the SEC.</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/fredwilson" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/fredwilson" target="_blank">@fredwilson</a>
	<span class="time">Aug 29, 2013</span>
	<a href="/posts/a-vc-some-thoughts-on-the-secs-rulemaking-on-general-solicitation/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">4 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/a-vc-some-thoughts-on-the-secs-rulemaking-on-general-solicitation#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li class="hidden-xs">
	<div class="content">
	<a class="title" href="/posts/vhx" target="_blank">VHX</a>
	
	<a href="http://www.usv.com/2013/08/vhx.php" class="source" target="_blank">www.usv.com</a>
	
	<div class="excerpt">New investment from USV</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/aweissman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/344513261581924513/b3735cda4529be5530c9d29b6f8e148e_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/aweissman" target="_blank">@aweissman</a>
	<span class="time">August 29, 2013</span>
	<a href="/posts/vhx/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">3 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/vhx#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li class="hidden-xs">
	<div class="content">
	<a class="title" href="/posts/transparency-in-government-surveillance" target="_blank">Transparency in Government Surveillance</a>
	
	<a href="/posts/transparency-in-government-surveillance" class="source" target="_blank">usv.com</a>
	
	<div class="excerpt">Today, we have joined a large and diverse group of companies, non-profits and consumer advocates in an open letter urging the US government to allow internet and telecom companies to freely report statistics on government surveillance requests.  As we've discussed before, standing up for your users is a feature.  As we all move more and more of our lives online and into our phones, the data we are producing -- and sharing, whether we know it or not -- is growing exponentially. The extent to whic...</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/nickgrossman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/nickgrossman" target="_blank">@nickgrossman</a>
	<span class="time">July 18, 2013</span>
	<a href="/posts/transparency-in-government-surveillance/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">3 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/transparency-in-government-surveillance#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li class="hidden-xs">
	<div class="content">
	<a class="title" href="/posts/sigfig" target="_blank">SigFig</a>
	
	<a href="/posts/sigfig" class="source" target="_blank">usv.com</a>
	
	<div class="excerpt">Investment management is an increasingly important problem.  With the decline of defined benefit plans and the increasingly shaky social security system, most people will have to rely primarily on their savings and retirement accounts to fund living expenses after they stop working.  But investing is complicated and time consuming, and the array of options is bewildering to most people: stocks, bonds, mutual funds, ETFs, real estate partnerships, MLP's, etc.   Today we are announcing an investme...</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/johnbuttrick" target="_blank">
	<img src="https://si0.twimg.com/sticky/default_profile_images/default_profile_2_normal.png" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/johnbuttrick" target="_blank">@johnbuttrick</a>
	<span class="time">July 03, 2013</span>
	<a href="/posts/sigfig/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/sigfig#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li class="hidden-xs">
	<div class="content">
	<a class="title" href="/posts/firebase" target="_blank">Firebase</a>
	
	<a href="/posts/firebase" class="source" target="_blank">usv.com</a>
	
	<div class="excerpt">Arthur C. Clarke famously wrote that &quot;any sufficiently advanced technology is indistinguishable from magic.&quot; I have always had mixed feelings about this quote because as an engineer my reaction to something really advanced like self driving cars is to want to understand the science behind it. So does that mean there is no &quot;magic&quot; for engineers?  I remember first looking at Twilio and thinking it can't really be that easy to receive a phone call using a program. A couple lines of code? That's all...</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/albertwenger" target="_blank">
	<img src="https://si0.twimg.com/profile_images/1773890030/aew_artistic_normal.gif" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/albertwenger" target="_blank">@albertwenger</a>
	<span class="time">June 20, 2013</span>
	<a href="/posts/firebase/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/firebase#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li class="hidden-xs">
	<div class="content">
	<a class="title" href="/posts/auxmoney" target="_blank">Auxmoney</a>
	
	<a href="/posts/auxmoney" class="source" target="_blank">usv.com</a>
	
	<div class="excerpt">Today we are delighted to announce that we have made an investment in Auxmoney, an online credit marketplace in Germany. The CEO, Raffael Johnen was in London last week and appeared on a LeWeb panel with the CEOs of two other USV companies, Renaud Laplanche from Lending Club and Samir Desai from Funding Circle.   Like Lending Club, Auxmoney is a marketplace for consumer credit that matches consumers seeking loans with investors seeking better risk-adjusted returns than those offered by banks and...</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/johnbuttrick" target="_blank">
	<img src="https://si0.twimg.com/sticky/default_profile_images/default_profile_2_normal.png" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/johnbuttrick" target="_blank">@johnbuttrick</a>
	<span class="time">June 11, 2013</span>
	<a href="/posts/auxmoney/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">2 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/auxmoney#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li class="hidden-xs">
	<div class="content">
	<a class="title" href="/posts/yahoo-acquires-tumblr" target="_blank">Yahoo acquires Tumblr</a>
	
	<a href="/posts/yahoo-acquires-tumblr" class="source" target="_blank">usv.com</a>
	
	<div class="excerpt">Yahoo announced today that they will acquire our portfolio company Tumblr.   In September of 2007 we, together with Spark Capital, invested in a 3 person start-up founded by David Karp, a 21 year old coder who had not finished high school. At the time, our biggest challenge was convincing David to drop the four other projects he was working on to focus on Tumblr. Once he did, he quickly built one of the world's greatest platforms for self expression. Over the last five years, Tumblr became much ...</div>
	<div class="meta">
	<div class="avatar">
	<a href="http://www.twitter.com/BradUSV" target="_blank">
	<img src="https://si0.twimg.com/profile_images/52435733/bio_brad_normal.jpg" alt="thumbnail">
	</a>
	</div>
	<a class="username" href="http://www.twitter.com/BradUSV" target="_blank">@BradUSV</a>
	<span class="time">May 20, 2013</span>
	<a href="/posts/yahoo-acquires-tumblr/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/yahoo-acquires-tumblr#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	</ul><!--end of feed-->
	<a class="more-link" href="/featured_posts">See All Featured Posts</a>
	</section><!--end of featured-feed-->
	<section class="hot-newest-feed">
	<ul class="tabs">
	  <li class="is-active"><a class="btn" href="?sort_by=hot">Hot</a></li>
	  <li><a class="btn" href="?sort_by=new">Newest</a></li>
	  <li class="submit-btn"><a class="btn btn-primary" href="">Submit a post</a></li>
	</ul>
	<ul class="feed">
	
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/garychou" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3292748896/a94514170806ebf29c2f481023217967_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.wired.com/opinion/2013/09/focus-on-people-not-tech-and-other-impt-lessons-for-interaction-design-and-life/" target="_blank">Let’s Stop Focusing on Shiny Gadgets and Start Using Tech to Empower People</a>
	<a href="http://www.wired.com/opinion/2013/09/focus-on-people-not-tech-and-other-impt-lessons-for-interaction-design-and-life/" class="source" target="_blank">www.wired.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/garychou" target="_blank">@garychou</a>
	<span class="time">14 hours ago</span>
	<a href="/posts/lets-stop-focusing-on-shiny-gadgets-and-start-using-tech-to-empower-people/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">40 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/lets-stop-focusing-on-shiny-gadgets-and-start-using-tech-to-empower-people#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/fredwilson" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://falkvinge.net/2013/08/31/more-thoughts-on-the-coming-swarm-economy/" target="_blank">More Thoughts On The Coming Swarm Economy - Falkvinge on Infopolicy</a>
	<a href="http://falkvinge.net/2013/08/31/more-thoughts-on-the-coming-swarm-economy/" class="source" target="_blank">falkvinge.net</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/fredwilson" target="_blank">@fredwilson</a>
	<span class="time">2 hours ago</span>
	<a href="/posts/more-thoughts-on-the-coming-swarm-economy-falkvinge-on-infopolicy/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">2 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/more-thoughts-on-the-coming-swarm-economy-falkvinge-on-infopolicy#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/christinacaci" target="_blank">
	<img src="https://si0.twimg.com/profile_images/1043543563/temp_normal.jpg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://mobile.theverge.com/2013/2/6/3950664/phil-zimmermann-wants-to-save-you-from-your-phone" target="_blank">Phil Zimmerman's looking even more prescient these days</a>
	<a href="http://mobile.theverge.com/2013/2/6/3950664/phil-zimmermann-wants-to-save-you-from-your-phone" class="source" target="_blank">mobile.theverge.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/christinacaci" target="_blank">@christinacaci</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/phil-zimmermans-looking-even-more-prescient-these-days/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">10 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/phil-zimmermans-looking-even-more-prescient-these-days#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/bwats" target="_blank">
	<img src="https://si0.twimg.com/profile_images/378800000426206820/2f6d04c6b302bf60423190f62b4005ce_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://brianwatson.me/post/60459985680/ios-first-android-second" target="_blank">iOS First, Android Second</a>
	<a href="http://brianwatson.me/post/60459985680/ios-first-android-second" class="source" target="_blank">brianwatson.me</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/bwats" target="_blank">@bwats</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/ios-first-android-second/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">8 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/ios-first-android-second#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/bwats" target="_blank">
	<img src="https://si0.twimg.com/profile_images/378800000426206820/2f6d04c6b302bf60423190f62b4005ce_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://epicbrowser.com/" target="_blank">If DuckDuckGo built a browser... | &quot;Epic Privacy Browser&quot;</a>
	<a href="http://epicbrowser.com/" class="source" target="_blank">epicbrowser.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/bwats" target="_blank">@bwats</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/if-duckduckgo-built-a-browser-epic-privacy-browser/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">6 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/if-duckduckgo-built-a-browser-epic-privacy-browser#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/aweissman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/344513261581924513/b3735cda4529be5530c9d29b6f8e148e_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.asymco.com/2013/09/06/third-to-a-billion/" target="_blank">Third to a billion | asymco</a>
	<a href="http://www.asymco.com/2013/09/06/third-to-a-billion/" class="source" target="_blank">www.asymco.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/aweissman" target="_blank">@aweissman</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/third-to-a-billion-asymco/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/third-to-a-billion-asymco#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/fredwilson" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://continuations.com/post/60444129080/disagreeing-with-bruce-schneier-more-crypto-is-not-the" target="_blank">Continuations : Disagreeing with Bruce Schneier: More Crypto is Not the Answer</a>
	<a href="http://continuations.com/post/60444129080/disagreeing-with-bruce-schneier-more-crypto-is-not-the" class="source" target="_blank">continuations.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/fredwilson" target="_blank">@fredwilson</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/continuations-disagreeing-with-bruce-schneier-more-crypto-is-not-the-answer/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">3 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/continuations-disagreeing-with-bruce-schneier-more-crypto-is-not-the-answer#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/nickgrossman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.theverge.com/2013/9/5/4696618/google-chrome-apps-chrome-os-windows-os-x-blink" target="_blank">Google's Trojan horse: how Chrome Apps will finally take on Windows | The Verge</a>
	<a href="http://www.theverge.com/2013/9/5/4696618/google-chrome-apps-chrome-os-windows-os-x-blink" class="source" target="_blank">www.theverge.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/nickgrossman" target="_blank">@nickgrossman</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/googles-trojan-horse-how-chrome-apps-will-finally-take-on-windows-the-verge/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">2 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/googles-trojan-horse-how-chrome-apps-will-finally-take-on-windows-the-verge#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/nickgrossman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://nickgrossman.is/post/60439679445/social-connections-from-something-you-inherit-to" target="_blank">Social Connections: from Something You Inherit to Something You Earn | Nick Grossman's Slow Hunch</a>
	<a href="http://nickgrossman.is/post/60439679445/social-connections-from-something-you-inherit-to" class="source" target="_blank">nickgrossman.is</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/nickgrossman" target="_blank">@nickgrossman</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/social-connections-from-something-you-inherit-to-something-you-earn-nick-grossmans-slow-hunch/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/social-connections-from-something-you-inherit-to-something-you-earn-nick-grossmans-slow-hunch#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/nickgrossman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.theguardian.com/world/2013/sep/05/nsa-gchq-encryption-codes-security" target="_blank">NSA and GCHQ unlock privacy and security on the internet | World news | The Guardian</a>
	<a href="http://www.theguardian.com/world/2013/sep/05/nsa-gchq-encryption-codes-security" class="source" target="_blank">www.theguardian.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/nickgrossman" target="_blank">@nickgrossman</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/nsa-and-gchq-unlock-privacy-and-security-on-the-internet-world-news-the-guardian/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/nsa-and-gchq-unlock-privacy-and-security-on-the-internet-world-news-the-guardian#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/aweissman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/344513261581924513/b3735cda4529be5530c9d29b6f8e148e_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://andrewchen.co/2013/09/03/ignore-pr-and-buzz-use-google-trends-to-assess-traction-instead/" target="_blank">Ignore PR and buzz, use Google Trends to assess traction instead</a>
	<a href="http://andrewchen.co/2013/09/03/ignore-pr-and-buzz-use-google-trends-to-assess-traction-instead/" class="source" target="_blank">andrewchen.co</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/aweissman" target="_blank">@aweissman</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/ignore-pr-and-buzz-use-google-trends-to-assess-traction-instead/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/ignore-pr-and-buzz-use-google-trends-to-assess-traction-instead#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/aweissman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/344513261581924513/b3735cda4529be5530c9d29b6f8e148e_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.theguardian.com/commentisfree/2013/sep/05/government-betrayed-internet-nsa-spying" target="_blank">The US government has betrayed the internet. We need to take it back | Bruce Schneier</a>
	<a href="http://www.theguardian.com/commentisfree/2013/sep/05/government-betrayed-internet-nsa-spying" class="source" target="_blank">www.theguardian.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/aweissman" target="_blank">@aweissman</a>
	<span class="time">September 06, 2013</span>
	<a href="/posts/the-us-government-has-betrayed-the-internet-we-need-to-take-it-back-bruce-schneier/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/the-us-government-has-betrayed-the-internet-we-need-to-take-it-back-bruce-schneier#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/aweissman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/344513261581924513/b3735cda4529be5530c9d29b6f8e148e_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://hunterwalk.com/2013/09/05/web-rings-for-the-win-adding-zemanta-tech-circles-to-my-blog/" target="_blank">Web Rings For The Win! Adding Zemanta Tech Circles to My Blog | Hunter Walk</a>
	<a href="http://hunterwalk.com/2013/09/05/web-rings-for-the-win-adding-zemanta-tech-circles-to-my-blog/" class="source" target="_blank">hunterwalk.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/aweissman" target="_blank">@aweissman</a>
	<span class="time">September 05, 2013</span>
	<a href="/posts/web-rings-for-the-win-adding-zemanta-tech-circles-to-my-blog-hunter-walk/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">2 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/web-rings-for-the-win-adding-zemanta-tech-circles-to-my-blog-hunter-walk#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/albertwenger" target="_blank">
	<img src="https://si0.twimg.com/profile_images/1773890030/aew_artistic_normal.gif" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="https://www.aboutthedata.com/" target="_blank">AboutTheData.com</a>
	<a href="https://www.aboutthedata.com/" class="source" target="_blank">www.aboutthedata.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/albertwenger" target="_blank">@albertwenger</a>
	<span class="time">September 05, 2013</span>
	<a href="/posts/aboutthedatacom/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">2 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/aboutthedatacom#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/aweissman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/344513261581924513/b3735cda4529be5530c9d29b6f8e148e_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://finance.fortune.cnn.com/2013/09/03/venture-capital-classic/?utm_source=buffer&amp;utm_campaign=Buffer&amp;utm_content=bufferb1b3b&amp;utm_medium=twitter" target="_blank">Defending the defense of venture capital “classic.</a>
	<a href="http://finance.fortune.cnn.com/2013/09/03/venture-capital-classic/?utm_source=buffer&amp;utm_campaign=Buffer&amp;utm_content=bufferb1b3b&amp;utm_medium=twitter" class="source" target="_blank">finance.fortune.cnn.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/aweissman" target="_blank">@aweissman</a>
	<span class="time">September 05, 2013</span>
	<a href="/posts/defending-the-defense-of-venture-capital-classic/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/defending-the-defense-of-venture-capital-classic#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/fredwilson" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.youtube.com/watch?v=aXSY6bxdWGQ" target="_blank">Joe Lhota on the power of open data and open innovation</a>
	<a href="http://www.youtube.com/watch?v=aXSY6bxdWGQ" class="source" target="_blank">www.youtube.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/fredwilson" target="_blank">@fredwilson</a>
	<span class="time">September 05, 2013</span>
	<a href="/posts/joe-lhota-on-the-power-of-open-data-and-open-innovation/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">2 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/joe-lhota-on-the-power-of-open-data-and-open-innovation#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/AlexanderMPease" target="_blank">
	<img src="https://si0.twimg.com/profile_images/2425968860/zg9wdsxlfgecxog9lkwz_normal.png" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://techcrunch.com/2013/09/05/bitalino/" target="_blank">How to hack on medical QS</a>
	<a href="http://techcrunch.com/2013/09/05/bitalino/" class="source" target="_blank">techcrunch.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/AlexanderMPease" target="_blank">@AlexanderMPease</a>
	<span class="time">September 05, 2013</span>
	<a href="/posts/how-to-hack-on-medical-qs/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/how-to-hack-on-medical-qs#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/fredwilson" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3580641456/82c873940343750638b7caa04b4652fe_normal.jpeg" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.polygon.com/features/2013/9/4/4660780/bitcoin-satoshi-nakamoto" target="_blank">The ghost of Bitcoin | Polygon</a>
	<a href="http://www.polygon.com/features/2013/9/4/4660780/bitcoin-satoshi-nakamoto" class="source" target="_blank">www.polygon.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/fredwilson" target="_blank">@fredwilson</a>
	<span class="time">September 04, 2013</span>
	<a href="/posts/the-ghost-of-bitcoin-polygon/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">4 votes</span>
	</a>
	
	<a class="comments-count" href="/posts/the-ghost-of-bitcoin-polygon#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/nickgrossman" target="_blank">
	<img src="https://si0.twimg.com/profile_images/3608605926/71036b2e9d4deff52fdacd8196c40ce5_normal.png" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://www.theatlantic.com/technology/archive/2012/04/social-medias-small-positive-role-in-human-relationships/256346/" target="_blank">Social Media's Small, Positive Role in Human Relationships - Zeynep Tufekci - The Atlantic</a>
	<a href="http://www.theatlantic.com/technology/archive/2012/04/social-medias-small-positive-role-in-human-relationships/256346/" class="source" target="_blank">www.theatlantic.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/nickgrossman" target="_blank">@nickgrossman</a>
	<span class="time">September 05, 2013</span>
	<a href="/posts/social-medias-small-positive-role-in-human-relationships-zeynep-tufekci-the-atlantic/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/social-medias-small-positive-role-in-human-relationships-zeynep-tufekci-the-atlantic#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	<li>
	<div class="avatar">
	<a href="http://www.twitter.com/br_ttany" target="_blank">
	<img src="https://si0.twimg.com/profile_images/1217456552/theoffice_normal.JPG" alt="thumbnail">
	</a>
	</div>
	<div class="content">
	
	<a class="title" href="http://dealbook.nytimes.com/2013/09/04/lending-start-up-commonbond-raises-100-million-with-pandit-as-investor/?_r=0" target="_blank">Lending Start-Up CommonBond Raises $100 Million, With Pandit as Investor</a>
	<a href="http://dealbook.nytimes.com/2013/09/04/lending-start-up-commonbond-raises-100-million-with-pandit-as-investor/?_r=0" class="source" target="_blank">dealbook.nytimes.com</a>
	
	<div class="meta">
	<a class="username" href="http://www.twitter.com/br_ttany" target="_blank">@br_ttany</a>
	<span class="time">September 04, 2013</span>
	<a href="/posts/lending-start-up-commonbond-raises-100-million-with-pandit-as-investor/upvote" class="votes-count ajax_upvote_link upvote-button">
	<i class="icon-arrow-up icon"></i>
	<span class="value">1 vote</span>
	</a>
	
	<a class="comments-count" href="/posts/lending-start-up-commonbond-raises-100-million-with-pandit-as-investor#disqus_thread" target="_blank">0 comments</a>
	</div>
	</div>
	</li>
	
	</ul><!--end of feed-->
	<div id="pagination-next-prev">
	
	
	<a class="next-page" href="?sort_by=hot&anchor=522781a1c5de030011364836&action=after&count=20">Next</a>
	
	</div>
	</section>
	</div><!--end of main-->
	
	
	
	
	
<?php /*
<div id="community">

<div class="primary clearfix">
		<div class="container">


		<div class="jumbotron">
		  <p><b>Union Square Ventures</b> is a small, collegial partnership managing $700,000,000 across four funds. Our portfolio companies create services that have the potential to fundamentally transform important markets.</p>
		</div>

		<!--<div class="posts-intro">
			USV community

		</div>-->
		<nav class="clearfix section-nav">
		  <ul class="btn-list-horz" id="stream-nav">
			  <!--<li class="community-label">USV Community</li>-->
			  <li class="is-active"><a class="btn btn-small" href="#">Hot</a></li>
			  <li><a class="btn btn-small" href="#">New</a></li>
			<li style="float: right"><a class="btn btn-small btn-primary" id="submit-btn" href="<?php bloginfo('siteurl'); ?>/submit">+ Submit a post</a></li>
		  </ul>
		</nav>	


		<div id="post-form" class="is-visuallyhidden">
		  <form id="quick-add-form" action="#" method="post">
			<fieldset class="clearfix">
			  <h5 class="form-title">Submit a Post</h5>
			  <p><input type="text" class="input-block" name="title" placeholder="Title" autocomplete="false"></p>
			  <p><input type="text" class="input-block" name="url" placeholder="URL" autocomplete="false"></p>
			  <p><textarea class="input-block" name="body" placeholder="Notes"></textarea></p>
			  <input type="submit" class="btn btn-primary" value="Submit Post">
			  <a href="#" class="" id="close-post-form">Cancel</a>
			</fieldset>
		  </form>
		</div>

		<ul class="unstyled-list post-list" id="posts-stream">
		  <?php for ($i = 0; $i < 15; $i++): ?>
		  <li>
			<article class="post clearfix">
			  <span class="avatar"><img class="avatar" src="<?php bloginfo('template_directory'); ?>/images/avatar-fredwilson.png"></span>
			  <h4 class="post-title"><a class="link" href="#">Kickstarter &amp; Network Effects <span class="source">www.kickstarter.com</span></a></h4>
			  <div class="meta">
				  <span><a class="username" href="http://www.twitter.com/br_ttany" target="_blank">@br_ttany</a></span>
				  <span class="time">1 minute ago</span>
				  <a href="/posts/connect-up-finalist-orchestra-puts-users-at-center-stage-psfk/upvote" class="votes-count ajax_upvote_link upvote-button">
				  <span class="value">1 vote</span>
				  </a>
				  <a class="comments-count" href="/posts/connect-up-finalist-orchestra-puts-users-at-center-stage-psfk#disqus_thread" target="_blank" data-disqus-identifier="522f4c83cebbd4001156b22e">0 </a>
			  </div>
		  	</article>
		  </li>
		  <?php endfor; ?>
	  </ul>


		</div>
	  </div>

  	<div class="secondary clearfix">
		<div class="container">

			<!--<div class="posts-intro">
				Featured		
			</div>-->

		<ul class="unstyled-list post-list">
			<?php for ($i = 0; $i < 4; $i++): ?>
			<li>
				<article class="post clearfix">
				  <h4 class="post-title"><a class="link" href="#">VHX <span class="source">usv.com</span></a></h4>
				  <p>Content distribution has traditionally been defined by scarcity: in the number of channels available to watch TV; the number of theaters to watch films; the number of radio stations to listen to music; the number of bookstores to buy books; and so-on. The Internet, however, fundamentally alters this dynamic, by vastly increasing the number of distribution points as well as the number of content choices that an average person has. If one wanted to watch a movie today they could do so via Netflix, Amazon, Apple, Youtube, Vudu, Vimeo and many, many other channels. And with technologies like Chromecast and...</p>
				  <div class="meta">
					 <span class="avatar"><img class="avatar" src="<?php bloginfo('template_directory'); ?>/images/avatar-aweissman.png"></span>
					  <span class="author"><a href="http://twitter.com/aweissman">@aweissman</a></span>
					  <span class="date nobreak">August 29, 2013</span> <br />
					  <a href="/posts/connect-up-finalist-orchestra-puts-users-at-center-stage-psfk/upvote" class="votes-count ajax_upvote_link upvote-button">
					  <span class="value">1 vote</span>
					  </a>
					  <a class="comments-count" href="/posts/connect-up-finalist-orchestra-puts-users-at-center-stage-psfk#disqus_thread" target="_blank" data-disqus-identifier="522f4c83cebbd4001156b22e">0 </a>

				  </div>

				  <!--<div class="actions">
					<a href="#" class="likes"><img src="<?php bloginfo('template_directory'); ?>/images/heart.png">&nbsp;28</a>
					<a href="#" class="comments"><img src="<?php bloginfo('template_directory'); ?>/images/balloon.png">&nbsp;11</a>
				  </div>-->
				</article>
			  </li>
			<?php endfor; ?>
		</ul>

	  </div>
	  </div>

</div><!-- /community -->
*/ ?>

  <?php get_footer(); ?>
