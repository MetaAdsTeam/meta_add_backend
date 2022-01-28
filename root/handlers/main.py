import json
from datetime import date

from root import enums
from root.handlers import BaseHandler


class MainHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        value = self.get_argument('key')
        r = json.dumps({'key': value})
        self.write(r)
