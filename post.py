import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from forms import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import InputRequired
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

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
        self.vars.update({'posts': self.db.posts.find()})
        self.render('templates/posts/index.html', **self.vars)

    def detail(self, id):
        id = minifier.base62_to_int(id)
        res = self.db.posts.find_one({'_id': int(id)})
        if not res:
            raise tornado.web.HTTPError(404)
        self.vars.update({'post': res})
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
        body = form.body.data
        video_ext = VideoExtension(configs={})
        body_html = markdown(body, extensions=[video_ext], output_format='html5', safe_mode=False)
        post = {
            'title': form.title.data,
            'body_html': body_html,
            'body_raw': body,
            '_id': id,
            'user': self.get_current_user(),
            'date_created': dt.datetime.now(),
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

