import datetime
from typing import Any, Optional

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
import sqlalchemy as sa
from logging import Logger
import root
import root.log_lib as log_lib
import root.exceptions as exceptions
import root.models as models
import root.data_classes as dc


class MS:
    __logger: 'log_lib.Logger' = None

    def __init__(
            self, session_: Session,
            context_: Optional['root.Context'] = None,
            user: Optional['dc.UserWeb'] = None
    ):
        self.session = session_
        self.context = context_ or root.context
        self.user = user

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
                models.AdSpotsStats,
                models.Publisher,
            ).join(
                models.AdSpotType,
                models.AdSpot.spot_type_id == models.AdSpotType.id,
            ).join(
                models.AdSpotsStats,
                models.AdSpot.id == models.AdSpotsStats.spot_id
            ).join(
                models.Publisher,
                models.AdSpot.publisher_id == models.Publisher.id
            )
        ).all()
        return [
            dc.AdSpot(
                row.AdSpot.id,
                row.AdSpotType.name,
                row.AdSpot.description,
                row.Publisher.name,
                row.AdSpotType.name,
                row.AdSpot.price,
                row.AdSpot.preview_url,
                row.AdSpot.preview_thumb_url,
                row.AdSpot.spot_metadata,
                row.AdSpotsStats.likes,
                row.AdSpotsStats.views_amount,
                row.AdSpotsStats.average_time,
                row.AdSpotsStats.max_traffic,
            ) for row in rows
        ]

    def get_adspot(self, id_: int) -> 'dc.AdSpot':
        row: Any['models.AdSpot', models.AdSpotType] = self.session.execute(
            select(
                models.AdSpot,
                models.AdSpotType,
                models.AdSpotsStats,
                models.Publisher,
            ).join(
                models.AdSpotType,
                models.AdSpot.spot_type_id == models.AdSpotType.id,
            ).join(
                models.AdSpotsStats,
                models.AdSpot.id == models.AdSpotsStats.spot_id
            ).join(
                models.Publisher,
                models.AdSpot.publisher_id == models.Publisher.id
            ).filter(
                models.AdSpot.id == id_,
            )
        ).first()
        return row and dc.AdSpot(
            row.AdSpot.id,
            row.AdSpotType.name,
            row.AdSpot.description,
            row.Publisher.name,
            row.AdSpotType.name,
            row.AdSpot.price,
            row.AdSpot.preview_url,
            row.AdSpot.preview_thumb_url,
            row.AdSpot.spot_metadata,
            row.AdSpotsStats.likes,
            row.AdSpotsStats.views_amount,
            row.AdSpotsStats.average_time,
            row.AdSpotsStats.max_traffic,
        )

    def get_creatives(self) -> list['dc.Creative']:
        q = select(
            models.Creative,
            models.CreativeType,
        ).join(
            models.CreativeType,
            models.Creative.creative_type_id == models.CreativeType.id,
        )
        if self.user:
            q = q.filter(models.Creative.advert_id == self.user.id)

        rows: list['models.Creative'] = self.session.execute(q).all()
        return [
            dc.Creative(
                row.Creative.id,
                row.CreativeType.name,
                row.Creative.nft_ref,
                row.Creative.url,
                row.Creative.name,
            ) for row in rows
        ]

    def get_creative(self, id_) -> 'dc.Creative':
        _id = int(id_)
        q = select(
            models.Creative,
            models.CreativeType,
        ).join(
            models.CreativeType,
            models.Creative.creative_type_id == models.CreativeType.id,
        ).where(
            models.Creative.id == _id,
        )
        if self.user:
            q = q.filter(models.Creative.advert_id == self.user.id)

        row: models.Creative = self.session.execute(q).first()
        return row and dc.Creative(
            row.Creative.id,
            row.CreativeType.name,
            row.Creative.nft_ref,
            row.Creative.url,
            row.Creative.name,
        )

    def add_creative(self, creative):
        self.session.add(creative)
        self.session.commit()

    def delete_creative(self, id_):
        _id = int(id_)
        q = delete(
            models.Creative
        ).filter(
            models.Creative.id == _id
        )
        if self.user:
            q = q.filter(models.Creative.advert_id == self.user.id)
        self.session.execute(q)
        self.session.commit()

    def get_playbacks(self) -> list['dc.Playback']:
        q = select(
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
        if self.user:
            q = q.filter(models.Advertiser.id == self.user.id)

        rows: list['models.Playback'] = self.session.execute(q).all()
        return [
            dc.Playback(
                row.Playback.id,
                row.AdSpot.name,
                row.TimeSlot.from_time.timestamp(),
                row.TimeSlot.to_time.timestamp(),
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
                row.Playback.taken_at,
                row.Playback.processed_at,
            ) for row in rows
        ]

    def get_playback(self, id_) -> 'dc.Playback':
        _id = int(id_)
        q = select(
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
        ).where(
            models.Playback.id == _id
        )
        if self.user:
            q = q.filter(models.Advertiser.id == self.user.id)

        row: models.Playback = self.session.execute(q).first()
        return row and dc.Playback(
            row.Playback.id,
            row.AdSpot.name,
            row.TimeSlot.from_time.timestamp(),
            row.TimeSlot.to_time.timestamp(),
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
            row.Playback.taken_at,
            row.Playback.processed_at,
        )

    def allocate_pending_playbacks(self) -> list['dc.AdTask']:
        from_dt = datetime.datetime.utcnow()
        to_dt = from_dt + datetime.timedelta(seconds=15)
        rows: list['models.Playback'] = self.session.execute(
            select(
                models.Playback.id,
                models.Playback.taken_at,
                models.Playback.adspot_id,
                models.Creative.path,
                models.TimeSlot.from_time,
                models.TimeSlot.to_time,
                models.AdSpot.publish_url,
                models.AdSpot.stop_url,
                models.AdSpot.delay_before_publish,
            ).select_from(
                models.Playback
            ).join(
                models.Creative,
                models.Playback.creative_id == models.Creative.id,
            ).join(
                models.TimeSlot,
                models.Playback.timeslot_id == models.TimeSlot.id,
            ).join(
                models.AdSpot,
                models.Playback.adspot_id == models.AdSpot.id,
            ).filter(
                sa.or_(
                    sa.and_(
                        models.Playback.taken_at.is_(None),
                        models.Playback.processed_at.is_(None),
                        models.TimeSlot.from_time.between(from_dt, to_dt)
                    ),
                    sa.and_(
                        models.Playback.taken_at.isnot(None),
                        models.Playback.processed_at.is_(None),
                        models.TimeSlot.to_time.between(from_dt, to_dt)
                    )
                )
            )
        ).all()

        def get_call_time(task_row):
            if task_row.taken_at is None:
                return task_row.from_time - datetime.timedelta(
                    seconds=task_row.delay_before_publish)
            return task_row.to_time

        tasks: list['dc.AdTask'] = []
        expires_dt_by_ap: dict[int, datetime.datetime] = {}
        for row in sorted(rows, key=get_call_time):
            primarily = row.taken_at is None
            call_at = get_call_time(row)
            if primarily:
                api_url = row.publish_url
                expires_dt_by_ap[row.adspot_id] = row.to_time
            else:
                api_url = row.stop_url
                if ex_dt := expires_dt_by_ap.get(row.adspot_id):
                    # filter simultaneous requests
                    if ex_dt > call_at:
                        continue
            tasks.append(
                dc.AdTask(
                    row.id,
                    row.adspot_id,
                    api_url,
                    call_at,
                    primarily,
                    dc.AdTaskConfig(
                        row.path,
                        row.from_time,
                        row.to_time,
                    )
                )
            )
        return tasks

    def mark_task_complete(self, task: 'dc.AdTask'):
        state_at = datetime.datetime.utcnow()
        if task.primarily:
            state = {models.Playback.taken_at.key: state_at}
        else:
            state = {models.Playback.processed_at.key: state_at}
        self.session.execute(
            update(
                models.Playback
            ).where(
                models.Playback.id == task.playback_id
            ).values(
                **state
            ).execution_options(
                synchronize_session="evaluate"
            )
        )

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

    def get_timeslots_by_adspot_id(self, id_: int) -> 'dc.TimeSlot':
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
            row.TimeSlot.from_time.timestamp(),
            row.TimeSlot.to_time.timestamp(),
            row.TimeSlot.locked,
            row.Playback.play_price,  # TODO: recheck
        )

    def add_playback(self, playback):
        self.session.add(playback)
        self.session.commit()

    def delete_playback(self, id_):
        _id = int(id_)
        if self.user:
            user_sub_q = select(
                models.Creative.id
            ).filter(
                models.Creative.advert_id == self.user.id
            ).subquery()
            q = delete(
                models.Playback
            ).filter(
                models.Playback.creative_id.in_(user_sub_q),
                models.Playback.id == _id,
            )
        else:
            q = delete(
                models.Playback
            ).filter(
                models.Playback.id == _id,
            )
        self.session.execute(q)
        self.session.commit()

    def get_playback_statuses(self) -> list['dc.PlaybackStatuses']:
        q = select(models.PlaybackStatus)
        rows: list[models.PlaybackStatus] = self.session.execute(q).all()
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
                row.TimeSlot.from_time.timestamp(),
                row.TimeSlot.to_time.timestamp(),
                row.TimeSlot.locked,
                row.Playback.play_price,
            ) for row in rows
        ]

    def add_timeslot(self, timeslot):
        self.session.add(timeslot)
        self.session.commit()
        return timeslot.id

    def add_playback_timeslot(self, timeslot, playback):
        self.session.add(timeslot)
        self.session.flush()
        if timeslot.id:
            playback.timeslot_id = timeslot.id
            self.session.add(playback)
            self.session.commit()
        else:
            self.session.rollback()

    def authorize(self, login: str, password: str) -> 'dc.UserWeb':
        advertiser = self.session.query(
            models.Advertiser
        ).filter(
            models.Advertiser.login == login
        ).first()
        if not advertiser or advertiser.password != password:
            raise exceptions.UnauthorizedError(
                'Invalid username/password combination'
            )
        session_till = datetime.datetime.utcnow() + datetime.timedelta(
            hours=self.context.user_session_timeout)
        return dc.UserWeb(
            advertiser.id,
            advertiser.login,
            advertiser.name,
            advertiser.wallet_ref,
            session_till.isoformat()
        )
