from root import models
from root.handlers import BaseHandler


class TimeSlotsHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_timeslots())

    async def post(self):
        timeslot = models.TimeSlot(
            self.json_args['from_time'],
            self.json_args['to_time'],
            self.json_args['locked'],
        )
        self.ms.add_timeslot(timeslot)
        await self.send_ok()
