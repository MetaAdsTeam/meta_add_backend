from typing import Optional

from root.handlers import BaseHandler, non_authorized


class AdSpotsHandler(BaseHandler):
    async def get(self, id_: Optional[str] = None):
        if id_ is not None:
            await self.send_json(self.ms.get_adspot(int(id_)))
        else:
            await self.send_json(self.ms.get_adspots())


@non_authorized
class AdSpotStreamHandler(BaseHandler):
    async def get(self, id_: str):
        stream_url = self.ms.get_adspot_stream(int(id_))
        if stream_url:
            self.redirect(stream_url)
        else:
            await self.send_failed('There are no stream now', 404)
