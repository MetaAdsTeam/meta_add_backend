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
class AdPlace:
    id: int
    system: str
    place_id: str
    name: str


@dataclass
class AdSpot:
    id: int
    ad_place_name: str
    ad_place_desc: str
    price: int
    publisher_id: int


@dataclass
class Content:
    id: int
    type: str
    nft_ref: str
    nft_bin: str
    url: str
    name: str
