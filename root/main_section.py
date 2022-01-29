from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from logging import Logger
import root
import root.log_lib as log_lib
import root.models as models
import root.data_classes as dc


class MS:
    __logger: 'log_lib' = None

    def __init__(self, session_: Session, context_: 'root.Context' = None):
        self.session = session_
        if context_ is None:
            context_ = root.context
        self.context = context_

    @property
    def logger(self) -> Logger:
        if self.__logger is None:
            self.__logger = root.log_lib.get_logger(self.__class__.__name__)
        return self.__logger

    def get_adspots(self) -> list['dc.AdPlace']:
        rows: list[Any['models.AdPlace', models.AdSpotType]] = self.session.execute(
            select(
                models.AdPlace,
                models.AdSpotType,
            ).join(
                models.AdSpotType,
                models.AdPlace.adspot_type == models.AdSpotType.id,
            )
        ).all()
        return [
            dc.AdPlace(
                row.AdPlace.id,
                row.AdSpotType.name,
                row.AdPlace.place_id,
                row.AdPlace.name,
            ) for row in rows
        ]
