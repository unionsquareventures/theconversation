import app.basic

#####################
### Google Hangout Shortcuts
### /brian /albert, etc
#####################
class HangoutShortcuts(app.basic.BaseHandler):
  def get(self, name):
    new_url = '/'
    #
    # google hangout shortcuts
    #
    if self.request.path == '/albert':
      new_url = 'https://plus.google.com/hangouts/_/event/cdhdic31990mu30tmdbec3ucbos'
    elif self.request.path == '/andy':
      new_url = 'https://plus.google.com/hangouts/_/event/coak3i6919ch7m9dvlq50no4smo'
    elif self.request.path == '/brad':
      new_url = 'https://plus.google.com/hangouts/_/event/cd8eu889t345f9ht2i4tf68o26k'
    elif self.request.path == '/brian':
      new_url = 'https://plus.google.com/hangouts/_/event/cih6nepuqsbt1trfaegmubvpjps'
    elif self.request.path == '/brittany':
      new_url = 'https://plus.google.com/hangouts/_/event/c46j88paq1gt2dqs2rt8ulmlfp0'
    elif self.request.path == '/conferenceroom':
      new_url = 'https://plus.google.com/hangouts/_/event/csjrctgcaphdptmqacnfisq0i2g'
    elif self.request.path == '/conference':
      new_url = 'https://plus.google.com/hangouts/_/event/csjrctgcaphdptmqacnfisq0i2g'
    elif self.request.path == '/eventspace':
      new_url = 'https://plus.google.com/hangouts/_/event/csrdap1091spu3cg3kvgs8o9a08'
    elif self.request.path == '/library':
      new_url = 'https://plus.google.com/hangouts/_/event/cltm1dbi65rplvbpcvptbm5n35s'
    elif self.request.path == '/fred':
      new_url = 'https://plus.google.com/hangouts/_/event/cis1kcq11fkqlj12egf0pu74tlc'
    elif self.request.path == '/john':
      new_url = 'https://plus.google.com/hangouts/_/event/ctqb0oilbu12jor3sa1j9mn9jto'
    elif self.request.path == '/nick':
      new_url = 'https://plus.google.com/hangouts/_/event/cmnm4k9uet7ctf18eqs5ih417r4'
    elif self.request.path == '/zander':
      new_url = 'https://plus.google.com/hangouts/_/event/cagmh53vocn6pvc0b6su6k6ovd4'
    
    #
    # do the redirect
    #
    self.redirect(new_url, permanent=True)


#####################
### REDIRECT OLD LINKS TO NEW LOCATIONS
### /pages/.*$ /team.*$ /investments$ /focus$
#####################
class RedirectMappings(app.basic.BaseHandler):
  def get(self):
    new_url = '/'
    if self.request.path.find('/portfolio/') == 0:
        new_url = '/portfolio'
    #
    # foursquare shortcut
    #
    elif self.request.path == '/office':
      new_url = 'https://foursquare.com/v/union-square-ventures/4a17665af964a52056791fe3'
    #
    # google hangout shortcuts
    #
    elif self.request.path == '/albert':
      new_url = 'https://plus.google.com/hangouts/_/event/cdhdic31990mu30tmdbec3ucbos'
    elif self.request.path == '/andy':
      new_url = ''
    elif self.request.path == '/brad':
      new_url = ''
    elif self.request.path == '/brian':
      new_url = 'https://plus.google.com/hangouts/_/event/cih6nepuqsbt1trfaegmubvpjps'
    elif self.request.path == '/brittany':
      new_url = ''
    elif self.request.path == '/conferenceroom':
      new_url = ''
    elif self.request.path == '/eventspace':
      new_url = ''
    elif self.request.path == '/fred':
      new_url = 'https://plus.google.com/hangouts/_/event/cis1kcq11fkqlj12egf0pu74tlc'
    elif self.request.path == '/john':
      new_url = ''
    elif self.request.path == '/nick':
      new_url = ''
    elif self.request.path == '/zander':
      new_url = ''
    elif self.request.path.find('/network/') == 0:
        new_url = '/network'
    elif self.request.path.find('/about/') == 0:
        new_url = '/about'
    elif self.request.path.find('/jobs/') == 0:
        new_url = '/jobs'
    elif self.request.path.find('brad') > -1:
      new_url = '/about#brad-burnham'
    elif self.request.path.find('fred') > -1:
      new_url = '/about#fred-wilson'
    elif self.request.path.find('albert') > -1:
      new_url = '/about#albert-wenger'
    elif self.request.path.find('/team') > -1:
      new_url = '/about'
    elif self.request.path.find('focus') > -1:
      new_url = '/about'
    elif self.request.path.find('investments') > -1:
      new_url = '/portfolio'
    elif self.request.path.find('pages') > -1:
      team = [
        'brad-burnham',
        'fred-wilson',
        'albert-wenger',
        'john-buttrick',
        'andy-weissman',
        'nick-grossman',
        'kerri-rachlin',
        'veronica-keaveney',
        'gillian-campbell',
        'brittany-laughlin',
        'alexander-pease',
        'brian-watson'
      ]
      for person in team:
        if self.request.path.find(person) > -1:
          new_url = '/about#' + person

    self.redirect(new_url, permanent=True)

