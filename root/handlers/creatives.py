from typing import Optional

from root import models
from root.handlers import BaseHandler


class CreativesHandler(BaseHandler):

    async def get(self, id_: Optional[str] = None):
        if id_ is not None:
            await self.send_json(self.ms.get_creative(int(id_)))
        else:
            await self.send_json(self.ms.get_creatives())

    async def post(self):
        status = await self.ms.add_creative(
            self.json_args['name'],
            self.json_args['file'],
            self.json_args['filename'],
            self.json_args.get('description'),
        )
        if status != 200:
            await self.send_failed()
            return None
        await self.send_json(self.ms.get_creatives())

    async def delete(self, id_):
        self.ms.delete_creative(id_)
        await self.send_ok()
