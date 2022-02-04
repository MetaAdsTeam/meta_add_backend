import sys
from contextlib import suppress
from datetime import datetime, date
import pickle
from typing import Optional, Awaitable, Any

from deeply import Deeply
from sqlalchemy.orm import Session
from tornado import escape
from tornado.template import Loader
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.concurrent import Future
import jwt

from root import Context
import root.db_controller as db_controller
import root.main_section as main_section
import root.data_classes as dc
import root.utils as utils
import root.exceptions as exceptions
from root.log_lib import get_logger


logger = get_logger(__name__)


class BaseHandler(RequestHandler):
    __sc: 'db_controller.SessionContext' = None
    __sc_cm: 'db_controller.WithSessionContextManager' = None
    __ms: 'main_section.MS' = None
    json_args: dict = None
    template_loader: Loader = None
    context: 'Context' = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    @property
    def logger(self):
        return self.settings['logger']

    def check_auth(self):
        assert self.current_user

    def prepare(self):
        self._prepare_json_args()
        self.context = self.settings['context']
        self.check_auth()

    def _request_summary(self) -> str:
        return "%s [%s] %s " % (
            self.request.method,
            self.remote_ip,
            self.request.uri.removeprefix('/api'),
        )

    def get_current_user(self) -> 'dc.UserWeb':
        auth: str = self.request.headers.get('Authorization')
        if auth:
            token = auth.removeprefix('Bearer ')

            user_dict = jwt.decode(
                token,
                self.context.api_secret,
                algorithms=[self.context.jwt_algorithm]
            )
            user = dc.UserWeb.init_from_dict(user_dict)

            if datetime.fromisoformat(user.session_exp) < datetime.utcnow():
                raise exceptions.UnauthorizedError(
                    'Your session has expired'
                )
            return user

        raise exceptions.UnauthorizedError()

    def _prepare_json_args(self):
        content_type = self.request.headers.get('Content-Type', '')
        if any((i in content_type for i in ('application/x-json', 'application/json'))):
            # if self.request.headers.get('Content-Type') in ('application/x-json', 'application/json'):
            self.json_args = json_decode(self.request.body) if self.request.body else {}
        else:  # self.request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            self.json_args = {}
            for k, v in self.request.arguments.items():
                if len(v) == 1:
                    self.json_args[k] = v[0].decode('utf-8')
                elif len(v) > 1:
                    self.json_args[k] = [v[i].decode('utf-8') for i in range(len(v))]

    def on_finish(self):
        if self.__sc_cm is not None:
            self.__sc_cm.__exit__(None, None, None)

    @property
    def ms(self) -> 'main_section.MS':
        if self.__ms is None:
            self.__ms = main_section.MS(self.session, self.context, self.current_user)
        return self.__ms

    @property
    def sc(self) -> 'db_controller.SessionContext':
        if self.__sc is None:
            self.__sc_cm = self.context.db_controller.with_sc()
            self.__sc = self.__sc_cm.__enter__()
        return self.__sc

    @property
    def session(self) -> Session:
        return self.sc.session

    @property
    def remote_ip(self):
        return self.request.headers.get("X-Real-Ip") or \
               self.request.headers.get("X-Forwarded-For") or \
               self.request.remote_ip

    def write_error(self, status_code: int, **kwargs):
        reason: Optional[str] = kwargs.get('reason', None)
        error_type: Optional[str] = None
        if 'exc_info' in kwargs:
            _, err, _ = kwargs['exc_info']
            if isinstance(err, exceptions.APIError):
                self.set_status(err.code)
                status_code = err.code
                reason = err.message
                if hasattr(err, 'error_type'):
                    error_type = err.error_type
        if reason is None:
            if self._reason:
                reason = self._reason
            else:
                reason = f'Web server error {status_code}.'

        if status_code == 500:
            status_code = 400
            self.set_status(400)
            if sys.exc_info()[0] == KeyError:
                reason = f'Argument `{sys.exc_info()[1].args[0]}` is required but not specified.'
            else:
                reason = repr(sys.exc_info()[1])

        self.logger.warning(f'Handler error! Status: {status_code}, reason: {reason}')
        self.set_header('Content-Type', 'application/json')
        if error_type:
            self.finish(escape.json_encode({'msg': reason, 'type': error_type}))
        else:
            self.finish(escape.json_encode({'msg': reason}))

    async def send_no_data(self):
        await self.send_json({'msg': 'No data'}, 404)

    async def send_ok(self, status: int = 200):
        await self.send_json({'msg': 'ok'}, status)

    async def send_failed(self, msg: str = 'failed', status: int = 400):
        await self.send_json({'msg': msg}, status)

    async def send_json(self, data, status: int = 200) -> None:
        if data is None:
            return await self.send_failed('Not found', 404)
        self.set_header('Content-Type', 'application/json')
        self.set_status(status)
        if self.__sc is not None:
            self.__sc.close()
        if isinstance(data, list):
            data = {'data': data}
        try:
            body = escape.json_encode(data)
        except TypeError:
            data = Deeply._Deeply__deep_dict(data, Deeply.rules)  # noqa
            body = escape.json_encode(data)
        await self.finish(body)


def non_authorized(cls):
    cls.check_auth = lambda _: ...
    cls.get_current_user = lambda _: ...
    return cls
