from sqlalchemy import Column, Integer, String

from root import models


class Publisher(models.Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    wallet_ref = Column(String, nullable=False)
    service_ref = Column(String, nullable=False)

    def __init__(
            self,
            name,
            service_ref,
    ):
        self.name = name,
        self.service_ref = service_ref,
