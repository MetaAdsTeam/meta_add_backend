from sqlalchemy import Column, Integer, String, ForeignKey, Float

from root import models


class AdSpot(models.Base):
    __tablename__ = 'adspots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    spot_type_id = Column(Integer, ForeignKey('adspot_types.id'))
    price = Column(Float, nullable=False, default=0)
    spot_metadata = Column(String)

    def __init__(
            self,
            name,
            description,
            publisher_id,
            spot_type_id,
            price,
            spot_metadata,
    ):
        self.name = name
        self.description = description
        self.publisher_id = publisher_id
        self.spot_type_id = spot_type_id
        self.price = price
        self.spot_metadata = spot_metadata
