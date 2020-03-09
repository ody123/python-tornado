import tornado.testing


class BaseAsyncHTTPTestCase(tornado.testing.AsyncHTTPTestCase):

    def http_fetch(self, url, *args, **kwargs):
        self.http_client.fetch(url, self.stop, *args, **kwargs)
        return self.wait()