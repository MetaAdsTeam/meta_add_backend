from typing import Optional

from root.handlers import BaseHandler
import root.exceptions as exc


class CreativesHandler(BaseHandler):

    async def get(self, id_: Optional[str] = None):
        if id_ is not None:
            await self.send_json(self.ms.get_creative(int(id_)))
        else:
            await self.send_json(self.ms.get_creatives())

    async def post(self):
        try:
            await self.ms.add_creative(
                self.json_args['name'],
                self.json_args['file'],
                self.json_args['filename'],
                self.json_args.get('description'),
            )
        except exc.APIError as e:
            await self.send_failed()
        else:
            await self.send_json(self.ms.get_creatives())

    async def delete(self, id_):
        self.ms.delete_creative(id_)
        await self.send_ok()

    async def put(self, id_):
        try:
            self.ms.set_blockchain_ref(id_, self.json_args['blockchain_ref'])
        except exc.APIError as e:
            await self.send_failed(e.message)
        else:
            await self.send_ok()
