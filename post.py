import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from forms import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import InputRequired

from base import BaseHandler
from minifier import Minifier

minifier = Minifier()

class PostForm(Form):
    title = TextField('title', [InputRequired()])
    body = TextAreaField('body', [InputRequired()])


class PostHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(PostHandler, self).__init__(*args, **kwargs)
        self.vars['minifier'] = minifier

    def get(self, params=''):
        # TODO: Do this inside the routes w/ kwargs
        if params.find('/') == -1:
            params += '/'
        id, action = params.split('/')
        # Route new, detail, and index
        if id == 'new':
            self.new()
            return
        if id and action == '':
            self.detail(id)
            return
        if action == 'edit':
            self.edit()
            return
        self.index()

    def index(self):
        # list posts
        self.vars['posts'] = self.db.posts.find()
        self.render('templates/posts/index.html', **self.vars)

    def detail(self, id):
        id = minifier.base62_to_int(id)
        res = self.db.posts.find_one({'_id': int(id)})
        if not res:
            raise tornado.web.HTTPError(404)

        self.vars['post'] = res
        self.render('templates/posts/get.html', **self.vars)

    # Create a post
    @tornado.web.authenticated
    def new(self, form=PostForm()):
        self.vars['form'] = form
        self.render('templates/posts/new.html', **self.vars)

    @tornado.web.authenticated
    def post(self):
        form = PostForm(self.request.arguments)
        if not form.validate():
            self.new(form=form)

        counter = self.db.postsCounter.find_and_modify(query={'_id': 'chipmunks_counter'},
                                                      update={'$inc': {'value': 1}},
                                                      upsert=True, new=True)
        id = counter['value']
        post = {
            'title': form.title.data,
            'body': form.body.data,
            '_id': id,
        }
        self.db.posts.insert(post)
        self.redirect('/posts/%s' % minifier.int_to_base62(post['_id']))

    # Update a post
    @tornado.web.authenticated
    def edit(self):
        id = minifier.base62_to_int(id)
        res = self.db.posts.find_one({'_id': int(id)})
        if not res:
            raise tornado.web.HTTPError(404)

    @tornado.web.authenticated
    def put(self, id=''):
        pass

