from root.handlers import BaseHandler, non_authorized


@non_authorized
class AdSpotTypesHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_adspot_types())
