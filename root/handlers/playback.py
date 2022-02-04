import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class PlaybackHandler(BaseHandler):

    async def delete(self, id_):
        print(type(id_))
        self.ms.delete_playbacks(id_)
        await self.send_ok()
