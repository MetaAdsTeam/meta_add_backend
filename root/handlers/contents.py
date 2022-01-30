import json
from dataclasses import asdict
from datetime import date

from root import enums
from root.handlers import BaseHandler


class ContentsHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        self.write(
            json.dumps(
                {k: asdict(w) for k, w in enumerate(self.ms.get_contents())}
            )
        )
