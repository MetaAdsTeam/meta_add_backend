from sqlalchemy import Column, Integer, String

from root import models


class Publisher(models.Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)