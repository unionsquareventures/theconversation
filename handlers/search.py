from base import BaseHandler
from models import Post
import tornado.web

class SearchHandler(BaseHandler):
    def get(self):
        # Ensure there is a full text index
        db = Post._get_db()
        query = self.get_argument('query', '')
        if not query:
            self.vars.update({
                'query': '',
                'total_count': 0,
            })
            self.render('search/index.html', **self.vars)
            return
        page = abs(int(self.get_argument('page', '1')))
        per_page = abs(int(self.get_argument('per_page', '10')))
        results = db.command('text', 'post', search=query,
                                    filter={'deleted': False})
        results = results['results']
        total_count = len(results)
        results = results[(page-1)*per_page:(page-1)*per_page+per_page]
        posts = [Post(**r['obj']) for r in results]
        self.vars.update({
            'posts': posts,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'query': query,
        })
        self.render('search/index.html', **self.vars)
