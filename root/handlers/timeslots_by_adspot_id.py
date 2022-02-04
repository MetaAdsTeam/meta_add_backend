from root.handlers import BaseHandler


class TimeslotsByAdspotId(BaseHandler):
    async def get(self, id_):
        await self.send_json(self.ms.get_timeslots_by_adspot_id(id_))
