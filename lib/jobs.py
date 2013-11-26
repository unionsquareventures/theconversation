import urllib

# Parse a rss feed from Indeed
  def parse_rss(self, company_name):
    base_url = "http://rss.indeed.com/rss?q=company%3A%28" + urllib.urlencode(company_name) + "%29" 
    print base_url