import base64
import hashlib
import hmac
import json
import re
import requests
import settings
import time

from lib import postsdb
from lib import userdb
from lib import template_helpers

import logging

#
# Note: all requests assume that they are being run
# by the current user
#

def get_networks(username):
	api_link = "https://www.yammer.com/api/v1/networks/current.json"
	params = {}
	return do_api_request(api_link, username, 'GET')


#####################################################
#### ACTUALLY HANDLE THE REQUESTS/RESPOSNE TO THE API
#####################################################
def do_api_request(api_link, username, method='GET', params={}):
	account = userdb.get_user_by_screen_name(username)
	token = account.get('yammer').get('access_token').get('token')
	if not token:
		return "No token"
	
	headers = {'Authorization': 'Bearer %s' % token}
	try:
		if method.upper() == 'GET':
			if len(params.keys()) > 0:
				r = requests.get(
					api_link,
					params=params,
					headers=headers,
					verify=False
				)
			else:
				r = requests.get(
					api_link,
					headers=headers,
					verify=False
				)
		else:
			r = requests.post(
				api_link,
				params=params,
				headers=headers,
				verify=False
			)
		yammer = r.json()
	except:
		yammer = {}
	return yammer