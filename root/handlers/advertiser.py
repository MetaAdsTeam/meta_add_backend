import json
from datetime import date

import jwt

from root import enums
from root.handlers import BaseHandler


class LoginHandler(BaseHandler):
    async def post(self):
        user = self.ms.authorize(**self.json_args)

        token = jwt.encode(
            user.to_web(),
            self.context.api_secret,
            algorithm=self.context.jwt_algorithm
        )
        resp = {'Authorization': f'Bearer {token}'}
        await self.send_json(resp)


class AdvertiserHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        pass
