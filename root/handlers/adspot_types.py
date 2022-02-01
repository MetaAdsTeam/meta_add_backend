import json
from dataclasses import asdict

from root.handlers import BaseHandler


class AdSpotTypesHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        self.write(
            json.dumps(
                {'data': [asdict(w) for k, w in enumerate(self.ms.get_adspot_types())]}
            )
        )
