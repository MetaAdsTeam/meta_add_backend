import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class TimeSlotsHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        self.write(
            json.dumps(
                {'data': [asdict(w) for k, w in enumerate(self.ms.get_timeslots())]}
            )
        )

    async def post(self):
        # print(self.json_args)
        try:
            timeslot = models.TimeSlot(**self.json_args)
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_timeslot(timeslot)
            await self.send_ok()
