from datetime import datetime, date
import pickle
from typing import Optional, Awaitable, Any

from sqlalchemy.orm import Session
from tornado import escape
from tornado.template import Loader
from tornado.web import RequestHandler
from tornado.escape import json_decode
from tornado.concurrent import Future

from root import Context
import root.db_controller as db_controller
import root.main_section as main_section
import root.utils as utils
from root.log_lib import get_logger


logger = get_logger(__name__)


class BaseHandler(RequestHandler):
    __sc: 'db_controller.SessionContext' = None
    __sc_cm: 'db_controller.WithSessionContextManager' = None
    __ms: 'main_section.MS' = None
    json_args: dict = {}
    template_loader: Loader = None
    context: 'Context' = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        self._prepare_json_args()
        self.context = self.settings['context']

    def _request_summary(self) -> str:
        return "%s [%s] %s " % (
            self.request.method,
            self.remote_ip,
            self.request.uri.removeprefix('/api'),
        )

    def _prepare_json_args(self):
        content_type = self.request.headers.get('Content-Type', '')
        if any((i in content_type for i in ('application/x-json', 'application/json'))):
            # if self.request.headers.get('Content-Type') in ('application/x-json', 'application/json'):
            self.json_args = json_decode(self.request.body) if self.request.body else {}
        else:  # self.request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
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
            self.__ms = main_section.MS(self.session)
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

