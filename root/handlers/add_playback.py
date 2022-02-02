import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class AddPlaybackHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    # def get(self):
    #     self.write(
    #         json.dumps(
    #             {'data': [asdict(w) for k, w in enumerate(self.ms.get_playbacks())]}
    #         )
    #     )

    async def post(self):
        # print(self.json_args)
        try:
            timeslot = models.TimeSlot(
                self.json_args.get('from_time'),
                self.json_args.get('to_time'),
                self.json_args.get('locked'),
            )
            creative = models.Playback(
                self.json_args.get('adspot_id'),
                self.json_args.get('timeslot_id'),
                self.json_args.get('creative_id'),
                self.json_args.get('status_id'),
                self.json_args.get('smart_contract'),
                self.json_args.get('play_price'),
                None,
            )
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_playback_timeslot(timeslot, creative)
            await self.send_ok()

    # async def delete(self):
    #     id_s = self.json_args.get('id_s', [])
    #     if not isinstance(id_s, list):
    #         id_s = [id_s]
    #     self.ms.delete_playback(id_s)
    #     await self.send_ok()
