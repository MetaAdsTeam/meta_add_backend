import datetime
from dataclasses import dataclass, field


@dataclass
class DBConfig:
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
class AdSpot:
    id: int
    name: str
    description: str
    publisher_id: int
    spot_type: str
    price: float
    spot_metadata: str


@dataclass
class Creative:
    id: int
    type: str
    nft_ref: str
    url: str
    name: str


@dataclass
class Playback:
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
    publish_url: str


@dataclass
class AdSpotStats:
    id: int
    likes: int
    views_amount: int
    average_time: int
    max_traffic: int


@dataclass
class AdTaskConfig:
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime


@dataclass
class TimeSlot:
    id: int
    from_time: int
    to_time: int
    locked: bool
    price: float


@dataclass
class PlaybackStatuses:
    id: int
    name: str


@dataclass
class AdSpotTypes:
    id: int
    name: str
    publish_url: str


# @dataclass
# class TimeSlots:
#     id: int
#     from_time: int
#     to_time: int
#     locked: bool
