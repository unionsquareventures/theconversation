# Based upon Cole Maclean's http://stackoverflow.com/questions/15981257/
from __future__ import division
import math
import urlparse
import urllib
import os
import tornado.web

def update_querystring(url, **kwargs):
    base_url = urlparse.urlsplit(url)
    query_args = urlparse.parse_qs(base_url.query)
    query_args.update(kwargs)
    for arg_name, arg_value in kwargs.iteritems():
        if arg_value is None:
            if query_args.has_key(arg_name):
                del query_args[arg_name]

    query_string = urllib.urlencode(query_args, True)
    return urlparse.urlunsplit((base_url.scheme, base_url.netloc,
        base_url.path, query_string, base_url.fragment))

class MainModule(tornado.web.UIModule):
    """Pagination links display."""

    def render(self, page, page_size, results_count, show_pages=False):
        pages = int(math.ceil(results_count / page_size)) if results_count else 0

        def get_page_url(page):
            # don't allow ?page=1
            if page <= 1:
                page = None
            return update_querystring(self.request.uri, page=page)

        next = page + 1 if page < pages else None
        previous = page - 1 if page > 1 else None

        path = os.path.dirname(os.path.realpath(__file__))
        return self.render_string(os.path.join(path, 'main.html'), page=page, pages=pages, next=next,
                previous=previous, get_page_url=get_page_url, show_pages=show_pages)
