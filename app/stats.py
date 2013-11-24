import app.basic

from datetime import datetime, timedelta

from lib import postsdb

######################
### WEEKLY STATS
### /stats/shares/weekly
######################
class WeeklyShareStats(app.basic.BaseHandler):
  def get(self):
    # get the stats based on the past 7 days
    today = datetime.today()
    week_ago = today + timedelta(days=-7)

    single_post_count = 0
    unique_posters = postsdb.get_unique_posters(week_ago, today)
    for user in unique_posters:
      if user['count'] == 1:
        single_post_count += 1

    stats = []
    stats.append({'name':'total','link':'','count':postsdb.get_post_count_for_range(week_ago, today)})
    stats.append({'name':'unique posters', 'link':'','count':len(unique_posters)})
    stats.append({'name':'single post count', 'link':'','count':single_post_count})

    self.render('stats/share_stats.html', stats=stats)

