import json
from dataclasses import asdict

from deeply import Deeply
from tornado.web import authenticated

from root import enums, models
from root.handlers import BaseHandler


class CreativesHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    @authenticated
    async def get(self):
        await self.send_json(
            {
                'data': list(map(Deeply.to_web, self.ms.get_creatives()))
            }
        )

    async def post(self):
        try:
            creative = models.Creative(**self.json_args)
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_creative(creative)
            await self.send_ok()

    async def delete(self):
        id_s = self.json_args.get('id_s', [])
        if not isinstance(id_s, list):
            id_s = [id_s]
        self.ms.delete_creatives(id_s)
        await self.send_ok()
