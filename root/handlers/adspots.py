import json
from dataclasses import asdict

from root.handlers import BaseHandler


class AdSpotsHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_adspots())
