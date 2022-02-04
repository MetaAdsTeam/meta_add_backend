from root.handlers import BaseHandler


class PlaybackStatusesHandler(BaseHandler):
    async def get(self):
        await self.send_json(self.ms.get_playback_statuses())
