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
