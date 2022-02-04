import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class PlaybacksHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_playbacks())

