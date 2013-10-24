import tornado.web

class RedirectHandler(tornado.web.RequestHandler):
    def get(self, person=None):
        if person:
            self.redirect('http://www.usv.com/about#' + person, permanent=True)
        else:
            self.redirect('http://www.usv.com', permanent=True)

