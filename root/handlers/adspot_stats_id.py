from root.handlers import BaseHandler, non_authorized


@non_authorized
class AdSpotStatsIdHandler(BaseHandler):
    async def get(self, id_):
        await self.send_json(self.ms.get_adspot_stats(id_))
