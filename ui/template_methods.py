from urlparse import urlparse
from lib.sanitize import tinymce_valid_elements
import datetime

# A dictionary of methods to be made available for each template to use.
# See: http://www.tornadoweb.org/en/branch2.0/overview.html?highlight=ui_modules#ui-modules
def template_methods():
    return {
            'tinymce_valid_elements': tinymce_valid_elements_wrapper,
            'twitter_avatar_size': twitter_avatar_size,
            'pretty_date': pretty_date,
            }

def tinymce_valid_elements_wrapper(handler, media=True):
    return tinymce_valid_elements(media=media)

# Twitter URLs are stored as their 'normal' size
# eg. http://a0.twimg.com/profile_images/3428823565/9c49c693a9b7527b3fb7e36f6bba627f_normal.png
def twitter_avatar_size(handler, url, size):
    if size == 'original':
        url = url.replace('_normal', '')
    else:
        url = url.replace('_normal', '_%s' % size)
    return url

# Adapted from http://bit.ly/17wpDuh
def pretty_date(handler, d):
    diff = datetime.datetime.now() - d
    s = diff.seconds
    if diff.days != 0:
        return d.strftime('%b %d, %Y')
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s/3600)

