import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class PlaybackIdHandler(BaseHandler):

    async def get(self, id_):
        await self.send_json(self.ms.get_playback(id_))

    async def delete(self, id_):
        self.ms.delete_playback(id_)
        await self.send_ok()
