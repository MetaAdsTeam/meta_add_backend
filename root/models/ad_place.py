from sqlalchemy import Column, Integer, String, ForeignKey

from root import models


class AdPlace(models.Base):
    __tablename__ = 'ad_places'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    place_id = Column(String, nullable=False)
    publisher = Column(Integer, ForeignKey('publishers.id'))
    adspot_type = Column(Integer, ForeignKey('adspot_types.id'))
    price = Column(Integer, nullable=False, default=0)

    def __init__(
            self,
            name,
            place_id,
            publisher,
            adspot_type,
            price,
    ):
        self.name = name
        self.place_id = place_id
        self.publisher = publisher
        self.adspot_type = adspot_type
        self.price = price
