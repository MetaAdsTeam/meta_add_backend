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
    price: int
    spot_metadata: str


@dataclass
class Creative:
    id: int
    type: str
    nft_ref: str
    nft_bin: str
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
    status_name: str
    smart_contract: str
    spot_price: int
    play_price: int
    locked: bool
