import json
from dataclasses import asdict
from typing import Optional

from root.handlers import BaseHandler


class AdSpotsHandler(BaseHandler):
    async def get(self, id_: Optional[str] = None):
        if id_ is not None:
            await self.send_json(self.ms.get_adspot(int(id_)))
        else:
            await self.send_json(self.ms.get_adspots())
