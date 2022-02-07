from typing import Optional

from root import models
from root.handlers import BaseHandler


class PlaybacksHandler(BaseHandler):
    async def get(self, id_: Optional[str] = None):
        if id_ is not None:
            await self.send_json(self.ms.get_playback(int(id_)))
        else:
            await self.send_json(self.ms.get_playbacks())

    async def post(self):
        timeslot = models.TimeSlot(
            self.json_args.get('from_time'),
            self.json_args.get('to_time'),
            self.json_args.get('locked'),
        )
        creative = models.Playback(
            self.json_args.get('adspot_id'),
            None,
            self.json_args.get('creative_id'),
            self.json_args.get('status_id'),
            self.json_args.get('smart_contract'),
            self.json_args.get('play_price'),
            None,
        )
        self.ms.add_playback_timeslot(timeslot, creative)
        await self.send_ok()

    async def delete(self, id_: str):
        self.ms.delete_playback(int(id_))
        await self.send_ok()
