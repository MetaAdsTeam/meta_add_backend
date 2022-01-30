import json
from datetime import date

from root import enums
from root.handlers import BaseHandler


class AdSpotHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        data = {
            1: {'id': 1, 'name': 'AdSpotHandler 1', 'publisher_id': 1, 'adspot_type': 1, 'metadata': ''},
            2: {'id': 2, 'name': 'AdSpotHandler 2', 'publisher_id': 1, 'adspot_type': 2, 'metadata': ''},
            3: {'id': 3, 'name': 'AdSpotHandler 3', 'publisher_id': 2, 'adspot_type': 1, 'metadata': ''},
            4: {'id': 4, 'name': 'AdSpotHandler 4', 'publisher_id': 2, 'adspot_type': 2, 'metadata': ''},
            5: {'id': 5, 'name': 'AdSpotHandler 5', 'publisher_id': 1, 'adspot_type': 1, 'metadata': ''},
            6: {'id': 6, 'name': 'AdSpotHandler 6', 'publisher_id': 1, 'adspot_type': 2, 'metadata': ''},
        }
        r = json.dumps(data)
        self.write(r)
