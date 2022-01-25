import logging
from time import sleep
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.engine as engine

import root.exceptions as exceptions
from root.log_lib import get_logger


class SessionContext:
    __session: 'Session' = None

    def __init__(self, engine_: 'engine.Engine'):
        self.__engine: 'engine.Engine' = engine_

    @property
    def session(self) -> 'Session':
        if self.__session is None:
            self.__session = Session(self.__engine, expire_on_commit=False)
        return self.__session

    @session.setter
    def session(self, session: 'Session'):
        self.__session = session

    def close(self):
        try:
            self.session.commit()
        except Exception as ex:
            logging.warning(
                'Session commit error, rollback ...\n{}'.format(ex)
            )
            self.session.rollback()
        finally:
            self.session.close()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            if hasattr(e, 'detail'):
                raise exceptions.APIError(
                    f'One of arguments are wrong: {e.detail}'
                )
            else:
                raise exceptions.APIError(
                    f'One of arguments are wrong. '
                    f'Please make sure you are sending right request.'
                )

    def flush(self, *args, **kwargs):
        try:
            self.session.flush(*args, **kwargs)
        except Exception as e:
            try:
                details = 'One of arguments are wrong. ' + \
                          e.args[0].split('\n')[-2]
            except (AttributeError, KeyError):
                details = f'One of arguments are wrong. ' \
                          f'Please make sure you are sending right request.'
            self.session.rollback()
            raise exceptions.APIError(details)


class WithSessionContextManager:
    def __init__(self, db_controller: 'DBController'):
        self.db_controller = db_controller
        self.sc: Optional[SessionContext] = None
        self.__a_session_cm = None

    def __enter__(self):
        self.sc = self.db_controller.make_sc()
        return self.sc

    def __exit__(self, err_type, err_value, err_traceback):
        self.sc.close()


class DBController:
    """Database controller."""

    __engine: 'engine.Engine' = None

    def __init__(self, context):
        self.logger = get_logger(self.__class__.__name__)
        self.app_context = context
        self.logger.debug('DBController started.')

    @property
    def engine(self):
        if self.__engine is None:
            self.__engine = sa.create_engine(
                self.app_context.db_config.db_con_string,
                echo=False,
                encoding='utf-8'
            )
        return self.__engine

    def make_sc(self) -> SessionContext:
        while self.engine is None:
            sleep(.05)
        return SessionContext(self.__engine)

    def with_sc(self) -> WithSessionContextManager:
        return WithSessionContextManager(self)

    def stop(self):
        if self.__engine is not None:
            self.__engine.dispose()
        self.logger.debug('DBController stopped.')
