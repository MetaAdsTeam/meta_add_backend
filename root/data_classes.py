import datetime
from dataclasses import dataclass, field
from typing import Optional

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
    description: str
    publisher_name: str
    publisher_wallet_ref: str
    spot_type: str
    price: float
    preview_url: str
    preview_thumb_url: str
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

    def to_web(self):
        ordinal = super().to_web()
        ordinal['from_time'] = self.start_date.timestamp()
        ordinal['to_time'] = self.end_date.timestamp()
        return ordinal


@dataclass
class AdTask(Deeply):
    playback_id: int
    ad_spot_id: int
    api_url: str
    call_at: datetime.datetime
    primarily: bool
    config: 'AdTaskConfig'


@dataclass
class TimeSlot(Deeply):
    id: Optional[int]
    from_time: datetime.datetime
    to_time: datetime.datetime
    locked: bool
    price: float

    def __contains__(self, item: datetime.datetime):
        return self.from_time <= item <= self.to_time


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
    path: str
    from_time: datetime.datetime
    to_time: datetime.datetime


@dataclass
class StreamWeb(Deeply):
    url: str
    is_image: bool
    from_time: datetime.datetime
    to_time: datetime.datetime
    msg: str
