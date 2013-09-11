import time
import urlparse
import urllib
import httplib2

try:
    import json
except ImportError:
    import simplejson as json

if not hasattr(urlparse, 'parse_qsl'):
    import cgi
    urlparse.parse_qsl = cgi.parse_qsl

class Client(httplib2.Http):

    def __init__(self, config):
        super(Client, self).__init__()
        self.config = config
        self.codespeed_url = None

        self.force_exception_to_status_code = True

    def request(self, *args, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['User-Agent'] = self.config.user_agent
        if 'body' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['body'] = json.dumps(kwargs['body'])

        resp, body = super(Client, self).request(*args, **kwargs)
        if body:
            try:
                body = json.loads(body)
            except ValueError:
                body = {'error' : {'message' : body}}
        else:
            body = None

        return resp, body

    def _cs_request(self, url, method, **kwargs):
        if not self.codespeed_url:
            self.authenticate()

        try:
            resp, body = self.request(self.codespeed_url + url, method, **kwargs)
            return resp, body
        except Exception, ex:
            self.authenticate()
            resp, body = self.request(self.codespeed_url + url, method, **kwargs)
            return resp, body

    def get(self, url, **kwargs):
        url = self._munge_get_url(url)
        return self._cs_request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self._cs_request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self._cs_request(url, 'PUT', **kwargs)

    def delete(self, url, **kwargs):
        return self._cs_request(url, 'DELETE', **kwargs)

    def authenticate(self):
        headers = {
            'X-Auth-User': self.config.username
        }
        self.codespeed_url = 'http://172.16.8.37:8000/api/v1'

    def _munge_get_url(self, url):
        scheme, netloc, path, query, frag = urlparse.urlsplit(url)
        query = urlparse.parse_qsl(query)
        query = urllib.urlencode(query)
        return urlparse.urlunsplit((scheme, netloc, path, query, frag))
