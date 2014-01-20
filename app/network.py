import app.basic
from lib import yammer, userdb, postsdb
from slugify import slugify

###############
### USV NETWORK
### /network
###############
class Welcome(app.basic.BaseHandler):
	def get(self):
		# get the last 6 posts tagged usv-network (and published by staff)
		in_usvnetwork = False
		account = userdb.get_user_by_screen_name(self.current_user)
		if account:		
			in_usvnetwork = account.get('in_usvnetwork', False)
		
		if in_usvnetwork:
			user = account['yammer']['user']
			user['mugshot_url'] = user['mugshot_url_template'].replace('{width}', '150').replace('{height}', '150')
			self.render('network/loggedin.html', user=user)
		else:			
			related_posts = postsdb.get_latest_staff_posts_by_tag('usv-network', 6)
			self.render('network/loggedout.html', related_posts=related_posts)