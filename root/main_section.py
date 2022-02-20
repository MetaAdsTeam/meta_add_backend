import base64
import datetime
import json
import os
from typing import Optional, Union

import aiofiles
import aiohttp
from aiohttp.web import HTTPException
from sqlalchemy import select, delete, update, Date, cast
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
import sqlalchemy as sa
from logging import Logger
import root
import root.log_lib as log_lib
import root.models as models
import root.utils as utils
import root.data_classes as dc
import root.exceptions as exc


class MS:
    __logger: 'log_lib.Logger' = None

    def __init__(
            self, session_: Session,
            context_: Optional['root.Context'] = None,
            request_user: Optional['dc.RequestUser'] = None,
            user: Optional['dc.UserWeb'] = None
    ):
        self.session = session_
        self.context = context_ or root.context
        self.__user = user
        self.request_user = request_user

    @property
    def user(self) -> Optional['dc.UserWeb']:
        if self.__user is None and self.request_user:
            self.__user = self.authorize(
                self.request_user.meta_mask,
                self.request_user.near
            )
        return self.__user

    @property
    def logger(self) -> Logger:
        if self.__logger is None:
            self.__logger = root.log_lib.get_logger(self.__class__.__name__)
        return self.__logger

    def get_adspots(self, ids: Optional[list[int]] = None) -> list['dc.AdSpot']:
        q = select(
            models.AdSpot,
            models.AdSpotType,
            models.AdSpotsStats,
            models.Publisher,
        ).outerjoin(
            models.AdSpotType,
            models.AdSpot.spot_type_id == models.AdSpotType.id,
        ).outerjoin(
            models.AdSpotsStats,
            models.AdSpot.id == models.AdSpotsStats.spot_id
        ).outerjoin(
            models.Publisher,
            models.AdSpot.publisher_id == models.Publisher.id
        ).order_by(
            sa.desc(models.AdSpot.active),
            models.AdSpot.spot_type_id
        )
        if ids is not None:
            q = q.filter(models.AdSpot.id.in_(ids))
        rows: list[Union['models.AdSpot', models.AdSpotType]] = self.session.execute(q).all()
        return [
            dc.AdSpot(
                row.AdSpot.id,
                row.AdSpot.name,
                row.AdSpot.active,
                row.AdSpot.description,
                row.Publisher.name,
                row.Publisher.wallet_ref,
                row.AdSpotType.name,
                row.AdSpot.price,
                row.AdSpot.preview_url,
                row.AdSpot.preview_thumb_url,
                row.AdSpot.jump_url,
                row.AdSpot.spot_metadata,
                row.AdSpotsStats and row.AdSpotsStats.likes,
                row.AdSpotsStats and row.AdSpotsStats.views_amount,
                row.AdSpotsStats and row.AdSpotsStats.average_time,
                row.AdSpotsStats and row.AdSpotsStats.max_traffic,
            ) for row in rows
        ]

    def get_adspot(self, id_: int) -> 'dc.AdSpot':
        adspots = self.get_adspots([id_])
        return adspots[0] if adspots else None

    def get_actual_adspots_stream(
            self,
            adspot_ids: Optional[list[int]] = None,
            moment: Optional['datetime.datetime'] = None,
    ) -> list['Row']:
        if moment is None:
            moment = datetime.datetime.utcnow()

        stream_q = select(
            models.Playback.adspot_id,
            models.Creative.path,
            models.TimeSlot.from_time,
            models.TimeSlot.to_time,
        ).join(
            models.Playback,
            models.Playback.creative_id == models.Creative.id,
        ).join(
            models.TimeSlot,
            models.TimeSlot.id == models.Playback.timeslot_id,
        ).join(
            models.AdSpot,
            models.AdSpot.id == models.Playback.adspot_id,
        ).filter(
            sa.or_(
                sa.and_(
                    models.Creative.moderated.isnot(False),
                    models.AdSpot.spot_type_id != 2,  # Any ads except Offline
                ),
                sa.and_(
                    models.Creative.moderated.is_(True),
                    models.AdSpot.spot_type_id == 2,  # Offline ads
                ),
            ),
            models.TimeSlot.from_time <= moment,
            models.TimeSlot.to_time > moment,
        )

        if adspot_ids is not None:
            stream_q = stream_q.filter(
                models.Playback.adspot_id.in_(adspot_ids),
            )

        stream_rows = self.session.execute(stream_q).all()
        return stream_rows

    def path_to_url(self, media_path: str) -> str:
        stream_filename: str = media_path.removeprefix(self.context.static_path)
        return self.context.static_url + stream_filename

    def stream_file_meta(self, stream_path: str) -> tuple[str, bool]:
        stream_filename: str = stream_path.removeprefix(self.context.static_path)
        stream_url = self.path_to_url(stream_path)
        is_image = utils.is_image(stream_filename)
        return stream_url, is_image

    def get_adspot_default_stream(self, id_: int) -> Optional[dc.StreamWeb]:
        file_path = self.session.query(
            models.AdSpot.default_media
        ).filter(
            models.AdSpot.default_media.isnot(None),
            models.AdSpot.id == id_
        ).first()[0]

        if not file_path:
            return None

        stream_url, is_image = self.stream_file_meta(file_path)
        from_time = datetime.datetime.utcnow()
        to_time = from_time.replace(second=59)

        return dc.StreamWeb(
            stream_url,
            is_image,
            True,
            from_time,
            to_time,
            'ok',
        )

    def get_adspot_stream(self, id_: int) -> Optional[dc.StreamWeb]:
        stream_rows = self.get_actual_adspots_stream([id_])
        if not stream_rows:
            return self.get_adspot_default_stream(id_)
        stream_data = dc.StreamData(**stream_rows[0])
        stream_url, is_image = self.stream_file_meta(stream_data.path)

        return dc.StreamWeb(
            stream_url,
            is_image,
            False,
            stream_data.from_time,
            stream_data.to_time,
            'ok',
        )

    def get_creatives(self, ids: Optional[list[int]] = None, mint: bool = False) -> list['dc.Creative']:
        q = select(
            models.Creative,
        ).where(
            models.Creative.moderated.isnot(False)
        )
        if mint:
            q = q.filter(models.Creative.blockchain_ref.isnot(None))
        if ids is not None:
            q = q.filter(models.Creative.id.in_(ids))
        if self.user:
            q = q.filter(models.Creative.advert_id == self.user.id)

        rows: list['models.Creative'] = self.session.execute(q).all()
        return [
            dc.Creative(
                row.Creative.id,
                row.Creative.nft_ref,
                row.Creative.url,
                row.Creative.name,
                row.Creative.description,
                row.Creative.blockchain_ref,
            ) for row in rows
        ]

    def get_creative(self, id_: int) -> 'dc.Creative':
        creatives = self.get_creatives([id_])
        return creatives[0] if creatives else None

    async def upload_file_to_nft_storage(self, filepath):
        headers = {'Authorization': f'Bearer {self.context.nft_api_key}'}
        async with aiofiles.open(filepath, mode='rb') as f:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        self.context.nft_api_url,
                        data={'file': f},
                        headers=headers
                ) as resp:
                    response = await resp.text()
            if resp.status != 200:
                raise exc.APIError(resp.reason, resp.status)
            json_response = json.loads(response)
            return resp.status, json_response['value']['cid']

    async def add_creative(
            self,
            name: str,
            file: str,
            filename: str,
            description: str,
    ):
        advert_id = self.user.id
        safe_filename = utils.safe_filename(filename)
        filename = f'{int(datetime.datetime.utcnow().timestamp())}_{safe_filename}'
        filepath = os.path.join(self.context.static_path, filename)
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(file))
        url = self.context.static_url + filename

        try:
            status, nft_ref = await self.upload_file_to_nft_storage(filepath)
        except IOError:
            exc.APIError(f'Could not read file: {filepath}')
        except HTTPException as e:
            exc.APIError(e.reason)
        except exc.APIError as e:
            exc.APIError(e.message)
        else:
            thumbnail = utils.make_thumbnail(filepath)
            creative = models.Creative(
                advert_id,
                None,  # TODO: remove useless field
                nft_ref,
                None,
                name,
                description,
                url,
                filepath,
                thumbnail
            )
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

    def edit_creative(self, id_, blockchain_ref):
        _id = int(id_)
        q = update(
            models.Creative
        ).where(
            models.Creative.id == _id
        ).values(
            blockchain_ref=blockchain_ref
        ).returning(
            models.Creative.id
        )
        if self.user:
            q = q.filter(models.Creative.advert_id == self.user.id)
        updated = self.session.execute(q)
        if not updated.rowcount:
            raise exc.APIError(f'Creative id = {_id} not found.')
        self.session.commit()

    def edit_playback(self, id_, status, smart_contract):
        _id = int(id_)
        if self.user:
            user_sub_q = select(
                models.Creative.id
            ).filter(
                models.Creative.advert_id == self.user.id
            ).scalar_subquery()
            q = update(
                models.Playback
            ).where(
                models.Playback.creative_id.in_(user_sub_q),
                models.Playback.id == _id
            ).values(
                status=status,
                smart_contract=smart_contract,
            ).returning(
                models.Playback.id
            ).execution_options(synchronize_session=False)
        else:
            q = update(
                models.Playback
            ).where(
                models.Playback.id == _id
            ).values(
                status=status,
                smart_contract=smart_contract,
            ).returning(
                models.Playback.id
            )
        updated = self.session.execute(q)
        if not updated.rowcount:
            raise exc.APIError(f'Playback id = {_id} not found or no rights to edit this id.')
        self.session.commit()

    def get_playbacks(self, ids: Optional[list[int]] = None) -> list['dc.Playback']:
        q = select(
            models.Playback,
            models.Creative,
            models.CreativeType,
            models.TimeSlot,
            models.AdSpot,
            models.AdSpotType,
            models.AdSpotsStats,
        ).join(
            models.Creative,
            models.Playback.creative_id == models.Creative.id,
        ).outerjoin(
            models.CreativeType,
            models.Creative.creative_type_id == models.CreativeType.id,
        ).join(
            models.Advertiser,
            models.Creative.advert_id == models.Advertiser.id,
        ).join(
            models.TimeSlot,
            models.Playback.timeslot_id == models.TimeSlot.id,
        ).join(
            models.AdSpot,
            models.Playback.adspot_id == models.AdSpot.id,
        ).join(
            models.AdSpotType,
            models.AdSpot.spot_type_id == models.AdSpotType.id,
        ).join(
            models.AdSpotsStats,
            models.AdSpot.id == models.AdSpotsStats.spot_id,
        ).order_by(
            sa.desc(models.Playback.id)
        )
        if ids is not None:
            q = q.filter(models.Playback.id.in_(ids))
        if self.user:
            q = q.filter(models.Advertiser.id == self.user.id)

        rows: list['models.Playback'] = self.session.execute(q).all()

        playbacks = []

        for row in rows:

            preview = row.AdSpot.preview_thumb_url
            if row.Creative.thumbnail:
                preview = self.path_to_url(row.Creative.thumbnail)

            playbacks.append(
                dc.Playback(
                    row.Playback.id,
                    row.AdSpot.id,
                    row.AdSpot.name,
                    row.AdSpotsStats.likes,
                    preview,
                    row.AdSpot.jump_url,
                    row.TimeSlot.from_time,
                    row.TimeSlot.to_time,
                    row.Creative.advert_id,
                    row.Creative.name,
                    row.Creative.description,
                    row.Creative.url,
                    row.Creative.path,
                    row.Playback.status and row.Playback.status.value,
                    row.Playback.smart_contract,
                    row.AdSpot.price,
                    row.TimeSlot.locked,
                    row.AdSpotType.name,
                    row.Playback.taken_at,
                    row.Playback.processed_at,
                )
            )

        return playbacks

    def get_playback(self, id_: int) -> 'dc.Playback':
        playbacks = self.get_playbacks([id_])
        return playbacks[0] if playbacks else None

    def get_adspot_defaults(
            self,
            from_dt: datetime.datetime,
            to_dt: datetime.datetime,
            ids: Optional[list[int]] = None,
            not_ids: Optional[list[int]] = None,
    ) -> list['dc.AdSpotDefault']:
        curr_streams = self.get_actual_adspots_stream(moment=from_dt)
        active_ad_spot_ids = [s[0] for s in curr_streams]

        defaults_q = select(
            models.AdSpot.id,
            models.AdSpot.publish_url,
            models.AdSpot.default_media
        ).filter(
            models.AdSpot.id.notin_(active_ad_spot_ids),
            models.AdSpot.active.is_(True),
            models.AdSpot.publish_url.isnot(None),
            models.AdSpot.default_media.isnot(None),
        )

        if ids is not None:
            defaults_q = defaults_q.filter(models.AdSpot.id.in_(ids))
        if not_ids is not None:
            defaults_q = defaults_q.filter(models.AdSpot.id.notin_(not_ids))

        default_rows = self.session.execute(defaults_q).all()

        defaults = [
            dc.AdSpotDefault(
                row[0],
                row[1],
                dc.AdTaskConfig(
                    row[2],
                    from_dt,
                    to_dt,
                    True
                )
            )
            for row in default_rows
        ]
        return defaults

    def allocate_pending_playbacks(
            self,
            from_dt: datetime.datetime,
            to_dt: datetime.datetime
    ) -> list['dc.AdTask']:
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
                        models.Creative.moderated.isnot(False),
                        models.AdSpot.spot_type_id != 2,    # Any ads except Offline
                    ),
                    sa.and_(
                        models.Creative.moderated.is_(True),
                        models.AdSpot.spot_type_id == 2,    # Offline ads
                    ),
                ),
                models.Playback.smart_contract.isnot(None),
                models.AdSpot.active.is_(True),
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
                        api_url = None  # Do not send a request
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
                        False
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

    def get_timeslots_by_adspot_id(
            self,
            id_: int,
            client_time: 'Optional[datetime.datetime]' = None
    ) -> list['dc.TimeSlot']:
        client_day_start, client_day_end = None, None
        if client_time:
            client_day_start = client_time.replace(hour=0, minute=0, second=0, microsecond=0)
            client_day_end = client_day_start.replace(hour=23, minute=59)
        q = select(
                models.Playback,
                models.TimeSlot,
                models.AdSpot,
            ).join(
                models.TimeSlot,
                models.Playback.timeslot_id == models.TimeSlot.id,
            ).join(
                models.AdSpot,
                models.Playback.adspot_id == models.AdSpot.id,
            ).filter(
                models.AdSpot.id == id_,
            )
        if client_time is not None:
            q = q.filter(
                models.TimeSlot.from_time >= utils.cut_timezone(client_day_start),
                models.TimeSlot.from_time <= utils.cut_timezone(client_day_end),
            )
        rows: list['models.TimeSlot'] = self.session.execute(q).all()
        db_time_slots = [
            dc.TimeSlot(
                row.TimeSlot.id,
                row.TimeSlot.from_time,
                row.TimeSlot.to_time,
                row.TimeSlot.locked,
                row.AdSpot.price
            ) for row in rows
        ]
        if client_time is None:
            return db_time_slots

        adspot_price = self.session.query(
            models.AdSpot.price
        ).filter(
            models.AdSpot.id == id_
        ).first().price

        time_slots = []
        for i in range(24 * 60):
            dt = client_day_start.replace(hour=i // 60, minute=i % 60)
            # dt = datetime.datetime.combine(date_, datetime.time(i // 60, i % 60))
            locked_ts = next((ts for ts in db_time_slots if dt in ts), None)
            if locked_ts:
                time_slots.append(locked_ts)
            else:
                time_slots.append(dc.TimeSlot(
                    None,
                    dt,
                    dt + datetime.timedelta(minutes=1),
                    False,
                    adspot_price
                ))
        return time_slots

    def get_timeslots_by_date(self, date_: str) -> list['dc.TimeSlot']:
        _date = datetime.datetime.fromisoformat(date_).date()
        rows: list['models.TimeSlot'] = self.session.execute(
            select(
                models.TimeSlot,
            ).filter(
                cast(models.TimeSlot.from_time, Date) == _date,
            )
        ).all()
        return [
            dc.TimeSlot(
                row.TimeSlot.id,
                row.TimeSlot.from_time,
                row.TimeSlot.to_time,
                row.TimeSlot.locked,
                0
            ) for row in rows
        ]

    def add_playback(self, playback):
        self.session.add(playback)
        self.session.commit()

    def delete_playback(self, id_: int):
        if self.user:
            user_sub_q = select(
                models.Creative.id
            ).filter(
                models.Creative.advert_id == self.user.id
            ).scalar_subquery()
            q = delete(
                models.Playback
            ).where(
                models.Playback.creative_id.in_(user_sub_q),
                models.Playback.id == id_,
            ).execution_options(synchronize_session=False)
        else:
            q = delete(
                models.Playback
            ).where(
                models.Playback.id == id_,
            )
        self.session.execute(q)
        self.session.commit()

    def get_adspot_types(self) -> list['dc.AdSpotTypes']:
        rows: list[models.AdSpotType] = self.session.execute(
            select(
                models.AdSpotType,
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
                models.AdSpot,
            ).join(
                models.Playback,
                models.Playback.timeslot_id == models.TimeSlot.id,
            ).join(
                models.AdSpot,
                models.Playback.adspot_id == models.AdSpot.id,
            )
        ).all()
        return [
            dc.TimeSlot(
                row.TimeSlot.id,
                row.TimeSlot.from_time,
                row.TimeSlot.to_time,
                row.TimeSlot.locked,
                row.AdSpot.price
            ) for row in rows
        ]

    def add_timeslot(self, timeslot):
        self.session.add(timeslot)
        self.session.commit()
        return timeslot.id

    def add_playback_timeslot(self, timeslot: 'models.TimeSlot', playback: 'models.Playback'):
        if (timeslot.to_time - timeslot.from_time).seconds > self.context.max_timeslot_duration:
            raise exc.APIError(f'APIError: period from_time-to_time is must be '
                               f'smaller than {self.context.max_timeslot_duration} sec')

        q = select(
            models.TimeSlot.id,
        ).join(
            models.Playback,
            models.TimeSlot.id == models.Playback.timeslot_id,
        ).where(
            models.TimeSlot.from_time >= timeslot.from_time,
            models.TimeSlot.to_time < timeslot.from_time,
            models.Playback.adspot_id == playback.adspot_id,
            models.Playback.smart_contract.isnot(None),
        )

        exist_playback = self.session.execute(q).first()

        if exist_playback:
            raise exc.APIError(f'APIError: period from_time+to_time '
                               f'should not be busy with other playback.')

        q = select(
            models.Creative.blockchain_ref
        ).where(
            models.Creative.id == playback.creative_id,
        )
        creative = self.session.execute(q).first()
        if not creative:
            raise exc.APIError(f'Current creative.id={playback.creative_id} is unavailable.')
        elif not creative.blockchain_ref:
            raise exc.APIError('Current creative.blockchain_ref is empty.')

        self.session.add(timeslot)
        self.session.flush()
        if timeslot.id:
            playback.timeslot_id = timeslot.id
            self.session.add(playback)
            self.session.commit()
            self.session.refresh(playback)
            return dc.PlaybackRaw(
                playback.id,
                playback.adspot_id,
                playback.timeslot_id,
                playback.creative_id,
                playback.status and playback.status.value,
                playback.smart_contract,
                playback.processed_at,
            )
        else:
            self.session.rollback()

    def register_advertiser(self, login: str, wallet_ref: str, name: str = None):
        advertiser = models.Advertiser(login, wallet_ref, name)
        self.session.add(advertiser)
        self.session.flush()
        return advertiser

    def authorize(self, login: str, wallet_ref: str = None) -> 'dc.UserWeb':
        advertiser = self.session.query(
            models.Advertiser
        ).filter(
            models.Advertiser.login == login
        ).first()

        if advertiser is None:
            advertiser = self.register_advertiser(login, wallet_ref, )
        elif advertiser.wallet_ref != wallet_ref:
            advertiser.wallet_ref = wallet_ref

        return dc.UserWeb(
            advertiser.id,
            advertiser.login,
            advertiser.name,
            advertiser.wallet_ref,
        )
