import jwt

from root.handlers import BaseHandler, non_authorized


@non_authorized
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

    def get(self):
        pass
