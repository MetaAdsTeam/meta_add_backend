from sqlalchemy import Column, Integer, String, ForeignKey

from root import models


class AdSpot(models.Base):
    __tablename__ = 'adspots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    adspot_type_id = Column(Integer, ForeignKey('adspot_types.id'))
    ad_metadata = Column(String)

    def __init__(
            self,
            name,
            publisher_id,
            adspot_type_id,
            metadata,
    ):
        self.name = name
        self.publisher_id = publisher_id
        self.adspot_type_id = adspot_type_id
        self.metadata = metadata
