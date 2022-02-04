import json
from dataclasses import asdict

from root import models
from root.handlers import BaseHandler


class TimeSlotsHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_timeslots())

    async def post(self):
        # print(self.json_args)
        try:
            timeslot = models.TimeSlot(**self.json_args)
        except TypeError as e:
            await self.send_failed(str(e))
        else:
            self.ms.add_timeslot(timeslot)
            await self.send_ok()
