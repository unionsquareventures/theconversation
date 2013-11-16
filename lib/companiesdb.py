import pymongo
from mongo import db

"""
{
  'id': 0
  'name': ''
  'url': ''
  'description': ''
  'logo_filename': ''
  'locations': ''
  'investment_series': ''
  'investment_year': ''
  'categories': ''
  'status': ''
  'slug': ''
  'investment_post_slug': ''
}
"""

def get_companies_by_status(status):
  # order by name
  return list(db.company.find({'status':status}, sort=[('name', pymongo.ASCENDING)]))

def get_company_by_slug(slug):
  return db.company.find_one({'slug':slug})

def save_company(company):
  if 'id' not in company.keys() or company['id'] == '':
    # need to create a new company id
    company['id'] = db.company.count() + 1

  company['id'] = int(company['id'])
  return db.company.update({'slug':company['slug']}, company, upsert=True)

