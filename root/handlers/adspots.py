import json
from dataclasses import asdict

from root.handlers import BaseHandler


class AdSpotsHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        self.write(
            json.dumps(
                {k: asdict(w) for k, w in enumerate(self.ms.get_adspots())}
            )
        )

    def get(self):
        self.post()
