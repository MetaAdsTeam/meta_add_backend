from typing import Any

from sqlalchemy import select, insert, delete
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

    def get_adspot(self, id_: int) -> 'dc.AdSpot':
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

    def get_creatives(self) -> list['dc.Creative']:
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
            dc.Creative(
                row.Creative.id,
                row.CreativeType.name,
                row.Creative.nft_ref,
                row.Creative.url,
                row.Creative.name,
            ) for row in rows
        ]

    def add_creative(self, creative):
        self.session.add(creative)
        self.session.commit()

    def delete_creatives(self, id_s):
        self.session.execute(
            delete(models.Creative).where(models.Creative.id.in_(id_s))
        )
        self.session.commit()

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
                models.AdSpotType
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
            ).join(
                models.AdSpotType,
                models.AdSpot.spot_type_id == models.AdSpotType.id,
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
                row.Creative.path,
                row.PlaybackStatus.name,
                row.Playback.smart_contract,
                row.AdSpot.price,
                row.Playback.play_price,
                row.TimeSlot.locked,
                row.AdSpotType.name,
                row.AdSpotType.publish_url,
                row.Playback.processed_at,
            ) for row in rows
        ]

    def get_adspot_stats(self, id_: int) -> 'dc.AdSpotStats':
        row: models.AdSpotsStats = self.session.execute(
            select(
                models.AdSpotsStats,
            ).filter(
                models.AdSpotsStats.id == id_,
            )
        ).first()
        return row and dc.AdSpotStats(
            row.AdSpotsStats.id,
            row.AdSpotsStats.likes,
            row.AdSpotsStats.views_amount,
            row.AdSpotsStats.average_time,
            row.AdSpotsStats.max_traffic,
        )

    def get_timeslots_by_adspot_id(self, id_: int) -> 'dc.Timeslot':
        row: models.TimeSlot = self.session.execute(
            select(
                models.Playback,
                models.TimeSlot,
                models.AdSpot,
                models.AdSpotsStats,
            ).join(
                models.TimeSlot,
                models.Playback.timeslot_id == models.TimeSlot.id,
            ).join(
                models.AdSpot,
                models.Playback.adspot_id == models.AdSpot.id,
            ).join(
                models.AdSpotsStats,
                models.AdSpotsStats.spot_id == models.AdSpot.id,
            ).filter(
                models.AdSpotsStats.id == id_,
            )
        ).first()
        return row and dc.TimeSlot(
            row.TimeSlot.id,
            row.TimeSlot.from_time,
            row.TimeSlot.to_time,
            row.TimeSlot.locked,
            row.Playback.play_price,
        )

    def add_playback(self, playback):
        self.session.add(playback)
        self.session.commit()

    def delete_playbacks(self, id_s):
        self.session.execute(
            delete(models.Creative).where(models.Creative.id.in_(id_s))
        )
        self.session.commit()

    def get_playback_statuses(self) -> list['dc.PlaybackStatuses']:
        rows: list[models.PlaybackStatus] = self.session.execute(
            select(
                models.PlaybackStatus,
            )
        ).all()
        return [
            dc.PlaybackStatuses(
                row.PlaybackStatus.id,
                row.PlaybackStatus.name,
            ) for row in rows
        ]

    def get_adspot_types(self) -> list['dc.AdSpotTypes']:
        rows: list[models.AdSpotType] = self.session.execute(
            select(
                models.PlaybackStatus,
            )
        ).all()
        return [
            dc.AdSpotTypes(
                row.AdSpotType.id,
                row.AdSpotType.name,
                row.AdSpotType.publish_url,
            ) for row in rows
        ]

    def get_timeslots(self) -> list['dc.TimeSlot']:
        rows: list['models.TimeSlot'] = self.session.execute(
            select(
                models.TimeSlot,
                models.Playback,
            ).join(
                models.Playback,
                models.Playback.timeslot_id == models.TimeSlot.id,
            )
        ).all()
        return [
            dc.TimeSlot(
                row.TimeSlot.id,
                row.TimeSlot.from_time,
                row.TimeSlot.to_time,
                row.TimeSlot.locked,
                row.Playback.play_price,
            ) for row in rows
        ]
