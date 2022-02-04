from root import models
from root.handlers import BaseHandler


class CreativesHandler(BaseHandler):

    async def get(self):
        await self.send_json(self.ms.get_creatives())
