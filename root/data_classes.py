import datetime
from dataclasses import dataclass, field
from typing import Optional

import pytz
from deeply import Deeply


@dataclass
class DBConfig(Deeply):
    server: str
    port: int
    name: str
    login: str
    password: str
    pool_size: int = field(default=25)
    max_overflow: int = field(default=100)

    @property
    def db_con_string(self) -> str:
        return f'postgresql://{self.login}:{self.password}' \
               f'@{self.server}:{self.port}/{self.name}'


@dataclass
class AdSpot(Deeply):
    id: int
    name: str
    active: bool
    description: str
    publisher_name: str
    publisher_wallet_ref: str
    spot_type: str
    price: float
    preview_url: str
    preview_thumb_url: str
    jump_url: str
    spot_metadata: str
    likes: int
    views_amount: int
    average_time: int
    max_traffic: int


@dataclass
class AdSpotStats(Deeply):
    id: int
    likes: int
    views_amount: int
    average_time: int
    max_traffic: int


@dataclass
class Creative(Deeply):
    id: int
    nft_ref: str
    url: str
    name: str
    description: str
    blockchain_ref: str


@dataclass
class Playback(Deeply):
    id: int
    adspot_name: str
    adspot_likes: int
    preview_thumb_url: str
    jump_url: str
    from_time: datetime
    to_time: datetime
    advert_id: int
    creative_name: str
    creative_description: str
    creative_url: str
    creative_path: str
    status: str
    smart_contract: str
    spot_price: int
    locked: bool
    adspot_type_name: str
    taken_at: datetime
    processed_at: datetime


@dataclass
class PlaybackRaw(Deeply):
    id: int
    adspot_id: int
    timeslot_id: int
    creative_id: int
    status: str
    smart_contract: str
    processed_at: datetime


@dataclass
class AdTaskConfig(Deeply):
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    is_default: bool

    def to_web(self):
        ordinal = super().to_web()
        ordinal['from_time'] = self.start_date.timestamp()
        ordinal['to_time'] = self.end_date.timestamp()
        return ordinal


@dataclass
class AdTask(Deeply):
    playback_id: int
    ad_spot_id: int
    api_url: Optional[str]
    call_at: datetime.datetime
    primarily: bool
    config: 'AdTaskConfig'

    def __post_init__(self):
        if self.api_url == 'NULL':
            self.api_url = None


@dataclass
class AdSpotDefault(Deeply):
    ad_spot_id: int
    api_url: str
    config: 'AdTaskConfig'


@dataclass
class TimeSlot(Deeply):
    id: Optional[int]
    from_time: datetime.datetime
    to_time: datetime.datetime
    locked: bool
    price: float

    def __contains__(self, item: datetime.datetime):
        if (
                item.tzinfo is not None and self.from_time.tzinfo is not None
                or
                item.tzinfo is None and self.from_time.tzinfo is None
        ):
            return self.from_time <= item < self.to_time
        elif self.from_time.tzinfo is not None:
            return self.from_time <= item.replace(tzinfo=pytz.UTC) < self.to_time
        return self.from_time.replace(tzinfo=pytz.UTC) <= item < self.to_time.replace(tzinfo=pytz.UTC)


@dataclass
class AdSpotTypes(Deeply):
    id: int
    name: str


@dataclass
class RequestUser(Deeply):
    near: str
    meta_mask: str


@dataclass
class UserWeb(Deeply):
    id: int
    login: str
    name: str
    wallet_ref: str


@dataclass
class StreamData(Deeply):
    adspot_id: int
    path: str
    from_time: datetime.datetime
    to_time: datetime.datetime


@dataclass
class StreamWeb(Deeply):
    url: str
    is_image: bool
    is_default: bool
    from_time: datetime.datetime
    to_time: datetime.datetime
    msg: str
