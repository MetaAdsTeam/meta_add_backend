import json
from dataclasses import asdict

from root.handlers import BaseHandler


class AdSpotStatsIdHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self, id_):
        result = None
        adspot = self.ms.get_adspot_stats(id_)
        if adspot:
            result = asdict(adspot)
        self.write(
            json.dumps(result)
        )

    def get(self, id_):
        self.post(id_)