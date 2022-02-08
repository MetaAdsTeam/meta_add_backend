from root.handlers import BaseHandler


class TimeSlotsDateHandler(BaseHandler):

    async def get(self, date_):
        await self.send_json(self.ms.get_timeslots_by_date(date_))
