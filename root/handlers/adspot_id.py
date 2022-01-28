import json
from datetime import date

from root import enums
from root.handlers import BaseHandler


class AdSpotId(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self, id_):
        data = {
            1: {'id': 1, 'name': 'AdSpot 1', 'publisher_id': 1, 'adspot_type': 1, 'metadata': ''},
            2: {'id': 2, 'name': 'AdSpot 2', 'publisher_id': 1, 'adspot_type': 2, 'metadata': ''},
            3: {'id': 3, 'name': 'AdSpot 3', 'publisher_id': 2, 'adspot_type': 1, 'metadata': ''},
            4: {'id': 4, 'name': 'AdSpot 4', 'publisher_id': 2, 'adspot_type': 2, 'metadata': ''},
            5: {'id': 5, 'name': 'AdSpot 5', 'publisher_id': 1, 'adspot_type': 1, 'metadata': ''},
            6: {'id': 6, 'name': 'AdSpot 6', 'publisher_id': 1, 'adspot_type': 2, 'metadata': ''},
        }
        if not id_:
            r = json.dumps(data)
        else:
            r = json.dumps(data.get(int(id_), {}))
        self.write(r)
