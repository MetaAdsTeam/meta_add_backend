import json
from dataclasses import asdict

from root import enums, models
from root.handlers import BaseHandler


class CreativesHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        self.write(
            json.dumps(
                {'data': [asdict(w) for k, w in enumerate(self.ms.get_creatives())]}
            )
        )

    async def post(self):
        try:
            creative = models.Creative(**self.json_args)
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_creative(creative)
            await self.send_ok()
