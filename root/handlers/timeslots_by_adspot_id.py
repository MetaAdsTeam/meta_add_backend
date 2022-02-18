from datetime import datetime, date
from typing import Optional

from root.handlers import BaseHandler


class TimeslotsByAdspotId(BaseHandler):
    async def post(self, id_: str):
        client_time = self.json_args.get('client_time')
        if client_time is not None:
            client_time = datetime.fromisoformat(client_time)
            await self.send_json(
                self.ms.get_timeslots_by_adspot_id(int(id_), client_time)
            )
        else:
            await self.send_json(
                self.ms.get_timeslots_by_adspot_id(int(id_))
            )
