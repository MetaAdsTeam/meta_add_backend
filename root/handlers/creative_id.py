from root import models
from root.handlers import BaseHandler


class CreativeIdHandler(BaseHandler):

    async def get(self, id_):
        await self.send_json(self.ms.get_creative(id_))

    async def delete(self, id_):
        self.ms.delete_creative(id_)
        await self.send_ok()
