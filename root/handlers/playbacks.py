import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class PlaybacksHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_playbacks())

    async def post(self):
        # print(self.json_args)
        try:
            creative = models.Playback(**self.json_args)
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_playback(creative)
            await self.send_ok()

    async def delete(self):
        id_s = self.json_args.get('id_s', [])
        if not isinstance(id_s, list):
            id_s = [id_s]
        self.ms.delete_playbacks(id_s)
        await self.send_ok()
