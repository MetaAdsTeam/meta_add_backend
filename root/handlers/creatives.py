from root import models
from root.handlers import BaseHandler


class CreativesHandler(BaseHandler):

    async def get(self):
        await self.send_json(self.ms.get_creatives())

    async def post(self):
        try:
            creative = models.Creative(**self.json_args)
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_creative(creative)
            await self.send_ok()
