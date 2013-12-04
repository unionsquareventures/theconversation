from base import BaseHandler
from models import Post
import tornado.web

class SearchHandler(BaseHandler):
    def get(self):
        # Ensure there is a full text index
        db = Post._get_db()
        query = self.get_argument('query', '')
        tag = self.get_argument('tag', '')
        if not (query or tag):
            self.vars.update({
                'query': '',
                'tag': '',
                'total_count': 0,
            })
            self.render('search/index.html', **self.vars)
            return
        page = abs(int(self.get_argument('page', '1')))
        per_page = abs(int(self.get_argument('per_page', '10')))

        if query:
            results = db.command('text', 'post', search=query,
                                    filter={'deleted': False})
            results = results['results']
            total_count = len(results)
            results = results[(page-1)*per_page:(page-1)*per_page+per_page]
            posts = [Post(id=r['obj']['_id'],**r['obj']) for r in results]
        else:
            results = Post.objects(tags=tag)
            total_count = len(results)
            posts = results[(page-1)*per_page:(page-1)*per_page+per_page]

        self.vars.update({
            'posts': posts,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'query': query,
            'tag': tag,
        })
        self.render('search/index.html', **self.vars)
