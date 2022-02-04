from root import models
from root.handlers import BaseHandler


class CreativeHandler(BaseHandler):

    async def post(self):
        creative = models.Creative(**self.json_args)
        self.ms.add_creative(creative)
        await self.send_ok()
