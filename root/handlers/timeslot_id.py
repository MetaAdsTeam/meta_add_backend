import json
from datetime import date

from root import enums
from root.handlers import BaseHandler


class TimeSlotIdHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self, id_):
        pass
