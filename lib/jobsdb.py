# Need to import tornado setting manually if running as a standalone script
import sys
sys.path.insert(0, '/Users/AlexanderPease/git/usv/website/usv')
import settings

import urllib
import json
from mongo import db
import companiesdb
import pymongo

INDEED_API_URL = 'http://api.indeed.com/ads/apisearch'
INDEED_PUBLISHER_ID = '9648379283006957'

"""
{
    "_id": {
        "$oid": "52951ad2bf814a94370317a0"
    },
    "city": "San Francisco",
    "position": "Operations", # Job title determined by Gary's parse_position
    "date": "Tue, 26 Nov 2013 03:07:57 GMT",
    "latitude": 37.774727,
    "url": "http://www.indeed.com/rc/clk?jk=d16f4523a3212c0b&qd=9FdQIF7yu...",
    "jobtitle": "TV Production Associate",
    "company": "Twitter",
    "formattedLocationFull": "San Francisco, CA",
    "longitude": -122.41758,
    "onmousedown": "indeed_clk(this, '842');",
    "snippet": "use tools such as the new Mirror API...", 
    "source": "Twitter",
    "state": "CA",
    "sponsored": false,
    "country": "US",
    "formattedLocation": "San Francisco, CA",
    "jobkey": "d16f4523a3212c0b", #Unique job id from Indeed
    "id": 349,
    "expired": false,
    "formattedRelativeTime": "19 hours ago"
}
"""

''' Returns all jobs, default sorted by date added '''
def get_all():
	return list(db.job.find(sort=[('date', pymongo.ASCENDING)]))

''' Saves a job to the database. Job argument is a dict.'''
def save_job(job):
  if 'id' not in job.keys() or job['id'] == '':
    # need to create a new job id
    job['id'] = db.job.count() + 1

  job['id'] = int(job['id'])

  # If this is a new job, need to add Gary's position field
  if 'position' not in job.keys() or job['position'] == '':
    job['position'] = parse_position(job['jobtitle'])
  
  # Indeed's jobkey is the unique identifier
  return db.job.update({'jobkey':job['jobkey']}, job, upsert=True)

''' Returns complete list of categories, i.e. Gary's position field'''
def get_categories():
	# Position is the field name for Gary's categories
	return get_aggregation("$position")

''' Returns complete list of locations with jobs'''
def get_locations():
	return get_aggregation("$formattedLocation")

''' Returns complete list of companies with jobs'''
def get_companies():
	return get_aggregation("$company")

''' Lower level method using db.aggregate() 
	Returns list in alphabetical order'''
def get_aggregation(arg):
	# I'm sure there's a more elegant way to do this
	id_name = '_id'
	aggregation = db.job.aggregate(
					{ '$group' : 
						{ id_name : arg }
					})
	result = aggregation['result'] # result is a dict
	return_list = []
	for return_dict in result:
		return_list.append(return_dict['_id'])
	return sorted(return_list)


###############################
### Non-model functions and scripts
###############################

''' Updates job listings for all companies '''
def update_all():
    for c in companiesdb.get_companies_by_status('current'):
	    print 'Pulling jobs for %s' % c['name']
	    job_list = get_json(c['name'])
	    job_list = clean_jobs(c['name'], job_list)
	    for job in job_list:
	      save_job(job)

''' Returns a list of jobs (each one a dict) for a given company '''
def get_json(company):
	query = {'publisher': INDEED_PUBLISHER_ID, 'company': company}
	api_url = INDEED_API_URL + '?publisher=%s' % INDEED_PUBLISHER_ID
	api_url += '&q=company%3A' # %3A doesn't work with %s for some reason
	api_url += '(%s)' % company
	api_url += '&l=&sort=&radius=&st=&jt=&start=$start&limit=1000&fromage=$indeed_fromage&filter=&co=&latlong=1&chnl=&userip=1.2.3.4&v=2&format=json'
	data = json.load(urllib.urlopen(api_url)) # data is a dict
	return data['results']

''' Ensures all jobs are for the given company only'''
def clean_jobs(company, job_list):
	good_jobs = []
	for job in job_list:
		# Rules for certain portfolio companies
		job['company'] = job['company'].replace('.com', '') # Kickstarter.com, etc. 
		job['company'] = job['company'].replace('Labs', '') # foursquare labs
		job['company'] = job['company'].replace('USA', '') # Funding Circle USA
		job['company'] = job['company'].replace('Inc.', '') # Twilio Inc. 
		job['company'] = job['company'].replace('Inc', '') # WorkMarket Inc
		job['company'] = job['company'].replace('Wealth Management', '') # SigFig Wealth Management
		job['company'] = job['company'].replace('DISQUS', 'Disqus')
		job['company'] = job['company'].replace('Heyzap', 'HeyZap')
		job['company'] = job['company'].replace('foursquare', 'Foursquare')
		
		# Remove job from list if company name is not an exact match
		if job['company'].lower() == company.lower():
			good_jobs.append(job)
		else:
			print "!!!!!!!!!!!!!!!!"
			print "Removed job for company %s" % job['company']

	return good_jobs


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

# To run as script or cronjob
if __name__ == "__main__":
	print db.company