#####################
### REDIRECT OLD POST REQUESTS TO NEW LOCATIONS
### /(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<slug>[\w\s-]+).php$
#####################
class RedirectPosts(app.basic.BaseHandler):
  def get(self, year, month, slug):
    new_url = '/'
    try:
      url = '/%s/%s/%s.php' % (year, month, slug)
      # hard coded mapping of old post urls
      old_posts = {
        "/2005/09/is-bill-gates-t.php": "/posts/is-bill-gates-the-cat-with-nine-lives",
        "/2005/10/location-locati.php": "/posts/location-location-location",
        "/2005/10/the-problem-wit.php": "/posts/the-problem-with-podcasts",
        "/2005/10/wikis.php": "/posts/wikis",
        "/2005/10/inspiration.php": "/posts/inspiration",
        "/2005/10/downturns.php": "/posts/downturns",
        "/2005/10/impact-media.php": "/posts/impact-media",
        "/2005/10/a-new-dimension.php": "/posts/a-new-dimension",
        "/2005/10/indeed.php": "/posts/indeed",
        "/2005/10/delicious.php": "/posts/delicious",
        "/2005/10/audience-manage.php": "/posts/audience-management",
        "/2005/09/union-square-ve.php": "/posts/union-square-ventures",
        "/2005/10/10-steps-to-a-h.php": "/posts/10-steps-to-a-hugely-successful-web-20-company",
        "/2005/10/founders.php": "/posts/founders",
        "/2005/10/hello-world.php": "/posts/hello-world",
        "/2005/10/web-services-ar.php": "/posts/web-services-are-different",
        "/2005/10/metrics.php": "/posts/metrics",
        "/2005/10/management-case.php": "/posts/management-case-base-case-and-worst-case",
        "/2005/10/usv-sessions-1.php": "/posts/union-square-sessions-1-peer-production",
        "/2005/10/usv-sessions-1-1.php": "/posts/union-square-sessions-1-photos",
        "/2005/10/union-square-se.php": "/posts/union-square-sessions-1-transcript",
        "/2005/10/peer-production.php": "/posts/peer-production-in-action",
        "/2005/10/we-dont-get-it.php": "/posts/we-dont-get-it",
        "/2005/10/vc-cliche-of-th.php": "/posts/vc-cliche-of-the-week",
        "/2005/10/seeking-a-super.php": "/posts/seeking-a-super-talented-productdesign-person",
        "/2005/10/sessions-top-te.php": "/posts/sessions-top-ten-insights-one",
        "/2005/10/post.php": "/posts/sessions-top-ten-insights-two",
        "/2005/11/sessions-top-te-2.php": "/posts/sessions-top-ten-insights-three",
        "/2005/11/vc-cliche-of-th-1.php": "/posts/vc-cliche-of-the-week-2",
        "/2005/11/sessions-top-te-1.php": "/posts/sessions-top-ten-insights-four",
        "/2005/11/will-live-kill.php": "/posts/will-live-kill",
        "/2005/11/sessions-top-te-3.php": "/posts/sessions-top-ten-insights-five",
        "/2005/11/vc-cliche-of-th-2.php": "/posts/vc-cliche-of-the-week-3",
        "/2005/11/are-reputations.php": "/posts/sessions-top-ten-insights-six-reputations-are-not-portable",
        "/2005/11/our-customer-is.php": "/posts/our-customer-is-the-entrepreneur",
        "/2005/11/sessions-top-te-5.php": "/posts/sessions-top-ten-insights-seven-less-control-can-create-more-value",
        "/2005/11/cliche-of-the-w.php": "/posts/cliche-of-the-week",
        "/2005/11/sessions-top-te-4.php": "/posts/sessions-top-ten-insights-eight-putting-a-string-on-data",
        "/2005/11/evolution-vs-in.php": "/posts/evolution-vs-intelligent-design",
        "/2005/11/cliche-of-the-w-1.php": "/posts/cliche-of-the-week-2",
        "/2005/11/powered-by.php": "/posts/powered-by",
        "/2005/11/cliche-of-the-w-2.php": "/posts/cliche-of-the-week-3",
        "/2005/12/cliche-of-the-w-3.php": "/posts/cliche-of-the-week-4",
        "/2005/12/a-delicious-eig-1.php": "/posts/a-delicious-eight-months",
        "/2005/12/cliche-of-the-w-4.php": "/posts/cliche-of-the-week-5",
        "/2005/12/cliche-of-the-w-5.php": "/posts/cliche-of-the-week-6",
        "/2006/01/vc-cliche-of-th-3.php": "/posts/cliche-of-the-week-7",
        "/2006/01/cliche-of-the-w-6.php": "/posts/cliche-of-the-week-8",
        "/2006/01/web-services-in.php": "/posts/web-services-in-the-mist",
        "/2006/01/rich-media-real.php": "/posts/rich-media-realities",
        "/2006/01/advertising-out.php": "/posts/advertising-out-of-context",
        "/2006/01/instant-job-boa.php": "/posts/instant-job-board",
        "/2006/01/indeed-job-data-1.php": "/posts/indeed-job-data",
        "/2006/01/physics-the-sec.php": "/posts/physics-the-second-law-of-thermodynamics",
        "/2006/02/web-20-is-an-ox.php": "/posts/web-20-is-an-oxymoron",
        "/2006/02/post-1.php": "/posts/mathematics-how-much-is-enough",
        "/2006/02/feedburner.php": "/posts/feedburner",
        "/2006/02/why-we-invested.php": "/posts/why-we-invested-in-feedburner",
        "/2006/02/research-and-de.php": "/posts/research-and-development",
        "/2006/02/advisory-capita.php": "/posts/advisory-capital",
        "/2006/02/web-services-an.php": "/posts/web-services-and-devices",
        "/2006/03/tacoda-raises-1.php": "/posts/tacoda-raises-12-million",
        "/2006/03/looking-ahead.php": "/posts/looking-ahead",
        "/2006/03/will-computing-1.php": "/posts/will-computing-ever-be-as-invisible-as-electricity",
        "/2006/03/yes-but.php": "/posts/yes-but",
        "/2006/04/taking-web-serv.php": "/posts/taking-web-services-to-the-office",
        "/2006/04/why-has-the-flo.php": "/posts/why-has-the-flow-of-technology-reversed",
        "/2006/05/a-stray-thought-1.php": "/posts/a-stray-thought-on-the-micro-chunking-of-media",
        "/2006/05/user-tagging-is-1.php": "/posts/user-tagging-is-fundamental",
        "/2006/05/on-influence-1.php": "/posts/on-influence",
        "/2006/05/introducing-bug.php": "/posts/introducing-bug-labs",
        "/2006/05/advertising-to.php": "/posts/advertising-to-job-seekers",
        "/2006/05/what-else-are-y.php": "/posts/what-else-are-you-interested-in",
        "/2006/05/replicating-sil.php": "/posts/replicating-silicon-valley",
        "/2006/06/how-does-indeed-1.php": "/posts/how-does-indeed-make-money",
        "/2006/06/etsy-1.php": "/posts/etsy",
        "/2006/06/why-we-admire-c.php": "/posts/why-we-admire-craigslist",
        "/2006/06/oddcast.php": "/posts/oddcast",
        "/2006/06/union-square-se-1.php": "/posts/union-square-sessions-2-public-policy-and-innovation",
        "/2006/06/sessions.php": "/posts/sessions",
        "/2006/07/a-bittersweet-m.php": "/posts/a-bittersweet-moment",
        "/2006/07/through-the-loo-1.php": "/posts/through-the-looking-glass-into-the-net-neutrality-debate",
        "/2006/07/sessions-patent.php": "/posts/do-patents-encourage-or-stifle-innovation",
        "/2010/01/we-need-an-independent-invention-defense-to-minimize-the-damage-of-aggressive-patent-trolls.php": "/posts/we-need-an-independent-invention-defense-to-minimize-the-damage-of-aggressive-patent-trolls",
        "/2006/07/looking-for-the.php": "/posts/looking-for-the-right-person",
        "/2006/08/our-focus.php": "/posts/our-focus",
        "/2006/08/potential-to-ch-1.php": "/posts/potential-to-change-the-structure-of-markets",
        "/2006/08/information-tec.php": "/posts/information-technology-leverage",
        "/2006/08/defensibility.php": "/posts/defensibility",
        "/2006/08/scalability.php": "/posts/scalability",
        "/2006/08/business-develo.php": "/posts/business-development-20",
        "/2006/08/welcome-andrew-1.php": "/posts/welcome-andrew-parker",
        "/2006/09/other-things-we.php": "/posts/other-things-we-look-for",
        "/2006/09/history-doesnt-1.php": "/posts/history-doesnt-repeat-itself-but-it-does-rhyme",
        "/2006/09/early-stage-inv.php": "/posts/early-stage-investing",
        "/2006/09/traction.php": "/posts/traction",
        "/2006/10/lead-investor.php": "/posts/lead-investor",
        "/2006/10/deal-size-1.php": "/posts/deal-size",
        "/2006/11/customer-servic.php": "/posts/customer-service-is-the-new-marketing",
        "/2006/11/geography-1.php": "/posts/geography",
        "/2007/01/founders-and-ma.php": "/posts/founders-and-management",
        "/2007/01/why-we-dont-inv.php": "/posts/why-we-dont-invest-in-competitive-businesses",
        "/2007/01/whats-next.php": "/posts/whats-next",
        "/2007/01/siaa-preview-ke-1.php": "/posts/siaa-preview-keynote",
        "/2007/02/adaptiveblue.php": "/posts/adaptiveblue",
        "/2007/02/outsidein.php": "/posts/outsidein",
        "/2007/04/targetspot-1.php": "/posts/targetspot",
        "/2007/04/reserves.php": "/posts/reserves",
        "/2007/04/cash-flow-forec-1.php": "/posts/cash-flow-forecasting-isnt-what-it-used-to-be",
        "/2007/05/job-board.php": "/posts/job-board",
        "/2007/05/who-do-you-trus.php": "/posts/who-do-you-trust-to-edit-your-news",
        "/2007/05/dick-costolo-on.php": "/posts/dick-costolo-on-wallstrip",
        "/2007/05/feedburner-is-a.php": "/posts/feedburner-is-acquired-by-google",
        "/2007/06/wesabe-is-more.php": "/posts/wesabe-is-more-than-a-personal-financial-service",
        "/2007/06/introducing-alb.php": "/posts/introducing-albert-wenger",
        "/2007/07/clickable.php": "/posts/clickable",
        "/2007/07/twitter.php": "/posts/twitter",
        "/2007/07/aoltime-warner-1.php": "/posts/aoltime-warner-buys-tacoda",
        "/2007/08/hiring-a-vp-of.php": "/posts/hiring-a-vp-of-engineering-or-cto-for-non-techie-first-time-founders",
        "/2007/09/what-i-want-fro-1.php": "/posts/what-i-want-from-bug-labs",
        "/2007/09/post-2.php": "/posts/there-are-no-open-web-services",
        "/2007/09/i-want-a-new-pl.php": "/posts/i-want-a-new-platform",
        "/2007/09/union-square-se-2.php": "/posts/union-square-sessions-3-hacking-philanthropy",
        "/2007/10/hacking-philant.php": "/posts/hacking-philanthropy-the-transcript",
        "/2010/02/twilio.php": "/posts/twilio",
        "/2007/10/markets-and-phi.php": "/posts/markets-and-philanthropy",
        "/2007/10/tumblr.php": "/posts/tumblr",
        "/2007/11/why-past-perfor.php": "/posts/why-past-performance-is-a-good-predictor-of-future-returns-in-the-venture-capital-asset-class",
        "/2007/11/failure-rates-i.php": "/posts/failure-rates-in-early-stage-venture-deals",
        "/2007/11/why-early-stage.php": "/posts/why-early-stage-venture-investments-fail",
        "/2008/01/zynga-game-netw.php": "/posts/zynga-game-network",
        "/2007/12/googles-data-as.php": "/posts/googles-data-asset",
        "/2008/01/etsys-new-finan.php": "/posts/etsys-new-financing-and-what-they-are-going-to-do-with-it",
        "/2008/02/were-hiring.php": "/posts/were-hiring",
        "/2008/03/new-fund-same-f.php": "/posts/new-fund-same-focus",
        "/2008/03/targetspot-rais.php": "/posts/targetspot-raises-series-b-round",
        "/2008/03/disqus.php": "/posts/disqus",
        "/2008/03/structural-chan.php": "/posts/structural-change-and-marketplaces",
        "/2008/04/covestor.php": "/posts/covestor",
        "/2008/04/i-may-have-a-ne.php": "/posts/i-may-have-a-new-platform",
        "/2008/04/this-is-nuts.php": "/posts/this-is-nuts",
        "/2008/04/ab-meta.php": "/posts/ab-meta",
        "/2008/04/wesabe-steps-ou.php": "/posts/wesabe-steps-out",
        "/2008/05/outsidein-steps.php": "/posts/outsidein-steps-it-up",
        "/2008/05/losing-jason.php": "/posts/losing-jason",
        "/2008/05/pinch-media-inv.php": "/posts/pinch-media-investing-on-a-new-platform",
        "/2008/06/the-spooky-econ.php": "/posts/the-weird-economics-of-information",
        "/2008/06/and-then-there-1.php": "/posts/and-then-there-were-five",
        "/2008/06/call-for-topics.php": "/posts/call-for-topics",
        "/2008/06/internet-for-ev.php": "/posts/internet-for-everyone",
        "/2008/06/twitter-raises.php": "/posts/twitter-raises-a-second-round-of-funding",
        "/2008/07/twitter-acquire.php": "/posts/twitter-acquires-summize",
        "/2008/07/10gen.php": "/posts/10gen",
        "/2008/07/meetup-the-orig.php": "/posts/meetup-the-original-web-meets-world-company",
        "/2008/07/zynga-announces.php": "/posts/zynga-announces-new-investment-from-kleiner-perkins-and-ivp",
        "/2008/09/zemanta-1.php": "/posts/zemanta",
        "/2008/09/power-to-the-pe-1.php": "/posts/power-to-the-people",
        "/2008/09/why-the-flow-of.php": "/posts/why-the-flow-of-innovation-has-reversed",
        "/2008/10/return-path.php": "/posts/return-path",
        "/2008/11/boxee.php": "/posts/boxee",
        "/2008/12/amee.php": "/posts/amee",
        "/2009/01/arguing-from-fi.php": "/posts/arguing-from-first-principles",
        "/2009/02/twitter-fills-t.php": "/posts/twitter-fills-the-tank",
        "/2009/02/pinch-medias-ip.php": "/posts/pinch-medias-iphone-app-store-secrets",
        "/2009/03/dave-morgan-lau.php": "/posts/welcome-back-dave",
        "/2009/03/hacking-educati.php": "/posts/hacking-education",
        "/2009/04/open-spectrum-i.php": "/posts/open-spectrum-is-good-policy",
        "/2009/05/hacking-education.php": "/posts/hacking-education-2",
        "/2009/05/heyzap.php": "/posts/heyzap",
        "/2009/06/bring-the-world.php": "/posts/bring-the-world-to-your-event",
        "/2009/06/the-mobile-chal.php": "/posts/the-mobile-challenge",
        "/2009/08/chris-and-malco.php": "/posts/chris-and-malcolm-are-both-wrong",
        "/2009/09/foursquare.php": "/posts/foursquare",
        "/2009/10/introducing-tra.php": "/posts/introducing-trackedcom",
        "/2012/06/duolingo.php": "/posts/duolingo",
        "/2009/08/our-focus-intro.php": "/posts/our-focus-intro",
        "/2010/04/hiring-update.php": "/posts/hiring-update",
        "/2010/02/software-patents-are-the-problem-not-the-answer.php": "/posts/software-patents-are-the-problem-not-the-answer",
        "/2010/03/communicator-done-replicator-next-the-future-of-making-stuff.php": "/posts/communicator-done-replicator-next-the-future-of-making-stuff",
        "/2010/03/bidding-goodbye-to-andrew.php": "/posts/bidding-goodbye-to-andrew",
        "/2010/04/usv-is-hiring.php": "/posts/we-are-hiring",
        "/2010/04/hiring-update-2.php": "/posts/hiring-update-2",
        "/2010/04/hiring-update-3.php": "/posts/hiring-update-3",
        "/2010/05/stackoverflow.php": "/posts/stack-overflow",
        "/2010/05/hiring-update-4.php": "/posts/hiring-update-4",
        "/2010/06/final-hiring-update.php": "/posts/final-hiring-update",
        "/2010/06/a-new-analyst-at-usv.php": "/posts/a-new-member-of-the-usv-team",
        "/2010/06/web-services-as-governments.php": "/posts/web-services-as-governments",
        "/2010/06/work-market.php": "/posts/work-market",
        "/2013/01/hi-im-brittany-laughlin-im.php": "/posts/joining-union-square-ventures",
        "/2010/06/getting-started.php": "/posts/getting-started",
        "/2010/07/policies-to-encourage-startup-innovation.php": "/posts/policies-to-encourage-startup-innovation",
        "/2010/08/a-threat-to-startups.php": "/posts/a-threat-to-startups",
        "/2010/08/internet-architecture-and-innovation.php": "/posts/internet-architecture-and-innovation",
        "/2010/09/shapeways.php": "/posts/shapeways",
        "/2010/11/tasty-labs.php": "/posts/tasty-labs",
        "/2010/12/10gen-fills-the-tank.php": "/posts/10gen-fills-the-tank",
        "/2010/12/edmodo.php": "/posts/edmodo",
        "/2010/12/an-applications-agnostic-approach.php": "/posts/internet-access-should-be-application-agnostic",
        "/2013/05/circle-up.php": "/posts/circleup",
        "/2011/01/soundcloud.php": "/posts/soundcloud",
        "/2011/01/the-opportunity-fund.php": "/posts/the-opportunity-fund",
        "/2011/03/kik.php": "/posts/kik",
        "/2011/03/innovation-in-education.php": "/posts/innovation-in-education",
        "/2011/03/stack-overflow-becomes-stack-exchange.php": "/posts/stack-overflow-becomes-stack-exchange",
        "/2011/03/kickstarter.php": "/posts/kickstarter",
        "/2011/06/canvas.php": "/posts/canvas",
        "/2011/06/the-protect-ip-act-will-slow-start-up-innovation.php": "/posts/the-protect-ip-act-will-slow-start-up-innovation",
        "/2011/08/lending-club-1.php": "/posts/lending-club",
        "/2011/08/skillshare.php": "/posts/skillshare",
        "/2011/09/jig---when-you-need-a-little-help.php": "/posts/jig-when-you-need-a-little-help",
        "/2011/09/wattpad.php": "/posts/wattpad",
        "/2012/06/wattpads-continued-re-imagining-of-the-book.php": "/posts/wattpads-continued-re-imagining-of-the-book",
        "/2011/09/turntable.php": "/posts/turntable",
        "/2011/09/were-hiring-1.php": "/posts/were-hiring-2",
        "/2011/10/analyst-hiring-update.php": "/posts/analyst-hiring-update",
        "/2011/10/duck-duck-go.php": "/posts/duck-duck-go",
        "/2011/10/my-back-pages.php": "/posts/my-back-pages",
        "/2011/10/codecademy.php": "/posts/codecademy",
        "/2011/10/analyst-hiring-update-2.php": "/posts/analyst-hiring-update-2",
        "/2011/11/help-protect-internet-innovation.php": "/posts/help-protect-internet-innovation",
        "/2011/11/what-comes-next.php": "/posts/what-comes-next",
        "/2012/02/dwolla.php": "/posts/dwolla",
        "/2012/03/the-freedom-to-innovate.php": "/posts/the-freedom-to-innovate",
        "/2012/04/funding-circle.php": "/posts/funding-circle",
        "/2012/04/the-twitter-patent-hack.php": "/posts/the-twitter-patent-hack",
        "/2012/04/hacking-society.php": "/posts/hacking-society",
        "/2012/05/b-corporation.php": "/posts/b-corporation",
        "/2012/05/behance.php": "/posts/behance",
        "/2012/05/investment-thesis-usv.php": "/posts/investment-thesis-usv",
        "/2012/06/internet-presence-usv.php": "/posts/the-next-stage-of-usvcom",
        "/2012/06/and-then-there-were-nine.php": "/posts/and-then-there-were-nine",
        "/2012/06/hello-world-1.php": "/posts/hello-world-2",
        "/2012/06/joining-usv.php": "/posts/joining-usv",
        "/2012/07/brewster.php": "/posts/brewster",
        "/2012/08/networks-and-the-enterprise.php": "/posts/networks-and-the-enterprise",
        "/2012/09/pollenware.php": "/posts/pollenware",
        "/2012/10/researching-online-education.php": "/posts/researching-online-education",
        "/2012/10/looking-for-design-talent.php": "/posts/looking-for-design-talent",
        "/2012/11/visualizing-our-investments.php": "/posts/visualizing-our-investments",
        "/2012/12/behance-joins-adobe-to-scale-creative-network.php": "/posts/behance-joins-adobe-to-scale-creative-network",
        "/2013/02/hailo.php": "/posts/hailo",
        "/2013/03/sift-science.php": "/posts/sift-science",
        "/2013/04/kitchensurfing.php": "/posts/kitchensurfing",
        "/2013/04/foursquare-checks-in.php": "/posts/foursquare-checks-in",
        "/2013/04/shapeways-restocks.php": "/posts/shapeways-restocks",
        "/2013/04/science-exchange.php": "/posts/science-exchange",
        "/2013/05/coinbase.php": "/posts/coinbase",
        "/2013/05/the-patent-quality-improvement-act.php": "/posts/the-patent-quality-improvement-act",
        "/2013/05/yahoo-acquires-tumblr.php": "/posts/yahoo-acquires-tumblr",
        "/2013/06/auxmoney-1.php": "/posts/auxmoney",
        "/2013/06/firebase.php": "/posts/firebase",
        "/2013/07/sigfig.php": "/posts/sigfig",
        "/2013/07/transparency-in-government-surveillance.php": "/posts/transparency-in-government-surveillance",
        "/2013/10/splice.php": "/posts/splice",
        "/2013/08/vhx.php": "/posts/vhx"
      }
      new_url = old_posts[url]
    except:
      new_url = '/'

    self.redirect(new_url, permanent=True)
