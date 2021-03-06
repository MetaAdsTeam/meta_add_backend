import contextlib
import os
from typing import Any, Optional

import yaml
import root.data_classes as dc

from root.db_controller import DBController, WithSessionContextManager


class Context:
    def __init__(self):
        self.project_path: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.logs_path: str = os.path.join(self.project_path, 'logs')
        for folder in (self.logs_path,):
            if not os.path.exists(folder):
                with contextlib.suppress(Exception):
                    os.mkdir(folder)
        default_config_path: str = os.path.join(self.project_path, 'default.yaml')
        config_path: str = os.path.join(self.project_path, 'config.yaml')
        with open(default_config_path, 'r') as f:
            self.config: dict[str, Any] = yaml.safe_load(f)
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config.update(yaml.safe_load(f) or {})
        else:
            with open(config_path, 'w+') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        self.debug_mode: bool = self.config.get('debug_mode', False)
        self.static_path: str = self.config['static_path']
        self.static_url: str = self.config['static_url']
        self.uri_prefix: str = self.config.get('uri_prefix', '')
        self.nft_api_url: str = self.config['nft_api_url']
        self.nft_api_key: str = self.config['nft_api_key']
        self.api_secret: str = self.config['api_secret']
        self.jwt_algorithm: str = self.config['jwt_algorithm']
        self.user_session_timeout: int = self.config['user_session_timeout']
        self.max_timeslot_duration: int = self.config.get('max_timeslot_duration', 60)
        self.near_env: str = self.config['near_env']
        self.near_account_id: str = self.config['near_account_id']
        db: dict[str, Any] = self.config['db']
        self.db_config = dc.DBConfig(**db)
        self.__db_controller: Optional['DBController'] = None

    def load_db_controller(self) -> 'DBController':
        if self.__db_controller is None:
            self.__db_controller = DBController(self)
        return self.__db_controller

    def stop(self) -> None:
        if self.__db_controller is not None:
            self.__db_controller.stop()

    @property
    def db_controller(self) -> 'DBController':
        if self.__db_controller is None:
            raise Exception(
                'DB Controller not loaded. Use "load_db_controller()".')
        return self.__db_controller

    @property
    def sc(self) -> 'WithSessionContextManager':
        db_controller = self.load_db_controller()
        return db_controller.with_sc()
