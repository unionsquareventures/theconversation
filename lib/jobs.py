# Need to import tornado setting manually if running as a standalone script
import sys
sys.path.insert(0, '/Users/AlexanderPease/git/usv/website/usv')
import settings

import urllib2, json
import feedparser
from mongo import db

INDEED_API_URL = 'http://api.indeed.com/ads/apisearch'
INDEED_PUBLISHER_ID = '9648379283006957'


"""
{
  'id': 0
  'company': ''
  'jobtitle': ''
  'city': ''
  'state': ''
  'country': ''
  'formattedLocation': ''
  'date': ''
  'location': ''
  'url': ''
  'jobkey': '' # Unique identifier from Indeed
  'position': '' # From Gary's parse_position
}
"""

''' Returns a list of jobs (each one a dict) for a given company '''
def get_json(company):
	# Create and call api url
	# company_name = urllib.urlencode(company_name) 
	api_url = INDEED_API_URL + '?publisher=%s' % INDEED_PUBLISHER_ID
	api_url += '&q=company%3A' # %3A doesn't work with %s for some reason
	api_url += '(%s)' % company
	api_url += '&l=&sort=&radius=&st=&jt=&start=$start&limit=1000&fromage=$indeed_fromage&filter=&co=&latlong=1&chnl=&userip=1.2.3.4&v=2&format=json'
	data = json.load(urllib2.urlopen(api_url)) # data is a dict
	return data['results']

''' Adds a job to the database. Overwrite flag specifies to overwrite/modify jobs we already have listed '''
def add_job(job_dict, overwrite=False):
	# Check if this job already exists
	if not overwrite:# and job['jobkey'] in db.jobs.:
		print 'Job already in database, not overwritten'
		return 
	
	url = entry['link']
	position = parse_position(entry['title'])
	#location

''' Parses job position title from a string '''
def parse_position(string):
	string = string.lower()
	if any(x.lower() in string for x in ['QA', 'Quality Assurance']):
		return 'Engineering - QA'
	elif any(x.lower() in string for x in ['Operations Associate', 'Procurement', 'Office Admin', 'Office Manager', 'Administrative Assistant', 'Executive Assistant', 'Chief of Staff', 'Office Administrator', 'Office Assistant']):
		return 'Administrative'
	elif any(x.lower() in string for x in ['DBA', 'MySQL', 'Database', 'Data Operations']):
		return 'Database Administration'
	elif any(x.lower() in string for x in ['Finance', 'Financial Analyst', 'Treasury', 'Controller', 'Tax Senior', 'Accountant', 'Accounts Payable', 'Payroll', 'Contracts Administrator', 'Contract Administrator', 'Legal', 'Counsel', 'Paralegal', 'General Ledger', 'Tax Manager']):
		return 'Legal & Finance'
	elif any(x.lower() in string for x in ['Technical Sourcer', 'University Relations', 'Startup Talent Manager', 'Recruit', 'HR', 'Human Resources', 'Talent Acquisition']):
		return 'HR & Recruiting'
	elif any(x.lower() in string for x in ['Community', 'Customer', 'Fanatic', 'Moderator', 'Evangelist', 'Contact Center Operations', 'Service Desk Manager']):
		return 'Community Management & Support'
	elif any(x.lower() in string for x in ['Support', 'Trust and Safety']):
		return 'Customer Support'
	elif any(x.lower() in string for x in ['Datacenter', 'Hardware Engineer', 'Datacenter Manager', 'Network Security', 'Network Engineer', 'DevOps', 'Dev Ops', 'Site Reliability', 'Tech Ops', 'Sysadmin', 'Release', 'IT Sys Admin', 'Operations Engineer', 'Systems Engineer', 'Systems Engineering', 'System Administrator', 'Data Center', 'System Admin', 'IT Administrator', 'Infrastructure', 'Online Operations', 'Systems Administrator', 'Systems Administator']):
		return 'Engineering - Operations'
	elif any(x.lower() in string for x in ['Prototyper', 'Frontend', 'Front-End', 'Front End', 'jQuery', 'UI Engineer', 'UI Developer', 'User Interface Engineer', 'Front-end', 'Javascript', 'Flash']):
		return 'Engineering - Front End'
	elif any(x.lower() in string for x in ['Visual', 'Artist', 'Graphic Designer', 'Art Director']):
		return 'Design - Visual/Artist'
	elif any(x.lower() in string for x in ['Interaction Design', 'Information Architect', 'UX', 'User Research', 'User Experience', 'Product Designer', 'Information Designer', 'UI Designer', 'User Interface Design']):
		return 'Design - Interaction/UX'
	elif any(x.lower() in string for x in ['Design']):
		return 'Design'
	elif any(x.lower() in string for x in ['iOS', 'Android', 'Blackberry', 'Mobile', 'Symbian', 'iPhone']):
		return 'Engineering - Mobile'
	elif any(x.lower() not in string for x in ['Sales Engineer', 'Business']) and any(x.lower() in string for x in ['Architect', 'Software Architect', 'Development Manager', 'SDET', 'Engineer', 'ENGINEER', 'Technology', 'Developer', 'Security Architect', 'Information Architect', 'Ops', 'Release Manager']):
		if any(x.lower() in string for x in ['Senior', 'Sr', 'Lead']):
	   		return 'Engineering - Senior'
		elif any(x.lower() in string for x in ['VP', 'Manager', 'Chief', 'Director']):
	  		return 'Engineering - Management'
	 	else:
			return 'Engineering'
	elif any(x.lower() in string for x in ['Communications', 'Corporate Communications', 'Communications Manager', 'Marketing', 'Social Media', 'PR Coordinator', 'Events Coordinator', 'Events Program', 'Brand Manager', 'Public Relations', 'Market Research']):
		return 'Marketing'
	elif any(x.lower() in string for x in ['Production', 'Operations', 'Supply Chain']):
		return 'Operations'
	elif any(x.lower() in string for x in ['Product']):
		return 'Product Management'
	elif any(x.lower() in string for x in ['Project', 'Program Manager', 'Producer', 'Netsuite', 'PMO', 'CRM Administrator']):
		return 'Project Management'
	elif any(x.lower() in string for x in ['Account ', 'Agency and Brand', 'Sales', 'Business Develop', 'Partner Relations', 'Channel', 'Revenue', 'Relationship', 'Lead Gen', 'Client', 'Online Digital Media SALES', 'Partnerships', 'Sponsorship Development']):
		return 'Sales & Business Development'
	elif any(x.lower() in string for x in ['Editor', 'Copywriter', 'Technical Writer', 'Writer', 'Content']):
		return 'Content & Editorial'
	elif any(x.lower() in string for x in ['Insight', 'User Researcher', 'Chief Scientist', 'Data Engineer', 'Data Scientist', 'Data Analyst', 'Crime Analyst', 'Capacity Planning Analyst', 'Fraud Analyst', 'Optimization Analyst', 'Data Researcher', 'Research Analyst', 'BI Analyst', 'Business Intelligence', 'Reporting Analyst', 'Analytics', 'Data Warehouse', 'Statistical Analyst', 'Data Mining', 'Scientist', 'Research Assistant', 'Insights']):
		return 'Data & Analytics'
	elif any(x.lower() in string for x in ['General Manager', 'Managing Director', 'Regional Director', 'Head of']):
		return 'General Management'
	#elif any(x.lower() in string for x in ['Country Lead', 'Global', 'Multinational', 'International', 'Territory']):
	#	return 'International'
	else:
		return 'Other'


	

	

if __name__ == "__main__":
	print db.company
