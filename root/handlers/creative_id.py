from root import models
from root.handlers import BaseHandler


class CreativeIdHandler(BaseHandler):

    async def delete(self, id_):
        self.ms.delete_creative(id_)
        await self.send_ok()
