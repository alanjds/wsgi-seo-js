# coding: utf-8
import urlparse
import urllib
from werkzeug.wrappers import Request, Response
from werkzeug import wsgi
import selenium.webdriver


class AjaxCrawlingMiddleware(object):
    """Implements Google's "protocol" to crawl AJAX pages
    
    The protocol is described here: https://developers.google.com/webmasters/ajax-crawling/docs/specification
    """
    def __init__(self, app):
        self.app = app
        super(AjaxCrawlingMiddleware, self).__init__()

    def __call__(self, environ, start_response):
        qs_dict = urlparse.parse_qs(wsgi.get_query_string(environ), keep_blank_values=True)
        if '_escaped_fragment_' in qs_dict:
            app_iter = self.ajax_crawler(environ, start_response)
        else:
            app_iter = self.app(environ, start_response)

        return app_iter

    def ajax_crawler(self, environ, start_response):
        request = Request(environ)
        ugly_url = request.url
        pretty_url = None
    
        qs_dict = urlparse.parse_qs(request.query_string, keep_blank_values=True)
        fragment = qs_dict.pop('_escaped_fragment_')[0]

        pretty_qs = urllib.urlencode(qs_dict, doseq=True)
        pretty_url = request.host_url.strip('/') + request.path + '?' + pretty_qs
        if fragment:
            pretty_url += '#!' + fragment #.encode('quopri') ??
            raise NotImplementedError('Not handling non-empty fragments (yet)')

        driver = selenium.webdriver.PhantomJS()
        driver.get(pretty_url)
        html_snapshot = driver.page_source
        driver.quit()
    
        text = html_snapshot
        response = Response(text, mimetype='text/html') # MIME is just a sane guess
        return response(environ, start_response)
