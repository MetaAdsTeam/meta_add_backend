import json
from dataclasses import asdict

from root.handlers import BaseHandler


class AdSpotIdHandler(BaseHandler):
    async def get(self, id_):
        await self.send_json(self.ms.get_adspot(id_))
