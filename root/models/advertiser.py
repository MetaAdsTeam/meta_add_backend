from sqlalchemy import Column, Integer, String
import sqlalchemy_utils.types.password as pwd

from root import models


class Advertiser(models.Base):
    __tablename__ = 'advertisers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    login = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    wallet_ref = Column(String, nullable=False)

    def __init__(self, login: str, wallet_ref: str, name: str):
        self.login = login
        self.name = name
        self.wallet_ref = wallet_ref
