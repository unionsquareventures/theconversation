from urlparse import urlparse

# A dictionary of methods to be made available for each template to use.
# See: http://www.tornadoweb.org/en/branch2.0/overview.html?highlight=ui_modules#ui-modules
def template_methods():
    return {'twitter_avatar_size': twitter_avatar_size}

# Twitter URLs are stored as their 'normal' size
# eg. http://a0.twimg.com/profile_images/3428823565/9c49c693a9b7527b3fb7e36f6bba627f_normal.png
def twitter_avatar_size(handler, url, size):
    if size == 'original':
        url = url.replace('_normal', '')
    else:
        url = url.replace('_normal', '_%s' % size)
    return url
