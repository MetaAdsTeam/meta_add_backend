import datetime
from dataclasses import dataclass, field

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
class Creative(Deeply):
    id: int
    type: str
    nft_ref: str
    url: str
    name: str


@dataclass
class Playback(Deeply):
    id: int
    adspot_name: str
    from_time: int
    to_time: int
    advert_id: int
    creative_name: str
    creative_description: str
    creative_url: str
    creative_path: str
    status_name: str
    smart_contract: str
    spot_price: int
    play_price: float
    locked: bool
    adspot_type_name: str
    taken_at: datetime
    processed_at: datetime


@dataclass
class AdTaskConfig(Deeply):
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime


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
    id: int
    from_time: int
    to_time: int
    locked: bool
    price: float


@dataclass
class PlaybackStatuses(Deeply):
    id: int
    name: str


@dataclass
class AdSpotTypes(Deeply):
    id: int
    name: str


@dataclass
class UserWeb(Deeply):
    id: int
    login: str
    name: str
    wallet_ref: str
    session_exp: str
