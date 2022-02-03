from sqlalchemy import Column, Integer, String
import sqlalchemy_utils.types.password as pwd

from root import models
import root.data_classes as dc


class Advertiser(models.Base):
    __tablename__ = 'advertisers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(
        pwd.PasswordType(
            schemes=['pbkdf2_sha512', 'md5_crypt'],
            deprecated=['md5_crypt']
        ),
        nullable=False
    )
    name = Column(String, nullable=False)
    wallet_ref = Column(String, nullable=False)

    def __init__(self, login: str, password: str, name: str, wallet_ref: str):
        self.login = login
        self.password = password
        self.name = name
        self.wallet_ref = wallet_ref
