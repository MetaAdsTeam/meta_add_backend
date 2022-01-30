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

    def get_adspots(self) -> list['dc.AdSpot']:
        rows: list[Any['models.AdSpot', models.AdSpotType]] = self.session.execute(
            select(
                models.AdSpot,
                models.AdSpotType,
            ).join(
                models.AdSpotType,
                models.AdSpot.spot_type_id == models.AdSpotType.id,
            )
        ).all()
        return [
            dc.AdSpot(
                row.AdSpot.id,
                row.AdSpotType.name,
                row.AdSpotType.description,
                row.AdSpot.publisher_id,
                row.AdSpot.adspot_type,
                row.AdSpot.price,
                row.AdSpot.spot_metadata,
            ) for row in rows
        ]

    def get_adspot(self, id_) -> 'dc.AdSpot':
        row: Any['models.AdSpot', models.AdSpotType] = self.session.execute(
            select(
                models.AdSpot,
                models.AdSpotType,
            ).join(
                models.AdSpotType,
                models.AdSpot.spot_type_id == models.AdSpotType.id,
            ).filter(
                models.AdSpot.id == id_,
            )
        ).first()
        return row and dc.AdSpot(
            row.AdSpot.id,
            row.AdSpotType.name,
            row.AdSpotType.description,
            row.AdSpot.publisher_id,
            row.AdSpot.adspot_type,
            row.AdSpot.price,
            row.AdSpot.spot_metadata,
        )

    def get_adspotsss(self, id_) -> 'dc.AdSpot':
        pass
        # row = self.session.execute(
        #     select(
        #         models.AdSpot,
        #         models.AdSpotType,
        #         models.Publisher,
        #     ).join(
        #         models.AdSpotType,
        #         models.AdSpot.adspot_type_id == models.AdSpotType.id,
        #     ).join(
        #         models.Publisher,
        #         models.AdSpot.publisher_id == models.Publisher.id,
        #     ).filter(
        #         models.AdSpot.id == id_,
        #     )
        # ).first()
        # return dc.AdSpot(
        #     row.AdSpot.id,
        #     row.AdSpotType.name,
        #     row.AdSpot.place_id,
        #     row.AdSpot.price,
        #     row.Publisher.id,
        # )

    def get_creatives(self) -> list['dc.Content']:
        pass
        # rows: list['models.Creative'] = self.session.execute(
        #     select(
        #         models.Creative,
        #         models.CreativeType,
        #     ).join(
        #         models.CreativeType,
        #         models.Creative.content_type_id == models.CreativeType.id,
        #     )
        # ).all()
        # return [
        #     dc.Content(
        #         row.Content.id,
        #         row.ContentTypes.name,
        #         row.Content.nft_ref,
        #         str(row.Content.nft_bin),
        #         row.Content.url,
        #         row.Content.name,
        #     ) for row in rows
        # ]
