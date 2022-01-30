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
                row.AdSpot.description,
                row.AdSpot.publisher_id,
                row.AdSpotType.name,
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
            row.AdSpot.description,
            row.AdSpot.publisher_id,
            row.AdSpotType.name,
            row.AdSpot.price,
            row.AdSpot.spot_metadata,
        )

    def get_creatives(self) -> list['dc.Content']:
        rows: list['models.Creative'] = self.session.execute(
            select(
                models.Creative,
                models.CreativeType,
            ).join(
                models.CreativeType,
                models.Creative.creative_type_id == models.CreativeType.id,
            )
        ).all()
        return [
            dc.Content(
                row.Content.id,
                row.ContentTypes.name,
                row.Content.nft_ref,
                str(row.Content.nft_bin),
                row.Content.url,
                row.Content.name,
            ) for row in rows
        ]

    def get_playbacks(self) -> list['dc.Playback']:
        rows: list['models.Playback'] = self.session.execute(
            select(
                models.Playback,
                models.Creative,
                models.CreativeType,
                models.Advertiser,
                models.TimeSlot,
                models.PlaybackStatus,
                models.AdSpot,
            ).join(
                models.Creative,
                models.Playback.creative_id == models.Creative.id,
            ).join(
                models.CreativeType,
                models.Creative.creative_type_id == models.CreativeType.id,
            ).join(
                models.Advertiser,
                models.Creative.advert_id == models.Advertiser.id,
            ).join(
                models.TimeSlot,
                models.Playback.timeslot_id == models.TimeSlot.id,
            ).join(
                models.PlaybackStatus,
                models.Playback.status_id == models.PlaybackStatus.id,
            ).join(
                models.AdSpot,
                models.Playback.adspot_id == models.AdSpot.id,
            )
        ).all()
        return [
            dc.Playback(
                row.Playback.id,
                row.AdSpot.name,
                row.TimeSlot.from_time,
                row.TimeSlot.to_time,
                row.Creative.advert_id,
                row.Creative.name,
                row.Creative.description,
                row.Creative.url,
                row.PlaybackStatus.name,
                row.Playback.smart_contract,
                row.Playback.spot_price,
                row.Playback.play_price,
            ) for row in rows
        ]
