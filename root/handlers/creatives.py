from typing import Optional

from root import models
from root.handlers import BaseHandler


class CreativesHandler(BaseHandler):

    async def get(self, id_: Optional[str] = None):
        if id_ is not None:
            await self.send_json(self.ms.get_creative(int(id_)))
        else:
            await self.send_json(self.ms.get_creatives())

    async def delete(self, id_):
        self.ms.delete_creative(id_)
        await self.send_ok()
