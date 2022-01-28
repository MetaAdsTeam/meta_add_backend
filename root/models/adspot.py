from sqlalchemy import Column, Integer, String, ForeignKey

from root import models


class AdSpot(models.Base):
    __tablename__ = 'adspots'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    ad_place_id = Column(Integer, ForeignKey('ad_places.id'))
    spot_metadata = Column(String)

    def __init__(
            self,
            name,
            ad_place_id,
            spot_metadata,
    ):
        self.name = name
        self.ad_place_id = ad_place_id
        self.spot_metadata = spot_metadata
