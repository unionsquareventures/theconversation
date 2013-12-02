# Run by Heroku Scheduler every 5min
import settings
import datetime
import logging

from lib import companiesdb
from lib import hackpad
from lib import postsdb
from lib import userdb

# set our config values up
#staff_bonus = int(self.get_argument('staff_bonus', -3))
staff_bonus = -3
#time_penalty_multiplier = float(self.get_argument('time_penalty_multiplier', 2.0))
time_penalty_multiplier = 2.0
#grace_period = float(self.get_argument('grace_period', 6.0))
grace_period = 6.0
#comments_multiplier = float(self.get_argument('comments_multiplier', 3.0))
comments_multiplier = 3.0
#votes_multiplier = float(self.get_argument('votes_multiplier', 1.0))
votes_multiplier = 1.0
#min_votes = float(self.get_argument('min_votes', 2))
min_votes = 2

# get all the posts that have at least the 'min vote threshold'
posts = postsdb.get_posts_with_min_votes(min_votes)

data = []
for post in posts:
  # determine how many hours have elapsed since this post was created
  tdelta = datetime.datetime.now() - post['date_created']
  hours_elapsed = tdelta.seconds/3600 + tdelta.days*24

  # determine the penalty for time decay
  time_penalty = 0
  if hours_elapsed > grace_period:
    time_penalty = hours_elapsed - grace_period
  if hours_elapsed > 12:
    time_penalty = time_penalty * 1.5
  if hours_elapsed > 18:
    time_penalty = time_penalty * 2

  # get our base score from downvotes
  #base_score = post['downvotes'] * -1
  base_score = 0

  # determine if we should assign a staff bonus or not
  if post['user']['username'] in settings.get('staff'):
    staff_bonus = staff_bonus
  else:
    staff_bonus = 0

  # determine how to weight votes
  votes_base_score = 0
  if post['votes'] == 1 and post['comment_count'] > 2:
    votes_base_score = -2
  if post['votes'] > 8 and post['comment_count'] == 0:
    votes_base_score = -2

  scores = {}
  # now actually calculate the score
  total_score = base_score
  
  scores['votes'] = (votes_base_score + post['votes'] * votes_multiplier)
  total_score += scores['votes']
  
  scores['comments'] = (post['comment_count'] * comments_multiplier)
  total_score += scores['comments']
  
  scores['time'] = (time_penalty * time_penalty_multiplier * -1)
  total_score += scores['time']
  
  total_score += staff_bonus
  post['scores'] = scores

  # and save the new score
  postsdb.update_post_score(post['slug'], total_score)

  data.append({
    'username': post['user']['username'],
    'title': post['title'],
    'slug': post['slug'],
    'date_created': post['date_created'],
    'hours_elapsed': hours_elapsed,
    'votes': post['votes'],
    'comment_count': post['comment_count'],
    'staff_bonus': staff_bonus,
    'time_penalty': time_penalty,
    'total_score': total_score,
    'scores': scores
  })

data = sorted(data, key=lambda k: k['total_score'], reverse=True)