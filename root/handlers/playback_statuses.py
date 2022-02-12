import root.enums as enums
from root.handlers import BaseHandler


class PlaybackStatusesHandler(BaseHandler):
    async def get(self):
        await self.send_json([e.value for e in enums.PlaybackStatus])
