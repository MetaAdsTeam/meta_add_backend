from sqlalchemy import Column, Integer, String

from root import models


class ContentTypes(models.Base):
    __tablename__ = 'content_types'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name
