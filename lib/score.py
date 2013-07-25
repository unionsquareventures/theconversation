import time
from math import log

"""
Every 12.5 hours new posts will count for an additional score point.
The log10 of the total votes will calculate the score point equivalent
for summation.

Based upon: http://bit.ly/170DOpR
"""
def calculate_score(votes, date_created):
    adjusted_votes = log(max(abs(votes), 1), 10)
    sign = 1 if votes > 0 else 0
    age_factor = 45000.0 # ~12.5 hour increments
    timestamp = time.mktime(date_created.timetuple())
    score = adjusted_votes + round(sign * timestamp / age_factor)
    return score
