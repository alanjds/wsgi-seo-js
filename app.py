from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Flask World!"


import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import get_query_string


class AjaxCrawlingMiddleware(object):
    """Implements Google's "protocol" to crawl AJAX pages
    
    The protocol is described here: https://developers.google.com/webmasters/ajax-crawling/docs/specification
    """
    def __init__(self, app):
        self.app = app
        super(AjaxCrawlingMiddleware, self).__init__()

    def __call__(self, environ, start_response):
        qs_dict = urlparse.parse_qs(get_query_string(environ), keep_blank_values=True)
        #import ipdb; ipdb.set_trace()
        if '_escaped_fragment_' in qs_dict:
            app_iter = ajax_crawled_application(environ, start_response)
        else:
            app_iter = self.app(environ, start_response)

        return app_iter


def ajax_crawled_application(environ, start_response):
    request = Request(environ)
    text = 'Hello Werkzeug %s!' % request.args.get('name', 'World')
    response = Response(text, mimetype='text/plain')
    return response(environ, start_response)

app.wsgi_app = AjaxCrawlingMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)

